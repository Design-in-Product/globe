#!/usr/bin/env python3
"""Flat-v7 spike: projection-morph spin reveal for the flat view.

During a supercontinent hold, the equirectangular map morphs into a Mollweide
projection, the planet rotates a full 360 degrees UNDER the fixed projection
(continents deform as they pass through its distortion zones), then the map
morphs back to equirectangular and the ordinary timeline resumes.

Pure numpy + matplotlib mesh warp — no cartopy, no new dependencies.
Draft on the Pangaea texture (geo frame 750):

  python3 scripts/test_flat_morph.py
  ffmpeg -framerate 24 -i test_flat_morph/morph_%04d.png -pix_fmt yuv420p \
      test_flat_morph/preview.mp4
"""

import os
import argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
from scipy.ndimage import map_coordinates

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ap = argparse.ArgumentParser()
ap.add_argument("--source", default=os.path.join(ROOT, "frames", "globe_frame_0750.png"))
ap.add_argument("--out", default=os.path.join(ROOT, "test_flat_morph"))
ap.add_argument("--resx", type=int, default=960)
ap.add_argument("--resy", type=int, default=480)
ap.add_argument("--nlon", type=int, default=512, help="mesh cells (lon); ≈resx for per-pixel quality")
ap.add_argument("--nlat", type=int, default=256, help="mesh cells (lat); ≈resy for per-pixel quality")
args = ap.parse_args()

SOURCE = args.source
OUT_DIR = args.out
os.makedirs(OUT_DIR, exist_ok=True)

RES_X, RES_Y = args.resx, args.resy
FPS = 24
OCEAN = '#1a425a'

# Phases (seconds): hold, morph out, rotate 360, morph back, hold
PHASES = [1.5, 2.0, 5.0, 2.0, 1.5]

# Mesh density (cells)
NLON, NLAT = args.nlon, args.nlat


def smootherstep(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * t * (t * (t * 6 - 15) + 10)


def mollweide_theta(lat_rad):
    """Solve 2θ + sin 2θ = π sin(lat) by Newton iteration (vectorized)."""
    theta = lat_rad.copy()
    target = np.pi * np.sin(lat_rad)
    for _ in range(10):
        f = 2 * theta + np.sin(2 * theta) - target
        fp = 2 + 2 * np.cos(2 * theta)
        step = np.where(np.abs(fp) > 1e-9, f / fp, 0.0)
        theta = theta - step
    return theta


# ── Static geometry ───────────────────────────────────────────
# Mesh vertices over DISPLAY coordinates (lon', lat): the projection frame is
# fixed; rotation shifts only the texture sampled onto it.
lon_edges = np.linspace(-180, 180, NLON + 1)
lat_edges = np.linspace(-90, 90, NLAT + 1)
LON, LAT = np.meshgrid(lon_edges, lat_edges)

# Equirectangular vertex positions, normalized to [-1, 1] each axis
EQ_X = LON / 180.0
EQ_Y = LAT / 90.0

# Mollweide vertex positions, normalized to the same [-1, 1] envelope
theta_edges = mollweide_theta(np.radians(lat_edges))
THETA = np.repeat(theta_edges[:, None], NLON + 1, axis=1)
MO_X = (2 * np.sqrt(2) / np.pi) * np.radians(LON) * np.cos(THETA) / (2 * np.sqrt(2) / np.pi * np.pi)
MO_Y = np.sqrt(2) * np.sin(THETA) / np.sqrt(2)

# Texture-sampling grid at cell centers
lon_c = (lon_edges[:-1] + lon_edges[1:]) / 2
lat_c = (lat_edges[:-1] + lat_edges[1:]) / 2
LON_C, LAT_C = np.meshgrid(lon_c, lat_c)

img = np.asarray(Image.open(SOURCE).convert('RGB'), dtype=np.float32) / 255.0
H, W = img.shape[:2]
ROW_F = np.clip((90 - LAT_C) / 180.0 * H - 0.5, 0, H - 1)


def sample_colors(lon0):
    """Bilinearly sample the source texture, planet rotated by lon0 degrees."""
    col_f = (((LON_C + lon0 + 180.0) % 360.0) / 360.0 * W - 0.5) % W
    coords = np.stack([ROW_F.ravel(), col_f.ravel()])
    out = np.empty((*LON_C.shape, 3), dtype=np.float32)
    for c in range(3):
        out[..., c] = map_coordinates(img[..., c], coords, order=1,
                                      mode='grid-wrap').reshape(LON_C.shape)
    return out


# ── Frame schedule ────────────────────────────────────────────
frames = []  # (s_morph, lon0)
for phase, dur in enumerate(PHASES):
    n = int(round(dur * FPS))
    for k in range(n):
        t = k / max(n - 1, 1)
        if phase == 0:
            frames.append((0.0, 0.0))
        elif phase == 1:
            frames.append((smootherstep(t), 0.0))
        elif phase == 2:
            frames.append((1.0, 360.0 * smootherstep(t)))
        elif phase == 3:
            frames.append((1.0 - smootherstep(t), 0.0))
        else:
            frames.append((0.0, 0.0))

print(f"Rendering {len(frames)} morph frames ({sum(PHASES):.1f}s at {FPS}fps)...")

for i, (s, lon0) in enumerate(frames):
    X = (1 - s) * EQ_X + s * MO_X
    Y = (1 - s) * EQ_Y + s * MO_Y
    C = sample_colors(lon0)

    fig = plt.figure(figsize=(RES_X / 100, RES_Y / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(-1.03, 1.03)
    ax.set_ylim(-1.03, 1.03)
    ax.set_axis_off()
    fig.patch.set_facecolor('black')
    ax.pcolormesh(X, Y, C, shading='flat', rasterized=True)
    fig.savefig(os.path.join(OUT_DIR, f"morph_{i:04d}.png"),
                dpi=100, facecolor='black')
    plt.close(fig)
    if (i + 1) % 48 == 0:
        print(f"  [{i+1}/{len(frames)}]")

print(f"✓ Done → {OUT_DIR}/")
