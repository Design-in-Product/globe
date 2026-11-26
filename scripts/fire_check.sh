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
#
# Brief 11-25 (Klatch unit-513): a fallible read whose consumers IGNORE the
# result fails as a silent survival, not a break — so the detector must plant
# the null and read the downstream state, not wait for an error. Every read
# in this script that can come back empty was classified 2026-11-25 by what
# its consumer does; nine continued into a clean-looking line (planted and
# read: the sync printed nothing, two inboxes read stale, the deploy-retry
# census shrank, 0 fires due read as all logged, login days went blank, a
# missing TSV read 0/0, the bulk sweep read "none", and the VERDICT read an
# empty capture — and a part-run abort — as clean). Each is named now, and
# run_checks ends with a sentinel the verdict requires.
set -uo pipefail
ts() { TZ=America/Los_Angeles date "+%F %T %Z"; }
cd "$(git rev-parse --show-toplevel)"
# The failure labels the VERDICT counts, one per line (brief 11-20, Klatch
# unit-486: a label that is a substring of another — GUARDED inside UNGUARDED —
# lets a stable reader pick up the wrong row). Kept as a list so the pairwise
# self-check below can read it and so both greps share one key.
# MEASURED TRUE, by coincidence (brief 11-21, Klatch unit-493): no healthy line
# contains a label — but the key is applied to every printed line, including
# sibling-inbox memo FILENAMES copied verbatim, and those miss the key only
# because they are lowercase-hyphenated by convention ("not-a-pass" is not
# "not a pass"). Nothing enforces that. The failure direction is a visible
# false NOT-clean verdict on a strangely named memo, which a reader dismisses;
# the silent direction (a real failure printed in a form the key misses) is
# the one the 11-18 positive controls guard.
FAIL_LABELS='NOT OK
GAP:
UNMEASURABLE
did not run
not a pass
NO RECORD
SYNTAX ERROR
GUARD TRIPPED
EXTRACTION FAILED
DECLARED-ABSENT
PRESENT-UNDECLARED
DECLARED-TWICE
UNREADABLE
UNIGNORED BULK
TIMEOUT
ERRORED
STALE:
deployment failure
deployment error
deployment inactive'
FAILKEY=$(printf '%s\n' "$FAIL_LABELS" | paste -sd'|' -)
echo "fire check $(ts)"
# Brief 11-01 (Piper Morgan CIO, methodology-57 "an alarm needs a reader"): a
# check is unfinished until a named reader reads it at a named time through a
# named step. This script's reader is Tessera, twice a day, through the fire's
# first command — but that reader views the output through a grep -v and a
# tail, and a failure line that happened to match the filter would never be
# seen. So every check's output is captured and the LAST line is a verdict
# that counts the failure words, whatever filter sits in front of it.
run_checks() {

echo "--- sync ---"
# A fetch failure printed NOTHING here (planted 11-25: && skipped the merge
# line, and the mail and brief blocks below read a stale origin/main as now).
if git fetch -q origin 2>/dev/null; then git merge --ff-only origin/main 2>&1 | tail -1
else echo "  sync: git fetch origin failed — the mail and brief blocks below read a stale origin/main (NOT OK)"; fi

echo "--- mail (newest 3 per repo, read from origin/main) ---"
# Sibling repos are read from Tessera's OWN clones in ~/globe-mail (fetch +
# ls-tree on origin/main), never by pulling ../mediajunkie or
# ../designinproduct: those are other seats' live working trees and a pull
# there can autostash their edits into a commit under my name (Pard's rule,
# 2026-10-08). Until 2026-10-26 this block pulled them every fire.
echo "  globe:"; ls -t docs/mail 2>/dev/null | head -3 | sed "s/^/    /"
# The one key both the live line and its positive control use (single-sourced).
naming_me_key() { grep -iE 'tessera' | grep -viE '^docs/mail/(memo-|reply-|question-)?tessera-to-'; }
lcase=0   # real inbox filenames carrying a verdict label in lowercase (reach of the key's case rule; read below)
for r in mediajunkie designinproduct; do
  c="$HOME/globe-mail/$r"
  [ -d "$c/.git" ] || { echo "  $r: UNMEASURABLE (no clone at $c)"; continue; }
  git -C "$c" fetch -q origin 2>/dev/null || echo "  $r: fetch failed — this fire's read of the inbox is stale (NOT OK)"
  echo "  $r (origin/main $(git -C "$c" log origin/main -1 --format=%h -- docs/mail)):"
  # One git log with --name-only replaces the 40 `git show` spawns per repo this
  # line ran until 2026-11-05 (brief 11-05, Mediajunkie: a subprocess per item
  # is a silent O(n) bottleneck). Same output byte for byte; 0.68 s -> 0.05 s.
  git -C "$c" log origin/main --name-only --format= --diff-filter=A -n 40 -- docs/mail | awk 'NF && !seen[$0]++' | head -3 | sed "s|^docs/mail/|    |"
  # Memos in a SIBLING inbox that name me (to- or cc-) among the last 40 added,
  # keyed on the FILENAME, not the commit subject: brief 11-12 (Klatch) — a key
  # over optional metadata returns a plausible, too-small count; commit
  # subjects name the recipient only when the sender's tool does, filenames
  # always do (dispatch convention). My own outbound (tessera-to-) is excluded.
  git -C "$c" log origin/main --name-only --format= --diff-filter=A -n 40 -- docs/mail | awk 'NF && !seen[$0]++' \
    | naming_me_key | head -3 | sed "s|^docs/mail/|    naming me: |"
  # Positive control (brief 11-15, Klatch via Pard: a matcher that reported 0 of
  # 105 fires published as ok for 13 days because nothing read the match count).
  # The line above is silent when nothing names me — and equally silent when the
  # key is broken. So the SAME key runs over the whole inbox, which is known to
  # hold memos whose FILENAME mentions me (at least one per inbox — 4 and 1 when
  # the control was written on 2026-11-15, all to Pard or Janus; nothing addressed
  # to me lands here). The control is a FLOOR (>= 1), not an exact count (brief
  # 11-18, Klatch: an exact pin on a population another repo owns goes false on
  # any drift; a floor only breaks if that population shrinks). The live count
  # prints below each fire, so the typed figures here never stand in for it.
  # 0 there means the key is blind, not the inbox quiet.
  known=$(git -C "$c" ls-tree -r --name-only origin/main -- docs/mail | naming_me_key | wc -l | tr -d ' ')
  if [ "${known:-0}" -eq 0 ]; then echo "    naming-me key: NOT OK — matched 0 over the whole inbox, which is known to name me; the line above is blind"
  else echo "    naming-me key control: $known known memo(s) over the whole inbox match"; fi
  lc=$(git -C "$c" ls-tree -r --name-only origin/main -- docs/mail | grep -ciE "$FAILKEY" || true); lcase=$((lcase+${lc:-0}))
done
echo "  addressed to tessera, newest 2:"; ls -t docs/mail | grep -iE "to-tessera|to-all" | head -2 | sed "s/^/    /"

echo "--- brief age (threshold derived from the delivery record) ---"
dated=$(ls docs/briefs/cross-pollination 2>/dev/null | grep -E "^[0-9]{4}-[0-9]{2}-[0-9]{2}\.md$" | sort)
if [ -z "$dated" ]; then
  echo "  UNMEASURABLE: no dated briefs on disk (current.md alone proves nothing)"
else
  newest=$(echo "$dated" | tail -1 | cut -c1-10)
  today=$(TZ=America/Los_Angeles date +%F)
  # Brief 11-25: an unparsable filename date here raised a bash arithmetic
  # error that ABORTED run_checks — 28 lines printed, VERDICT clean (planted
  # 11-25 with a brief named 2026-13-45.md). Parse first and name the failure.
  te=$(date -j -f %F "$today" +%s 2>/dev/null) || te=""
  ne=$(date -j -f %F "$newest" +%s 2>/dev/null) || ne=""
  # largest gap between consecutive dated briefs in the last 30 on record = the tolerated lateness
  maxgap=$(echo "$dated" | tail -30 | cut -c1-10 | python3 -c "
import sys,datetime as d
ds=[d.date.fromisoformat(l.strip()) for l in sys.stdin if l.strip()]
print(max((b-a).days for a,b in zip(ds,ds[1:])) if len(ds)>1 else 1)" 2>/dev/null) || maxgap=""
  if [ -z "$te" ] || [ -z "$ne" ] || [ -z "$maxgap" ]; then echo "  brief age: a brief filename date does not parse (newest '$newest', record gap '${maxgap:-unparsed}') — UNMEASURABLE (NOT OK)"
  else
    age=$(( (te - ne) / 86400 ))
    if [ "$age" -gt "$maxgap" ]; then echo "  STALE: newest brief $newest is $age d old; largest gap in record is $maxgap d"
    else echo "  ok: newest brief $newest, age $age d (record tolerates $maxgap d)"; fi
  fi
fi

echo "--- site ---"
# every tracked page, derived from git — not a hardcoded list (brief 10/06 finding 2)
git ls-files -z -- '*.html' | xargs -0 python3 scripts/check_explore_syntax.py | sed "s/^/  /"
# Explore manifest coverage (brief 10-26, Klatch round 457): the two kinds of
# absence named separately — DECLARED-ABSENT (page 404s) vs PRESENT-UNDECLARED
# (dead weight shipped). One "missing" word would hide one behind the other.
# The manifest list is derived from git, not typed (brief 11-09, Klatch: census
# the cross-references before changing one — this list was hardcoded in three
# places until 2026-11-09, so a third manifest would have gone unchecked in all
# of them). The derivation is scripts/explore_manifests.sh, shared with the
# hook (brief 11-10: two hand-typed copies of the rule are the defect again).
# An empty derived list is UNMEASURABLE, never a pass: the checker's usage
# message carries no failure word and would otherwise read as clean.
manifests=$(bash scripts/explore_manifests.sh)
if [ -z "$manifests" ]; then echo "  explore manifests: UNMEASURABLE (no scrubber_assets/*.json tracked)"
# shellcheck disable=SC2086
else printf '%s\n' "$manifests" | tr '\n' '\0' | xargs -0 python3 scripts/check_explore_manifest.py; fi
# Brief 10-31 (Piper Morgan CIO, methodology-48): name the question, then run
# the check against the case that should fail. Until 10-31 the dns line asked
# "is there a CNAME" (any target passed), the live line asked "did something
# return 200" (any page passed), the hook line printed a path and a mode bit
# without saying whether they were the right path or a script that parses.
# Each now compares against the thing the question is actually about.
dns_want="design-in-product.github.io."
dns=$(dig +short @8.8.8.8 globe.dinp.xyz CNAME 2>/dev/null | head -1)
if [ -z "$dns" ]; then echo "  dns globe.dinp.xyz: NO RECORD at 8.8.8.8 (NXDOMAIN?) (NOT OK)"
elif [ "$dns" = "$dns_want" ]; then echo "  dns globe.dinp.xyz: CNAME $dns"
else echo "  dns globe.dinp.xyz: CNAME $dns — expected $dns_want (NOT OK)"; fi
# One HTTP status read, retried up to 3x (3 s apart) while the edge answers
# 5xx or nothing (2026-11-16: a single 503 from the Pages edge read as "the
# exclusion is not live" — a transport failure is UNMEASURABLE, not a
# wrong answer). Args: URL, body file (/dev/null to discard), extra curl flags.
http_code() { local url=$1 out=$2; shift 2; local c try=0
  while :; do c=$(curl -s -o "$out" -w "%{http_code}" "$@" "$url"); try=$((try+1))
    case "$c" in 5*|000) [ "$try" -ge 3 ] && break; sleep 3;; *) break;; esac; done
  echo "$c"; }
