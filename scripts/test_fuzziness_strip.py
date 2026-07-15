#!/usr/bin/env python3
"""Prequel uncertainty test strip: apply a graduated 'deep time = fuzzy'
treatment to the cao2024 spike frames so xian can judge the effect.

Treatment per frame, scaled by age (1800 Ma = max, 1000 Ma = none):
  - desaturation toward a hazy blue-grey
  - contrast reduction (haze)
  - Gaussian blur on the whole map (soft coastlines)

Outputs individual treated frames plus a labeled vertical strip:
  test_deeptime/fuzziness_strip.png

Run: python3 scripts/test_fuzziness_strip.py   (any python with PIL)
"""

import os
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(ROOT, "test_deeptime")

# (time_ma, uncertainty 0..1) — full fuzz at 1800, crisp by 1000
FRAMES = [
    (1800, 1.00),
    (1650, 0.80),
    (1500, 0.60),
    (1350, 0.40),
    (1200, 0.20),
    (1000, 0.00),
]

MAX_BLUR = 6.0        # px at 2048-wide source
MAX_DESAT = 0.45      # fraction of color removed
MAX_DECONTRAST = 0.25 # fraction of contrast removed
HAZE = (60, 80, 100)  # blue-grey haze tint
MAX_HAZE_ALPHA = 0.18

THUMB_W = 1000

tiles = []
for time_ma, u in FRAMES:
    src = os.path.join(SRC_DIR, f"cao2024_{time_ma:04d}_ma.png")
    im = Image.open(src).convert('RGB')

    if u > 0:
        im = im.filter(ImageFilter.GaussianBlur(radius=MAX_BLUR * u))
        im = ImageEnhance.Color(im).enhance(1.0 - MAX_DESAT * u)
        im = ImageEnhance.Contrast(im).enhance(1.0 - MAX_DECONTRAST * u)
        haze = Image.new('RGB', im.size, HAZE)
        im = Image.blend(im, haze, MAX_HAZE_ALPHA * u)

    out = os.path.join(SRC_DIR, f"fuzzy_{time_ma:04d}_ma.png")
    im.save(out)

    thumb = im.resize((THUMB_W, THUMB_W // 2), Image.LANCZOS)
    draw = ImageDraw.Draw(thumb)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 34)
    except Exception:
        font = ImageFont.load_default()
    label = f"{time_ma} Ma   uncertainty {u:.0%}"
    draw.rectangle([0, 0, 460, 54], fill=(0, 0, 0))
    draw.text((14, 8), label, fill=(232, 232, 232), font=font)
    tiles.append(thumb)
    print(f"  ✓ {time_ma} Ma (u={u:.2f})")

strip = Image.new('RGB', (THUMB_W, (THUMB_W // 2) * len(tiles)))
for i, t in enumerate(tiles):
    strip.paste(t, (0, (THUMB_W // 2) * i))
strip_path = os.path.join(SRC_DIR, "fuzziness_strip.png")
strip.save(strip_path)
print(f"\n✓ Strip → {strip_path}")
