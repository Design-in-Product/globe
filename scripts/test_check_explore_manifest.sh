#!/usr/bin/env bash
# Tests for scripts/check_explore_manifest.py. Each refusal is keyed on its
# REASON string (brief 10-25): a test that only sees "exit 1" cannot tell the
# declared-absent guard from the unreadable-manifest guard.
set -uo pipefail
cd "$(dirname "$0")/.."
C=scripts/check_explore_manifest.py
T="${TMPDIR:-/tmp}/check_explore_manifest.$$"; mkdir -p "$T"; trap 'rm -rf "$T"' EXIT
pass=0; fail=0
run() {  # run <want-exit> <want-substring|-> <name>  (manifest at $T/m.json)
  local want=$1 sub=$2 name=$3 out got
  out=$(python3 "$C" "$T/m.json" 2>&1); got=$?
  if [ "$got" = "$want" ] && { [ "$sub" = - ] || printf '%s' "$out" | grep -qF -- "$sub"; }; then pass=$((pass+1))
  else fail=$((fail+1)); echo "FAIL: $name (want exit $want with '$sub', got $got: ${out:0:160})"; fi
}
mk() { printf '%s' "$2" > "$T/$1"; }   # mk <name> <content>
# 1. all declared present -> ok
mk a.webp x; mk b.webp x
mk m.json '{"keyframes":[{"time_ma":1,"file":"a.webp"},{"time_ma":0,"file":"b.webp"}]}'
run 0 "2 declared, 2 present" "complete manifest passes"
# 2. declared but absent -> refuse, named
rm "$T/b.webp"
run 1 "DECLARED-ABSENT: 'b.webp'" "declared-absent refuses with its name"
# 3. present but undeclared -> reported, exit 0 (page does not break)
mk b.webp x; mk c.webp x
run 0 "PRESENT-UNDECLARED: c.webp" "present-undeclared is reported, not refused"
# 4. both kinds at once keep their separate labels (the brief's point)
rm "$T/a.webp"
out=$(python3 "$C" "$T/m.json" 2>&1); got=$?
if [ "$got" = 1 ] && grep -qF "DECLARED-ABSENT: 'a.webp'" <<< "$out" && grep -qF "PRESENT-UNDECLARED: c.webp" <<< "$out"; then pass=$((pass+1)); else fail=$((fail+1)); echo "FAIL: mixed absence not split by kind: $out"; fi
# 5. empty file field counts as declared-absent, not a crash
mk a.webp x; rm "$T/c.webp"
mk m.json '{"keyframes":[{"time_ma":1,"file":""},{"time_ma":0,"file":"b.webp"}]}'
run 1 "DECLARED-ABSENT: ''" "empty file field is declared-absent"
# 6. unreadable manifest -> exit 2 with its own reason, not declared-absent
mk m.json '{"keyframes": ['
run 2 "UNREADABLE" "broken JSON refuses for the unreadable reason"
mk m.json '{"frames":[]}'
run 2 "UNREADABLE" "manifest without keyframes key refuses for the unreadable reason"
# 7. duplicate declaration is named
mk m.json '{"keyframes":[{"time_ma":1,"file":"a.webp"},{"time_ma":0,"file":"a.webp"}]}'
run 0 "DECLARED-TWICE: a.webp" "duplicate declaration is reported"
# 8. the live manifests pass (this is the fire's real check)
out=$(python3 "$C" scrubber_assets/keyframes.json scrubber_assets/future/keyframes-future.json 2>&1); got=$?
if [ "$got" = 0 ] && ! grep -qE 'ABSENT|UNDECLARED|TWICE' <<< "$out"; then pass=$((pass+1)); else fail=$((fail+1)); echo "FAIL: live manifests: $out"; fi
echo "check_explore_manifest tests: $pass passed, $fail failed"
[ "$fail" = 0 ]
