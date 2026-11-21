#!/usr/bin/env bash
# Tests for scripts/check_log_times.sh (brief 11-19). Every case is relative to
# the clock at run time, so the suite passes at any hour. Run: bash scripts/test_check_log_times.sh
set -uo pipefail
cd "$(dirname "$0")/.."
G=scripts/check_log_times.sh
export TZ=America/Los_Angeles
pass=0; fail=0
MSG_EST='written as an estimate'
MSG_X='written with an x'
MSG_FUT='after the clock'
MSG_FILE='future-dated log is refused'
MSG_POS='does not open it'
expect() {  # expect <exit> <date> <name> <<< input
  local want=$1 d=$2 name=$3 got
  bash "$G" "$d" >/dev/null 2>&1; got=$?
  if [ "$got" = "$want" ]; then pass=$((pass+1)); else fail=$((fail+1)); echo "FAIL: $name (want exit $want, got $got)"; fi
}
expect_msg() {  # expect_msg <substring> <date> <name> <<< input : must refuse (1) for this reason
  local want=$1 d=$2 name=$3 err got
  err=$(bash "$G" "$d" 2>&1 >/dev/null); got=$?
  if [ "$got" = 1 ] && printf '%s' "$err" | grep -qF -- "$want"; then pass=$((pass+1)); else fail=$((fail+1)); echo "FAIL: $name (want refusal with '$want', got exit $got: ${err:0:140})"; fi
}
today=$(date +%F); nowhm=$(date +%H:%M)
yesterday=$(date -v-1d +%F 2>/dev/null || date -d yesterday +%F)
tomorrow=$(date -v+1d +%F 2>/dev/null || date -d tomorrow +%F)
# a moment two hours ahead, as (date, HH:MM) — crosses midnight correctly
ahead=$(date -v+2H '+%F %H:%M' 2>/dev/null || date -d '+2 hours' '+%F %H:%M'); ahead_d=${ahead% *}; ahead_hm=${ahead#* }
# a moment two hours behind
behind=$(date -v-2H '+%F %H:%M' 2>/dev/null || date -d '-2 hours' '+%F %H:%M'); behind_d=${behind% *}; behind_hm=${behind#* }

# --- passes: times read from the clock, in the past or now ---
expect 0 "$behind_d" "heading two hours ago passes" <<< "## $behind_hm PT — cycle fire
Sync: fine.
Drain: done."
expect 0 "$today" "heading at the current minute passes (grace for the write)" <<< "## $nowhm PT — cycle fire
Drain: done."
expect 0 "$yesterday" "yesterday's log, late heading, passes" <<< '## 23:59 PT — wake
Drain: done.'
expect 0 "$behind_d" "range heading passes on its first time" <<< "## ${behind_hm}–23:59 PT — xian in session
Drain: done."
expect 0 "$behind_d" "body times in the past pass" <<< "## $behind_hm PT — fire
Second mail check at $behind_hm: nothing. Deployed in 118 s; 1:03 ghost unchanged."
expect 0 "$yesterday" "a UTC body time is not future-checked" <<< '## 16:25 PT — continued
upload finalized at 00:25:01.08Z, deploy listed at 00:25:01.41Z.
Drain: done.'
expect 0 "$yesterday" "untimed heading and title pass" <<< '# 2026-11-19 — Tessera log
## Work log
Drain: done.'
expect 0 "$yesterday" "tilde before a non-time number is not an estimate" <<< '## 10:22 PT — fire
pointer 6 adds ~50 s; the artifact is ~532 MB.'
# --- refusals: estimates of record ---
expect_msg "$MSG_EST" "$yesterday" "~HH:MM heading refused" <<< '## ~16:40 PT — xian answered'
expect_msg "$MSG_EST" "$yesterday" "≈HH:MM heading refused" <<< '## ≈17:00 PT — picker shipped'
expect_msg "$MSG_EST" "$yesterday" "'## about HH:MM' heading refused" <<< '## about 16:40 PT — xian answered'
expect_msg "$MSG_X" "$yesterday" "HH:Mx heading refused" <<< '## 13:0x PT — Duty-cycle fire (scheduled)'
expect_msg "$MSG_X" "$yesterday" "HH:xx heading refused" <<< '## 10:xx PT — fire'
expect_msg "$MSG_X" "$yesterday" "x-minute inside a heading's parenthetical refused" <<< '## CORRECTION (2026-09-27, 10:2x fire) — my diagnosis was wrong'
expect_msg "$MSG_X" "$yesterday" "x-minute in a body line refused" <<< '## 10:22 PT — fire
Mail: none since the advisor question (answered 06:xx).'
expect_msg "$MSG_X" "$yesterday" "x-minute quoting another seat's stamp refused" <<< '## 10:22 PT — fire
Pard 16:3x: my memo reached him only now.'
expect_msg "$MSG_X" "$yesterday" "x-minute under a ### heading refused" <<< '### 20:33 — COMPLETE. 21:0x — assembled and delivered'
# --- passes: projections and plans in body text are estimates by nature ---
expect 0 "$yesterday" "ETA with a tilde in the body passes" <<< '## 10:22 PT — fire
Remaining ~1,537 frames × ~6.5 s ≈ 2.8 h → ETA ~21:00.'
expect 0 "$yesterday" "a planned time quoted from a notice passes" <<< '## 14:02 PT — Mail wake: Pard, Amber reboot ~15:00
Drain: done.'
expect 0 "$yesterday" "about-HH:MM in the body passes: only a heading's own time is checked" <<< '## 10:22 PT — fire
the render should finish at about 16:40.'
# --- heading-time position (brief 11-21): the own time opens the heading or the heading is untimed ---
expect 0 "$behind_d" "### heading opening with its time passes" <<< "### $behind_hm — COMPLETE, delivered"
expect_msg "$MSG_FUT" "$ahead_d" "### heading two hours ahead refused (### is future-checked too)" <<< "### $ahead_hm — assembled"
expect_msg "$MSG_POS" "$yesterday" "own time in a trailing parenthetical refused" <<< '## Session start (05:51)'
expect_msg "$MSG_POS" "$yesterday" "own time after a label refused" <<< "## xian's calls (18:00)"
expect_msg "$MSG_POS" "$yesterday" "quoted time with no own time refused (would otherwise be read as the own time)" <<< '## Mail wake — Pard reboots Amber at 15:00
Drain: done.'
expect_msg "$MSG_POS" "$yesterday" "### heading with a mid-line time refused" <<< '### Notes — assembled at 20:33'
expect 0 "$behind_d" "heading time at start followed by a quoted time passes" <<< "## $behind_hm PT — mail wake: Pard reboots Amber at 23:59"
# --- refusals: future ---
expect_msg "$MSG_FUT" "$ahead_d" "heading two hours ahead refused" <<< "## $ahead_hm PT — fire
Drain: done."
expect_msg "$MSG_FILE" "$tomorrow" "tomorrow's log refused even with an untimed heading" <<< '## Work log
Drain: done.'
# --- exit 2: the gate must not pass when it cannot measure ---
expect 2 "not-a-date" "bad date argument is exit 2, not a pass" <<< '## 10:22 PT — fire'
expect 2 "" "missing date argument is exit 2" <<< '## 10:22 PT — fire'
# --- cripple pass: disarm one branch in a scratch copy; the case that proved it must now pass ---
SCRATCH="${TMPDIR:-/tmp}/check_log_times_cripple.$$"
cripple() {  # cripple <name> <sed-expr> <date> <input>
  local name=$1 expr=$2 d=$3 input=$4 got
  sed -e "$expr" "$G" > "$SCRATCH"
  cmp -s "$G" "$SCRATCH" && { fail=$((fail+1)); echo "FAIL: cripple '$name' changed nothing"; return; }
  printf '%s\n' "$input" | bash "$SCRATCH" "$d" >/dev/null 2>&1; got=$?
  if [ "$got" = 0 ]; then pass=$((pass+1)); else fail=$((fail+1)); echo "FAIL: cripple '$name' still refuses (exit $got) — the case was proving a backstop"; fi
}
cripple "x-minute branch disarmed"   's/^EST_X=.*/EST_X="NEVERMATCHES"/' "$yesterday" '## 13:0x PT — fire'
cripple "heading-estimate branch disarmed" 's/grep -qiE .(~|≈|about|approx)./grep -qiE "NEVERMATCHES"/' "$yesterday" '## ~16:40 PT — xian answered'
cripple "future branch disarmed"   's/-gt \$((now + 60))/-gt 9999999999/' "$ahead_d" "## $ahead_hm PT — fire"
cripple "heading-position branch disarmed" 's/^HAS_T=.*/HAS_T="NEVERMATCHES"/' "$yesterday" '## Session start (05:51)'
cripple "file-date branch disarmed" 's/"\$d" > "\$today"/"x" > "y"/' "$tomorrow" '## Work log'
rm -f "$SCRATCH"
echo "check_log_times tests: $pass passed, $fail failed"
[ "$fail" = 0 ]
