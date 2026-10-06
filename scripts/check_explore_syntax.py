#!/usr/bin/env python3
"""Syntax-check the module script inside explore/index.html.

There is no browser on Amber, so this is the only automated check the
explore page gets. It therefore has to fail loudly rather than pass
vacuously. Verified three-arm on 2026-09-24 (prompted by brief 9/24,
Klatch Round 262 — "an arm never shown to go red is consistent with an
arm that cannot"):

    A  real page             -> pass
    B  injected syntax error -> fail    (the check is real, not vacuous)
    C  extraction yields ""  -> pass    <- the hole MIN_CHARS closes

Arm C is the reason for the guard: `node --check` on an empty file
succeeds, so a regex that quietly stopped matching (someone adds an
attribute to the script tag, switches quote style, splits the block)
would have printed "syntax OK" having checked nothing. Same failure class
as the July ASS-overlay incident, where a silent fallback shipped a film
with no overlay and reported success.

A first draft of this lived in bash and died of a bash-3.2 heredoc-inside-
command-substitution parse error — while exiting 0. A checker that breaks
and reports success is the exact thing this file exists to prevent, so:
Python, no shell quoting, explicit exit codes.

Usage:  python3 scripts/check_explore_syntax.py [page.html ...]   (default: explore/index.html)
Exits:  0 ok · 1 syntax error · 2 extraction failed · 3 guard tripped
"""
import os
import re
import subprocess
import sys
import tempfile

MIN_CHARS = 1000
STUBS = [
    ('from "three"', 'from "data:text/javascript,export default {}"'),
    ('from "three/addons/controls/OrbitControls.js"',
     'from "data:text/javascript,export const OrbitControls = class {}"'),
]


def blocks(html):
    """Every inline <script> body — module or classic — that is not a src= include.
    Brief 10/06 finding 2: a check that hardcodes one file/one kind is a coverage
    claim for that file, not for 'the site'. Until 10-06 this matched only
    type="module", so index.html's classic script (the live hero's film
    chaining) had no gate at all."""
    out = []
    for m in re.finditer(r'<script\b([^>]*)>(.*?)</script>', html, re.S | re.I):
        attrs, body = m.group(1), m.group(2)
        if re.search(r'\bsrc\s*=', attrs, re.I):
            continue
        kind = "module" if re.search(r'type\s*=\s*["\']module["\']', attrs, re.I) else \
               ("skip" if re.search(r'type\s*=', attrs, re.I) and not re.search(r'javascript', attrs, re.I) else "classic")
        if kind != "skip":
            out.append((kind, body))
    return out


def check_page(page):
    html = open(page).read()
    bs = blocks(html)
    if not bs:
        print(f"{page}: no inline scripts (nothing to check)")
        return 0, 0
    fails = 0
    for i, (kind, src) in enumerate(bs, 1):
        n = len(src)
        if n < MIN_CHARS:
            print(f"GUARD TRIPPED: {page} script #{i} ({kind}) extracted only {n} chars (< {MIN_CHARS}); "
                  f"extraction, not the page, is suspect", file=sys.stderr)
            return 3, len(bs)
        for old, new_ in STUBS:
            src = src.replace(old, new_)
        fd, tmp = tempfile.mkstemp(suffix=".mjs" if kind == "module" else ".js")
        try:
            with os.fdopen(fd, "w") as f:
                f.write(src)
            r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
            if r.returncode != 0:
                print(f"{page} script #{i} ({kind}): SYNTAX ERROR", file=sys.stderr)
                print(r.stderr.rstrip(), file=sys.stderr)
                fails += 1
        finally:
            os.unlink(tmp)
    return (1 if fails else 0), len(bs)


def main(*pages):
    pages = list(pages) or ["explore/index.html"]
    worst, total = 0, 0
    for page in pages:
        if not os.path.exists(page):
            print(f"EXTRACTION FAILED: {page} not found", file=sys.stderr); return 2
        rc, n = check_page(page); total += n; worst = max(worst, rc)
        if rc == 0 and n:
            print(f"{page}: {n} inline script block(s) OK")
    print(f"denominator: {total} script block(s) across {len(pages)} page(s)")
    return worst


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
