#!/usr/bin/env python3
"""Prequel production textures: 1800 -> 1000 Ma ensemble-superposition frames.

Design (all xian-decided, 2026-07-28/29 — docs/design/prequel-production-design-2026-07-28.md):
cao2024 model · 1 Ma per frame · 9 COHERENT members (per-plate pole jitter +
coherent time jitter, drawn once per member and scaled by the u-ramp) ·
u(t) linear 1.0 @ 1800 Ma -> 0.0 @ 1000 Ma.

Coherence under resume/split: every perturbation is derived deterministically
from (SEED, member, plate_id) via SeedSequence — NOT from draw order — so a
resumed run, or parallel FRAME_START/FRAME_END workers, produce byte-identical
worlds. (The lazy-draw approach in test_ensemble_motion.py breaks on resume.)

Frame naming: prequel_frame_NNNN.png where NNNN = 1800 - Ma (0000 = 1800 Ma,
0800 = 1000 Ma) — index increases forward in time, like the main film.

Run (nohup-detached per convention; output OUTSIDE the repo):
  cd ~/Development/globe
  nohup .venv/bin/python scripts/generate_prequel_frames.py \
      > ~/globe-render/prequel_frames.log 2>&1 &

Resume is free (complete PNGs are skipped; truncated ones re-rendered).
Split across workers with FRAME_START/FRAME_END env vars (inclusive indices).
"""

import os
import time
import numpy as np
from scipy.ndimage import map_coordinates
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data", "plate-models")
OUT_DIR = os.path.expanduser(os.environ.get(
    "PREQUEL_OUT", "~/globe-render/prequel_frames"))
os.makedirs(OUT_DIR, exist_ok=True)

T_START, T_END = 1800, 1000          # Ma, inclusive
N_MEMBERS = 9
POLE_SIGMA_DEG = 5.0
TIME_SIGMA_MA = 25.0
SEED = 42
IMAGE_WIDTH, IMAGE_HEIGHT, DPI = 2048, 1024, 200

# The map crystallizes in (xian + Tessera, 2026-08-01): plate boundaries in
# the main film's style fade from 0 to full opacity as u -> 0, so the
# prequel's terminal frame converges on the main film's opening STYLE, not
# just its geometry. Boundaries are the very thing the deep-time model can't
# constrain — they appear as the science firms up.
BOUNDARY_FADE_START = 1150.0         # Ma; alpha 0 here -> 1 at 1000 Ma
RIDGE_COLOR = '#ff6b35'
TRENCH_COLOR = '#e63946'
# Main film draws at 4096 wide; we draw at 2048, so halve linewidths to keep
# the same on-screen weight after assembly scales both to output width.
BOUNDARY_LW = dict(ridges=0.4, transforms=0.3, trenches=0.4)


def boundary_alpha(t):
    return max(0.0, min(1.0, (BOUNDARY_FADE_START - t) /
                        (BOUNDARY_FADE_START - float(T_END))))

FRAME_START = int(os.environ.get("FRAME_START", "-1"))
FRAME_END = int(os.environ.get("FRAME_END", "-1"))

OCEAN_COLOR = '#1a425a'
CONTINENT_COLOR = '#a07c5a'
COASTLINE_COLOR = '#5c442e'


def u_ramp(t):
    """1.0 at 1800 Ma -> 0.0 at 1000 Ma, linear (the xian-confirmed ramp)."""
    return max(0.0, min(1.0, (t - 1000.0) / 800.0))


def png_complete(path):
    """True only for a fully-written PNG (valid IEND trailer)."""
    try:
        if os.path.getsize(path) < 100:
            return False
        with open(path, "rb") as f:
            f.seek(-12, os.SEEK_END)
            return f.read(12) == b"\x00\x00\x00\x00IEND\xaeB`\x82"
    except OSError:
        return False


def member_time_unit(member):
    """Deterministic unit normal for member's coherent time jitter."""
    return np.random.default_rng(
        np.random.SeedSequence((SEED, 0, member))).normal()


def member_plate_perturb(member, plate_id):
    """Deterministic (pole, angle_unit) for (member, plate) — order-independent."""
    r = np.random.default_rng(np.random.SeedSequence((SEED, 1, member, plate_id)))
    z = r.uniform(-1, 1)
    lon = r.uniform(-180, 180)
    return (np.degrees(np.arcsin(z)), lon), r.normal()