live_body=$(mktemp "${TMPDIR:-/tmp}/fire_live.XXXXXX")
code=$(http_code https://globe.dinp.xyz/explore/ "$live_body")
marker=$(grep -c "scrubber_assets/" "$live_body" 2>/dev/null || true); rm -f "$live_body"
if [ "$code" != 200 ]; then echo "  live /explore/: $code (NOT OK)"
elif [ "${marker:-0}" -eq 0 ]; then echo "  live /explore/: 200 but the body has no scrubber_assets/ reference — some other page is answering (NOT OK)"
else echo "  live /explore/: 200, atlas page ($marker scrubber_assets refs)"; fi
python3 scripts/wait_pages.py --timeout 5 2>&1 | sed "s/^/  /"; pw=${PIPESTATUS[0]}
[ "$pw" -ge 2 ] && echo "  pages: did not run (exit $pw) — not a pass"
# Pages exclusion took effect (11-12): the first plain-file entry of
# .pages-exclude must 404 on the live site and the hero film must still 200.
# Reads the list, so a renamed entry is probed by its new name; no entry at
# all is "unmeasured", not a pass.
ex=$(grep -vE '^[[:space:]]*(#|$)' .pages-exclude 2>/dev/null | grep -v '/$' | grep -v ' ' | head -1)
if [ -z "$ex" ]; then echo "  pages exclude: no plain-file entry in .pages-exclude — exclusion unmeasured (NOT OK)"
else
  exc=$(http_code "https://globe.dinp.xyz/$ex" /dev/null)
  hero=$(http_code "https://globe.dinp.xyz/tectonic_globe_v8.mp4" /dev/null -I)
  if [ "$exc" = 404 ] && [ "$hero" = 200 ]; then echo "  pages exclude: /$ex 404, hero film 200 (exclusion live)"
  elif case "$exc$hero" in *5[0-9][0-9]*|*000*) true;; *) false;; esac; then echo "  pages exclude: edge answered /$ex $exc, hero film $hero after 3 tries — UNMEASURABLE this fire (NOT OK)"
  else echo "  pages exclude: /$ex returned $exc (want 404), hero film $hero (want 200) (NOT OK)"; fi
