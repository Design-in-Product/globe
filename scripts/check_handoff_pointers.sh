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
gaps=0; checked=0; skipped=0; skipnote=""
gap() { gaps=$((gaps+1)); echo "    GAP: $*"; }
# A pointer that could not be measured this run is SKIPPED, counted apart from
# the consistent ones and named in the summary (brief 10-30, Klatch: a map
# keyed on verdicts is blind to members still in a measurement state, and
# reads as complete at the moment it is filed). Until 10-30 a skipped
# pointer 1 was folded into "N pointers present and consistent".
skip() { skipped=$((skipped+1)); skipnote="${skipnote:+$skipnote; }$*"; }
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
elif [ -z "$last" ]; then skip "header-vs-commit (untracked copy, no commit date)"
elif [[ "$hdr" < "$last" ]] && ! git diff --quiet -- "$H"; then skip "header-vs-commit (file is being edited; the commit will carry today's header)"
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
# Key anchored on the FILMS object itself, any quote style (brief 11-19, Klatch: a
# key that a no-op rewrite can flip measures coincidence — the old single-quote
# key read nothing (exit 3) on a copy of index.html with the quotes swapped).
films=$(sed -n '/const FILMS = {/,/^ *};/p' index.html | grep -oE "tectonic_[a-z_0-9]+\.mp4" | sed 's/\.mp4$//' | sort -u)
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
# Pointer 6: typed test-case counts vs the scripts' own summary lines (brief
# 11-17, Klatch: a figure typed into a record is indistinguishable from one
# read from the output, and is exactly right until the standing value goes
# stale — the check belongs at write time, against the output itself). Each
# test script this file NAMES is run and its "P passed, F failed" read: the
# typed N must equal P+F and F must be 0. ~55 s for the six.
# Key (brief 11-19, Klatch: a key a no-op reword can flip, or silently drop a
# member from, measures textual coincidence): the census is every
# `scripts/test_*.sh` the handoff names anywhere; the count is then looked for
# inside that name's own table cell, before any other backticked path. Until
# 2026-11-19 the key was "name within 40 chars of '(N cases'": moving the count
# a few words away dropped the script from the census with the verdict still
# green (16 of 16). Now a named script with no count is SKIPPED by name; one
# whose script is missing or prints no summary is a GAP, not a skip.
while IFS= read -r t; do
  [ -n "$t" ] || continue
  checked=$((checked+1))
  # Brief 11-23 (Klatch unit-505): the instrument reads bytes, not intent. Until
  # 2026-11-23 this took the FIRST "(N cases" after the name anywhere in the file
  # — which on 11-22 was the header's history clause, agreeing with the table row
  # by coincidence; the next day the row said 15 and the clause 14, and the
  # check reported the clause. Now every count the file attaches to the name is
  # read, and two different figures are themselves a GAP.
  ns=$(grep -F "\`$t\`" "$H" | grep -oE "\`$t\`[^|\`]*" | grep -oE '\(([0-9]+) cases' | grep -oE '[0-9]+' | sort -un)
  if [ -z "$ns" ]; then skip "$t is named without a case count to verify"; continue; fi
  if [ "$(printf '%s\n' "$ns" | wc -l | tr -d ' ')" -ne 1 ]; then gap "handoff states different case counts for $t ($(printf '%s' "$ns" | paste -sd, -)) — one is stale"; continue; fi
  n=$ns
  if [ ! -f "$t" ]; then gap "handoff names $t ($n cases) but no such script"; continue; fi
  summ=$(bash "$t" 2>&1 | grep -oE '[0-9]+ passed, [0-9]+ failed' | tail -1)
  if [ -z "$summ" ]; then gap "$t printed no 'P passed, F failed' summary — its $n-case claim is unmeasured"; continue; fi
  pz=${summ%% passed*}; fz=${summ##*passed, }; fz=${fz%% failed}
  if [ "$fz" -ne 0 ]; then gap "$t: $summ — the handoff presents it as a passing $n-case suite"
  elif [ $((pz+fz)) -ne "$n" ]; then gap "handoff says $t has $n cases; it ran $((pz+fz)) ($summ) — typed figure is stale"
  else echo "    $t: $summ (handoff says $n cases)"; fi
done < <(grep -oE '\`scripts/test_[a-z_]+\.sh\`' "$H" | tr -d '\`' | sort -u)
sk=""; [ "$skipped" -gt 0 ] && sk=", $skipped SKIPPED not measured: $skipnote"
if [ "$gaps" = 0 ]; then echo "  handoff: $((checked-skipped)) of $checked pointers present and consistent$sk (header $hdr, last commit ${last:-uncommitted}, newest log $newest_log)"; exit 0
else echo "  handoff: $gaps of $checked pointers GAP (NOT OK)$sk"; exit 1; fi
