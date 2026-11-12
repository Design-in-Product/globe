#!/usr/bin/env python3
"""Pages reference gate: every asset a published page names must be inside
the folder that gets uploaded.

Why (2026-11-12, Claude Duet's proposal via xian): the Pages artifact is the
whole checkout, ~809 MB, of which ~300 MB is films and plate data no page
links. Excluding them shrinks the upload, but an exclude list is hand-typed
and a page can start linking an excluded file later — that would 404 after a
green deploy. This gate runs on the STAGED folder before upload, so a page
that names a file the staging dropped (or never had) refuses the deploy.

What counts as a reference, read from every *.html under the root:
  src= href= poster= data-src=  attributes, "…" '…' or unquoted (relative or /root)
  url(...)                       in inline CSS
  "quoted" or 'quoted' literals  ending in a hosted asset extension — this is
                                 how index.html names its films (FILMS table)
  a literal that does not resolve from the page's folder is retried against
  every string constant in the page that ends in "/" (explore's
  `const ASSETS = "../scrubber_assets/"`) — no evaluation, just the bases
  a resolved *.json with a "keyframes" list requires every declared file
                                 (the Explore scrubber fetches them by name);
                                 a fetched *.json that does not parse is UNRESOLVED
A reference with a scheme (https:, data:, mailto:), a fragment-only href, or
a `${` template is not gated. A href ending in "/" must be a folder.

Census (report only): every file >= 1 MB under the root that no page
references is printed as PRESENT-UNREFERENCED, biggest first, so bulk that
nothing serves is visible instead of silently uploaded.

Usage: check_pages_refs.py <root>      (~0.1 s for this site, no network)
Exit 0 = every reference resolves; 1 = at least one UNRESOLVED (named with
its page); 2 = root unusable or no page found (a vacuous pass is not a pass).
"""
import json
import os
import re
import sys

EXT = r"(?:mp4|webm|json|webp|png|jpg|jpeg|gif|svg|ico|css)"
# double-quoted, single-quoted or unquoted attribute values (brief 11-12: a
# selector that sees one format silently skips the rest; this one saw "…" only)
# …and read inside TAGS only: `video.src = FILMS[era][view]` in a script body
# is an assignment, not an attribute (the unquoted form matched it on 11-12).
TAG = re.compile(r'<[a-zA-Z][^>]*>')
ATTR = re.compile(r'(?<![\w.-])(?:src|href|poster|data-src)\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^\s"\'=<>`]+))')
CSSURL = re.compile(r'url\(\s*["\']?([^"\')]+)["\']?\s*\)')
LITERAL = re.compile(r'["\']([^"\'\s<>]+?\.' + EXT + r')["\']')
BASES = re.compile(r'\b(?:const|let|var)\s+\w+\s*=\s*["\']([^"\']*/)["\']')
SKIP = re.compile(r'^(?:[a-z][a-z0-9+.-]*:|#|\$\{)', re.I)
CENSUS_MIN = 1 << 20


def norm(root, base_dir, ref):
    ref = ref.split("#")[0].split("?")[0]
    p = os.path.join(root, ref.lstrip("/")) if ref.startswith("/") else os.path.join(base_dir, ref)
    return os.path.normpath(p)


def inside(root, p):
    return p == root or p.startswith(root + os.sep)


def check(root):
    root = os.path.abspath(root)
    if not os.path.isdir(root):
        print(f"  {root}: not a folder (NOT OK)")
        return 2
    pages = []
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if not x.startswith(".") and x != "node_modules"]  # .git .github .venv
        pages += [os.path.join(d, f) for f in files if f.endswith(".html")]
    if not pages:
        print(f"  {root}: no .html page found — nothing gated (NOT OK)")
        return 2
    referenced, unresolved = set(), []
    for page in sorted(pages):
        rel_page = os.path.relpath(page, root)
        try:
            text = open(page, encoding="utf-8", errors="replace").read()
        except OSError as e:
            print(f"  {rel_page}: UNREADABLE ({e}) (NOT OK)")
            return 2
        pdir = os.path.dirname(page)
        bases = [norm(root, pdir, b) for b in BASES.findall(text)]
        strict = [(a or b or c, "attr") for tag in TAG.findall(text) for a, b, c in ATTR.findall(tag)]
        strict += [(r, "css") for r in CSSURL.findall(text)]
        loose = [(r, "literal") for r in LITERAL.findall(text)]
        n = 0
        for ref, kind in strict + loose:
            if not ref or SKIP.match(ref):
                continue
            cands = [norm(root, pdir, ref)]
            if kind == "literal":
                cands += [os.path.normpath(os.path.join(b, ref)) for b in bases]
            hit = None
            for c in cands:
                if not inside(root, c):
                    continue
                want_dir = ref.endswith("/")
                if (os.path.isdir(c) if want_dir else os.path.isfile(c)):
                    hit = c
                    break
            if hit is None:
                unresolved.append((rel_page, ref, kind))
                continue
            n += 1
            referenced.add(hit)
            if hit.endswith(".json"):
                n += manifest_refs(root, hit, referenced, unresolved, rel_page)
        print(f"  {rel_page}: {n} references resolved")
    for rel_page, ref, kind in unresolved:
        print(f"    UNRESOLVED: {rel_page} names {ref!r} ({kind}) and it is not in the upload")
    census(root, referenced)
    return 1 if unresolved else 0


def manifest_refs(root, path, referenced, unresolved, rel_page):
    try:
        m = json.load(open(path))
    except (OSError, ValueError) as e:
        # a page fetches it and it does not parse: the live page breaks there.
        # Named, not skipped (brief 11-12: a parser must fail on what it cannot
        # read, or it returns a plausible pass).
        unresolved.append((rel_page, os.path.relpath(path, root) + " does not parse as JSON (" + e.__class__.__name__ + ")", "manifest"))
        return 0
    keys = m.get("keyframes") if isinstance(m, dict) else None
    if not isinstance(keys, list):
        return 0  # valid JSON that is not a keyframe manifest: nothing more to require
    d = os.path.dirname(path)
    n = 0
    for k in keys:
        f = k.get("file", "") if isinstance(k, dict) else ""
        p = os.path.normpath(os.path.join(d, f))
        if f and inside(root, p) and os.path.isfile(p):
            referenced.add(p)
            n += 1
        else:
            unresolved.append((rel_page, os.path.relpath(path, root) + " -> " + (f or "<no file>"), "manifest"))
    return n


def census(root, referenced):
    big = []
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if not x.startswith(".") and x != "node_modules"]  # .git .github .venv
        for f in files:
            p = os.path.join(d, f)
            if p not in referenced and os.path.getsize(p) >= CENSUS_MIN:
                big.append((os.path.getsize(p), os.path.relpath(p, root)))
    big.sort(reverse=True)
    tot = sum(s for s, _ in big)
    print(f"  census: {len(referenced)} referenced files; {len(big)} unreferenced files >= 1 MB "
          f"({tot / 1048576:.0f} MB) in the upload")
    for s, p in big:
        print(f"    PRESENT-UNREFERENCED: {p} ({s / 1048576:.1f} MB)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: check_pages_refs.py <root>", file=sys.stderr)
        sys.exit(2)
    sys.exit(check(sys.argv[1]))
