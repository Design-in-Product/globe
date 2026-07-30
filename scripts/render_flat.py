#!/usr/bin/env python3
"""
Assemble flat-projection (equirectangular) companion video with crossfade
blending and (flat-v7) lens-per-hold projection-morph reveals.

No Blender needed — reads source PNGs and camera-path timing; crossfades
between geological frames with PIL, renders hold-window morphs via
flat_morph.py (numpy/scipy/matplotlib — run with the repo .venv).

Flat-v7 production (v8 spin path, lens arc on the four holds):
    CAMERA_PATH_FILE=camera_path_spin_v8.json \
    FRAMES_DIR=~/globe-render/frames \
    OUTPUT_PATH=./tectonic_flat_v7.mp4 \
    .venv/bin/python scripts/render_flat.py

Legacy plain build: LENS_HOLDS=0 python3 scripts/render_flat.py
"""

import json
import os
import sys
import subprocess
import tempfile
import shutil
import time

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ── Configuration ─────────────────────────────────────────────
# Env-overridable (matches render_globe.py) so v8-path runs need no edits.
CAMERA_PATH_FILE = os.path.abspath(os.environ.get("CAMERA_PATH_FILE", "./camera_path.json"))
FRAMES_DIR = os.path.abspath(os.path.expanduser(os.environ.get("FRAMES_DIR", "./frames")))
OUTPUT_PATH = os.path.abspath(os.environ.get("OUTPUT_PATH", "./tectonic_flat_v6.mp4"))
FRAME_PREFIX = os.environ.get("FRAME_PREFIX", "globe_frame_")  # prequel: prequel_frame_
FPS = 24
RES_X = 1920
RES_Y = 960  # 2:1 equirectangular aspect ratio
CROSSFADE_HALF = 1  # frames from each side of transition = 2-frame crossfade window

# Lens-per-hold reveals (flat-v7, xian-approved arc). Holds are detected as
# runs of ≥ MIN_HOLD frames at constant time_ma; lenses are assigned in arc
# order. Disable (plain flat film) with LENS_HOLDS=0.
LENS_HOLDS = os.environ.get("LENS_HOLDS", "1") != "0"
LENS_ARC = ["sinusoidal", "azimuthal-s", "mollweide", "ortho"]
MIN_HOLD = 100
MORPH_FRAMES = 24  # each side; remainder of the hold is the 360° rotate-under

# Overlay is burned in with PIL at frame-creation time. (Amber's Homebrew
# ffmpeg ships without libass/freetype — no ass/subtitles/drawtext filters —
# so the old ASS pass silently fell back to no overlay. PIL removes the
# dependency entirely.)
_FONT_PATH = "/System/Library/Fonts/Helvetica.ttc"
_TIME_FONT = ImageFont.truetype(_FONT_PATH, 44)
_ERA_FONT = ImageFont.truetype(_FONT_PATH, 28)


def stamp_overlay(im, time_ma, era):
    """Burn the time + era labels onto a RES_X x RES_Y frame (bottom-left,
    matching the v6 ASS style: white time over grey era, black outline)."""
    d = ImageDraw.Draw(im)
    time_str = f"{int(time_ma)} Ma"
    d.text((40, RES_Y - 30 - 52), time_str, font=_TIME_FONT,
           fill=(255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0))
    if era:
        d.text((40, RES_Y - 30 - 52 - 40), era, font=_ERA_FONT,
               fill=(204, 204, 204), stroke_width=2, stroke_fill=(0, 0, 0))
    return im