fi
# 2026-11-23: the deploy retry (added 11-13) recovers an artifact race silently —
# wait_pages above reads "deployed" either way, and whether the retry fired was
# read by hand from the run's steps each fire (runs 45055648358 on 11-22 and
# 45296844062 on 11-23 both raced: upload finalized, deploy-pages looked <1 s
# later and found 0). Read here instead: for the last 10 completed runs on main,
# the "wait 30 s" step's conclusion is "skipped" (first try) or "success" (the
# retry fired). Informational, not a failure — the retry working is the design;
# a rising count is the thing to notice. Control: run 45296844062, a known race,
# must read as a retry; a reader that cannot see it is named UNMEASURABLE.
if command -v gh >/dev/null 2>&1; then
  retry_of() { gh run view "$1" --json jobs -q '.jobs[] | .steps[] | select(.name | test("wait 30")) | .conclusion' 2>/dev/null | head -1; }
  rids=$(gh run list --workflow pages.yml --branch main --status completed --limit 10 --json databaseId -q '.[].databaseId' 2>/dev/null)
  rn=0; rr=0; ru=0; rl=""
  # Brief 11-25: a run whose read failed was dropped from both counts and the
  # census quietly shrank (planted: 9 unreadable runs read "fired on 1 of the
  # last 1 runs", no failure word). An unreadable run is counted and named.
  for id in $rids; do c=$(retry_of "$id"); [ -n "$c" ] || { ru=$((ru+1)); continue; }; rn=$((rn+1)); [ "$c" = success ] && { rr=$((rr+1)); rl="$rl $id"; }; done
  rctl=$(retry_of 45296844062)
  if [ "$rctl" != success ]; then echo "  pages retry: control run 45296844062 (a known race) read '${rctl:-nothing}', expected success — the retry reader is blind (UNMEASURABLE) (NOT OK)"
  elif [ "$rn" -eq 0 ]; then echo "  pages retry: no completed run readable — UNMEASURABLE (NOT OK)"
  elif [ "$ru" -gt 0 ]; then echo "  pages retry: fired on $rr of $rn readable runs, but $ru of the last $((rn+ru)) could not be read — census incomplete (UNMEASURABLE) (NOT OK)"
  else echo "  pages retry: fired on $rr of the last $rn runs${rl:+ (runs$rl)} (control: known race reads as a retry, 1)"; fi
