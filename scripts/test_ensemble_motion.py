#!/usr/bin/env python3
"""Prequel draft-ladder step 1: does the ensemble cloud read in MOTION?

Renders a 50-Myr window (1550 -> 1500 Ma, 1 Ma steps) of ensemble-superposition
textures — same member logic as test_ensemble_uncertainty.py, u from the
full-span ramp — then assembles a preview at ~main-film tempo.

Run (nohup-detached; ~77 min for 459 member renders at ~10 s each):
  nohup .venv/bin/python scripts/test_ensemble_motion.py > motion_draft.log 2>&1 &
"""

import argparse
import os
import subprocess
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("--coherent", action="store_true",
                help="fixed per-member perturbations (smooth parallel worlds) "
                     "instead of per-frame re-rolls (boiling fringes)")
ap.add_argument("--start", type=int, default=1550, help="start time (Ma)")
ap.add_argument("--end", type=int, default=1500, help="end time (Ma)")
ap.add_argument("--step", type=int, default=1, help="cadence (Ma per frame)")
ap.add_argument("--fps", type=int, default=10, help="preview framerate")
ap.add_argument("--tag", default=None,
                help="output tag (dir test_deeptime/<tag>/, preview <tag>.mp4); "
                     "default keeps the original motion/motion_coherent naming")
args = ap.parse_args()

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data", "plate-models")
VARIANT = args.tag or ("motion_coherent" if args.coherent else "motion")
OUT_DIR = os.path.join(ROOT, "test_deeptime", VARIANT)
os.makedirs(OUT_DIR, exist_ok=True)

IMAGE_WIDTH, IMAGE_HEIGHT, DPI = 2048, 1024, 200
T_START, T_END, T_STEP = args.start, args.end, args.step
N_MEMBERS = 9
POLE_SIGMA_DEG = 5.0
TIME_SIGMA_MA = 25.0
SEED = 42
FPS_OUT = args.fps

OCEAN_COLOR = '#1a425a'
CONTINENT_COLOR = '#a07c5a'
COASTLINE_COLOR = '#5c442e'


def u_ramp(t):
    """Full-span uncertainty ramp: 1.0 at 1800 Ma -> 0.0 at 1000 Ma."""
    return max(0.0, min(1.0, (t - 1000.0) / 800.0))


print("Loading cao2024 plate model...")
from plate_model_manager import PlateModelManager
import pygplates

pm_manager = PlateModelManager()
model_data = pm_manager.get_model("cao2024", data_dir=DATA_DIR)
rotation_model = pygplates.RotationModel(model_data.get_rotation_model())
continents_file = model_data.get_layer("ContinentalPolygons")
print("✓ model loaded")

rng = np.random.default_rng(SEED)
wrapper = pygplates.DateLineWrapper(0.0)


def random_pole():
    z = rng.uniform(-1, 1)
    lon = rng.uniform(-180, 180)
    return np.degrees(np.arcsin(z)), lon


# Coherent mode: each member's perturbation is drawn ONCE (unit-scale) and
# reused across all frames, scaled by u(t) — nine smooth parallel worlds whose
# disagreement is the cloud. Reconstruction error is time-correlated, so this
# samples the joint distribution over time; per-frame re-rolls (default) sample
# each instant independently and the fringes boil.
member_dt_unit = {}           # member -> unit normal (time jitter)
member_plate_perturb = {}     # (member, plate_id) -> (pole, angle_unit)


def render_member(time_ma, u, member):
    if u > 0 and member > 0:
        if args.coherent:
            if member not in member_dt_unit:
                member_dt_unit[member] = rng.normal()
            dt = member_dt_unit[member] * TIME_SIGMA_MA * u
        else:
            dt = rng.normal(0, TIME_SIGMA_MA * u)
    else:
        dt = 0.0
    t = max(0.0, time_ma + dt)

    reconstructed = []
    pygplates.reconstruct(continents_file, rotation_model, reconstructed, t)
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
                if args.coherent:
                    key = (member, pid)
                    if key not in member_plate_perturb:
                        member_plate_perturb[key] = (random_pole(), rng.normal())
                    pole, angle_unit = member_plate_perturb[key]
                    angle = np.radians(angle_unit * POLE_SIGMA_DEG * u)
                else:
                    pole = random_pole()
                    angle = np.radians(rng.normal(0, POLE_SIGMA_DEG * u))
                plate_rot[pid] = pygplates.FiniteRotation(pole, angle)
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


times = list(range(T_START, T_END - 1, -T_STEP))
n_rendered = n_skipped = 0
for fi, time_ma in enumerate(times):
    out = os.path.join(OUT_DIR, f"motion_{fi:04d}.png")
    if os.path.exists(out) and os.path.getsize(out) > 100:
        n_skipped += 1
        continue
    u = u_ramp(time_ma)
    acc = None
    for m in range(N_MEMBERS if u > 0 else 1):
        buf = render_member(time_ma, u, m)
        acc = buf if acc is None else acc + buf
    Image.fromarray((acc / (N_MEMBERS if u > 0 else 1)).astype(np.uint8)).save(out)
    n_rendered += 1
    print(f"  ✓ [{fi + 1}/{len(times)}] {time_ma} Ma (u={u:.2f})", flush=True)

print(f"\n✓ Textures: {n_rendered} rendered, {n_skipped} already on disk, "
      f"of {len(times)} total")

preview = os.path.join(ROOT, "test_deeptime",
                       f"{args.tag or ('motion_draft_coherent' if args.coherent else 'motion_draft')}.mp4")
cmd = ["ffmpeg", "-y", "-loglevel", "error",
       "-framerate", str(FPS_OUT),
       "-i", os.path.join(OUT_DIR, "motion_%04d.png"),
       "-vf", "scale=1280:640:flags=lanczos",
       "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p",
       "-movflags", "+faststart", preview]
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode != 0:
    print(f"✗ ffmpeg failed: {r.stderr[:500]}")
    raise SystemExit(1)
print(f"✓ Preview → {preview} ({len(times)} frames at {FPS_OUT} fps "
      f"≈ {len(times) / FPS_OUT:.1f} s)")
