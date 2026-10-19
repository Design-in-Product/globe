# 2026-10-19 — Tessera log

## 10:22 fire

Sync: `5dd5bf0` (brief pointer). Mail: nothing new. `fire_check.sh`: site and /explore/ 200, Pages deployed for `5dd5bf0`, no stray Blender, no live declarations.

**Brief 10-19 applied here — my drain guard was fail-open too.** The pre-commit guard opened a checked block only on `## HH:MM PT` headings. Since 10-16 I have written `## 16:22 fire`, `## 21:16 wake — …`, `## 05:04 wake — …` and the range form `## 11:35–12:00 PT` (the en dash breaks the pattern), so eight entries passed unchecked; each carried a Drain line by habit, which is exactly the "green that gets believed" shape. Fix, Janus's way: any `## ` heading opens a block (every section in a tessera log is an entry). The check now lives in `scripts/check_drain.sh` (stdin = added lines) so it is testable; `scripts/test_check_drain.sh` runs 29 cases built from eight real heading strings copied from this week's logs, plus the deferral grammar (29/29 pass). End-to-end: a staged entry without a Drain line was refused by the hook before this commit. The hook's pipeline is also `pipefail`-safe now (an all-deletion diff no longer refuses by accident). Rule for the future, in the test file: add a line to HEADS whenever a new heading shape appears.

Drain: health check; brief applied (guard fixed, tested, proven). Deferred: ship + old-frame clearance (blocker: xian has not watched the second cut in motion); crossfade decision (blocker: xian's call). Two clean mail checks (10:22, 10:31).

## 16:22 fire

Sync: up to date at `4285a5c`. Mail: nothing new. `fire_check.sh`: site and /explore/ 200, Pages deployed for `4285a5c`, no stray Blender, no live declarations. Second cut still staged in `review-2/` for xian (since 10-17 10:44).

Drain: health check only; nothing else unblocked. Deferred: ship + old-frame clearance (blocker: xian has not watched the second cut in motion); crossfade decision (blocker: xian's call). Two clean mail checks (16:22, 16:23).
