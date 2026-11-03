# 2026-11-02 — Tessera log

## 10:22 PT — cycle fire: brief 11-02 applied — the pre-commit hook was blind to renames

Sync: ff to ba9fc95 (brief 11-02). Mail: nothing new to me in globe, mediajunkie or designinproduct (newest to-tessera still xian's one-line memo of 10-30, acted on). Health: VERDICT clean across 43 lines — Pages deployed for ba9fc95, DNS at the Pages target, /explore/ 200 with the atlas body, manifests 23/23 and 56/56, hook OK, launchd loaded with last exit 0, handoff 14 of 14 pointers, no unignored bulk, no stray Blender or supervisor, 0 live and 0 expired declarations, 111 GB free with 15 local snapshots.

Brief 11-02 (Piper Morgan CIO, piper-guards): read together with CIO's correction memo to Janus of 10:09 — the guard did not pass silently, it blocked with its reason on the wrong channel; 0.2.2 is not installed anywhere; no test found the stdout line. Corrected action: assert that a refusal's TEXT reaches the channel the reader sees, and enumerate every form of the operation a guard gates (the same commit closed a `git mv`/`git rm` bypass).

Channel: every refusal in scripts/hooks/pre-commit and scripts/check_drain.sh already goes to stderr (grepped: all six `>&2`). For a git hook run through Bash both channels reach me anyway; the stderr discipline is kept.

Coverage: not covered. All four staged-file reads in the hook used `git diff --cached --name-only --diff-filter=…` without `--no-renames`, so git reported a `git mv` as R, which none of the A/M/D filters select. A renamed keyframe skipped the manifest gate; a renamed-and-edited page or log would skip the syntax and drain gates. Proven in a scratch path-clone with hooksPath set (not in the live repo, where a bypass would have landed): `git mv scrubber_assets/0050ma.webp 0051ma.webp` staged as R100 and committed clean under the old hook, exit 0. Fix: `--no-renames` on all four reads, so the rename is seen as D + A. Proven in the same clone with the patched hook copied in: the rename is refused, exit 1, stdout 0 bytes, stderr carries the manifest's `DECLARED-ABSENT: '0050ma.webp'` and `PRESENT-UNDECLARED: 0051ma.webp` lines plus the hook's one-line reason; nothing landed. An honest commit (a log append with a Drain line) still passes under the patched hook, exit 0. This live commit is the second positive case.

Drain: brief applied (hook rename gap closed, proven red under the old hook and green/red under the new one); nothing else unblocked. Deferred with blockers, all xian's: preview → live swap (blocker: his edit review of previews/home-2026-10-21/), 1:03 ghost test render (blocker: his verdict), sequel treatment and licence (blocker: his decisions).

## 16:23 PT — 16:22 fire — no-op, all green

Synced: already at c7a4d35, nothing new on origin/main. Fire check VERDICT clean (43 lines, no failure line): brief 11-02 age 0 d; 8 pages / 4 inline script blocks OK; both keyframe manifests 0/0; dns CNAME correct; live /explore/ is the atlas page; Pages deployed (workflow) for c7a4d35; hook gated, launchd loaded last exit 0; 0 stray Blender, 0 supervisor, 0 cpu declarations, 0 expired; disk 111 GB free, render tree 28 G, 15 local TM snapshots; handoff 14/14; unignored bulk none.

Mail: nothing new in globe docs/mail today. Sibling repos carry 34 (mediajunkie) + 8 (designinproduct) memos dated today, all Piper Morgan guards 0.2.2 restart traffic between Pard, the CIO, Janus and the PM seats; grep across all 42 for tessera / to-all / globe hits one subject line ("every seat is on a LaunchAgent", about PM seats). None addressed to me, none to act on. The 11-02 brief and its CIO correction were applied at 10:22 (rename bypass closed, c7a4d35).

Drain: nothing unblocked. Deferred with blockers, all xian's: preview → live swap (blocker: his edit review of previews/home-2026-10-21/), 1:03 ghost test render (blocker: his verdict), sequel treatment and licence (blocker: his decisions). Two mail checks follow: this fire's check 1 above was clean; check 2 after push.
