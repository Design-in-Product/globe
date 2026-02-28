#!/usr/bin/env python3
"""
Assemble flat-projection (equirectangular) companion video with crossfade blending.

No Blender needed — reads source PNGs from frames/ and uses
camera_path.json for timing + subtitle data. Crossfades between
consecutive geological frames using PIL alpha-blending for smooth transitions.

Usage:
    python3 scripts/render_flat.py
"""

import json
import os
import subprocess
import tempfile
import shutil
import time

from PIL import Image

# ── Configuration ─────────────────────────────────────────────
CAMERA_PATH_FILE = os.path.abspath("./camera_path.json")
FRAMES_DIR = os.path.abspath("./frames")
OUTPUT_PATH = os.path.abspath("./tectonic_flat_v3.mp4")
OVERLAY_SCRIPT = os.path.abspath("./overlay_flat.ass")
FPS = 24
RES_X = 1920
RES_Y = 960  # 2:1 equirectangular aspect ratio
CROSSFADE_HALF = 1  # frames from each side of transition = 2-frame crossfade window


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

# ── Create temp directory with frames ─────────────────────────
# Non-crossfade frames: symlink to source PNG
# Crossfade frames: PIL-blended PNG saved to temp dir
print(f"\nCreating frames (symlinks + crossfade blends)...")
tmp_dir = tempfile.mkdtemp(prefix="flat_frames_")
blend_start = time.time()

# Image cache: keep only the 2 images needed for current crossfade
image_cache = {}  # geo_idx -> PIL Image
blend_count = 0

for i, pf in enumerate(path_frames):
    dst = os.path.join(tmp_dir, f"frame_{i + 1:04d}.png")

    if i in crossfade_map:
        geo_a, geo_b, alpha = crossfade_map[i]

        # Load images into cache if not already there
        if geo_a not in image_cache:
            image_cache[geo_a] = Image.open(
                os.path.join(FRAMES_DIR, f"globe_frame_{geo_a:04d}.png")
            )
        if geo_b not in image_cache:
            image_cache[geo_b] = Image.open(
                os.path.join(FRAMES_DIR, f"globe_frame_{geo_b:04d}.png")
            )

        # Alpha-blend between the two geological frames
        blended = Image.blend(image_cache[geo_a], image_cache[geo_b], alpha)
        blended.save(dst)
        blend_count += 1

        # Evict cache entries no longer needed (keep only current pair)
        for cached_idx in list(image_cache.keys()):
            if cached_idx != geo_a and cached_idx != geo_b:
                del image_cache[cached_idx]
    else:
        # No crossfade — symlink to source PNG
        geo_idx = pf["geo_frame_idx"]
        src = os.path.join(FRAMES_DIR, f"globe_frame_{geo_idx:04d}.png")
        os.symlink(src, dst)

    # Progress reporting every 200 frames
    if (i + 1) % 200 == 0:
        elapsed = time.time() - blend_start
        print(f"  [{i+1}/{total_frames}] {blend_count} blends so far ({elapsed:.1f}s)")

# Clear image cache
image_cache.clear()
blend_elapsed = time.time() - blend_start
print(f"  Created {total_frames} frames ({blend_count} crossfade blends in {blend_elapsed:.1f}s)")

# ── Generate ASS subtitle file ────────────────────────────────
# Same logic as render_globe.py but adjusted for 1920x960 resolution
print(f"\nGenerating subtitle overlay...")

