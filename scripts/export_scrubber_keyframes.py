#!/usr/bin/env python3
"""Phase-1 keyframe export for the WebGL scrubber (roadmap item 5).

Budget CONFIRMED by xian 2026-09-22 after the resolution comparison:
4096x2048 WebP, quality 90 (~491 KB/frame; 15 frames ~7.4 MB). Same
pixels as the source PNG at a third the weight.

Range: main film first (xian, 2026-09-12) — the 15 named eras in
camera_path_spin_v8.json, 1000 -> 0 Ma. Prequel range is a fast-follow.

Frame-index mapping (verified against scripts/generate_frames.py):
TIME_START=1000, TIME_STEP=1, frame_idx 0-indexed -> idx = 1000 - time_ma.

Writes scrubber_assets/<time_ma>ma.webp plus scrubber_assets/keyframes.json
(the manifest the explore page reads). Honest accounting: reports every
frame written, skipped, or missing; exits non-zero if any source is absent.
"""
import json
import os
import sys
from PIL import Image

SRC_DIR = os.path.expanduser("~/globe-render/frames")
CAMERA_PATH = "camera_path_spin_v8.json"
OUT_DIR = "scrubber_assets"
SIZE = (4096, 2048)
WEBP_QUALITY = 90


def frame_path(time_ma):
    return os.path.join(SRC_DIR, f"globe_frame_{1000 - time_ma:04d}.png")


def main():
    with open(CAMERA_PATH) as f:
        eras = json.load(f)["eras"]
    os.makedirs(OUT_DIR, exist_ok=True)

    manifest, n_written, n_missing = [], 0, 0
    for era in eras:
        t, label = era["time_ma"], era["label"]
        src = frame_path(t)
        if not os.path.exists(src):
            print(f"MISSING {t:4d} Ma ({label}): {src}")
            n_missing += 1
            continue
        im = Image.open(src).convert("RGB")
        assert im.size == SIZE, f"{src}: expected {SIZE}, got {im.size}"
        out = os.path.join(OUT_DIR, f"{t:04d}ma.webp")
        im.save(out, "WEBP", quality=WEBP_QUALITY)
        kb = os.path.getsize(out) / 1024
        manifest.append({"time_ma": t, "label": label, "file": f"{t:04d}ma.webp"})
        n_written += 1
        print(f"wrote {t:4d} Ma  {kb:6.0f} KB  {label}")

    with open(os.path.join(OUT_DIR, "keyframes.json"), "w") as f:
        json.dump({
            "budget": f"{SIZE[0]}x{SIZE[1]} WebP q{WEBP_QUALITY} (xian, 2026-09-22)",
            "source": CAMERA_PATH,
            "keyframes": manifest,
        }, f, indent=2)

    total_kb = sum(os.path.getsize(os.path.join(OUT_DIR, k["file"])) for k in manifest) / 1024
    print(f"\n{n_written} written, {n_missing} missing, {len(eras)} expected; "
          f"total {total_kb/1024:.1f} MB")
    if n_missing or n_written != len(eras):
        print("INCOMPLETE — not a full keyframe set.")
        sys.exit(1)


if __name__ == "__main__":
    main()
