#!/usr/bin/env bash
# The duty-cycle fire's health + mail block, as a script instead of a retyped
# one-liner (brief 9/30: a discipline you must remember is not structural).
#
# Adds the one check the hand version never had (brief 10/05, finding 2): the
# AGE of the newest dated cross-pollination brief, against a threshold derived
# from the delivery record itself — not a clock time, which would false-alarm
# whenever Janus runs an hour late. Presence of a brief proves the pipeline
# ever ran; age measures whether it is running.
#
# Every check prints a verdict. A check that cannot be measured says so rather
# than printing a pass (UNMEASURABLE is a state, silence is not).
set -uo pipefail
ts() { TZ=America/Los_Angeles date "+%F %T %Z"; }
cd "$(git rev-parse --show-toplevel)"
echo "fire check $(ts)"

echo "--- sync ---"
git fetch -q origin && git merge --ff-only origin/main 2>&1 | tail -1

echo "--- mail (newest 3 per repo) ---"
for d in . ../mediajunkie ../designinproduct; do
  [ -d "$d/.git" ] || { echo "  $d: not a repo"; continue; }
  [ "$d" != "." ] && git -C "$d" pull -q origin main 2>/dev/null
  echo "  $(basename "$(cd "$d" && pwd)"):"; (cd "$d" && ls -t docs/mail 2>/dev/null | head -3 | sed "s/^/    /")
done
echo "  addressed to tessera, newest 2:"; ls -t docs/mail | grep -iE "to-tessera|to-all" | head -2 | sed "s/^/    /"

echo "--- brief age (threshold derived from the delivery record) ---"
dated=$(ls docs/briefs/cross-pollination 2>/dev/null | grep -E "^[0-9]{4}-[0-9]{2}-[0-9]{2}\.md$" | sort)
if [ -z "$dated" ]; then
  echo "  UNMEASURABLE: no dated briefs on disk (current.md alone proves nothing)"
else
  newest=$(echo "$dated" | tail -1 | cut -c1-10)
  today=$(TZ=America/Los_Angeles date +%F)
  age=$(( ( $(date -j -f %F "$today" +%s) - $(date -j -f %F "$newest" +%s) ) / 86400 ))
  # largest gap between consecutive dated briefs in the last 30 on record = the tolerated lateness
  maxgap=$(echo "$dated" | tail -30 | cut -c1-10 | python3 -c "
import sys,datetime as d
ds=[d.date.fromisoformat(l.strip()) for l in sys.stdin if l.strip()]
print(max((b-a).days for a,b in zip(ds,ds[1:])) if len(ds)>1 else 1)")
  if [ "$age" -gt "$maxgap" ]; then echo "  STALE: newest brief $newest is $age d old; largest gap in record is $maxgap d"
  else echo "  ok: newest brief $newest, age $age d (record tolerates $maxgap d)"; fi
fi

echo "--- site ---"
python3 scripts/check_explore_syntax.py | sed "s/^/  /"
code=$(curl -s -o /dev/null -w "%{http_code}" https://globe.dinp.xyz/explore/); [ "$code" = 200 ] && echo "  live /explore/: 200" || echo "  live /explore/: $code (NOT OK)"
python3 scripts/wait_pages.py --timeout 5 | sed "s/^/  /"

echo "--- repo + host ---"
echo "  hook: $(git config core.hooksPath) exec=$(test -x scripts/hooks/pre-commit && echo yes || echo NO)"
echo "  stray blender: $(pgrep -fl "[B]lender" | wc -l | tr -d " ")   supervisor: $(pgrep -fl "[r]ender_supervised" | wc -l | tr -d " ")"
live=$(grep -v "^#" docs/cpu-declarations.tsv 2>/dev/null | awk -F"\t" -v now="$(TZ=America/Los_Angeles date +%Y-%m-%dT%H:%M)" '$2 > now {n++} END{print n+0}')
echo "  live cpu declarations: $live"
