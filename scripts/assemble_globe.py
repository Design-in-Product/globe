#!/usr/bin/env python3
"""Assemble a globe film from Blender-rendered frames + camera-path timing.

Replaces the dead ASS-overlay path (Amber's ffmpeg has no libass): the
time/era overlay is PIL-stamped per frame, then ffmpeg encodes filterless.
Optional terminal blend dissolves the film's last N frames into a target
frame (the prequel dissolves into the main globe film's opening render).

Env:
  CAMERA_PATH_FILE   timing/labels source (default ./camera_path.json)
  RENDER_DIR         Blender frames render_%04d.png (default ./render_frames)
  OUTPUT_PATH        output mp4 (default ./tectonic_globe.mp4)
  TERMINAL_BLEND_SRC optional image the last frames dissolve into
  TERMINAL_BLEND_FRAMES  dissolve length (default 72)
  INITIAL_BLEND_SRC  optional image the first frames dissolve out of
  INITIAL_BLEND_FRAMES   dissolve length (default 24)
"""

import json
import os
import subprocess
import tempfile
import shutil
import time

from PIL import Image, ImageDraw, ImageFont

CAMERA_PATH_FILE = os.path.abspath(os.environ.get("CAMERA_PATH_FILE", "./camera_path.json"))
RENDER_DIR = os.path.abspath(os.path.expanduser(os.environ.get("RENDER_DIR", "./render_frames")))
OUTPUT_PATH = os.path.abspath(os.environ.get("OUTPUT_PATH", "./tectonic_globe.mp4"))
TERMINAL_BLEND_SRC = os.path.expanduser(os.environ.get("TERMINAL_BLEND_SRC", ""))
TERMINAL_BLEND_FRAMES = int(os.environ.get("TERMINAL_BLEND_FRAMES", "72"))
# Mirror of the terminal blend for a film that CONTINUES another: the first N
# frames dissolve out of INITIAL_BLEND_SRC (the previous film's last frame).
# xian, 2026-10-06, on the sequel's opening: "The dissolve is nice and the
# jump-cut is too abrupt." The prequel's seam into the main film used the
# terminal form; this is the same seam language at the other end.
INITIAL_BLEND_SRC = os.path.expanduser(os.environ.get("INITIAL_BLEND_SRC", ""))
INITIAL_BLEND_FRAMES = int(os.environ.get("INITIAL_BLEND_FRAMES", "24"))
FPS = 24
RES_X, RES_Y = 1920, 1080

_FONT = "/System/Library/Fonts/Helvetica.ttc"
_TIME_FONT = ImageFont.truetype(_FONT, 48)
_ERA_FONT = ImageFont.truetype(_FONT, 32)


def time_label(time_ma):
    """Past reads 'N Ma'; the sequel stores future times as negative Ma and
    reads '+N Myr' (a '-200 Ma' stamp would be wrong, not just ugly)."""
    t = int(round(time_ma))
    return f"+{-t} Myr" if t < 0 else f"{t} Ma"


def stamp(im, time_ma, era):
    d = ImageDraw.Draw(im)
    d.text((40, RES_Y - 35 - 58), time_label(time_ma), font=_TIME_FONT,
           fill=(255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0))
    if era:
        d.text((40, RES_Y - 35 - 58 - 44), era, font=_ERA_FONT,
               fill=(204, 204, 204), stroke_width=2, stroke_fill=(0, 0, 0))
    return im


with open(CAMERA_PATH_FILE) as f:
    frames = json.load(f)["frames"]
total = len(frames)
print(f"Assembling {total} frames from {RENDER_DIR}")

initial_img = None
if INITIAL_BLEND_SRC:
    initial_img = Image.open(INITIAL_BLEND_SRC).convert("RGB").resize((RES_X, RES_Y), Image.LANCZOS)
    print(f"  Initial blend: first {INITIAL_BLEND_FRAMES} frames ← {INITIAL_BLEND_SRC}")
terminal_img = None
if TERMINAL_BLEND_SRC:
    terminal_img = Image.open(TERMINAL_BLEND_SRC).convert("RGB").resize((RES_X, RES_Y), Image.LANCZOS)
    print(f"  Terminal blend: last {TERMINAL_BLEND_FRAMES} frames → {TERMINAL_BLEND_SRC}")

tmp = tempfile.mkdtemp(prefix="globe_assembly_")
t0 = time.time()
n_stamped = n_missing = 0
for i, pf in enumerate(frames):
    src = os.path.join(RENDER_DIR, f"render_{i + 1:04d}.png")
    if not os.path.exists(src):
        n_missing += 1
        continue
    im = Image.open(src).convert("RGB")
    if im.size != (RES_X, RES_Y):
        im = im.resize((RES_X, RES_Y), Image.LANCZOS)
    if initial_img is not None and i < INITIAL_BLEND_FRAMES:
        # a runs 1→0: frame 0 is almost entirely the previous film's last frame.
        a = (INITIAL_BLEND_FRAMES - i) / (INITIAL_BLEND_FRAMES + 1)
        im = Image.blend(im, initial_img, a)
    if terminal_img is not None and i >= total - TERMINAL_BLEND_FRAMES:
        a = (i - (total - TERMINAL_BLEND_FRAMES) + 1) / (TERMINAL_BLEND_FRAMES + 1)
        im = Image.blend(im, terminal_img, a)
    stamp(im, pf["time_ma"], pf.get("era_label", ""))
    im.save(os.path.join(tmp, f"frame_{i + 1:04d}.png"))
    n_stamped += 1
    if (i + 1) % 400 == 0:
        print(f"  [{i + 1}/{total}] ({time.time() - t0:.0f}s)", flush=True)

print(f"  Stamped {n_stamped}, missing {n_missing}, of {total}")
if n_missing:
    raise SystemExit(f"✗ {n_missing} rendered frames missing — refusing to assemble a gappy film.")

r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error",
                    "-framerate", str(FPS), "-i", os.path.join(tmp, "frame_%04d.png"),
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-movflags", "+faststart", OUTPUT_PATH],
                   capture_output=True, text=True)
shutil.rmtree(tmp)
if r.returncode != 0:
    raise SystemExit(f"✗ ffmpeg failed: {r.stderr[-600:]}")
size = os.path.getsize(OUTPUT_PATH) / 1048576
print(f"✓ {OUTPUT_PATH}: {total} frames, {total / FPS:.1f}s, {size:.1f} MB, "
      f"overlay burned in, assembled in {time.time() - t0:.0f}s")
