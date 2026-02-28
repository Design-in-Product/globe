#!/usr/bin/env python3
"""
Generate equirectangular tectonic plate frames for Blender globe animation.

Produces 1000 PNG frames (1000 Ma → 0 Ma, 1 Ma steps) showing continental
positions, coastlines, and plate boundaries using the Merdith et al. (2021)
plate reconstruction model.

Output frames are 4096x2048 equirectangular (PlateCarree) projection,
suitable for UV-mapping onto a sphere in Blender.
"""

import os
import sys
import time as pytime
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Headless rendering — no GUI
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# ── Configuration ──────────────────────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data", "plate-models")
FRAMES_DIR = os.path.join(PROJECT_ROOT, "frames")
FRAME_PREFIX = "globe_frame_"

IMAGE_WIDTH = 4096
IMAGE_HEIGHT = 2048
DPI = 200

TIME_START = 1000  # Ma (Rodinia)
TIME_END = 0       # Ma (Present)
TIME_STEP = 1      # Ma per frame

# Color scheme
OCEAN_COLOR = '#1a425a'
CONTINENT_COLOR = '#a07c5a'
COASTLINE_COLOR = '#5c442e'
RIDGE_COLOR = '#ff6b35'
TRENCH_COLOR = '#e63946'

# ── Setup ──────────────────────────────────────────────────────
os.makedirs(FRAMES_DIR, exist_ok=True)

# Build time array: 1000, 995, 990, ..., 5, 0
times = np.arange(TIME_START, TIME_END - 1, -TIME_STEP)
total_frames = len(times)
print(f"Will generate {total_frames} frames from {TIME_START} Ma to {TIME_END} Ma")
print(f"Output: {FRAMES_DIR}/{FRAME_PREFIX}NNNN.png at {IMAGE_WIDTH}x{IMAGE_HEIGHT}")

# ── Load plate model ──────────────────────────────────────────
print("\nLoading Merdith2021 plate model...")

USE_GPLATELY = True
try:
    from plate_model_manager import PlateModelManager
    import gplately

    pm_manager = PlateModelManager()
    model_data = pm_manager.get_model("Merdith2021", data_dir=DATA_DIR)

    rotation_model = model_data.get_rotation_model()
    topology_features = model_data.get_topologies()
    static_polygons = model_data.get_static_polygons()
    coastlines = model_data.get_layer("Coastlines")
    continents = model_data.get_layer("ContinentalPolygons")

    model = gplately.PlateReconstruction(
        rotation_model, topology_features, static_polygons
    )
    gplot = gplately.PlotTopologies(
        model,
        coastlines=coastlines,
        continents=continents,
    )
    print("✓ gplately model loaded")

except Exception as e:
    print(f"⚠ gplately failed: {e}")
    print("Falling back to raw pygplates...")
    USE_GPLATELY = False

    import pygplates

    rot_files = []
    gpml_coast = []
    for root, dirs, files in os.walk(DATA_DIR):
        for f in files:
            if f.endswith('.rot'):
                rot_files.append(os.path.join(root, f))
            if f.endswith('.gpml') and 'coastline' in f.lower():
                gpml_coast.append(os.path.join(root, f))

    if not rot_files or not gpml_coast:
        print(f"✗ ERROR: Missing .rot or coastline .gpml in {DATA_DIR}")
        sys.exit(1)

    pg_rotation = pygplates.RotationModel(rot_files[0])
    pg_coastlines = pygplates.FeatureCollection(gpml_coast[0])
    print(f"✓ pygplates fallback loaded ({rot_files[0]})")


