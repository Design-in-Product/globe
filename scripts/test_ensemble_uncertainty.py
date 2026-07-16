#!/usr/bin/env python3
"""Prequel uncertainty v2: ENSEMBLE SUPERPOSITION instead of lens blur.

xian's insight (2026-07-15): deep-time uncertainty isn't defocus — plate
positions become a probability cloud. So render it literally: N ensemble
members, each a perturbed reconstruction —
  - per-plate rotation-pole jitter (incoherent: each plate wanders
    independently, scaled by uncertainty u)
  - coherent time jitter (positions smear along their true trajectories:
    "the motion is less predictable")
— then average the members. Solid where the possibilities agree, fading at
the fringes because fewer members put crust there.

Run in the gplately venv:
  ~/Development/atlas/.venv/bin/python scripts/test_ensemble_uncertainty.py

Output: test_deeptime/ensemble_NNNN_ma.png + ensemble_strip.png
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data", "plate-models")
OUT_DIR = os.path.join(ROOT, "test_deeptime")
os.makedirs(OUT_DIR, exist_ok=True)

IMAGE_WIDTH, IMAGE_HEIGHT, DPI = 2048, 1024, 200

# (time_ma, uncertainty 0..1) — same ramp as the blur strip for comparison
FRAMES = [
    (1800, 1.00),
    (1650, 0.80),
    (1500, 0.60),
    (1350, 0.40),
    (1200, 0.20),
    (1000, 0.00),
]

N_MEMBERS = 9          # ensemble size (u > 0)
POLE_SIGMA_DEG = 5.0   # per-plate positional jitter at u=1 (degrees)
TIME_SIGMA_MA = 25.0   # coherent time jitter at u=1 (Ma)
SEED = 42

OCEAN_COLOR = '#1a425a'
CONTINENT_COLOR = '#a07c5a'
COASTLINE_COLOR = '#5c442e'

print("Loading cao2024 plate model...")
from plate_model_manager import PlateModelManager
import pygplates

pm_manager = PlateModelManager()
model_data = pm_manager.get_model("cao2024", data_dir=DATA_DIR)
rotation_model = pygplates.RotationModel(model_data.get_rotation_model())
continents_file = model_data.get_layer("ContinentalPolygons")
print("✓ model loaded")

rng = np.random.default_rng(SEED)
wrapper = pygplates.DateLineWrapper(0.0)  # split polygons at the antimeridian


def random_pole():
    """Uniform random point on the sphere."""
    z = rng.uniform(-1, 1)
    lon = rng.uniform(-180, 180)
    lat = np.degrees(np.arcsin(z))
    return lat, lon


def render_member(time_ma, u, member):
    """Render one ensemble member to an RGB float array."""
    dt = rng.normal(0, TIME_SIGMA_MA * u) if u > 0 and member > 0 else 0.0
    t = max(0.0, time_ma + dt)

    reconstructed = []
    pygplates.reconstruct(continents_file, rotation_model, reconstructed, t)

    # One perturbation per plate id per member (coherent within a plate)
    plate_rot = {}

    fig = plt.figure(figsize=(IMAGE_WIDTH / DPI, IMAGE_HEIGHT / DPI), dpi=DPI,
                     facecolor=OCEAN_COLOR)
    ax = fig.add_axes([0, 0, 1, 1], projection=ccrs.PlateCarree(central_longitude=0))
    ax.set_global()
    ax.set_axis_off()
    ax.set_facecolor(OCEAN_COLOR)
    ax.patch.set_facecolor(OCEAN_COLOR)

    for rg in reconstructed:
        geom = rg.get_reconstructed_geometry()
        if geom is None:
            continue
        if u > 0 and member > 0:
            pid = rg.get_feature().get_reconstruction_plate_id()
            if pid not in plate_rot:
                angle = np.radians(rng.normal(0, POLE_SIGMA_DEG * u))
                plate_rot[pid] = pygplates.FiniteRotation(random_pole(), angle)
            geom = plate_rot[pid] * geom
        for wp in wrapper.wrap(geom, 2.0):
            pts = wp.get_exterior_points()
            if len(pts) < 3:
                continue
            lons = [p.get_longitude() for p in pts]
            lats = [p.get_latitude() for p in pts]
            ax.fill(lons, lats, color=CONTINENT_COLOR, edgecolor=COASTLINE_COLOR,
                    linewidth=0.4, transform=ccrs.PlateCarree())

    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())[..., :3].astype(np.float32)
    plt.close(fig)
    return buf


tiles = []
for time_ma, u in FRAMES:
    n = N_MEMBERS if u > 0 else 1
    acc = None
    for m in range(n):
        buf = render_member(time_ma, u, m)
        acc = buf if acc is None else acc + buf
    mean = (acc / n).astype(np.uint8)
    im = Image.fromarray(mean)
    out = os.path.join(OUT_DIR, f"ensemble_{time_ma:04d}_ma.png")
    im.save(out)
    print(f"  ✓ {time_ma} Ma (u={u:.2f}, {n} members)")

    thumb = im.resize((1000, 500), Image.LANCZOS)
    draw = ImageDraw.Draw(thumb)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 34)
    except Exception:
        font = ImageFont.load_default()
    draw.rectangle([0, 0, 560, 54], fill=(0, 0, 0))
    draw.text((14, 8), f"{time_ma} Ma   {n} superimposed possibilities",
              fill=(232, 232, 232), font=font)
    tiles.append(thumb)

strip = Image.new('RGB', (1000, 500 * len(tiles)))
for i, t in enumerate(tiles):
    strip.paste(t, (0, 500 * i))
strip_path = os.path.join(OUT_DIR, "ensemble_strip.png")
strip.save(strip_path)
print(f"\n✓ Strip → {strip_path}")
