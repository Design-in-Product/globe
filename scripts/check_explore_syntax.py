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

Usage:  python3 scripts/check_explore_syntax.py [page.html]
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


def main(page="explore/index.html"):
    html = open(page).read()
    m = re.search(r'<script type=["\']module["\'][^>]*>(.*?)</script>', html, re.S)
    if not m:
        print(f"EXTRACTION FAILED: no module script found in {page}", file=sys.stderr)
        return 2

    src = m.group(1)
    n = len(src)
    if n < MIN_CHARS:
        print(f"GUARD TRIPPED: extracted only {n} chars (< {MIN_CHARS}) from {page}.\n"
              f"The extraction is probably broken, not the page — "
              f"do not read this as a pass.", file=sys.stderr)
        return 3

    # Stub the CDN imports: we check our own syntax, not three.js.
    for old, new in STUBS:
        src = src.replace(old, new)

    fd, tmp = tempfile.mkstemp(suffix=".mjs")
    try:
        with os.fdopen(fd, "w") as f:
            f.write(src)
        r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
        if r.returncode != 0:
            print(f"{page}: MODULE SYNTAX ERROR", file=sys.stderr)
            print(r.stderr.rstrip(), file=sys.stderr)
            return 1
    finally:
        os.unlink(tmp)

    print(f"{page}: module syntax OK ({n} chars checked)")
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:2]))
