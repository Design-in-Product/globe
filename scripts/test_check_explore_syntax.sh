#!/usr/bin/env bash
# Tests for scripts/check_explore_syntax.py (brief 11-22, Klatch unit-496: a
# detector that returns "OK" cannot tell "no error" from "cannot fire" without
# a live positive control). The checker's three arms were verified by hand on
# 2026-09-24 and never again; this suite runs them every fire and in CI, each
# refusal keyed on its REASON string. Run: bash scripts/test_check_explore_syntax.sh
set -uo pipefail
cd "$(dirname "$0")/.."
C=scripts/check_explore_syntax.py
PY=$(command -v python3)
T="${TMPDIR:-/tmp}/check_explore_syntax.$$"; mkdir -p "$T"; trap 'rm -rf "$T"' EXIT
pass=0; fail=0
run() {  # run <want-exit> <want-substring|-> <name> <page...>
  local want=$1 sub=$2 name=$3; shift 3; local out got
  out=$("$PY" "$C" "$@" 2>&1); got=$?
  if [ "$got" = "$want" ] && { [ "$sub" = - ] || printf '%s' "$out" | grep -qF -- "$sub"; }; then pass=$((pass+1))
  else fail=$((fail+1)); echo "FAIL: $name (want exit $want with '$sub', got $got: ${out:0:160})"; fi
}
# a script body long enough to clear MIN_CHARS (1000), valid JS
long=$(printf 'const pad%03d = %d;\n' $(seq 1 60 | awk '{print $1, $1}'))
page() { printf '<!doctype html><html><body>%s</body></html>' "$1" > "$T/$2"; }   # page <body-html> <name>
# A. real pages pass (the fire's own check)
run 0 "inline script block(s) OK" "A: explore/index.html passes" explore/index.html
run 0 "inline script block(s) OK" "A: index.html (classic script) passes" index.html
# B. an injected syntax error in a module block is refused for the syntax reason
page "<script type=\"module\">$long
const broken = ;</script>" bad_module.html
run 1 "SYNTAX ERROR" "B: module block with a syntax error" "$T/bad_module.html"
# C. the same in a classic block (brief 10/06: classic scripts were ungated until then)
page "<script>$long
function ( { </script>" bad_classic.html
run 1 "SYNTAX ERROR" "C: classic block with a syntax error" "$T/bad_classic.html"
# D. extraction too short trips the guard, not a pass (arm C of the 09-24 proof)
page "<script type=\"module\">const a = 1;</script>" short.html
run 3 "GUARD TRIPPED" "D: short extraction trips the guard" "$T/short.html"
# E. no inline script is reported as nothing to check, exit 0
page "<p>words</p>" none.html
run 0 "nothing to check" "E: page with no inline script" "$T/none.html"
# F. a src= include is not an inline block
page "<script src=\"app.js\"></script>" src.html
run 0 "nothing to check" "F: src= include is skipped" "$T/src.html"
# G. a non-JS typed block (JSON data) is skipped
page "<script type=\"application/json\">{\"a\": 1</script>" json.html
run 0 "nothing to check" "G: application/json block is skipped" "$T/json.html"
# H. a missing page is an extraction failure, exit 2
run 2 "EXTRACTION FAILED" "H: missing page" "$T/absent.html"
# I. the three stubs let a real module import parse
page "<script type=\"module\">import * as THREE from \"three\";
import { OrbitControls } from \"three/addons/controls/OrbitControls.js\";
$long</script>" imports.html
run 0 "1 inline script block(s) OK" "I: module importing three parses through the stubs" "$T/imports.html"
# J. the denominator counts blocks across pages
page "<script type=\"module\">$long</script><script>$long</script>" two.html
run 0 "3 script block(s) across 2 page(s)" "J: denominator across two pages" "$T/two.html" "$T/imports.html"
# K. node missing is an extraction failure, exit 2 — never a quiet pass
out=$(PATH=/nonexistent "$PY" "$C" "$T/imports.html" 2>&1); got=$?
if [ "$got" = 2 ] && printf '%s' "$out" | grep -qF "EXTRACTION FAILED: node is not on PATH"; then pass=$((pass+1))
else fail=$((fail+1)); echo "FAIL: K: node off PATH (want exit 2 with the node reason, got $got: ${out:0:160})"; fi
# --- cripple pass: disarm one branch in a scratch copy; the case that proved it must now pass ---
cripple() {  # cripple <name> <sed-expr> <page>
  local name=$1 expr=$2 pg=$3 got S="$T/crippled.py"
  sed -e "$expr" "$C" > "$S"
  cmp -s "$C" "$S" && { fail=$((fail+1)); echo "FAIL: cripple '$name' changed nothing"; return; }
  "$PY" "$S" "$pg" >/dev/null 2>&1; got=$?
  if [ "$got" = 0 ]; then pass=$((pass+1)); else fail=$((fail+1)); echo "FAIL: cripple '$name' still refuses (exit $got) — the case was proving a backstop"; fi
}
cripple "MIN_CHARS guard disarmed" 's/^MIN_CHARS = 1000/MIN_CHARS = 0/' "$T/short.html"
cripple "node --check disarmed (version only)" 's/"--check"/"--version"/' "$T/bad_module.html"
echo "check_explore_syntax tests: $pass passed, $fail failed"
[ "$fail" = 0 ]
