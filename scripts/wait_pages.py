#!/usr/bin/env python3
"""Block until GitHub Pages has BUILT the commit that is on origin/main.

Why this exists (2026-10-02): polling builds/latest for status == "built"
and breaking on the first hit passed vacuously — the "built" belonged to
the PREVIOUS push, the new push's build hadn't registered yet, and the
live-site checks that followed ran against the old deploy. Same shape as
brief 10/01 finding 1: an assertion that passes because the thing never
ran. The fix is to assert the build's COMMIT, not its status.

Exit 0 only when status == built AND commit == target. 1 on errored,
2 on timeout. Prints what it verified so the log can quote it.

Usage: python3 scripts/wait_pages.py [--sha <full sha>] [--timeout 300]
"""
import argparse, json, subprocess, sys, time

REPO = "Design-in-Product/globe"


def sh(*a):
    return subprocess.run(a, capture_output=True, text=True).stdout.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sha", default=None, help="default: origin/main")
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--every", type=int, default=10)
    a = ap.parse_args()
    want = a.sha or sh("git", "rev-parse", "origin/main")
    t0 = time.time()
    while True:
        try:
            b = json.loads(sh("gh", "api", f"repos/{REPO}/pages/builds/latest"))
        except json.JSONDecodeError:
            b = {}
        st, c = b.get("status"), b.get("commit", "")
        if c == want and st == "built":
            print(f"pages: built for {want[:7]} ({int(time.time()-t0)}s)"); return 0
        if c == want and st == "errored":
            print(f"pages: ERRORED for {want[:7]}: {b.get('error',{}).get('message')}", file=sys.stderr); return 1
        if time.time() - t0 > a.timeout:
            print(f"pages: TIMEOUT after {a.timeout}s — latest build is {st} for {c[:7]}, wanted {want[:7]}",
                  file=sys.stderr); return 2
        time.sleep(a.every)


if __name__ == "__main__":
    sys.exit(main())