else echo "  pages retry: gh not on PATH — UNMEASURABLE (NOT OK)"; fi

echo "--- repo + host ---"
hp=$(git config core.hooksPath); hv=""
[ "$hp" = "scripts/hooks" ] || hv="hooksPath is '${hp:-unset}', not scripts/hooks"
[ -x scripts/hooks/pre-commit ] || hv="${hv:+$hv; }pre-commit not executable"
bash -n scripts/hooks/pre-commit 2>/dev/null || hv="${hv:+$hv; }pre-commit does not parse"
[ -z "$hv" ] && echo "  hook: scripts/hooks, pre-commit executable and parses" || echo "  hook: $hv (NOT OK — commits will not be gated)"
# The scheduler that wakes this seat (brief 11-01: a check needs a reader; the
# LaunchAgent's own launchd logs are empty by design, so its state is read here,
# by me, each fire). Fields from `launchctl list`: PID (or -), last exit, label.
la=$(launchctl list 2>/dev/null | awk '$3=="com.xian.tessera-cycle"{print $1" "$2}')
if [ -z "$la" ]; then echo "  launchd: com.xian.tessera-cycle NOT LOADED — no fire will come (NOT OK)"
elif [ "${la#* }" != 0 ]; then echo "  launchd: com.xian.tessera-cycle loaded, last exit ${la#* } (NOT OK)"
else echo "  launchd: com.xian.tessera-cycle loaded, last exit 0 (10:22 + 16:22 PT)"; fi
# Brief 11-23 (Piper Morgan via Pard): a fire that stops at a permission prompt
# nobody is there to answer writes nothing — and launchd still reads "last exit
# 0" above, because the injector exited, not the fire. The only trace a blocked
# fire leaves is a MISSING log entry. So every scheduled fire of the last 24 h
# that is more than an hour old must have a "## HH:MM" heading in its day's log
# within three hours of the fire (a fire folded into running work lands late,
# never early). Control: the same reader against a date with no log must
# report the fire missing (1) — a reader that cannot see a gap is not a reader.
fire_logged() {  # fire_logged <YYYY-MM-DD> <HH:MM> -> 0 heading in [fire, fire+3h] / 1 none / 2 unparsable
  local d=$1 hm=$2 f="logs/$1-tessera-log.md" fe he
  fe=$(date -j -f '%Y-%m-%d %H:%M' "$d $hm" +%s 2>/dev/null) || return 2
  [ -f "$f" ] || return 1
  while read -r h; do
    he=$(date -j -f '%Y-%m-%d %H:%M' "$d $h" +%s 2>/dev/null) || continue
    [ "$he" -ge "$fe" ] && [ "$he" -le $((fe + 10800)) ] && return 0
  done < <(grep -oE '^## *[0-9]{1,2}:[0-9]{2}' "$f" | grep -oE '[0-9]{1,2}:[0-9]{2}$')
  return 1
}
now_e=$(date +%s); due=0; missing=""
for d in "$(date -v-1d +%F)" "$(date +%F)"; do for hm in 10:22 16:22; do
  fe=$(date -j -f '%Y-%m-%d %H:%M' "$d $hm" +%s 2>/dev/null) || continue
  [ "$fe" -le $((now_e - 3600)) ] && [ "$fe" -ge $((now_e - 86400)) ] || continue
  due=$((due+1)); fire_logged "$d" "$hm" || missing="$missing $d $hm;"
