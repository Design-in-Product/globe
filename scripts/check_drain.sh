#!/usr/bin/env bash
# Drain guard: reads ADDED log lines on stdin (the "+" side of a staged diff,
# prefixes stripped) and refuses when a new entry lacks a "Drain:" line, or a
# Drain line defers work without naming a blocker. Exit 0 = pass, 1 = refuse.
#
# xian's rule via Janus, 2026-10-08: "the fire is a wake, not a time-box"
# (designinproduct/docs/conventions/duty-cycle-drain.md). Called from
# scripts/hooks/pre-commit; tested by scripts/test_check_drain.sh.
#
# Block opener: ANY "## " heading. Brief 10-19 (One Job, DinP): a guard that
# opens blocks only on one canonical heading shape ("## HH:MM PT — ...")
# silently checks nothing once the headings drift — here they drifted to
# "## 16:22 fire", "## 21:16 wake — ...", "## 11:35–12:00 PT" on 10-16 and
# eight entries went unchecked. Every ## section in a tessera log is an
# entry (one per fire or wake), so every one carries a Drain line.
set -uo pipefail
bad=0; head=""; seen_drain=0; in_block=0
check_block() {
  if [ "$in_block" = 1 ] && [ "$seen_drain" = 0 ]; then
    echo "check_drain: entry without a Drain: line — refused:" >&2; echo "    $head" >&2; bad=1
  fi
}
while IFS= read -r line; do
  if printf '%s' "$line" | grep -qE '^## '; then
    check_block; head="$line"; in_block=1; seen_drain=0
  elif printf '%s' "$line" | grep -qiE '^\**Drain:'; then
    seen_drain=1
    if printf '%s' "$line" | grep -qiE '\b(defer|deferred|later|next fire|tomorrow|by [0-9]{1,2}:[0-9]{2})\b' && \
       ! printf '%s' "$line" | grep -qiE '(blocked on|blocker:|waits? on|waiting on|needs .* from|owed by|awaits)'; then
      echo "check_drain: Drain line defers work without naming a blocker — refused:" >&2
      echo "    ${line:0:160}" >&2; bad=1
    fi
  fi
done
check_block
if [ "$bad" != 0 ]; then
  echo "    Rule: a fire is a wake, not a time-box. Do unblocked work now; defer only with a named blocker." >&2
  exit 1
fi
exit 0