print("Loading cao2024 plate model...")
from plate_model_manager import PlateModelManager
import pygplates

pm_manager = PlateModelManager()
model_data = pm_manager.get_model("cao2024", data_dir=DATA_DIR)
rotation_model = pygplates.RotationModel(model_data.get_rotation_model())
continents_file = model_data.get_layer("ContinentalPolygons")
print("✓ model loaded")

# ── Frame registration (per-plate) ────────────────────────────
# cao2024's reference frame at 1000 Ma is rotated ~9.85° from Merdith2021's
# (the main film's model); a few terranes are also genuinely repositioned.
# During the crystallization window each plate slerps onto Merdith's exact
# 1000 Ma position — unless its required move exceeds MAX_REG_DISP_DEG
# (a genuine model disagreement; dragging it would be worse than letting the
# terminal dissolve show the disagreement).
MAX_REG_DISP_DEG = 20.0
mer_model_data = PlateModelManager().get_model("Merdith2021", data_dir=DATA_DIR)
mer_rotation_model = pygplates.RotationModel(mer_model_data.get_rotation_model())
_reg_cache = {}


def registration_rotation(pid, w, sample_point):
    """w-weighted corrective rotation for plate pid (None = leave alone)."""
    if pid not in _reg_cache:
        try:
            Rc = rotation_model.get_rotation(1000.0, pid)
            Rm = mer_rotation_model.get_rotation(1000.0, pid)
            Rcorr = Rm * Rc.get_inverse()
            plat, plon, ang = Rcorr.get_lat_lon_euler_pole_and_angle_degrees()
            moved = Rcorr * sample_point
            disp = np.degrees(np.arccos(np.clip(
                np.dot(moved.to_xyz(), sample_point.to_xyz()), -1, 1)))
            _reg_cache[pid] = (plat, plon, ang) if disp <= MAX_REG_DISP_DEG else None
        except Exception:
            _reg_cache[pid] = None
    entry = _reg_cache[pid]
    if entry is None or w <= 0.0:
        return None
    plat, plon, ang = entry
    return pygplates.FiniteRotation((plat, plon), np.radians(ang * w))


# Topology plotting (boundary fade-in) via gplately, same as generate_frames.py
import gplately
_gplot_model = gplately.PlateReconstruction(
    model_data.get_rotation_model(),
    model_data.get_topologies(),
    model_data.get_static_polygons(),
)
gplot = gplately.PlotTopologies(
    _gplot_model,
    coastlines=model_data.get_layer("Coastlines"),
    continents=continents_file,
)
print("✓ topology plotter ready")

wrapper = pygplates.DateLineWrapper(0.0)


# Common rigid component of the frame offset (measured from the major
# cratons — identical across all of them): used to rotate the boundary-layer
# raster so boundaries track their per-plate-corrected continents.
REG_POLE_LAT, REG_POLE_LON, REG_ANGLE = 37.238544, -130.032507, 9.847544


def _rot_matrix(pole_lat, pole_lon, angle_deg):
    la, lo, th = map(np.radians, (pole_lat, pole_lon, angle_deg))
    k = np.array([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)])
    K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
    return np.eye(3) + np.sin(th) * K + (1 - np.cos(th)) * (K @ K)


def raster_rotate(img, w):
    """Rotate an equirect raster by w x the common registration rotation."""
    H, W = img.shape[:2]
    lon = np.radians((np.arange(W) + 0.5) / W * 360.0 - 180.0)
    lat = np.radians(90.0 - (np.arange(H) + 0.5) / H * 180.0)
    LON, LAT = np.meshgrid(lon, lat)
    xyz = np.stack([np.cos(LAT) * np.cos(LON),
                    np.cos(LAT) * np.sin(LON), np.sin(LAT)])
    Rinv = _rot_matrix(REG_POLE_LAT, REG_POLE_LON, -REG_ANGLE * w)
    v = np.einsum('ij,jhw->ihw', Rinv, xyz)
    row = np.clip((90.0 - np.degrees(np.arcsin(np.clip(v[2], -1, 1)))) / 180.0 * H - 0.5, 0, H - 1)
    col = ((np.degrees(np.arctan2(v[1], v[0])) + 180.0) / 360.0 * W - 0.5) % W
    coords = np.stack([row.ravel(), col.ravel()])
    out = np.empty_like(img)
    for c in range(img.shape[2]):
        out[..., c] = map_coordinates(img[..., c], coords, order=1,
                                      mode='grid-wrap').reshape(H, W)
    return out