done; done
fire_logged 2000-01-01 10:22; fctl=$?
if [ "$fctl" != 1 ]; then echo "  scheduled fires: reader control returned $fctl for a date with no log, expected 1 — the missing-entry check is blind (NOT OK)"
elif [ "$due" -eq 0 ]; then echo "  scheduled fires: 0 due in the last 24 h — with two fires a day at least one is always due, so the schedule reader is blind (NOT OK)"
elif [ -n "$missing" ]; then echo "  scheduled fires: $due due in the last 24 h, no log entry within 3 h of:$missing — a fire that writes nothing may be stopped at a prompt (NOT OK)"
else echo "  scheduled fires: $due due in the last 24 h, each has a log entry within 3 h (control: date with no log reads missing, 1)"; fi
# Login expiry for THIS seat's config dir (brief 11-13, Pard: credentials are
# stored per config dir and expire independently; a renewal elsewhere shows no
# warning here). Pard's cycle-check reads all three Amber entries; this line is
# the seat's own reading of its own entry, four-state like the rest.
cfg=${CLAUDE_CONFIG_DIR:-$HOME/.claude}
if ! command -v claude >/dev/null 2>&1; then echo "  login ($cfg): claude not on PATH — UNMEASURABLE (NOT OK)"
else
  exp=$(CLAUDE_CONFIG_DIR="$cfg" perl -e 'alarm 20; exec @ARGV' claude auth status 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("loginExpiresAt","") if d.get("loggedIn") else "")' 2>/dev/null || true)
  if [ -z "$exp" ]; then echo "  login ($cfg): not logged in or status unreadable — UNMEASURABLE (NOT OK)"
  else
    days=$(python3 -c 'import sys,datetime as d; e=d.datetime.fromisoformat(sys.argv[1].replace("Z","+00:00")); print((e-d.datetime.now(d.timezone.utc)).days)' "$exp" 2>/dev/null) || days=""
    if [ -z "$days" ]; then echo "  login ($cfg): expiry '$exp' did not parse — UNMEASURABLE (NOT OK)"
    elif [ "$days" -lt 7 ]; then echo "  login ($cfg): expires $exp — $days days left, renew now (NOT OK)"
    else echo "  login ($cfg): expires ${exp%T*}, $days days left"; fi
  fi
