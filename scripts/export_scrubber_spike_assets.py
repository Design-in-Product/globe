#!/usr/bin/env python3
"""Phase-0 spike asset prep for the WebGL scrubber (roadmap item 5).

Exports three main-film era keyframes (1000/250/0 Ma) as small JPEGs for
the throwaway orbit+crossfade feel-test, and a resolution/format
comparison grid (full frame + a 1:1 pixel crop) for xian's eyeball,
per the 2026-09-12 answers (main-era-first, eyeball-first, spike-first).

Frame-index mapping (verified against scripts/generate_frames.py):
TIME_START=1000, TIME_STEP=1, frame_idx is 0-indexed -> time_ma = 1000 - idx.
"""
import os
from PIL import Image

SRC_DIR = os.path.expanduser("~/globe-render/frames")
SPIKE_OUT = "previews/scrubber-spike/textures"
COMPARISON_OUT = "docs/design/scrubber-resolution-comparison-2026-09-18"

SPIKE_ERAS = [(1000, "Rodinia assembling"), (250, "Pangaea assembled"), (0, "Present day")]
SPIKE_SIZE = (2048, 1024)
SPIKE_JPEG_QUALITY = 88

# (label, size, format, save_kwargs)
COMPARISON_CANDIDATES = [
    ("4096x2048-png-original", (4096, 2048), "PNG", {}),
    ("2048x1024-webp-q80", (2048, 1024), "WEBP", {"quality": 80}),
    ("2048x1024-webp-q60", (2048, 1024), "WEBP", {"quality": 60}),
    ("1024x512-webp-q80", (1024, 512), "WEBP", {"quality": 80}),
]
# A coastline-dense region (western South America / SE Pacific margin at
# present day) picked for crop detail, in source-pixel coords at 4096x2048.
CROP_BOX_4096 = (900, 900, 1400, 1300)  # left, upper, right, lower


def frame_path(time_ma):
    idx = 1000 - time_ma
    return os.path.join(SRC_DIR, f"globe_frame_{idx:04d}.png")


def export_spike():
    os.makedirs(SPIKE_OUT, exist_ok=True)
    for time_ma, label in SPIKE_ERAS:
        src = frame_path(time_ma)
        im = Image.open(src).convert("RGB").resize(SPIKE_SIZE, Image.LANCZOS)
        out = os.path.join(SPIKE_OUT, f"{time_ma:04d}ma.jpg")
        im.save(out, "JPEG", quality=SPIKE_JPEG_QUALITY)
        print(f"spike: {time_ma:4d} Ma ({label}) -> {out} "
              f"({os.path.getsize(out)/1024:.0f} KB)")


def export_comparison():
    os.makedirs(COMPARISON_OUT, exist_ok=True)
    os.makedirs(os.path.join(COMPARISON_OUT, "crops"), exist_ok=True)
    src = frame_path(0)  # present day
    src_im = Image.open(src).convert("RGB")
    assert src_im.size == (4096, 2048), f"unexpected source size {src_im.size}"

    results = []
    for label, size, fmt, kwargs in COMPARISON_CANDIDATES:
        im = src_im if size == (4096, 2048) else src_im.resize(size, Image.LANCZOS)
        ext = "png" if fmt == "PNG" else "webp"
        full_path = os.path.join(COMPARISON_OUT, f"full-{label}.{ext}")
        im.save(full_path, fmt, **kwargs)

        # Crop the same geographic region at each resolution's native scale,
        # then upscale the crop to a common viewing size (512x400) with
        # nearest-neighbor-free LANCZOS so quality differences are visible
        # without the browser's own scaling smoothing them out.
        scale = size[0] / 4096
        box = tuple(int(c * scale) for c in CROP_BOX_4096)
        crop = im.crop(box)
        crop_view = crop.resize((512, 400), Image.NEAREST)
        crop_path = os.path.join(COMPARISON_OUT, "crops", f"crop-{label}.{ext}")
        crop_view.save(crop_path, fmt, **kwargs if fmt != "PNG" else {})

        size_kb = os.path.getsize(full_path) / 1024
        results.append((label, size, fmt, size_kb, full_path, crop_path))
        print(f"comparison: {label:28s} {size_kb:7.0f} KB  -> {full_path}")

    return results


if __name__ == "__main__":
    export_spike()
    print()
    export_comparison()