def render_boundary_layer(time_ma):
    """Plate boundaries (main-film style) on a transparent layer, as RGBA."""
    fig = plt.figure(figsize=(IMAGE_WIDTH / DPI, IMAGE_HEIGHT / DPI), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1], projection=ccrs.PlateCarree(central_longitude=0))
    ax.set_global()
    ax.set_axis_off()
    ax.patch.set_alpha(0.0)
    fig.patch.set_alpha(0.0)
    gplot.time = time_ma
    gplot.plot_ridges(ax, color=RIDGE_COLOR, linewidth=BOUNDARY_LW['ridges'])
    gplot.plot_transforms(ax, color=RIDGE_COLOR, linewidth=BOUNDARY_LW['transforms'], alpha=0.7)
    gplot.plot_trenches(ax, color=TRENCH_COLOR, linewidth=BOUNDARY_LW['trenches'])
    gplot.plot_subduction_teeth(ax, color=TRENCH_COLOR)
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba()).astype(np.float32)
    plt.close(fig)
    return buf


def render_member(time_ma, u, member):
    if u > 0 and member > 0:
        dt = member_time_unit(member) * TIME_SIGMA_MA * u
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

    reg_w = boundary_alpha(time_ma)   # registration rides the same ramp
    for rg in reconstructed:
        geom = rg.get_reconstructed_geometry()
        if geom is None:
            continue
        pid = rg.get_feature().get_reconstruction_plate_id()
        if reg_w > 0.0:
            reg = registration_rotation(pid, reg_w, geom.get_boundary_centroid())
            if reg is not None:
                geom = reg * geom
        if u > 0 and member > 0:
            if pid not in plate_rot:
                pole, angle_unit = member_plate_perturb(member, pid)
                angle = np.radians(angle_unit * POLE_SIGMA_DEG * u)
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


indices = list(range(0, T_START - T_END + 1))   # 0..800
n_rendered = n_skipped = n_out_of_range = n_repaired = 0
t0 = time.time()

for idx in indices:
    if (FRAME_START >= 0 and idx < FRAME_START) or \
       (FRAME_END >= 0 and idx > FRAME_END):
        n_out_of_range += 1
        continue
    out = os.path.join(OUT_DIR, f"prequel_frame_{idx:04d}.png")
    if os.path.exists(out):
        if png_complete(out):
            n_skipped += 1
            continue
        print(f"  ⚠ frame {idx}: TRUNCATED PNG on disk — re-rendering", flush=True)
        n_repaired += 1
    time_ma = T_START - idx
    u = u_ramp(time_ma)
    n = N_MEMBERS if u > 0 else 1
    acc = None
    for m in range(n):
        buf = render_member(time_ma, u, m)
        acc = buf if acc is None else acc + buf
    mean = acc / n
    b_alpha = boundary_alpha(time_ma)
    if b_alpha > 0.0:
        # Composite the crystallizing map over the averaged ensemble;
        # rotate the layer so boundaries track the registered continents
        layer = raster_rotate(render_boundary_layer(time_ma), b_alpha)
        a = (layer[..., 3:4] / 255.0) * b_alpha
        mean = mean * (1 - a) + layer[..., :3] * a
    Image.fromarray(mean.astype(np.uint8)).save(out)
    n_rendered += 1
    done = n_rendered
    rate = done / (time.time() - t0)
    remaining = sum(1 for j in indices
                    if not (FRAME_START >= 0 and j < FRAME_START)
                    and not (FRAME_END >= 0 and j > FRAME_END)) - done - n_skipped
    print(f"  ✓ [{idx:04d}] {time_ma} Ma (u={u:.2f}, {n} members) "
          f"— {rate * 3600:.0f} frames/h, ~{remaining / rate / 60:.0f} min left",
          flush=True)

elapsed = time.time() - t0
print(f"\n✓ Prequel texture pass complete in {elapsed / 60:.0f} min: "
      f"{n_rendered} rendered ({n_repaired} of those repaired truncations), "
      f"{n_skipped} already on disk, {n_out_of_range} outside frame range, "
      f"of {len(indices)} total → {OUT_DIR}")
if n_rendered + n_skipped + n_out_of_range != len(indices):
    print(f"⚠ Accounting mismatch — investigate before trusting this run.")
