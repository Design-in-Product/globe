#!/usr/bin/env python3
"""Block until GitHub Pages is SERVING the commit that is on origin/main.

Why this exists (2026-10-02): polling builds/latest for status == "built"
and breaking on the first hit passed vacuously — the "built" belonged to
the PREVIOUS push, the new push's build hadn't registered yet, and the
live-site checks that followed ran against the old deploy. Same shape as
brief 10/01 finding 1: an assertion that passes because the thing never
ran. The fix is to assert the build's COMMIT, not its status.

2026-10-09: Pages switched to the Actions artifact deploy
(build_type=workflow). In that mode pages/builds no longer records
anything; the truth is the `github-pages` environment's deployment for the
commit, and its latest status. This script reads the repo's build_type
once and asks the right API, so a one-call revert to legacy needs no
script change. Prints which mode it checked so the log can quote it.

Exit 0 only when the target commit is built/deployed successfully. 1 on
errored/failure, 2 on timeout.

Usage: python3 scripts/wait_pages.py [--sha <full sha>] [--timeout 300]
"""
import argparse, json, subprocess, sys, time

REPO = "Design-in-Product/globe"


def sh(*a):
    return subprocess.run(a, capture_output=True, text=True).stdout.strip()


def api(path):
    try:
        return json.loads(sh("gh", "api", path))
    except json.JSONDecodeError:
        return {}


def legacy(want):
    b = api(f"repos/{REPO}/pages/builds/latest")
    st, c = b.get("status"), b.get("commit", "")
    if c == want and st == "built":
        return "ok", "built (legacy)"
    if c == want and st == "errored":
        return "err", f"ERRORED (legacy): {b.get('error', {}).get('message')}"
    return "wait", f"latest build is {st} for {c[:7]}"


def workflow(want):
    deps = api(f"repos/{REPO}/deployments?environment=github-pages&sha={want}&per_page=5")
    if not isinstance(deps, list) or not deps:
        return "wait", "no github-pages deployment registered yet"
    d = deps[0]
    sts = api(f"repos/{REPO}/deployments/{d['id']}/statuses?per_page=1")
    state = sts[0]["state"] if isinstance(sts, list) and sts else "pending"
    if state == "success":
        return "ok", "deployed (workflow)"
    if state in ("failure", "error", "inactive"):
        return "err", f"deployment {state} (workflow) — see gh run list --workflow pages"
    return "wait", f"deployment {state}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sha", default=None, help="default: origin/main")
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--every", type=int, default=10)
    a = ap.parse_args()
    want = a.sha or sh("git", "rev-parse", "origin/main")
    mode = api(f"repos/{REPO}/pages").get("build_type", "legacy")
    probe = workflow if mode == "workflow" else legacy
    t0 = time.time()
    while True:
        state, msg = probe(want)
        if state == "ok":
            print(f"pages: {msg} for {want[:7]} ({int(time.time()-t0)}s)"); return 0
        if state == "err":
            print(f"pages: {msg} for {want[:7]}", file=sys.stderr); return 1
        if time.time() - t0 > a.timeout:
            print(f"pages: TIMEOUT after {a.timeout}s [{mode}] — {msg}, wanted {want[:7]}",
                  file=sys.stderr); return 2
        time.sleep(a.every)


if __name__ == "__main__":
    sys.exit(main())
