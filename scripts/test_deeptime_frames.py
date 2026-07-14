#!/usr/bin/env python3
"""Prequel spike (roadmap #2): render a few deep-time test frames from the
Cao et al. 2024 1.8 Ga model, in the same visual style as generate_frames.py,
to see what the Nuna era looks like in our pipeline.

Run in the gplately venv:
  ~/Development/atlas/.venv/bin/python scripts/test_deeptime_frames.py

Output: test_deeptime/cao2024_NNNN_ma.png (2048x1024 equirectangular drafts).
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data", "plate-models")
OUT_DIR = os.path.join(PROJECT_ROOT, "test_deeptime")
os.makedirs(OUT_DIR, exist_ok=True)

# Draft resolution (half of production 4096x2048)
IMAGE_WIDTH = 2048
IMAGE_HEIGHT = 1024
DPI = 200

# Spike times: Nuna assembly/peak/breakup → Rodinia handoff.
# 1000 Ma included to compare against the Merdith-based frame 0 we render today.
TEST_TIMES = [1800, 1650, 1500, 1350, 1200, 1050, 1000]

# House colors (generate_frames.py)
OCEAN_COLOR = '#1a425a'
CONTINENT_COLOR = '#a07c5a'
COASTLINE_COLOR = '#5c442e'
RIDGE_COLOR = '#ff6b35'
TRENCH_COLOR = '#e63946'

print("Loading cao2024 plate model...")
from plate_model_manager import PlateModelManager
import gplately

pm_manager = PlateModelManager()
model_data = pm_manager.get_model("cao2024", data_dir=DATA_DIR)

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
print("✓ cao2024 model loaded")

for time_ma in TEST_TIMES:
    fig = plt.figure(figsize=(IMAGE_WIDTH / DPI, IMAGE_HEIGHT / DPI), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1], projection=ccrs.PlateCarree(central_longitude=0))
    ax.set_global()
    ax.set_axis_off()
    ax.set_facecolor(OCEAN_COLOR)

    gplot.time = time_ma

    try:
        gplot.plot_continents(ax, facecolor=CONTINENT_COLOR, edgecolor='none', alpha=0.9)
    except Exception as e:
        print(f"  ⚠ continents failed at {time_ma} Ma: {e}")
    try:
        gplot.plot_coastlines(ax, color=COASTLINE_COLOR, linewidth=0.5)
    except Exception as e:
        print(f"  ⚠ coastlines failed at {time_ma} Ma: {e}")
    try:
        gplot.plot_ridges(ax, color=RIDGE_COLOR, linewidth=0.8)
    except Exception as e:
        print(f"  ⚠ ridges failed at {time_ma} Ma: {e}")
    try:
        gplot.plot_transforms(ax, color=RIDGE_COLOR, linewidth=0.6, alpha=0.7)
    except Exception as e:
        print(f"  ⚠ transforms failed at {time_ma} Ma: {e}")
    try:
        gplot.plot_trenches(ax, color=TRENCH_COLOR, linewidth=0.8)
    except Exception as e:
        print(f"  ⚠ trenches failed at {time_ma} Ma: {e}")
    try:
        gplot.plot_subduction_teeth(ax, color=TRENCH_COLOR)
    except Exception as e:
        print(f"  ⚠ teeth failed at {time_ma} Ma: {e}")

    out = os.path.join(OUT_DIR, f"cao2024_{time_ma:04d}_ma.png")
    fig.savefig(out, dpi=DPI, facecolor=OCEAN_COLOR, pad_inches=0)
    plt.close(fig)
    print(f"  ✓ {time_ma} Ma → {os.path.basename(out)}")

print(f"\n✓ Done: {len(TEST_TIMES)} deep-time test frames in {OUT_DIR}/")