# ── Crossfade schedule computation ────────────────────────────
def compute_crossfade_schedule(path_frames, crossfade_half=2):
    """
    Compute which animation frames need crossfading between geological textures.

    Returns dict: anim_frame_index -> (geo_idx_a, geo_idx_b, alpha)
    where alpha=0.0 means pure A and alpha=1.0 means pure B.
    """
    # Build runs: consecutive animation frames showing the same geo frame
    runs = []
    prev_geo = path_frames[0]["geo_frame_idx"]
    run_start = 0
    for i, pf in enumerate(path_frames):
        if pf["geo_frame_idx"] != prev_geo:
            runs.append((prev_geo, run_start, i, i - run_start))
            run_start = i
            prev_geo = pf["geo_frame_idx"]
    runs.append((prev_geo, run_start, len(path_frames), len(path_frames) - run_start))

    # Build crossfade map
    crossfade_map = {}
    for ri in range(len(runs) - 1):
        out_run = runs[ri]    # (geo_idx, start, end, length)
        in_run = runs[ri + 1]
        half = min(out_run[3] // 2, in_run[3] // 2, crossfade_half)
        if half < 1:
            continue
        window = 2 * half
        transition = in_run[1]  # first anim frame of incoming run
        for k in range(window):
            anim_idx = transition - half + k
            alpha = (k + 1) / (window + 1)
            crossfade_map[anim_idx] = (out_run[0], in_run[0], alpha)

    return crossfade_map


# ── Load camera path data ─────────────────────────────────────
print("Loading camera path data...")
with open(CAMERA_PATH_FILE, 'r') as f:
    camera_path = json.load(f)

path_frames = camera_path["frames"]
total_frames = len(path_frames)
duration_sec = total_frames / FPS

print(f"  Animation frames: {total_frames}")
print(f"  Duration: {duration_sec:.1f}s at {FPS}fps")
print(f"  Output: {OUTPUT_PATH}")

# ── Compute crossfade schedule ────────────────────────────────
crossfade_map = compute_crossfade_schedule(path_frames, CROSSFADE_HALF)
# Count unique geo frames to report transitions
n_geo_frames = len(set(pf["geo_frame_idx"] for pf in path_frames))
print(f"  Crossfade frames: {len(crossfade_map)} (across {n_geo_frames - 1} transitions)")

# ── Detect holds and build the lens-morph schedule ────────────
# morph_map: anim frame index -> (lens, s, lon0, geo_idx)
morph_map = {}
if LENS_HOLDS:
    from flat_morph import FlatMorph, hold_schedule

    holds = []
    run_start, prev_t = 0, path_frames[0]["time_ma"]
    for i, pf in enumerate(path_frames):
        if pf["time_ma"] != prev_t:
            if i - run_start >= MIN_HOLD:
                holds.append((run_start, i))
            run_start, prev_t = i, pf["time_ma"]
    if len(path_frames) - run_start >= MIN_HOLD:
        holds.append((run_start, len(path_frames)))

    if len(holds) != len(LENS_ARC):
        print(f"⚠ {len(holds)} holds detected but {len(LENS_ARC)} lenses in the arc"
              f" — pairing in order, extras get no lens.")
    morphers = {}
    for (start, end), lens in zip(holds, LENS_ARC):
        sched = hold_schedule(end - start, MORPH_FRAMES)
        geo_idx = path_frames[start]["geo_frame_idx"]
        for k, (s, lon0) in enumerate(sched):
            morph_map[start + k] = (lens, s, lon0, geo_idx)
        if lens not in morphers:
            morphers[lens] = FlatMorph(lens, resx=RES_X, resy=RES_Y)
        print(f"  Hold {path_frames[start]['time_ma']:.0f} Ma "
              f"(frames {start}-{end}, {end - start}f) → {lens}")
    print(f"  Lens-morph frames: {len(morph_map)}")

# ── Create temp directory with frames ─────────────────────────
# Non-crossfade frames: symlink to source PNG
# Crossfade frames: PIL-blended PNG saved to temp dir
print(f"\nCreating frames (symlinks + crossfade blends)...")
tmp_dir = tempfile.mkdtemp(prefix="flat_frames_")
blend_start = time.time()

# Image cache: keep only the 2 images needed for current crossfade
image_cache = {}  # geo_idx -> PIL Image
blend_count = 0

morph_count = 0
link_count = 0
morph_loaded_geo = {}  # lens -> geo_idx currently loaded
prev_static = None     # (geo_idx, time_ma, era) -> hardlink identical repeats
prev_dst = None


def load_resized(geo_idx):
    """Source texture resized to output resolution (cached)."""
    if geo_idx not in image_cache:
        im = Image.open(os.path.join(FRAMES_DIR, f"{FRAME_PREFIX}{geo_idx:04d}.png"))
        image_cache[geo_idx] = im.convert("RGB").resize((RES_X, RES_Y), Image.LANCZOS)
    return image_cache[geo_idx]


for i, pf in enumerate(path_frames):
    dst = os.path.join(tmp_dir, f"frame_{i + 1:04d}.png")
    time_ma, era = pf["time_ma"], pf.get("era_label", "")

    if i in morph_map:
        # Lens-morph hold frame (takes precedence; holds never crossfade)
        lens, s, lon0, geo_idx = morph_map[i]
        fm = morphers[lens]
        if morph_loaded_geo.get(lens) != geo_idx:
            fm.load_texture(os.path.join(FRAMES_DIR, f"{FRAME_PREFIX}{geo_idx:04d}.png"))
            morph_loaded_geo[lens] = geo_idx
        fm.render(s, lon0, dst)
        stamp_overlay(Image.open(dst).convert("RGB"), time_ma, era).save(dst)
        morph_count += 1
        prev_static = None
    elif i in crossfade_map:
        geo_a, geo_b, alpha = crossfade_map[i]
        blended = Image.blend(load_resized(geo_a), load_resized(geo_b), alpha)
        stamp_overlay(blended, time_ma, era).save(dst)
        blend_count += 1
        prev_static = None
        # Evict cache entries no longer needed (keep only current pair)
        for cached_idx in list(image_cache.keys()):
            if cached_idx != geo_a and cached_idx != geo_b:
                del image_cache[cached_idx]
    else:
        # Static frame: identical repeats within a run hardlink the previous
        geo_idx = pf["geo_frame_idx"]
        key = (geo_idx, time_ma, era)
        if key == prev_static and prev_dst:
            os.link(prev_dst, dst)
            link_count += 1
        else:
            frame = load_resized(geo_idx).copy()
            stamp_overlay(frame, time_ma, era).save(dst)
            prev_static, prev_dst = key, dst

    # Progress reporting every 200 frames
    if (i + 1) % 200 == 0:
        elapsed = time.time() - blend_start
        print(f"  [{i+1}/{total_frames}] {blend_count} blends, {morph_count} morphs, "
              f"{link_count} links so far ({elapsed:.1f}s)", flush=True)

# Clear image cache
image_cache.clear()
blend_elapsed = time.time() - blend_start
print(f"  Created {total_frames} frames ({blend_count} crossfade blends, "
      f"{morph_count} lens-morph renders, {link_count} hardlinked repeats "
      f"in {blend_elapsed:.1f}s)", flush=True)
if blend_count + morph_count + link_count > total_frames:
    print("⚠ Accounting mismatch in frame creation — investigate.")


# ── Assemble MP4 with ffmpeg ──────────────────────────────────
print(f"\nAssembling MP4: {OUTPUT_PATH}")
start_time = time.time()

# Frames are already RES_X x RES_Y with the overlay burned in — no filters.
ffmpeg_cmd = [
    "ffmpeg", "-y",
    "-framerate", str(FPS),
    "-i", os.path.join(tmp_dir, "frame_%04d.png"),
    "-c:v", "libx264",
    "-crf", "18",
    "-pix_fmt", "yuv420p",
    "-movflags", "+faststart",
    OUTPUT_PATH
]

result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)

if result.returncode == 0:
    elapsed = time.time() - start_time
    file_size = os.path.getsize(OUTPUT_PATH) / (1024 * 1024)
    print(f"\n✓ Flat projection video complete!")
    print(f"  Output: {OUTPUT_PATH}")
    print(f"  Duration: {duration_sec:.1f}s ({total_frames} frames at {FPS}fps)")
    print(f"  Resolution: {RES_X}×{RES_Y}, overlay burned in (PIL)")
    print(f"  File size: {file_size:.1f} MB")
    print(f"  Assembly time: {elapsed:.1f}s")
    print(f"  Crossfade blends: {blend_count}; lens morphs: {morph_count}")
else:
    print(f"\n✗ ffmpeg failed: {result.stderr[-800:]}")
    shutil.rmtree(tmp_dir)
    raise SystemExit(1)

# ── Cleanup ───────────────────────────────────────────────────
shutil.rmtree(tmp_dir)
print(f"  Cleaned up temp directory")
