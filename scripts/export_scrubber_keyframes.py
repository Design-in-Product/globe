#!/usr/bin/env python3
"""Keyframe export for the WebGL scrubber (roadmap item 5).

Budget CONFIRMED by xian 2026-09-22 after the resolution comparison:
WebP quality 90 at the source's native resolution. Main-film sources are
4096x2048 (~491 KB/frame); prequel sources are 2048x1024 — that is how the
9-member ensemble was rendered — so those export at native size rather
than upscaled (an upscale adds bytes, not information).

Ranges:
  main    — the 15 named eras in camera_path_spin_v8.json, 1000 -> 0 Ma
            (Phase 1, shipped 2026-09-22)
  prequel — 1800 -> 1200 Ma at the ICS period boundaries + the Nuna hold
            (fast-follow, xian "let's go for it" 2026-09-22). The 1000 Ma
            keyframe is the main film's (Merdith2021); the prequel's own
            1000 Ma frame is registered onto it and near-identical.

Frame-index mapping, both verified against the generator scripts:
  main:    generate_frames.py         idx = 1000 - time_ma
  prequel: generate_prequel_frames.py idx = 1800 - time_ma

Writes scrubber_assets/<time_ma>ma.webp and scrubber_assets/keyframes.json
(the manifest explore/index.html reads). Honest accounting: reports every
frame written or missing; exits non-zero if the set is incomplete.
"""
import json
import os
import sys
from PIL import Image

OUT_DIR = "scrubber_assets"
WEBP_QUALITY = 90

MAIN_SRC = os.path.expanduser("~/globe-render/frames")
MAIN_CAMERA_PATH = "camera_path_spin_v8.json"
MAIN_SIZE = (4096, 2048)

PREQUEL_SRC = os.path.expanduser("~/globe-render/prequel_frames")
PREQUEL_SIZE = (2048, 1024)
# (time_ma, label) — ICS Proterozoic period boundaries (compute_prequel_path.py
# PERIODS) plus the Nuna hold xian picked (1452 Ma). 1000 Ma comes from main.
PREQUEL_KEYFRAMES = [
    (1800, "Statherian — the probability cloud"),
    (1600, "Calymmian"),
    (1452, "Nuna / Columbia assembled"),
    (1400, "Ectasian"),
    (1200, "Stenian"),
]


def main_eras():
    with open(MAIN_CAMERA_PATH) as f:
        return [(e["time_ma"], e["label"], "main",
                 os.path.join(MAIN_SRC, f"globe_frame_{1000 - e['time_ma']:04d}.png"),
                 MAIN_SIZE) for e in json.load(f)["eras"]]


def prequel_eras():
    return [(t, label, "prequel",
             os.path.join(PREQUEL_SRC, f"prequel_frame_{1800 - t:04d}.png"),
             PREQUEL_SIZE) for t, label in PREQUEL_KEYFRAMES]


def main():
    eras = prequel_eras() + main_eras()
    os.makedirs(OUT_DIR, exist_ok=True)

    manifest, n_written, n_missing = [], 0, 0
    for t, label, source, src, size in eras:
        if not os.path.exists(src):
            print(f"MISSING {t:4d} Ma ({label}): {src}")
            n_missing += 1
            continue
        im = Image.open(src).convert("RGB")
        assert im.size == size, f"{src}: expected {size}, got {im.size}"
        out = os.path.join(OUT_DIR, f"{t:04d}ma.webp")
        im.save(out, "WEBP", quality=WEBP_QUALITY)
        kb = os.path.getsize(out) / 1024
        manifest.append({"time_ma": t, "label": label, "file": f"{t:04d}ma.webp",
                         "source": source, "width": size[0], "height": size[1]})
        n_written += 1
        print(f"wrote {t:4d} Ma  {kb:6.0f} KB  {size[0]}x{size[1]}  {label}")

    manifest.sort(key=lambda k: -k["time_ma"])
    with open(os.path.join(OUT_DIR, "keyframes.json"), "w") as f:
        json.dump({
            "budget": f"WebP q{WEBP_QUALITY} at native resolution (xian, 2026-09-22)",
            "span_ma": [manifest[0]["time_ma"], manifest[-1]["time_ma"]] if manifest else None,
            "sources": {"main": MAIN_CAMERA_PATH, "prequel": "ICS period boundaries + Nuna hold"},
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
