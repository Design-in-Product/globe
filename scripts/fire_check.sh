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

echo "--- mail (newest 3 per repo, read from origin/main) ---"
# Sibling repos are read from Tessera's OWN clones in ~/globe-mail (fetch +
# ls-tree on origin/main), never by pulling ../mediajunkie or
# ../designinproduct: those are other seats' live working trees and a pull
# there can autostash their edits into a commit under my name (Pard's rule,
# 2026-10-08). Until 2026-10-26 this block pulled them every fire.
echo "  globe:"; ls -t docs/mail 2>/dev/null | head -3 | sed "s/^/    /"
for r in mediajunkie designinproduct; do
  c="$HOME/globe-mail/$r"
  [ -d "$c/.git" ] || { echo "  $r: UNMEASURABLE (no clone at $c)"; continue; }
  git -C "$c" fetch -q origin 2>/dev/null || echo "  $r: fetch failed (showing last known origin/main)"
  echo "  $r (origin/main $(git -C "$c" log origin/main -1 --format=%h -- docs/mail)):"
  git -C "$c" log origin/main --format=%h -n 40 -- docs/mail | while read -r h; do git -C "$c" show --name-only --format= --diff-filter=A "$h" -- docs/mail; done | awk '!seen[$0]++' | head -3 | sed "s|^docs/mail/|    |"
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
# every tracked page, derived from git — not a hardcoded list (brief 10/06 finding 2)
python3 scripts/check_explore_syntax.py $(git ls-files "*.html") | sed "s/^/  /"
# Explore manifest coverage (brief 10-26, Klatch round 457): the two kinds of
# absence named separately — DECLARED-ABSENT (page 404s) vs PRESENT-UNDECLARED
# (dead weight shipped). One "missing" word would hide one behind the other.
python3 scripts/check_explore_manifest.py scrubber_assets/keyframes.json scrubber_assets/future/keyframes-future.json
dns=$(dig +short @8.8.8.8 globe.dinp.xyz CNAME 2>/dev/null | head -1); [ -n "$dns" ] && echo "  dns globe.dinp.xyz: CNAME $dns" || echo "  dns globe.dinp.xyz: NO RECORD at 8.8.8.8 (NXDOMAIN?) (NOT OK)"
code=$(curl -s -o /dev/null -w "%{http_code}" https://globe.dinp.xyz/explore/); [ "$code" = 200 ] && echo "  live /explore/: 200" || echo "  live /explore/: $code (NOT OK)"
python3 scripts/wait_pages.py --timeout 5 | sed "s/^/  /"

echo "--- repo + host ---"
echo "  hook: $(git config core.hooksPath) exec=$(test -x scripts/hooks/pre-commit && echo yes || echo NO)"
echo "  stray blender: $(pgrep -fl "[B]lender" | wc -l | tr -d " ")   supervisor: $(pgrep -fl "[r]ender_supervised" | wc -l | tr -d " ")"
live=$(grep -v "^#" docs/cpu-declarations.tsv 2>/dev/null | awk -F"\t" -v now="$(TZ=America/Los_Angeles date +%Y-%m-%dT%H:%M)" '$2 > now {n++} END{print n+0}')
echo "  live cpu declarations: $live"
# Ignore-list coverage sweep (brief 10-26, Piper Morgan whats-armed): .gitignore
# denies bulk by NAME (test_spin_*/, check_*/, render_frames_v7/ ...). A frame
# set that lands under a name no pattern anticipates is one `git add .` from
# the publishing trap (memory: globe-repo-publishing-trap). So each fire lists
# every untracked, non-ignored path and flags any that is big: a file over
# 5 MB or a directory holding over 50 files. "none" is the only clean verdict.
bulk=$(git status --porcelain -uall | grep '^??' | cut -c4- | python3 -c '
import os,sys
big=[]; dirs={}
for l in sys.stdin:
    f=l.rstrip("\n").strip("\"")
    if not os.path.isfile(f): continue
    if os.path.getsize(f) > 5*1024*1024: big.append(f"{f} ({os.path.getsize(f)//1048576} MB)")
    top=f.split("/")[0]
    if "/" in f: dirs[top]=dirs.get(top,0)+1
big += [f"{d}/ ({n} files)" for d,n in dirs.items() if n > 50]
print("\n".join(big))')
if [ -z "$bulk" ]; then echo "  unignored bulk: none (every untracked path is small; the ignore list covers the rest)"
else echo "  UNIGNORED BULK (no .gitignore pattern covers these; add one before any git add .) (NOT OK):"; echo "$bulk" | sed 's/^/    /'; fi
