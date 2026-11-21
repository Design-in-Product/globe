#!/usr/bin/env bash
# Log time gate: timestamps come from the clock, never estimated or future-dated.
#
# Brief 11-19 (Piper Morgan): "dates from the clock, not guessed" was a stated
# rule there, understood, and broken regularly — by the agent that had filed it
# as a correction in the same session. Made structural as a commit-time gate:
# ~60 commits through in five hours, zero false refusals. The same rule has
# stood here since 10-21 (memory: timestamps-from-the-clock) as a remembered
# obligation; this file makes it a refusal. Calibration 2026-11-19, copied from
# the replay of all 74 logs through this gate with their filename dates:
# 13 logs refused, 32 lines, every one an x-minute ("13:0x", "17:4x", "06:xx")
# or a tilde on a heading's own time ("## ~16:40 PT"), dated 09-19..11-03 (the
# 11-03 line quotes another seat's hand-typed stamp verbatim); 0 future-dated;
# 0 false refusals. A first cut that also refused "~HH:MM" in body text refused
# 7 more logs, all on projections ("ETA ~20:30", "reboots ~07:30 PT") — the
# body-tilde branch was dropped on that evidence, not tuned.
#
# Reads ADDED log lines on stdin (the "+" side of a staged diff, prefixes
# stripped — the same feed as check_drain.sh) for ONE log whose filename date
# is $1. Refuses when:
#   1. any added line writes a minute with an x ("13:0x", "17:4x", "06:xx") —
#      a digit nobody read is always an estimate of record, never a projection;
#   2. a heading's OWN time is marked as an estimate ("## ~16:40 PT", "## ≈17:00",
#      "## about 16:40") — a heading is the record's timestamp;
#   3. a timed heading falls after the Pacific clock on the file's date (a
#      minute of grace for the write itself);
#   4. the filename date itself is after today (Pacific).
# A tilde before a time in BODY text is allowed: the calibration replay found it
# used only for projections and plans ("ETA ~20:30", "finishes ~10:32", "Amber
# reboots ~07:30 PT"), which are estimates by nature, not records of when a
# thing happened. Body times are not future-checked: a body line may quote a
# UTC time or another day's ("upload finalized 00:25:01Z").
# Exit 0 = pass, 1 = refuse, 2 = usage/clock error (a gate that cannot read
# the clock must not pass). Called from scripts/hooks/pre-commit; tested by
# scripts/test_check_log_times.sh.
#
# Heading-time position (brief 11-21, Klatch unit-493, calibration 2026-11-21,
# copied from the replay of all 76 logs): the rule "a heading's own time opens
# the heading" was measured true on 184 of 186 timed headings and enforced by
# nothing; the two exceptions (07-13 "## xian's calls (18:00)", 07-14 "## Session
# start (05:51)") are the only lines the position rule refuses on replay — 2
# refused, 0 false. The alternative (read the first time found anywhere in the
# heading) was tested against its own hazard before this one was chosen: it
# takes a quoted time as the entry's own and checks the wrong row silently.
set -uo pipefail
export TZ=America/Los_Angeles
d=${1:-}
[[ "$d" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] || { echo "check_log_times: usage: check_log_times.sh YYYY-MM-DD < added-lines (got '$d')" >&2; exit 2; }
to_epoch() {  # to_epoch "YYYY-MM-DD HH:MM" -> seconds; BSD date first (Amber), GNU fallback
  date -j -f '%Y-%m-%d %H:%M' "$1" +%s 2>/dev/null || date -d "$1" +%s 2>/dev/null
}
now=$(date +%s) || { echo "check_log_times: cannot read the clock (exit 2)" >&2; exit 2; }
today=$(date +%F)
bad=0
if [[ "$d" > "$today" ]]; then
  echo "check_log_times: log is dated $d but today is $today — a future-dated log is refused" >&2; bad=1
fi
EST_X='\b[0-9]{1,2}:([0-9]x|x[0-9]|xx)\b'
HAS_T='[0-9]{1,2}:[0-9]{2}'   # any clock time at all (the position rule below)
while IFS= read -r line; do
  if printf '%s' "$line" | grep -qiE "$EST_X"; then
    echo "check_log_times: a minute is written with an x — an estimate, not a reading of the clock — refused:" >&2
    echo "    ${line:0:160}" >&2; bad=1
    continue
  fi
  # Brief 11-21 (Klatch unit-493): "a heading's own time opens the heading" was
  # measured true on 184 of 186 timed headings in the 74-log replay and enforced
  # by nothing — the two exceptions ("## xian's calls (18:00)", "## Session start
  # (05:51)") carry their time where the key below cannot see it, so neither the
  # estimate nor the future check ever ran on them. Reading the first time found
  # anywhere instead would take a quoted time ("## Mail wake — Pard reboots at
  # 15:00") as the entry's own and check the wrong row; refusing is the visible
  # failure. ## and ### alike; a heading with no time at all stays allowed.
  if printf '%s' "$line" | grep -qE '^#{2,3} ' && printf '%s' "$line" | grep -qE "$HAS_T" \
     && ! printf '%s' "$line" | grep -qE '^#{2,3} *(~|≈|about |approx\.? |approximately )?[0-9]{1,2}:[0-9]{2}'; then
    echo "check_log_times: the heading carries a time that does not open it — the clock gate reads a heading's own time only at its start; open the heading with the clock time, or leave it untimed — refused:" >&2
    echo "    ${line:0:160}" >&2; bad=1
    continue
  fi
  hd=$(printf '%s' "$line" | grep -oE '^#{2,3} *(~|≈|about |approx\.? |approximately )?[0-9]{1,2}:[0-9]{2}')
  [ -n "$hd" ] || continue
  if printf '%s' "$hd" | grep -qiE '(~|≈|about|approx)'; then
    echo "check_log_times: the heading's time is written as an estimate, not read from the clock — refused:" >&2
    echo "    ${line:0:160}" >&2; bad=1
    continue
  fi
  hm=$(printf '%s' "$hd" | grep -oE '[0-9]{1,2}:[0-9]{2}$')
  ts=$(to_epoch "$d $hm") || { echo "check_log_times: cannot parse '$d $hm' (exit 2)" >&2; exit 2; }
  [ -n "$ts" ] || { echo "check_log_times: cannot parse '$d $hm' (exit 2)" >&2; exit 2; }
  if [ "$ts" -gt $((now + 60)) ]; then
    echo "check_log_times: heading time $d $hm PT is after the clock ($(date '+%F %H:%M') PT) — a future-dated entry is refused:" >&2
    echo "    ${line:0:160}" >&2; bad=1
  fi
done
if [ "$bad" != 0 ]; then
  echo "    Rule: headings and times come from \`date\`, read at the moment of writing — never typed from memory or ahead of the clock." >&2
  exit 1
fi
exit 0
