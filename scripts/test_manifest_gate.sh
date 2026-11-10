#!/usr/bin/env bash
# Constructed-case test for the pre-commit Explore manifest gate and the
# derivation it reads (scripts/explore_manifests.sh).
#
# Brief 11-08: "proven in a clone" once is not a test. The 11-09 cure (list
# derived from git, empty list refused by name) was exercised by hand in a
# throwaway clone and never registered; brief 11-10 then showed the cure had
# copied its own rule by hand. This script builds each scenario against the
# COMMITTED hook in a no-checkout clone (commit the guard before testing it
# in a clone — memory 10-26), keys every refusal on its reason string, and
# ends with a cripple pass proving the third-manifest case tests the
# derivation and not a backstop.
# Run: scripts/test_manifest_gate.sh   (exit 0 = all pass; ~15 MB of tmp)
set -uo pipefail
cd "$(dirname "$0")/.."
MSG_ABSENT='declares a keyframe that is not on disk'
MSG_EMPTY='no Explore manifest'
pass=0; fail=0
T=$(mktemp -d "${TMPDIR:-/tmp}/manifest_gate.XXXXXX"); C="$T/clone"
trap 'rm -rf "$T"' EXIT
git clone -q --no-checkout . "$C" || { echo "FAIL: could not clone"; exit 1; }
git -C "$C" reset -q && git -C "$C" checkout -q HEAD -- scripts scrubber_assets && git -C "$C" config core.hooksPath scripts/hooks
G() { git -C "$C" -c user.name="Tessera (test)" -c user.email=t@example.invalid "$@"; }
# expect <0|1> <reason|-> <name> : commit what is staged; want this exit; a refusal must carry the reason
expect() {
  local want=$1 msg=$2 name=$3 err got
  err=$(G commit -q -m "$name" 2>&1 >/dev/null); got=$?
  if [ "$got" != "$want" ]; then fail=$((fail+1)); echo "FAIL: $name (want exit $want, got $got: ${err:0:160})"; return; fi
  if [ "$want" = 1 ] && ! printf '%s' "$err" | grep -qF -- "$msg"; then fail=$((fail+1)); echo "FAIL: $name refused for another reason: ${err:0:160}"; return; fi
  pass=$((pass+1))
}
# the derivation sees exactly the tracked manifests, read from the clone's index
want=$(git ls-files -- 'scrubber_assets/*.json' 'scrubber_assets/**/*.json' | sort -u)
got=$(bash "$C/scripts/explore_manifests.sh")
if [ -n "$got" ] && [ "$got" = "$want" ]; then pass=$((pass+1)); else fail=$((fail+1)); echo "FAIL: derivation differs from git ls-files: [$got]"; fi
# 0. baseline: a new undeclared asset is reported, not refused (the page does not break)
printf x > "$C/scrubber_assets/zz_test.webp"; G add -f scrubber_assets/zz_test.webp
expect 0 - "0: new undeclared asset commits with complete manifests"
# A. a tracked manifest edited to declare a file that is not on disk is refused, for that reason
python3 - "$C/scrubber_assets/keyframes.json" <<'PY'
import json,sys
p=sys.argv[1]; m=json.load(open(p)); m["keyframes"].append({"time_ma":9999,"file":"nope.webp"}); json.dump(m,open(p,"w"))
PY
G add scrubber_assets/keyframes.json; expect 1 "$MSG_ABSENT" "A: manifest declares a keyframe not on disk"
G restore -q --staged --worktree scrubber_assets/keyframes.json
# C. a THIRD manifest, never named anywhere, is read because the list is derived
printf '{"keyframes":[{"time_ma":1,"file":"nope.webp"}]}' > "$C/scrubber_assets/third.json"
G add scrubber_assets/third.json; expect 1 "$MSG_ABSENT" "C: a third manifest is gated through the derived list"
G rm -q --cached scrubber_assets/third.json
# B. no manifest tracked + an asset staged: refused by name, and the derivation prints nothing
G rm -q --cached scrubber_assets/keyframes.json scrubber_assets/future/keyframes-future.json
printf x > "$C/scrubber_assets/zz2.webp"; G add -f scrubber_assets/zz2.webp
empty=$(bash "$C/scripts/explore_manifests.sh")
if [ -z "$empty" ]; then pass=$((pass+1)); else fail=$((fail+1)); echo "FAIL: derivation not empty with no manifest tracked: [$empty]"; fi
expect 1 "$MSG_EMPTY" "B: asset staged with no manifest tracked"
G reset -q HEAD -- scrubber_assets/keyframes.json scrubber_assets/future/keyframes-future.json
G rm -q --cached scrubber_assets/zz2.webp
# Cripple pass: hand-type the two 11-08 names back into a scratch copy of the
# hook; case C must now COMMIT — the third manifest goes unchecked, which is
# exactly what the derivation exists to prevent.
sed -e 's|manifests=$(bash scripts/explore_manifests.sh)|manifests="scrubber_assets/keyframes.json scrubber_assets/future/keyframes-future.json"|' scripts/hooks/pre-commit > "$C/scripts/hooks/pre-commit"
cmp -s scripts/hooks/pre-commit "$C/scripts/hooks/pre-commit" && { fail=$((fail+1)); echo "FAIL: cripple changed nothing (sed matched no line)"; }
G add scrubber_assets/third.json
err=$(G commit -q -m "cripple" 2>&1 >/dev/null); got=$?
if [ "$got" = 0 ]; then pass=$((pass+1)); else fail=$((fail+1)); echo "FAIL: crippled hook still refuses (exit $got) — case C was proving a backstop, not the derivation: ${err:0:160}"; fi
echo "manifest gate tests: $pass passed, $fail failed"
[ "$fail" = 0 ]
