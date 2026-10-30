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
    """One API read. None means the call itself failed (gh down, api.github.com
    unreachable, auth) — a state the caller must name, never a value to .get()
    on. 10-30: an outage made this return {} and main() read build_type off
    it, silently falling to LEGACY mode and reporting a stale 2025 build as
    the verdict for today's sha. An error is never a finding (brief 10-27)."""
    r = subprocess.run(["gh", "api", path], capture_output=True, text=True)
    if r.returncode != 0 or not r.stdout.strip():
        api.last_error = (r.stderr.strip().splitlines() or ["no output"])[0]
        return None
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        api.last_error = "non-JSON reply"
        return None
api.last_error = ""


def legacy(want):
    b = api(f"repos/{REPO}/pages/builds/latest")
    if b is None:
        return "wait", f"gh api unreachable ({api.last_error})"
    st, c = b.get("status"), b.get("commit", "")
    if c == want and st == "built":
        return "ok", "built (legacy)"
    if c == want and st == "errored":
        return "err", f"ERRORED (legacy): {b.get('error', {}).get('message')}"
    return "wait", f"latest build is {st} for {c[:7]}"


def workflow(want):
    deps = api(f"repos/{REPO}/deployments?environment=github-pages&sha={want}&per_page=5")
    if deps is None:
        return "wait", f"gh api unreachable ({api.last_error})"
    if not isinstance(deps, list) or not deps:
        return "wait", "no github-pages deployment registered yet"
    d = deps[0]
    sts = api(f"repos/{REPO}/deployments/{d['id']}/statuses?per_page=1")
    if sts is None:
        return "wait", f"gh api unreachable ({api.last_error})"
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
    # the deployments API matches the full sha only; expand a short one
    want = sh("git", "rev-parse", a.sha or "origin/main")
    pages = api(f"repos/{REPO}/pages")
    if pages is None:
        # Cannot even learn which API to ask: say so and exit 2 (UNMEASURABLE),
        # distinct from 0 deployed and 1 failed. Never guess a mode.
        print(f"pages: UNMEASURABLE — gh api unreachable ({api.last_error}); wanted {want[:7]}", file=sys.stderr)
        return 2
    mode = pages.get("build_type", "legacy")
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