def render_frame_gplately(time_ma, frame_idx):
    """Render a single frame using gplately PlotTopologies."""
    fig_w = IMAGE_WIDTH / DPI
    fig_h = IMAGE_HEIGHT / DPI
    fig = plt.figure(figsize=(fig_w, fig_h), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1], projection=ccrs.PlateCarree(central_longitude=0))
    ax.set_global()
    ax.set_axis_off()
    ax.set_facecolor(OCEAN_COLOR)

    # Set reconstruction time
    gplot.time = time_ma

    # Continental polygons (filled)
    try:
        gplot.plot_continents(ax, facecolor=CONTINENT_COLOR, edgecolor='none', alpha=0.9)
    except Exception:
        pass

    # Coastlines
    try:
        gplot.plot_coastlines(ax, color=COASTLINE_COLOR, linewidth=0.5)
    except Exception:
        pass

    # Plate boundaries — not available for all time steps
    try:
        gplot.plot_ridges(ax, color=RIDGE_COLOR, linewidth=0.8)
    except Exception:
        pass

    try:
        gplot.plot_transforms(ax, color=RIDGE_COLOR, linewidth=0.6, alpha=0.7)
    except Exception:
        pass

    try:
        gplot.plot_trenches(ax, color=TRENCH_COLOR, linewidth=0.8)
    except Exception:
        pass

    try:
        gplot.plot_subduction_teeth(ax, color=TRENCH_COLOR)
    except Exception:
        pass

    # Save (no text label — subtitle overlay handles time/era display)
    out_path = os.path.join(FRAMES_DIR, f'{FRAME_PREFIX}{frame_idx:04d}.png')
    fig.savefig(out_path, dpi=DPI, facecolor=OCEAN_COLOR, pad_inches=0)
    plt.close(fig)
    return out_path


def render_frame_pygplates(time_ma, frame_idx):
    """Render a single frame using raw pygplates (fallback)."""
    fig_w = IMAGE_WIDTH / DPI
    fig_h = IMAGE_HEIGHT / DPI
    fig = plt.figure(figsize=(fig_w, fig_h), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1], projection=ccrs.PlateCarree(central_longitude=0))
    ax.set_global()
    ax.set_axis_off()
    ax.set_facecolor(OCEAN_COLOR)

    # Reconstruct coastlines
    reconstructed = []
    pygplates.reconstruct(pg_coastlines, pg_rotation, reconstructed, time_ma)

    for rg in reconstructed:
        polygon = rg.get_reconstructed_geometry()
        if polygon:
            points = polygon.to_lat_lon_list()
            lons = [p[1] for p in points]
            lats = [p[0] for p in points]
            ax.fill(lons, lats, color=CONTINENT_COLOR, edgecolor=COASTLINE_COLOR,
                    linewidth=0.5, transform=ccrs.Geodetic())

    # Save (no text label — subtitle overlay handles time/era display)
    out_path = os.path.join(FRAMES_DIR, f'{FRAME_PREFIX}{frame_idx:04d}.png')
    fig.savefig(out_path, dpi=DPI, facecolor=OCEAN_COLOR, pad_inches=0)
    plt.close(fig)
    return out_path


# ── Main rendering loop ───────────────────────────────────────
render_fn = render_frame_gplately if USE_GPLATELY else render_frame_pygplates

print(f"\nRendering {total_frames} frames using {'gplately' if USE_GPLATELY else 'pygplates'}...\n")
start = pytime.time()

for i, time_ma in enumerate(times):
    t0 = pytime.time()
    out_path = render_fn(time_ma, i)
    elapsed = pytime.time() - t0

    # Progress
    pct = (i + 1) / total_frames * 100
    total_elapsed = pytime.time() - start
    avg_per_frame = total_elapsed / (i + 1)
    remaining = avg_per_frame * (total_frames - i - 1)

    print(f"  [{i+1:3d}/{total_frames}] {pct:5.1f}%  {int(time_ma):4d} Ma  "
          f"{elapsed:.1f}s  ETA {remaining/60:.1f}min  → {os.path.basename(out_path)}")

total_time = pytime.time() - start
print(f"\n✓ Done! {total_frames} frames generated in {total_time/60:.1f} minutes")
print(f"  Output: {FRAMES_DIR}/")

# Verify
actual_frames = len([f for f in os.listdir(FRAMES_DIR)
                     if f.startswith(FRAME_PREFIX) and f.endswith('.png')])
if actual_frames == total_frames:
    print(f"  Verification: {actual_frames} frames found ✓")
else:
    print(f"  ⚠ Expected {total_frames} frames, found {actual_frames}")
