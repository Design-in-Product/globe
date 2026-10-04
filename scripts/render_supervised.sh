#!/usr/bin/env bash
# Crash-resilient driver for render_globe.py: relaunch from the first missing
# or truncated frame until the set is complete, with a crash budget.
#
# Why (2026-10-03): the sequel globe pass died at frame 9 with no error in
# the log — Blender 5.1.2 SIGSEGV'd inside Cycles' Metal kernel-pipeline
# compile (MTLBinaryArchive serializeToURL, on a shader-cache thread). Not
# the data, not the launch (both proven), not a stale on-disk cache (Blender
# keeps the archive in a per-session $TMPDIR). A single long-lived Blender
# process is therefore not a safe unit of work; a loop that resumes from
# the first gap is. render_globe.py's own png_complete() skips intact
# frames, so each relaunch costs only Blender startup (~15 s).
#
# A crash is an EVENT here, not silence: each one is counted and logged, the
# loop stops after MAX_CRASHES, and the exit code says why it stopped.
#
# Env (same as render_globe.py): FRAMES_DIR FRAME_PREFIX CAMERA_PATH_FILE RENDER_DIR
#      plus TOTAL_FRAMES (required), MAX_CRASHES (default 6), BLENDER (path).
set -uo pipefail
: "${TOTAL_FRAMES:?set TOTAL_FRAMES to the path frame count}"
: "${RENDER_DIR:?}"; : "${CAMERA_PATH_FILE:?}"; : "${FRAMES_DIR:?}"
BLENDER="${BLENDER:-/Applications/Blender.app/Contents/MacOS/Blender}"
MAX_CRASHES="${MAX_CRASHES:-6}"
LOG="${LOG:-$RENDER_DIR/../$(basename "$RENDER_DIR").supervisor.log}"
SCRIPT="$(cd "$(dirname "$0")" && pwd)/render_globe.py"
export OUTPUT_PATH=/dev/null
ts() { date "+%F %T"; }   # bash 3.2 chokes on single quotes inside $() inside double quotes

intact() {  # PNG with its IEND trailer present. Full-read grep: -q under pipefail can SIGPIPE xxd (10/02 lesson).
  [ -s "$1" ] && tail -c 12 "$1" | xxd -p | grep 49454e44 >/dev/null
}
# render_globe.py writes render_%04d with anim_frame+1: files are 1..TOTAL, and
# FRAME_START/FRAME_END are in that same 1-based space. Returns TOTAL+1 when complete.
first_missing() {
  local i; for ((i=1; i<=TOTAL_FRAMES; i++)); do
    local f; f=$(printf "%s/render_%04d.png" "$RENDER_DIR" "$i")   # no single quotes inside $(): bash 3.2
    intact "$f" || { echo "$i"; return; }
  done; echo "$((TOTAL_FRAMES+1))"
}

crashes=0
echo "$(ts) supervisor start: total=$TOTAL_FRAMES max_crashes=$MAX_CRASHES" | tee -a "$LOG"
while :; do
  start=$(first_missing)
  if [ "$start" -gt "$TOTAL_FRAMES" ]; then
    echo "$(ts) COMPLETE: $TOTAL_FRAMES/$TOTAL_FRAMES intact after $crashes crash(es)" | tee -a "$LOG"; exit 0
  fi
  echo "$(ts) launching from frame $start (crashes so far: $crashes)" | tee -a "$LOG"
  FRAME_START="$start" FRAME_END="$TOTAL_FRAMES" "$BLENDER" -b --python "$SCRIPT" >> "$LOG" 2>&1; rc=$?
  after=$(first_missing)
  if [ "$after" -gt "$TOTAL_FRAMES" ]; then continue; fi           # loop top prints COMPLETE
  crashes=$((crashes+1))
  echo "$(ts) CRASH #$crashes: blender rc=$rc, stopped at frame $after (made $((after-start)) frames this run)" | tee -a "$LOG"
  if [ "$after" -le "$start" ]; then
    echo "$(ts) NO PROGRESS from frame $start — not relaunching into the same wall" | tee -a "$LOG"; exit 3
  fi
  if [ "$crashes" -ge "$MAX_CRASHES" ]; then
    echo "$(ts) CRASH BUDGET EXHAUSTED ($MAX_CRASHES) at frame $after" | tee -a "$LOG"; exit 2
  fi
  sleep 3
done
