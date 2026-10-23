#!/usr/bin/env bash
# Tests for scripts/check_drain.sh against REAL headings copied from recent
# logs (brief 10-19: a hook whose tests only pass the canonical input cannot
# detect format drift). Add a line to HEADS whenever a new heading shape
# appears in logs/. Run: scripts/test_check_drain.sh  (exit 0 = all pass)
set -uo pipefail
cd "$(dirname "$0")/.."
G=scripts/check_drain.sh
pass=0; fail=0
expect() {  # expect <0|1> <name> <<< input
  local want=$1 name=$2 got
  bash "$G" >/dev/null 2>&1; got=$?
  if [ "$got" = "$want" ]; then pass=$((pass+1)); else fail=$((fail+1)); echo "FAIL: $name (want exit $want, got $got)"; fi
}
# Real heading shapes observed in logs/2026-10-1[2-9]-tessera-log.md as of 2026-10-19:
HEADS=(
  '## 10:22 PT — cycle fire'
  '## 16:22 fire'
  '## 21:16 wake — second cut complete; 1:03 root cause; scheduler misfire caught'
  '## 05:04 wake — prequel v3 Cycles pass launched'
  '## 11:35–12:00 PT — xian'"'"'s second round'
  '## 10:45–11:30 PT — xian in session: first-cut review'
  '## 16:22 PT — Duty-cycle fire (scheduled) — new rule: outside people'"'"'s details'
  '## 17:04 PT — mail wake: Pard'"'"'s "render is fine; one disk note"'
)
for h in "${HEADS[@]}"; do
  expect 1 "no Drain under: $h" <<< "$h
Sync: fine. Mail: none."
  expect 0 "Drain under: $h" <<< "$h
Sync: fine.
Drain: health check only; nothing else unblocked."
  expect 0 "bold Drain under: $h" <<< "$h
**Drain:** done."
done
# Deferral grammar
expect 1 "deferral without blocker" <<< '## 16:22 fire
Drain: deferred the ship to tomorrow.'
expect 0 "deferral with blocker:" <<< '## 16:22 fire
Drain: health check. Deferred: ship (blocker: xian has not watched the cut).'
expect 0 "deferral with waits on" <<< '## 16:22 fire
Drain: ship waits on xian watching the cut.'
# Deferral vocabulary (widened 2026-10-23, brief: One Job's hook caught these variants)
for w in 'postponed the ship' 'ship on hold' 'parked the ship' 'punted the ship' 'ship next cycle' 'ship next session' 'deferring the ship'; do
  expect 1 "deferral variant without blocker: $w" <<< "## 16:22 fire
Drain: $w."
  expect 0 "deferral variant with blocker: $w" <<< "## 16:22 fire
Drain: $w (blocker: xian has not watched the cut)."
done
# Ordinary words that are not deferrals must not trip it
expect 0 "prose containing 'later' only outside Drain" <<< '## 16:22 fire
Later in the day the render finished.
Drain: all done.'
expect 0 "Drain mentions a park (the noun) with no deferral" <<< '## 16:22 fire
Drain: done; nothing parked.'
# Two entries in one diff: the first lacks Drain, the second has it
expect 1 "first of two entries lacks Drain" <<< '## 10:22 fire
Sync.
## 16:22 fire
Drain: ok.'
# Editing an existing heading (rename, time fix) adds only the heading line;
# its Drain line is unchanged and absent from the diff — must pass.
expect 0 "renamed heading, no added body" <<< '## 16:51 — xian in session: second cut approved and SHIPPED (heading time from the ship commit'"'"'s clock)'
expect 0 "renamed heading then a new full entry" <<< '## 16:51 — ship (time fixed)
## 17:05 — mail wake
Pard acked.
Drain: corrections sent.'
expect 1 "renamed heading then a new entry lacking Drain" <<< '## 16:51 — ship (time fixed)
## 17:05 — mail wake
Pard acked.'
# Non-entry additions (a top-level title, body text) do not open a block
expect 0 "title and prose only" <<< '# 2026-10-19 — Tessera log
some added prose'
echo "check_drain tests: $pass passed, $fail failed"
[ "$fail" = 0 ]
