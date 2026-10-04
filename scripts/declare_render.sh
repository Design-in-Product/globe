#!/usr/bin/env bash
# Declare a Blender pass to Pard's cpu-hogs check BEFORE launching it.
#
# Appends one row to docs/cpu-declarations.tsv with an expiry HOURS from now
# (Pacific), commits, pushes, and verifies the row is on origin/main — because
# the check reads origin/main, not the working tree (Pard, 2026-10-04). A row
# that is not pushed is not a declaration.
#
# Why a script and not a note: brief 9/30 — a discipline that depends on
# remembering is not structural. render_supervised.sh warns if no live row is
# on origin/main when it starts.
#
# Usage: scripts/declare_render.sh HOURS "reason"      (HOURS <= 12: Pard's ceiling)
set -uo pipefail
HOURS="${1:?hours}"; REASON="${2:?reason}"
FILE=docs/cpu-declarations.tsv
if [ "$HOURS" -gt 12 ]; then echo "refusing: $HOURS h exceeds the 12 h ceiling; the row would be reported and not honoured" >&2; exit 2; fi
cd "$(git rev-parse --show-toplevel)"
expires=$(TZ=America/Los_Angeles date -v+"${HOURS}"H "+%Y-%m-%dT%H:%M")
printf "Blender\t%s\ttessera\t%s\n" "$expires" "$REASON" >> "$FILE"
git add "$FILE"
git commit -q -m "declare: Blender pass until $expires — $REASON" || { echo "nothing to commit" >&2; exit 3; }
git push -q origin HEAD:main || { echo "push failed; declaration NOT on record" >&2; exit 4; }
if git fetch -q origin && git show origin/main:"$FILE" | grep -F "$expires" >/dev/null; then
  echo "declared on origin/main: Blender until $expires ($REASON)"
else
  echo "row not visible on origin/main after push — do not launch" >&2; exit 5
fi
