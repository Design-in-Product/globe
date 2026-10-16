#!/usr/bin/env bash
# Re-make every live film in a named palette (roadmap item 4), end to end,
# into ~/globe-render/palette_<name>/ — nothing in the repo changes until a
# human has watched the result and the films are copied in by hand.
#
#   scripts/palette_pipeline.sh cobalt-brass [--dry-run | --flats-only]
# --flats-only stops before the Cycles stage (re-make the flats while a
# globe pass is already running; never start a second supervisor).
#
# Stages (each resumable; a rerun skips what is already on disk):
#   1. recolour the three texture sets (recolor_texture.py, 8-way). The sequel's
#      superposition takes a land ramp (LAND_RAMP, default #6b5530: any land at
#      all is amber — xian 10-16); PREQUEL_LAND_RAMP applies one to the cloud.
#   2. flat films, fast (PIL): main v8 -> prequel v2 (dissolves into main's
#      first frame) -> sequel v3 (dissolves out of main's last frame, PAN_SCROLL
#      from the sequel path's pan window, LENS_HOLDS=0 as shipped 10-06)
#   3. globe films, slow (Cycles via render_supervised.sh): main, prequel,
#      sequel; assemble_globe.py with the same seam blends as shipped.
# Run detached:  nohup scripts/palette_pipeline.sh cobalt-brass > ~/globe-render/palette_cobalt-brass/pipeline.log 2>&1 &
# Declare the Blender hours first (scripts/declare_render.sh) — the
# supervisor warns if no live row is on origin/main.
set -uo pipefail
P="${1:?palette name}"; DRY="${2:-}"
REPO="$(cd "$(dirname "$0")/.." && pwd)"
R=~/globe-render; W=$R/palette_$P; mkdir -p "$W"
# render_flat.py's lens morph imports matplotlib: use the repo venv (the one
# the shipped flats were built with), not the Homebrew python3.
PY="${PY:-$REPO/.venv/bin/python3}"; [ -x "$PY" ] || PY=python3
LAND_RAMP="${LAND_RAMP-#6b5530}"; PREQUEL_LAND_RAMP="${PREQUEL_LAND_RAMP-}"
ts() { date "+%F %T"; }
run() { echo "[$(ts)] $*"; [ "$DRY" = "--dry-run" ] && return 0; "$@"; local rc=$?; [ $rc -eq 0 ] || { echo "[$(ts)] FAILED (exit $rc): $1 — stopping"; exit 1; }; }

echo "[$(ts)] palette pipeline: $P -> $W"

# ── 1. textures ────────────────────────────────────────────────
run $PY "$REPO/scripts/recolor_texture.py" --palette "$P" --jobs 8 "$R/frames" "$W/frames"
run $PY "$REPO/scripts/recolor_texture.py" --palette "$P" --jobs 8 --pattern 'prequel_frame_*.png' ${PREQUEL_LAND_RAMP:+--land-ramp "$PREQUEL_LAND_RAMP"} "$R/prequel_frames" "$W/prequel_frames"
run $PY "$REPO/scripts/recolor_texture.py" --palette "$P" --jobs 8 --pattern 'sequel_frame_*.png' ${LAND_RAMP:+--land-ramp "$LAND_RAMP"} "$R/sequel_frames" "$W/sequel_frames"