ass_header = f"""[Script Info]
Title: Tectonic Globe Flat Projection Overlay
ScriptType: v4.00+
WrapStyle: 0
PlayResX: {RES_X}
PlayResY: {RES_Y}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: TimeLabel,Arial,44,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,0,1,40,40,30,1
Style: EraLabel,Arial,28,&H00CCCCCC,&H000000FF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,2,0,1,40,40,85,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def frame_to_ass_time(frame_num, fps):
    """Convert frame number to ASS timestamp (H:MM:SS.CC)."""
    total_seconds = frame_num / fps
    h = int(total_seconds // 3600)
    m = int((total_seconds % 3600) // 60)
    s = total_seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"


ass_events = []
prev_time_ma = None
prev_era = None
block_start_frame = 0

# Group consecutive frames with the same time_ma and era
for pf in path_frames:
    anim_f = pf["anim_frame"]
    time_ma = pf["time_ma"]
    era = pf.get("era_label", "")

    if time_ma != prev_time_ma or era != prev_era:
        # Close previous block
        if prev_time_ma is not None:
            start_ts = frame_to_ass_time(block_start_frame, FPS)
            end_ts = frame_to_ass_time(anim_f, FPS)
            time_str = f"{int(prev_time_ma)} Ma" if prev_time_ma == int(prev_time_ma) else f"{prev_time_ma:.1f} Ma"
            ass_events.append(
                f"Dialogue: 0,{start_ts},{end_ts},TimeLabel,,0,0,0,,{time_str}"
            )
            if prev_era:
                ass_events.append(
                    f"Dialogue: 0,{start_ts},{end_ts},EraLabel,,0,0,0,,{prev_era}"
                )
        block_start_frame = anim_f
        prev_time_ma = time_ma
        prev_era = era

# Close final block
if prev_time_ma is not None:
    start_ts = frame_to_ass_time(block_start_frame, FPS)
    end_ts = frame_to_ass_time(total_frames, FPS)
    time_str = f"{int(prev_time_ma)} Ma"
    ass_events.append(
        f"Dialogue: 0,{start_ts},{end_ts},TimeLabel,,0,0,0,,{time_str}"
    )
    if prev_era:
        ass_events.append(
            f"Dialogue: 0,{start_ts},{end_ts},EraLabel,,0,0,0,,{prev_era}"
        )

with open(OVERLAY_SCRIPT, 'w') as f:
    f.write(ass_header)
    f.write("\n".join(ass_events))
    f.write("\n")

print(f"  Subtitle file: {OVERLAY_SCRIPT} ({len(ass_events)} events)")

# ── Assemble MP4 with ffmpeg ──────────────────────────────────
print(f"\nAssembling MP4: {OUTPUT_PATH}")
start_time = time.time()

ffmpeg_cmd = [
    "ffmpeg", "-y",
    "-framerate", str(FPS),
    "-i", os.path.join(tmp_dir, "frame_%04d.png"),
    "-vf", f"scale={RES_X}:{RES_Y}:flags=lanczos,ass={OVERLAY_SCRIPT}",
    "-c:v", "libx264",
    "-crf", "18",
    "-pix_fmt", "yuv420p",
    OUTPUT_PATH
]

result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)

if result.returncode == 0:
    elapsed = time.time() - start_time
    file_size = os.path.getsize(OUTPUT_PATH) / (1024 * 1024)
    print(f"\n✓ Flat projection video complete!")
    print(f"  Output: {OUTPUT_PATH}")
    print(f"  Duration: {duration_sec:.1f}s ({total_frames} frames at {FPS}fps)")
    print(f"  Resolution: {RES_X}×{RES_Y}")
    print(f"  File size: {file_size:.1f} MB")
    print(f"  Assembly time: {elapsed:.1f}s")
    print(f"  Crossfade blends: {blend_count}")
else:
    print(f"\n✗ ffmpeg with subtitles failed: {result.stderr[:500]}")
    print("  Trying without subtitles...")
    ffmpeg_cmd_plain = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", os.path.join(tmp_dir, "frame_%04d.png"),
        "-vf", f"scale={RES_X}:{RES_Y}:flags=lanczos",
        "-c:v", "libx264",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        OUTPUT_PATH
    ]
    result2 = subprocess.run(ffmpeg_cmd_plain, capture_output=True, text=True)
    if result2.returncode == 0:
        elapsed = time.time() - start_time
        file_size = os.path.getsize(OUTPUT_PATH) / (1024 * 1024)
        print(f"\n✓ Flat projection video complete (no overlay)!")
        print(f"  File size: {file_size:.1f} MB")
    else:
        print(f"\n✗ ffmpeg failed: {result2.stderr[:500]}")
        shutil.rmtree(tmp_dir)
        raise SystemExit(1)

# ── Cleanup ───────────────────────────────────────────────────
shutil.rmtree(tmp_dir)
print(f"  Cleaned up temp directory")
