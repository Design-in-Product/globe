#!/usr/bin/env bash
# Content-pointer check for the living handoff (brief 10-27, Piper Morgan CIO):
# a commit-date freshness check is blind to content staleness — one edited
# character resets `git log -1` while the substantive sections rot. This
# searches the handoff for specific pointers that must agree with the rest of
# the repo, and exits with one of FOUR states so an error can never be read as
# a finding in either direction:
#   0 = every pointer present and consistent
#   1 = gaps (each named on stdout)
#   2 = pattern/tool error (a grep or git call failed for a reason other than no match)
#   3 = nothing matched at all (wrong file, empty file: the check did not run, it did not pass)
# Usage: check_handoff_pointers.sh [handoff.md]   (default: the living handoff)
set -uo pipefail
cd "$(git rev-parse --show-toplevel)" || exit 2
H="${1:-docs/handoff-tessera-2026-09-29.md}"
[ -r "$H" ] || { echo "  handoff: UNREADABLE $H (exit 2)"; exit 2; }
gaps=0; checked=0
gap() { gaps=$((gaps+1)); echo "    GAP: $*"; }
# 3: nothing matched — no section headings at all means this is not a handoff
nheads=$(grep -cE '^## ' "$H"); rc=$?
[ "$rc" -le 1 ] || { echo "  handoff: grep failed (exit 2)"; exit 2; }
[ "$nheads" -gt 0 ] || { echo "  handoff: NOTHING MATCHED in $H — no '## ' sections (exit 3)"; exit 3; }
# Pointer 1: the header's Updated date vs the file's last commit date. A body
# edit without a header bump is the single-character-reset case.
hdr=$(grep -oE '\*\*Updated [0-9]{4}-[0-9]{2}-[0-9]{2}\*\*' "$H" | head -1 | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}')
if git ls-files --error-unmatch -- "$H" >/dev/null 2>&1; then
  last=$(git log -1 --format=%ad --date=short -- "$H") || { echo "  handoff: git log failed (exit 2)"; exit 2; }
else last=""; fi   # an untracked copy (a test input) has no commit date; pointer 1 is skipped, not failed
checked=$((checked+1))
if [ -z "$hdr" ]; then gap "no '**Updated YYYY-MM-DD**' header"
elif [ -n "$last" ] && [[ "$hdr" < "$last" ]] && ! git diff --quiet -- "$H"; then :  # being edited now; the commit will carry today's header
elif [ -n "$last" ] && [[ "$hdr" < "$last" ]]; then gap "header says Updated $hdr but the file's last commit is $last (edited without re-dating: content may be stale)"; fi
# Pointer 2: the header must not trail the newest log by more than 14 days —
# the handoff is "current state"; two weeks of fires with no refresh is drift.
newest_log=$(ls logs 2>/dev/null | grep -oE '^[0-9]{4}-[0-9]{2}-[0-9]{2}' | sort | tail -1)
checked=$((checked+1))
if [ -n "$hdr" ] && [ -n "$newest_log" ]; then
  d=$(( ( $(date -j -f %F "$newest_log" +%s) - $(date -j -f %F "$hdr" +%s) ) / 86400 ))
  [ "$d" -le 14 ] || gap "header Updated $hdr is $d d behind the newest log ($newest_log); refresh the state sections"
fi
# Pointer 3: the ship set. Every film index.html's FILMS table serves must be named here.
films=$(grep -oE "'tectonic_[a-z_0-9]+\.mp4'" index.html | tr -d "'" | sed 's/\.mp4$//' | sort -u)
[ -n "$films" ] || { echo "  handoff: NOTHING MATCHED — no FILMS in index.html (exit 3)"; exit 3; }
for f in $films; do checked=$((checked+1)); grep -qF "$f" "$H" || gap "live film $f is not named in the handoff (ship set drift)"; done
# Pointer 4: required sections.
for sec in 'Operating model' 'Traps that cost real time' 'Where things live' 'Who owes what' 'Cold start'; do
  checked=$((checked+1)); grep -qE "^## $sec" "$H" || gap "section '## $sec' missing"
done
# Pointer 5: Who-owes-what vs the newest log's Drain line. If the latest Drain
# defers with a blocker on xian, the xian row cannot say he owes "Nothing".
drain=$(grep -ihE '^\**Drain:' "logs/$newest_log-tessera-log.md" 2>/dev/null | tail -1)
xrow=$(grep -E '^\| \*\*xian\*\* \|' "$H" | head -1 | cut -d'|' -f3)
checked=$((checked+1))
if [ -z "$xrow" ]; then gap "no xian row in 'Who owes what'"
elif printf '%s' "$drain" | grep -qiE 'blocker: (his|xian)' && printf '%s' "$xrow" | grep -qiE '^\s*Nothing'; then
  gap "latest Drain line defers on xian but 'Who owes what' says xian owes Nothing"
fi
if [ "$gaps" = 0 ]; then echo "  handoff: $checked pointers present and consistent (header $hdr, last commit ${last:-uncommitted}, newest log $newest_log)"; exit 0
else echo "  handoff: $gaps of $checked pointers GAP (NOT OK)"; exit 1; fi
