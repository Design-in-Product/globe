#!/usr/bin/env bash
# Constructed-case test for the pre-commit size gate (GitHub refuses blobs of
# 100 MiB or more; scripts/hooks/pre-commit refuses the commit first).
#
# Brief 11-08 (Klatch, unit-465sizeguard): "unreachable" / "never fires" is a
# claim about tests, not about code — the only proof is building the scenario.
# Until 2026-11-08 this gate had sat in the hook since 10-06 with no test that
# ever staged a 100 MiB file; its refusal message had never been seen. This
# script clones the repo (no checkout, index only), points core.hooksPath at
# the COMMITTED hook, and stages real files of exactly the boundary sizes.
# Run: scripts/test_size_gate.sh   (exit 0 = all pass; needs ~200 MB of tmp)
set -uo pipefail
cd "$(dirname "$0")/.."
LIMIT=104857600
MSG='GitHub refuses blobs of 100 MiB or more'
pass=0; fail=0
T=$(mktemp -d "${TMPDIR:-/tmp}/size_gate.XXXXXX"); C="$T/clone"
trap 'rm -rf "$T"' EXIT
git clone -q --no-checkout . "$C" || { echo "FAIL: could not clone"; exit 1; }
git -C "$C" reset -q && git -C "$C" checkout -q HEAD -- scripts && git -C "$C" config core.hooksPath scripts/hooks
G() { git -C "$C" -c user.name="Tessera (test)" -c user.email=t@example.invalid "$@"; }
mk() { mkfile -n "$2" "$C/$1" 2>/dev/null || head -c "$2" /dev/zero > "$C/$1"; }
# expect <0|1> <name> : run the staged commit; want this exit; a refusal must carry MSG
expect() {
  local want=$1 name=$2 err got
  err=$(G commit -q -m "$name" 2>&1 >/dev/null); got=$?
  if [ "$got" != "$want" ]; then fail=$((fail+1)); echo "FAIL: $name (want exit $want, got $got: ${err:0:140})"; return; fi
  if [ "$want" = 1 ] && ! printf '%s' "$err" | grep -qF -- "$MSG"; then fail=$((fail+1)); echo "FAIL: $name refused for another reason: ${err:0:140}"; return; fi
  pass=$((pass+1))
}
# A: a new file of exactly the limit is refused, for the size reason.
mk a.mp4 $LIMIT; G add -f a.mp4; expect 1 "A: new file at 100 MiB"; G reset -q HEAD -- a.mp4; rm -f "$C/a.mp4"
# B: one byte under the limit commits.
mk b.mp4 $((LIMIT-1)); G add -f b.mp4; expect 0 "B: new file at 100 MiB - 1"
# C: a MODIFIED tracked file that grows to the limit is refused (the gate's
# filter is AM; a test of A alone would not prove the M half).
mk b.mp4 $LIMIT; G add -f b.mp4; expect 1 "C: tracked file modified to 100 MiB"; G restore -q --staged --worktree b.mp4
# D: a rename of the just-committed 100 MiB-1 file passes (R is read as A+D
# under --no-renames; the A side is one byte under and must still pass).
G mv b.mp4 c.mp4; expect 0 "D: renamed file still under the limit"
# Cripple pass: disarm the size comparison in a scratch copy of the hook and
# prove case A now commits — i.e. the refusal above came from THIS gate.
sed -e "s/-ge $LIMIT/-ge 999999999999/" scripts/hooks/pre-commit > "$C/scripts/hooks/pre-commit"
cmp -s scripts/hooks/pre-commit "$C/scripts/hooks/pre-commit" && { fail=$((fail+1)); echo "FAIL: cripple changed nothing (sed matched no line)"; }
mk a.mp4 $LIMIT; G add -f a.mp4
err=$(G commit -q -m "cripple" 2>&1 >/dev/null); got=$?
if [ "$got" = 0 ]; then pass=$((pass+1)); else fail=$((fail+1)); echo "FAIL: crippled hook still refuses (exit $got) — case A was proving a backstop, not the size gate: ${err:0:140}"; fi
echo "size gate tests: $pass passed, $fail failed"
[ "$fail" = 0 ]
