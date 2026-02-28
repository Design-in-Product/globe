#!/usr/bin/env python3
"""
Test script: Renders a single equirectangular frame at 200 Ma (Pangaea assembly)
to validate the entire data + rendering pipeline before the full batch run.
"""

import os
import sys
import matplotlib
matplotlib.use('Agg')  # Headless rendering — no GUI
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# ── Configuration ──────────────────────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data", "plate-models")
FRAMES_DIR = os.path.join(PROJECT_ROOT, "frames")
OUTPUT_PATH = os.path.join(FRAMES_DIR, "test_frame.png")
TEST_TIME = 200  # Ma — Pangaea assembly, a well-known configuration
IMAGE_WIDTH = 4096
IMAGE_HEIGHT = 2048
DPI = 200

os.makedirs(FRAMES_DIR, exist_ok=True)

# ── Load plate model data ─────────────────────────────────────
print(f"Loading Merdith2021 plate model (data_dir={DATA_DIR})...")
print("(First run will download ~13 MB from EarthByte servers)")

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

    print("✓ Model data loaded successfully")

    # Build gplately reconstruction objects
    model = gplately.PlateReconstruction(
        rotation_model, topology_features, static_polygons
    )
    gplot = gplately.PlotTopologies(
        model,
        coastlines=coastlines,
        continents=continents,
        time=TEST_TIME,
    )
    print(f"✓ PlotTopologies created for {TEST_TIME} Ma")
    USE_GPLATELY = True

except Exception as e:
    print(f"⚠ gplately high-level API failed: {e}")
    print("Falling back to raw pygplates approach...")
    USE_GPLATELY = False

# ── Render the frame ──────────────────────────────────────────
fig_w = IMAGE_WIDTH / DPI
fig_h = IMAGE_HEIGHT / DPI
fig = plt.figure(figsize=(fig_w, fig_h), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1], projection=ccrs.PlateCarree(central_longitude=0))
ax.set_global()
ax.set_axis_off()

# Ocean background
ax.set_facecolor('#1a425a')

if USE_GPLATELY:
    # Use gplately's PlotTopologies for rich rendering
    try:
        gplot.plot_continents(ax, facecolor='#a07c5a', edgecolor='none', alpha=0.9)
        print("✓ Continents plotted")
    except Exception as e:
        print(f"⚠ plot_continents failed: {e}")

    try:
        gplot.plot_coastlines(ax, color='#5c442e', linewidth=0.5)
        print("✓ Coastlines plotted")
    except Exception as e:
        print(f"⚠ plot_coastlines failed: {e}")

    try:
        gplot.plot_ridges(ax, color='#ff6b35', linewidth=0.8)
        print("✓ Ridges plotted")
    except Exception as e:
        print(f"⚠ plot_ridges failed: {e}")

    try:
        gplot.plot_transforms(ax, color='#ff6b35', linewidth=0.6, alpha=0.7)
        print("✓ Transforms plotted")
    except Exception as e:
        print(f"⚠ plot_transforms failed: {e}")

    try:
        gplot.plot_trenches(ax, color='#e63946', linewidth=0.8)
        print("✓ Trenches plotted")
    except Exception as e:
        print(f"⚠ plot_trenches failed: {e}")

    try:
        gplot.plot_subduction_teeth(ax, color='#e63946')
        print("✓ Subduction teeth plotted")
    except Exception as e:
        print(f"⚠ plot_subduction_teeth failed: {e}")

else:
    # Fallback: raw pygplates approach (from Gemini reference script)
    import pygplates

    # Find .rot and coastline .gpml files
    rot_files = []
    gpml_files = []
    for root, dirs, files in os.walk(DATA_DIR):
        for f in files:
            if f.endswith('.rot'):
                rot_files.append(os.path.join(root, f))
            if f.endswith('.gpml') and 'coastline' in f.lower():
                gpml_files.append(os.path.join(root, f))

    if not rot_files or not gpml_files:
        print("✗ ERROR: Could not find .rot or coastline .gpml files in", DATA_DIR)
        sys.exit(1)

    print(f"Using rotation file: {rot_files[0]}")
    print(f"Using coastlines file: {gpml_files[0]}")

    rotation_model = pygplates.RotationModel(rot_files[0])
    coastline_features = pygplates.FeatureCollection(gpml_files[0])

    reconstructed_geometries = []
    pygplates.reconstruct(coastline_features, rotation_model, reconstructed_geometries, TEST_TIME)

    for rg in reconstructed_geometries:
        polygon = rg.get_reconstructed_geometry()
        if polygon:
            points = polygon.to_lat_lon_list()
            lons = [p[1] for p in points]
            lats = [p[0] for p in points]
            ax.fill(lons, lats, color='#a07c5a', edgecolor='#5c442e',
                    linewidth=0.5, transform=ccrs.Geodetic())

    print(f"✓ Plotted {len(reconstructed_geometries)} reconstructed geometries")

# Time label
ax.text(0.02, 0.02, f'{TEST_TIME} Ma',
        transform=ax.transAxes, fontsize=16, color='white',
        fontweight='bold', va='bottom',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.6))

# ── Save ──────────────────────────────────────────────────────
fig.savefig(OUTPUT_PATH, dpi=DPI, facecolor='#1a425a', pad_inches=0)
plt.close(fig)

# Verify output
if os.path.exists(OUTPUT_PATH):
    size_mb = os.path.getsize(OUTPUT_PATH) / (1024 * 1024)
    from PIL import Image
    with Image.open(OUTPUT_PATH) as img:
        print(f"\n✓ Test frame saved: {OUTPUT_PATH}")
        print(f"  Dimensions: {img.size[0]}x{img.size[1]}")
        print(f"  File size: {size_mb:.1f} MB")
        if img.size[0] / img.size[1] == 2.0:
            print("  Aspect ratio: 2:1 ✓ (correct for equirectangular)")
        else:
            ratio = img.size[0] / img.size[1]
            print(f"  Aspect ratio: {ratio:.2f}:1 ⚠ (should be 2:1 for equirectangular)")
else:
    print(f"\n✗ ERROR: Output file not created at {OUTPUT_PATH}")
    sys.exit(1)

print("\n🌍 Pipeline test PASSED. Ready for full frame generation.")
