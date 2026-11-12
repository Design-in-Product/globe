#!/usr/bin/env bash
# Constructed-case test for the Pages staging + reference gate
# (scripts/stage_pages.sh, scripts/check_pages_refs.py, .pages-exclude).
#
# Brief 11-08: a one-off proof is not a test. Each case builds a tiny git repo
# in tmp with the WORKING-TREE copies of the two scripts, keys every refusal
# on its reason string, ends with a cripple pass (the gate call removed: the
# excluded-file case must then stage, proving the refusal was the gate's and
# not a backstop), and finally stages the REAL tracked tree once to prove the
# live .pages-exclude is consistent with the live pages (~0.5 GB of tmp, a
# few seconds; removed on exit).
# Run: scripts/test_pages_stage.sh   (exit 0 = all pass)
set -uo pipefail
cd "$(dirname "$0")/.."
MSG_UNRES='not in the upload'
MSG_STALE='matches no tracked file'
MSG_NOPAGE='no .html page found'
pass=0; fail=0
T=$(mktemp -d "${TMPDIR:-/tmp}/pages_stage.XXXXXX"); R="$T/repo"
trap 'rm -rf "$T"' EXIT
ok()   { pass=$((pass+1)); }
bad()  { fail=$((fail+1)); echo "FAIL: $*"; }
build() {  # fresh constructed repo
  rm -rf "$R"; mkdir -p "$R/scripts" "$R/sub" "$R/assets" "$R/data"
  cp scripts/stage_pages.sh scripts/check_pages_refs.py "$R/scripts/"
  cat > "$R/index.html" <<'H'
<!doctype html><a href="sub/">sub</a> <a href="#top">top</a> <a href="https://example.invalid/x.mp4">ext</a>
<video src="a.mp4" poster="p.png"></video>
<style>body{background:url("p.png")}</style>
<script>const FILMS={main:'b.mp4'}; const ASSETS="assets/"; fetch(ASSETS+"keyframes.json");</script>
H
  printf '<!doctype html><img src="../p.png"><video src="/a.mp4"></video>' > "$R/sub/index.html"
  printf '{"keyframes":[{"time_ma":0,"file":"k1.webp"}]}' > "$R/assets/keyframes.json"
  for f in a.mp4 b.mp4 c.mp4 p.png assets/k1.webp data/raw.gpml; do printf 'x' > "$R/$f"; done
  printf '# test\nc.mp4\ndata/\n' > "$R/.pages-exclude"
  git -C "$R" init -q && git -C "$R" -c user.name=t -c user.email=t@example.invalid add -A \
    && git -C "$R" -c user.name=t -c user.email=t@example.invalid commit -q -m init
}
# stage <want-exit> <reason|-> <name> [dest]: run the stager in the constructed repo
stage() {
  local want=$1 msg=$2 name=$3 dest=${4:-$T/site_$RANDOM} out got
  out=$(bash "$R/scripts/stage_pages.sh" "$dest" 2>&1); got=$?
  if [ "$got" != "$want" ]; then bad "$name (want exit $want, got $got): $(printf '%s' "$out" | tail -3)"; return 1; fi
  if [ "$want" != 0 ] && ! printf '%s' "$out" | grep -qF -- "$msg"; then bad "$name refused for another reason: $(printf '%s' "$out" | tail -3)"; return 1; fi
  ok; LAST="$dest"; LASTOUT=$out
}
# 1. baseline: stages; excluded absent; every referenced form present
build; stage 0 - "1: baseline stages" "$T/site1" && {
  for f in a.mp4 b.mp4 p.png sub/index.html assets/keyframes.json assets/k1.webp .pages-exclude; do [ -f "$T/site1/$f" ] || bad "1: $f missing from the stage"; done
  [ -e "$T/site1/c.mp4" ] && bad "1: excluded c.mp4 was staged"
  [ -e "$T/site1/data" ] && bad "1: excluded data/ was staged"
  printf '%s' "$LASTOUT" | grep -q "1 files staged" && bad "1: count line unexpectedly says 1"
  printf '%s' "$LASTOUT" | grep -qE "^stage_pages: 10 files staged, 2 excluded by 2 rule" || bad "1: count line wrong: $(printf '%s' "$LASTOUT" | head -1)"
}
# 2. a page names an EXCLUDED file: refused, by reason, naming the page and file
build; printf '<video src="c.mp4"></video>' >> "$R/index.html"
stage 1 "$MSG_UNRES" "2: page links an excluded file" && { printf '%s' "$LASTOUT" | grep -q "index.html names 'c.mp4'" || bad "2: refusal does not name page+file"; }
# 3. a page names a file that never existed (JS literal form)
build; printf "<script>const X='ghost.mp4'</script>" >> "$R/index.html"
stage 1 "$MSG_UNRES" "3: page names a missing film literal" && { printf '%s' "$LASTOUT" | grep -q "'ghost.mp4' (literal)" || bad "3: refusal does not name the literal"; }
# 4. a stale exclude entry (no such tracked file) is refused by name
build; printf 'gone.mp4\n' >> "$R/.pages-exclude"
stage 1 "$MSG_STALE" "4: stale exclude entry" && { printf '%s' "$LASTOUT" | grep -q "'gone.mp4'" || bad "4: refusal does not name the entry"; }
# 5. a manifest a page fetches declares a keyframe that is not there
build; printf '{"keyframes":[{"time_ma":0,"file":"k1.webp"},{"time_ma":1,"file":"k9.webp"}]}' > "$R/assets/keyframes.json"
stage 1 "$MSG_UNRES" "5: manifest declares a missing keyframe" && { printf '%s' "$LASTOUT" | grep -q "keyframes.json -> k9.webp' (manifest)" || bad "5: refusal does not name manifest+file"; }
# 6. no page at all: the gate refuses a vacuous pass (exit 2 from the gate -> stager exits 1)
build; git -C "$R" rm -q index.html sub/index.html
stage 1 "$MSG_NOPAGE" "6: no html page is not a pass"
# 7. dest exists: refused without touching it
build; mkdir -p "$T/site7"; printf 'keep' > "$T/site7/marker"
stage 2 "refusing to stage over" "7: existing dest refused" "$T/site7" && { [ "$(cat "$T/site7/marker")" = keep ] || bad "7: dest was touched"; }
# 8. cripple: remove the gate call; case 2 must now STAGE
build; printf '<video src="c.mp4"></video>' >> "$R/index.html"
sed -i.bak '/check_pages_refs.py/d' "$R/scripts/stage_pages.sh" && rm -f "$R/scripts/stage_pages.sh.bak"
grep -q check_pages_refs "$R/scripts/stage_pages.sh" && bad "8: cripple left the gate call in place"
stage 0 - "8: crippled stager stages the excluded-file page (so case 2 tested the gate)"
# 9. the REAL tree: live .pages-exclude + live pages stage clean, excluded absent, hero present
out=$(bash scripts/stage_pages.sh "$T/real" 2>&1); got=$?
if [ "$got" = 0 ]; then ok; else bad "9: real tree refused (exit $got): $(printf '%s' "$out" | grep -E 'UNRESOLVED|NOT OK' | head -3)"; fi
[ -f "$T/real/tectonic_globe_v8.mp4" ] && [ -f "$T/real/explore/index.html" ] && [ -f "$T/real/CNAME" ] && [ -f "$T/real/.nojekyll" ] || bad "9: a served file is missing from the real stage"
first=$(grep -vE '^[[:space:]]*(#|$)' .pages-exclude | grep -v '/$' | head -1)
[ -e "$T/real/$first" ] && bad "9: excluded '$first' is in the real stage"
[ -e "$T/real/data/plate-models" ] && bad "9: data/plate-models/ is in the real stage"
echo "  real stage: $(printf '%s' "$out" | head -1 | sed 's/^stage_pages: //')"
echo "  real stage: $(printf '%s' "$out" | grep '^  census:')"
echo "pages stage tests: $pass passed, $fail failed"
[ "$fail" = 0 ]