# ── 2. flat films ──────────────────────────────────────────────
cd "$REPO"
# sequel pan window: the one long run where camera_lon moves while the geo frame holds
PAN=$($PY - <<'PYEOF'
import json
fr = json.load(open('sequel_camera_path.json'))['frames']
best = None; i = 0
while i < len(fr):
    j = i
    while j + 1 < len(fr) and fr[j+1]['geo_frame_idx'] == fr[i]['geo_frame_idx']: j += 1
    if j - i + 1 >= 200:
        moving = [k for k in range(i, j) if abs(fr[k+1]['camera_lon'] - fr[k]['camera_lon']) > 1e-6]
        if moving and (best is None or len(moving) > best[1]):
            best = (moving[0], len(moving))   # 288 as shipped 10-06
    i = j + 1
print(f"{best[0]}:{best[1]}:360")
PYEOF
)
echo "[$(ts)] sequel PAN_SCROLL=$PAN"
# The chained films blend into LABEL-FREE copies of main's first/last frames
# (DUMP_FIRST/DUMP_LAST), so the dissolve never shows two labels at once.
if [ ! -s "$W/tectonic_flat_v8.mp4" ] || [ ! -s "$W/flat_main_last.png" ]; then
  run env FRAMES_DIR="$W/frames" CAMERA_PATH_FILE=camera_path_spin_v8.json OUTPUT_PATH="$W/tectonic_flat_v8.mp4" \
      DUMP_FIRST="$W/flat_main_first.png" DUMP_LAST="$W/flat_main_last.png" $PY scripts/render_flat.py
  rm -f "$W/tectonic_prequel_v2.mp4" "$W/tectonic_sequel_flat_v3.mp4"   # their blend sources just changed
fi
if [ ! -s "$W/tectonic_prequel_v2.mp4" ]; then
  run env FRAMES_DIR="$W/prequel_frames" FRAME_PREFIX=prequel_frame_ CAMERA_PATH_FILE=prequel_camera_path.json \
      TERMINAL_BLEND_SRC="$W/flat_main_first.png" OUTPUT_PATH="$W/tectonic_prequel_v2.mp4" $PY scripts/render_flat.py
fi
if [ ! -s "$W/tectonic_sequel_flat_v3.mp4" ]; then
  run env FRAMES_DIR="$W/sequel_frames" FRAME_PREFIX=sequel_frame_ CAMERA_PATH_FILE=sequel_camera_path.json \
      INITIAL_BLEND_SRC="$W/flat_main_last.png" PAN_SCROLL="$PAN" LENS_HOLDS=0 \
      OUTPUT_PATH="$W/tectonic_sequel_flat_v3.mp4" $PY scripts/render_flat.py
fi
echo "[$(ts)] flats done: $(ls "$W"/*.mp4 2>/dev/null | xargs -n1 basename | tr '\n' ' ')"
[ "$DRY" = "--flats-only" ] && { echo "[$(ts)] flats-only: stopping before the Cycles stage"; exit 0; }

# ── 3. globe films (Cycles, hours) ─────────────────────────────
globe() {  # name frames prefix path total
  local name=$1 frames=$2 prefix=$3 path=$4 total=$5
  run env FRAMES_DIR="$frames" FRAME_PREFIX="$prefix" CAMERA_PATH_FILE="$REPO/$path" RENDER_DIR="$W/render_$name" \
      TOTAL_FRAMES="$total" LOG="$W/render_$name.supervisor.log" bash scripts/render_supervised.sh
}
globe main    "$W/frames"         globe_frame_   camera_path_spin_v8.json 2738
run env CAMERA_PATH_FILE=camera_path_spin_v8.json RENDER_DIR="$W/render_main" OUTPUT_PATH="$W/tectonic_globe_v8.mp4" $PY scripts/assemble_globe.py
globe prequel "$W/prequel_frames" prequel_frame_ prequel_camera_path.json 2186
run env CAMERA_PATH_FILE=prequel_camera_path.json RENDER_DIR="$W/render_prequel" TERMINAL_BLEND_SRC="$W/render_main/render_0001.png" \
    OUTPUT_PATH="$W/tectonic_prequel_globe_v2.mp4" $PY scripts/assemble_globe.py
globe sequel  "$W/sequel_frames"  sequel_frame_  sequel_camera_path.json  1795
run env CAMERA_PATH_FILE=sequel_camera_path.json RENDER_DIR="$W/render_sequel" INITIAL_BLEND_SRC="$W/render_main/render_2738.png" \
    OUTPUT_PATH="$W/tectonic_sequel_globe_v3.mp4" $PY scripts/assemble_globe.py
echo "[$(ts)] PIPELINE COMPLETE: $(ls "$W"/*.mp4 | xargs -n1 basename | tr '\n' ' ')"