fi
# Brief 11-22 (Klatch unit-496): a 0 from a form-keyed detector cannot tell
# "none running" from "pgrep cannot see processes". The control counts this
# very script by the same pipeline (a floor: >= 1; a parent shell can add one).
seen=$(pgrep -fl "[f]ire_check" | wc -l | tr -d " ")
if [ "${seen:-0}" -ge 1 ]; then ctl="control: this script seen by pgrep, $seen"
else ctl="control: pgrep did not see this script — the 0s are blind (NOT OK)"; fi
echo "  stray blender: $(pgrep -fl "[B]lender" | wc -l | tr -d " ")   supervisor: $(pgrep -fl "[r]ender_supervised" | wc -l | tr -d " ")   ($ctl)"
# Brief 11-25: with the file absent both counts read 0 and the line looked
# clean (planted); the planted-row control below proves awk, not the read.
tsv=docs/cpu-declarations.tsv
if [ ! -f "$tsv" ]; then echo "  cpu declarations: $tsv is missing — both counts would read 0 (UNMEASURABLE) (NOT OK)"
else
live=$(grep -v "^#" "$tsv" 2>/dev/null | awk -F"\t" -v now="$(TZ=America/Los_Angeles date +%Y-%m-%dT%H:%M)" '$2 > now {n++} END{print n+0}')
expired=$(grep -v "^#" "$tsv" 2>/dev/null | awk -F"\t" -v now="$(TZ=America/Los_Angeles date +%Y-%m-%dT%H:%M)" '$2 != "" && $2 <= now {n++} END{print n+0}')
# Same brief: the two counts above read a TSV through awk; a planted row dated
# 2000 must count as expired, or the 0s are the reader failing, not the file.
pl=$(printf 'planted\t2000-01-01T00:00\n' | awk -F"\t" -v now="$(TZ=America/Los_Angeles date +%Y-%m-%dT%H:%M)" '$2 != "" && $2 <= now {n++} END{print n+0}')
[ "${pl:-0}" = 1 ] && pctl="control: planted expired row counted, 1" || pctl="control: planted expired row counted ${pl:-0}, expected 1 — the reader is blind (NOT OK)"
echo "  live cpu declarations: $live   expired rows still in file: $expired$( [ "$expired" -gt 0 ] && echo "  <-- remove (Pard 10-28: noise that hides a real stale case)")   ($pctl)"
fi
# Disk (brief 10-28, Piper Morgan CIO re-run: a duty kept as a log habit lapses
# within days). On 10-21 I wrote "will log when df actually moves" after local
# Time Machine snapshots pinned the 14 GB the frame-set delete freed; df moved
# 96 -> 118 GB and the log never said so. A printed line each fire replaces the
# habit: free space, the render tree, and the snapshot count that can pin it.
echo "  disk: $(df -h / | awk 'NR==2{print $4}') free on /   render tree: $(du -sh ~/globe-render 2>/dev/null | cut -f1 || echo absent)   local TM snapshots: $(tmutil listlocalsnapshots / 2>/dev/null | grep -c . )"
# Living-doc content pointers (brief 10-27, Piper Morgan CIO): a commit date
# cannot see content staleness. Four states: present / gaps / error / nothing.
scripts/check_handoff_pointers.sh; hrc=$?
[ "$hrc" -le 1 ] || echo "  handoff check did not run (exit $hrc) — that is not a pass (NOT OK)"
# Ignore-list coverage sweep (brief 10-26, Piper Morgan whats-armed): .gitignore
# denies bulk by NAME (test_spin_*/, check_*/, render_frames_v7/ ...). A frame
# set that lands under a name no pattern anticipates is one `git add .` from
# the publishing trap (memory: globe-repo-publishing-trap). So each fire lists
# every untracked, non-ignored path and flags any that is big: a file over
# 5 MB or a directory holding over 50 files. "none" is the only clean verdict.
# Brief 11-25: a failed git status fed the sweep nothing and it printed "none"
# (planted) — no paths seen is not the same as no bulk. Status goes to a file
# first so its exit can be read (a NUL-separated list cannot sit in a variable).
st=$(mktemp "${TMPDIR:-/tmp}/fire_status.XXXXXX")
if ! git status --porcelain -z -uall > "$st" 2>/dev/null; then bulk="UNMEASURABLE: git status failed — the sweep saw no paths, which is not none"
else
bulk=$(tr '\0' '\n' < "$st" | grep '^??' | cut -c4- | python3 -c '
import os,sys
big=[]; dirs={}
for l in sys.stdin:
    f=l.rstrip("\n")
    if not os.path.isfile(f): continue
    if os.path.getsize(f) > 5*1024*1024: big.append(f"{f} ({os.path.getsize(f)//1048576} MB)")
    top=f.split("/")[0]
    if "/" in f: dirs[top]=dirs.get(top,0)+1
big += [f"{d}/ ({n} files)" for d,n in dirs.items() if n > 50]
print("\n".join(big))')
fi; rm -f "$st"
if [ -z "$bulk" ]; then echo "  unignored bulk: none (every untracked path is small; the ignore list covers the rest)"
elif [ "${bulk#UNMEASURABLE}" != "$bulk" ]; then echo "  unignored bulk: $bulk (NOT OK)"
else echo "  UNIGNORED BULK (no .gitignore pattern covers these; add one before any git add .) (NOT OK):"; echo "$bulk" | sed 's/^/    /'; fi
# Verdict-key self-check (brief 11-20, Klatch unit-486). Every label in
# FAIL_LABELS is compared with every other: one inside another would let a new
# label double-count or shadow a line. The control constructs the collision
# directly (GUARDED/UNGUARDED -> 1 pair) each run, so a broken comparer shows.
FAIL_LABELS="$FAIL_LABELS" python3 -c '
import os
def pairs(ls): return [(a,b) for a in ls for b in ls if a!=b and a in b]
ls=[l for l in os.environ["FAIL_LABELS"].split("\n") if l]
got=pairs(ls); ctl=pairs(["GUARDED","UNGUARDED"])
if len(ctl)!=1: print(f"  verdict key: comparer control returned {len(ctl)} pair(s) for GUARDED/UNGUARDED, expected 1 — self-check did not run (NOT OK)")
elif got: print(f"  verdict key: {len(ls)} labels, {len(got)} substring pair(s) {got} — a label inside another (NOT OK)")
else: print(f"  verdict key: {len(ls)} labels, 0 substring pairs (control GUARDED/UNGUARDED: 1 pair)")
' || echo "  verdict key: self-check did not run (NOT OK)"
# Brief 11-23 (Klatch unit-505): a gate reads bytes, not intent. What keeps a
# sibling memo filename carrying "timeout" or "errored" from reading as a
# failure line above is that the key is case-sensitive and filenames are
# lowercase by convention (annotated 11-21, never driven). Driven here: a
# planted lowercase filename must miss the key and the uppercase label must hit.
lo=$(printf '    memo-x-to-pard-timeout-errored-unreadable-2026-11-23.md\n' | grep -cE "$FAILKEY" || true)
hi=$(printf '  something TIMEOUT here\n' | grep -cE "$FAILKEY" || true)
# Brief 11-26 (Klatch unit-520): a declared blindspot whose only instances are
# the ones the declaring instrument planted is unfalsifiable, and its reach in
# production is a separate measurement. Both directions of this one are
# measured here, not just driven. Visible direction: real sibling-inbox
# filenames that carry a label word in lowercase (4 over both inboxes on
# 11-26) — the case rule is load-bearing for them, so it is not an idle guard.
# Silent direction: this script's own emitters (non-comment echo lines, the key
# definition excluded) that carry a label word in a case the key misses — on
# 11-26 exactly one, the healthy "unignored bulk: none" line; a failure emitter
# in that set would be a real failure the verdict cannot see, hence NOT OK.
miss=$(grep -nE '^[^#]*echo' "$0" | grep -vE 'FAIL_LABELS|FAILKEY|unignored bulk: none' | grep -iE "$FAILKEY" | grep -vE "$FAILKEY" | cut -d: -f1 | paste -sd, -)
if [ "${lo:-9}" -eq 0 ] && [ "${hi:-0}" -eq 1 ] && [ -z "$miss" ]; then echo "  verdict key: case-sensitive — planted lowercase memo filename misses (0), uppercase label hits (1); reach: $lcase real inbox filename(s) carry a label word in lowercase, 0 own emitters a failure could hide in (1 healthy emitter excluded by name)"
elif [ "${lo:-9}" -eq 0 ] && [ "${hi:-0}" -eq 1 ]; then echo "  verdict key: case-sensitive (planted: 0/1 as expected) but own emitter line(s) $miss carry a label word in a case the key misses — a failure printed there is invisible to the verdict (NOT OK)"
else echo "  verdict key: planted lowercase filename matched $lo time(s), uppercase label $hi — the mail block could forge or hide a verdict (NOT OK)"; fi
# Ignore-pattern census (brief 11-20, Klatch unit-487): a count of markers is
# an upper bound on markers doing work. The bulk sweep above trusts the ignore
# list by name; this line says which .gitignore patterns match a path on disk
# this fire and names the dormant ones (prophylactic names such as test_spin_*/
# that nothing on disk exercises today). Dormant is not stale — the names
# anticipate render output — but a dormant pattern is unproven, so it is named
# rather than folded into "covers the rest". Matching is whole-line (a pattern
# is not "used" because its text sits inside another pattern's text). A
# tracked file that an ignore pattern would match means the pattern is not
# load-bearing for it (added before the pattern, or forced): named as a smell.
pats=$(grep -vE '^[[:space:]]*(#|$)' .gitignore 2>/dev/null || true)
npats=$(printf '%s\n' "$pats" | grep -c . || true)
if [ "${npats:-0}" -eq 0 ]; then echo "  ignore patterns: .gitignore missing or empty — UNMEASURABLE (NOT OK)"
else
  used=$(git ls-files -o -i --exclude-standard --directory -z | xargs -0 git check-ignore -v --no-index -- 2>/dev/null | grep '^\.gitignore:' | cut -f1 | cut -d: -f3- | sort -u)
  nused=$(printf '%s\n' "$used" | grep -c . || true)
  dormant=""
  while IFS= read -r p; do
    [ -n "$p" ] || continue
    case $'\n'"$used"$'\n' in *$'\n'"$p"$'\n'*) ;; *) dormant="$dormant$p " ;; esac
  done <<< "$pats"
  shadow=$(git ls-files -z | xargs -0 git check-ignore -v --no-index -- 2>/dev/null | grep -c '^\.gitignore:' || true)
  echo "  ignore patterns: $npats in .gitignore, $nused matching a path on disk now, $((npats-nused)) dormant: ${dormant:-none}"
  # Brief 11-22: the shadow count's 0 needs a control that proves the pipeline
  # (check-ignore + the .gitignore filter) can fire — a planted name that a
  # dormant pattern matches must count 1.
  sctl=$(printf 'render_v7.log\n' | git check-ignore -v --no-index --stdin 2>/dev/null | grep -c '^\.gitignore:' || true)
  if [ "${sctl:-0}" = 1 ]; then
    [ "${shadow:-0}" -eq 0 ] && echo "  ignore patterns: 0 tracked files shadowed (control: planted render_v7.log counted, 1)" \
      || echo "  ignore patterns: $shadow tracked file(s) match an ignore pattern — not load-bearing for them (inspect) (control: planted render_v7.log counted, 1)"
  else echo "  ignore patterns: shadow control counted ${sctl:-0} for planted render_v7.log, expected 1 — the shadow count is blind (NOT OK)"; fi
