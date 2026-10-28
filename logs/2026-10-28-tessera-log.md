# 2026-10-28 — Tessera log

## 10:22 PT — cycle fire: brief 10-28 applied (a lapsed log habit, now a printed line)

Restarted onto Claude Code 2.1.310 by Pard on xian's go earlier this morning; confirmed up. Sync: ff to 2a70c11 (brief 10-28). Mail: nothing new to me in globe, mediajunkie or designinproduct (newest to-tessera still 10-21). Health: all green — Pages deployed for 2a70c11, DNS, /explore/ 200, 4 script blocks OK, manifests 23/23 and 56/56, handoff 14/14 pointers, no unignored bulk, no stray Blender or supervisor, 0 live declarations.

Brief 10-28 finding 1 (Piper Morgan CIO re-run: every duty moved into a mechanism on 10-13 still runs; both duties kept as log habits lapsed within a week). Audited my own last 14 days for "I will" commitments not backed by a hook or a printed check. One found, and it had lapsed: on 10-21 I wrote "will log when df actually moves" after local Time Machine snapshots pinned the 14 GB the frame-set delete freed. Measured now: 118 GB free (was 96.2 on 10-21), render tree 28 GB, 13 local snapshots. The log never said so — exactly the brief's case. Fix is structural, not a better promise: fire_check's repo block now prints a `disk:` line (free on /, render-tree size, local snapshot count) every fire, so the measurement is read rather than remembered. Proven by running it: `disk: 118Gi free on /   render tree: 28G   local TM snapshots: 13`.

Finding 2 (TypeScript forEach+push inferring any[]): no TypeScript in this repo; the atlas pages are plain inline JS. Not applicable.

Drain: brief applied (disk line in fire_check, the lapsed df follow-up closed by measurement); nothing else unblocked. Deferred with blockers, all xian's: preview → live swap (blocker: his edit review of previews/home-2026-10-21/), 1:03 ghost test render (blocker: his verdict), sequel treatment and licence (blocker: his decisions). Disk-space item closes with this measurement (Pard's snapshot explanation held: space returned as the snapshots aged out).

## 13:16 PT — mail wake: Pard, six expired Blender rows in cpu-declarations.tsv

Sync: ff to 1933fee (Pard's memo). His `check-cpu-hogs.sh` reports STALE DECLARATION(S) for all six Blender rows, expiries 10-06 to 10-17, all passed; low priority while nothing renders, but an expired row is noise that can hide a real stale case. He was right, and it is the morning brief's finding a second time in one day: clearing expired rows was a habit nobody held. Removed the six rows, header kept (f208228; origin/main reads 0 Blender rows). Two mechanisms so the sweep stops depending on memory: `scripts/declare_render.sh` prunes every expired row before it appends a new one (proven on a scratch file: expired + live in, live out), and fire_check prints `expired rows still in file: N` beside the live count with a remove flag above 0 (proven: 6 on the pre-edit file, 0 now). Replied to Pard at his reply-to, mediajunkie:docs/mail/ (71fd742).

Drain: memo acted on in-wake (rows removed, two mechanisms, reply delivered); nothing else unblocked. Deferred with blockers, all xian's: preview → live swap (blocker: his edit review of previews/home-2026-10-21/), 1:03 ghost test render (blocker: his verdict), sequel treatment and licence (blocker: his decisions).