fi
# Brief 11-26 (Klatch unit-520), second reach measurement: the 11-24 readers
# (-z / unquoted ls-files, names as separate arguments) guard against git's
# quoting of non-ASCII, control, '"' and '\' bytes in paths — and every proof
# of them so far used planted names in scratch clones. The production reach is
# the tracked tree itself: how many tracked names git would quote, and how many
# carry a space (git does not quote a space; a word-splitting reader would
# still break it). On 11-26: 0 quotable, 1 spaced (tectonic_globe_v1 copy.mp4,
# tracked since 02-28, in .pages-exclude). A 0 here says the floors were
# counts; the control classifies a planted non-ASCII, spaced name as both.
census=$(git ls-files -z | python3 -I -c '
import sys
ns=[n for n in sys.stdin.buffer.read().split(b"\0") if n]
q=[n for n in ns if any(c>127 or c<32 or c in b"\"\\" for c in n)]
sp=[n for n in ns if b" " in n]
ctl=b"caf\xc3\xa9 plate.mp4"
cq=int(any(c>127 or c<32 or c in b"\"\\" for c in ctl)); cs=int(b" " in ctl)
print(len(ns),len(q),len(sp),cq+cs," ".join(x.decode("utf-8","replace") for x in sp[:3]))' 2>/dev/null)
read -r tn tq tsp tctl tnames <<< "${census:-}"
if [ -z "$census" ]; then echo "  tracked names: census did not run — UNMEASURABLE (NOT OK)"
elif [ "${tctl:-0}" != 2 ]; then echo "  tracked names: classifier control read $tctl for a planted non-ASCII spaced name, expected 2 — the census is blind (NOT OK)"
else echo "  tracked names: $tn tracked, $tq git would quote, $tsp with a space${tnames:+ ($tnames)} — the -z readers' live population (control: planted non-ASCII spaced name classified both, 2)"; fi
# Completion sentinel: the verdict below requires this as the capture's last
# line, so a check that aborts the function part-way cannot read as clean.
echo "--- end of checks ---"
}
out=$(mktemp "${TMPDIR:-/tmp}/fire_check.XXXXXX")
run_checks 2>&1 | tee "$out"
# Brief 11-25 (Klatch unit-513): the verdict is the consumer every other line
# depends on, and it read an EMPTY capture as "clean — no failure line in 0
# lines" and a run that aborted after 28 lines as clean (both planted 11-25).
# Clean now needs a non-empty capture ending in run_checks' sentinel.
nl=$(wc -l < "$out" | tr -d ' ')
fails=$(grep -cE "$FAILKEY" "$out" || true)
if [ ! -s "$out" ]; then echo "VERDICT: the checks' output is empty — nothing ran or the capture failed (did not run — not a pass)"
elif [ "$(tail -1 "$out")" != "--- end of checks ---" ]; then echo "VERDICT: checks did not run to completion — output ends at line $nl: '$(tail -1 "$out" | cut -c1-120)' (not a pass)"; [ "${fails:-0}" -gt 0 ] && grep -nE "$FAILKEY" "$out" | head -8 | sed 's/^/  /'
elif [ "${fails:-0}" -eq 0 ]; then echo "VERDICT: clean — no failure line in $nl lines"
else echo "VERDICT: $fails FAILURE LINE(S) above — read them:"; grep -nE "$FAILKEY" "$out" | head -8 | sed 's/^/  /'; fi
rm -f "$out"
