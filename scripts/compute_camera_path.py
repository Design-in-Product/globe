#!/usr/bin/env python3
"""
Compute a smart camera path based on continental centroid tracking,
era-based overrides, smoothing, and variable pacing.

Outputs a JSON file with per-frame camera longitude/latitude and
frame timing (for variable pacing).

Pipeline:
  1. Compute continental centroid (center of mass of all land) at each timestep
  2. Apply Gaussian smoothing to prevent jerky camera motion
  3. Apply era-based overrides for key geological moments
  4. Compute variable pacing: slow on supercontinents, faster during dispersals
  5. Export camera_path.json for use by render_globe.py
"""

import os
import sys
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')

# ── Configuration ──────────────────────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data", "plate-models")
OUTPUT_PATH = os.path.join(PROJECT_ROOT, "camera_path.json")

TIME_START = 1000  # Ma
TIME_END = 0       # Ma
TIME_STEP = 1      # Ma

# Smoothing: sigma in units of frames (larger = smoother camera motion)
SMOOTH_SIGMA = 60  # ~60 Ma smoothing window (60 frames × 1 Ma = 60 Ma)

# ── Load plate model ──────────────────────────────────────────
print("Loading Merdith2021 plate model...")
from plate_model_manager import PlateModelManager
import gplately
import pygplates

pm_manager = PlateModelManager()
model_data = pm_manager.get_model("Merdith2021", data_dir=DATA_DIR)

rotation_model = model_data.get_rotation_model()
topology_features = model_data.get_topologies()
static_polygons = model_data.get_static_polygons()
continents_file = model_data.get_layer("ContinentalPolygons")

model = gplately.PlateReconstruction(
    rotation_model, topology_features, static_polygons
)
print("✓ Model loaded")

# ── Step 1: Compute largest-landmass centroid at each timestep ─
times = np.arange(TIME_START, TIME_END - 1, -TIME_STEP)
total_steps = len(times)

raw_lons = []
raw_lats = []
land_areas = []  # Total land area (used for dispersal metric)

# Adaptive clustering: escalate threshold until largest cluster covers enough land
CLUSTER_THRESHOLDS = [12, 18, 25]  # degrees on great circle, tried in order
MIN_CLUSTER_COVERAGE = 0.50         # stop escalating when largest cluster >= 50% of land

def haversine_deg(lat1, lon1, lat2, lon2):
    """Angular distance in degrees between two points on sphere."""
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
    return np.degrees(2 * np.arctan2(np.sqrt(a), np.sqrt(1-a)))

def find_root(parent, i):
    """Union-Find: find root with path compression."""
    while parent[i] != i:
        parent[i] = parent[parent[i]]
        i = parent[i]
    return i

def union(parent, rank, a, b):
    """Union-Find: merge two sets."""
    ra, rb = find_root(parent, a), find_root(parent, b)
    if ra == rb:
        return
    if rank[ra] < rank[rb]:
        ra, rb = rb, ra
    parent[rb] = ra
    if rank[ra] == rank[rb]:
        rank[ra] += 1

print(f"\nComputing largest-landmass centroids for {total_steps} timesteps...")
print(f"  Adaptive clustering thresholds: {CLUSTER_THRESHOLDS}° (min coverage: {MIN_CLUSTER_COVERAGE*100:.0f}%)")

for i, time_ma in enumerate(times):
    reconstructed = []
    pygplates.reconstruct(continents_file, rotation_model, reconstructed, time_ma)

    if not reconstructed:
        if raw_lons:
            raw_lons.append(raw_lons[-1])
            raw_lats.append(raw_lats[-1])
            land_areas.append(land_areas[-1])
        else:
            raw_lons.append(0.0)
            raw_lats.append(0.0)
            land_areas.append(0.0)
        continue

    # Extract polygon centroids and areas
    poly_data = []  # (lat, lon, area, cart_x, cart_y, cart_z)
    total_area = 0.0

    for rg in reconstructed:
        geom = rg.get_reconstructed_geometry()
        if geom is None:
            continue
        try:
            area = geom.get_area()
        except:
            area = 0.001
        if area <= 0:
            area = 0.001

        points = geom.to_lat_lon_list()
        if not points:
            continue

        clat = np.mean([p[0] for p in points])
        clon = np.mean([p[1] for p in points])
        clat_r, clon_r = np.radians(clat), np.radians(clon)

        poly_data.append({
            'lat': clat, 'lon': clon, 'area': area,
            'x': np.cos(clat_r) * np.cos(clon_r),
            'y': np.cos(clat_r) * np.sin(clon_r),
            'z': np.sin(clat_r),
        })
        total_area += area

    land_areas.append(total_area)

    if not poly_data:
        raw_lons.append(raw_lons[-1] if raw_lons else 0.0)
        raw_lats.append(raw_lats[-1] if raw_lats else 0.0)
        continue

    # Cluster polygons by proximity using Union-Find with adaptive threshold
    from collections import defaultdict
    n = len(poly_data)

    # Pre-compute pairwise distances (O(n^2) but n is typically < 500)
    pairwise_dist = {}
    for a_idx in range(n):
        for b_idx in range(a_idx + 1, n):
            pairwise_dist[(a_idx, b_idx)] = haversine_deg(
                poly_data[a_idx]['lat'], poly_data[a_idx]['lon'],
                poly_data[b_idx]['lat'], poly_data[b_idx]['lon']
            )

    best_cluster = None
    used_threshold = CLUSTER_THRESHOLDS[-1]

    for threshold in CLUSTER_THRESHOLDS:
        parent = list(range(n))
        rank_arr = [0] * n

        for (a_idx, b_idx), dist in pairwise_dist.items():
            if dist < threshold:
                union(parent, rank_arr, a_idx, b_idx)

        clusters = defaultdict(list)
        for idx in range(n):
            root = find_root(parent, idx)
            clusters[root].append(idx)

        candidate = max(clusters.values(),
                        key=lambda idxs: sum(poly_data[j]['area'] for j in idxs))
        candidate_area = sum(poly_data[j]['area'] for j in candidate)
        coverage = candidate_area / total_area if total_area > 0 else 0

        best_cluster = candidate
        used_threshold = threshold
        if coverage >= MIN_CLUSTER_COVERAGE:
            break  # Good enough coverage at this threshold

    # Compute area-weighted centroid of the largest cluster (in Cartesian)
    cx, cy, cz, carea = 0.0, 0.0, 0.0, 0.0
    for j in best_cluster:
        p = poly_data[j]
        cx += p['x'] * p['area']
        cy += p['y'] * p['area']
        cz += p['z'] * p['area']
        carea += p['area']

    cx /= carea
    cy /= carea
    cz /= carea

    centroid_lat = np.degrees(np.arctan2(cz, np.sqrt(cx**2 + cy**2)))
    centroid_lon = np.degrees(np.arctan2(cy, cx))

    raw_lons.append(centroid_lon)
    raw_lats.append(centroid_lat)

    if (i + 1) % 20 == 0 or i == 0:
        cluster_area_pct = carea / total_area * 100 if total_area > 0 else 0
        print(f"  [{i+1:3d}/{total_steps}] {int(time_ma):4d} Ma  "
              f"largest landmass: ({centroid_lat:+6.1f}°, {centroid_lon:+7.1f}°) "
              f"[{len(best_cluster)} polys, {cluster_area_pct:.0f}% of land, thresh={used_threshold}°]")

raw_lons = np.array(raw_lons)
raw_lats = np.array(raw_lats)
land_areas = np.array(land_areas)

print(f"✓ Largest-landmass centroids computed")

# ── Step 2: Compute dispersal metric ─────────────────────────
# Higher dispersal = continents spread out = faster camera movement appropriate
# Use the "spread" of continental positions relative to centroid
# This is measured by the standard deviation of polygon centroids
print("\nComputing dispersal metric...")

dispersal = np.zeros(total_steps)

for i, time_ma in enumerate(times):
    reconstructed = []
    pygplates.reconstruct(continents_file, rotation_model, reconstructed, time_ma)

    if not reconstructed:
        dispersal[i] = dispersal[max(0, i-1)]
        continue

    # Compute angular distance of each polygon centroid from the global centroid
    dists = []
    for rg in reconstructed:
        geom = rg.get_reconstructed_geometry()
        if geom is None:
            continue
        points = geom.to_lat_lon_list()
        if not points:
            continue
        plat = np.radians(np.mean([p[0] for p in points]))
        plon = np.radians(np.mean([p[1] for p in points]))
        clat = np.radians(raw_lats[i])
        clon = np.radians(raw_lons[i])

        # Haversine angular distance
        dlat = plat - clat
        dlon = plon - clon
        a = np.sin(dlat/2)**2 + np.cos(clat)*np.cos(plat)*np.sin(dlon/2)**2
        dist = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
        try:
            area = geom.get_area()
        except:
            area = 0.001
        dists.append(dist * max(area, 0.001))

    if dists:
        dispersal[i] = np.sum(dists) / max(land_areas[i], 0.001)
    else:
        dispersal[i] = dispersal[max(0, i-1)]

# Normalize dispersal to 0-1
d_min, d_max = dispersal.min(), dispersal.max()
if d_max > d_min:
    dispersal_norm = (dispersal - d_min) / (d_max - d_min)
else:
    dispersal_norm = np.zeros_like(dispersal)

print(f"✓ Dispersal metric computed (min={d_min:.4f}, max={d_max:.4f})")

# ── Step 3: Era-based overrides ───────────────────────────────
# Define key geological eras with known camera targets
# These override the computed centroid to ensure we're looking at the right thing
print("\nApplying era-based overrides...")

ERA_OVERRIDES = [
    # (time_ma, target_lon, target_lat, label, weight)
    # weight: 0 = use computed centroid, 1 = fully override to target
    (1000, None, None, "Rodinia assembling", 0.0),        # Trust centroid
    (900,  None, None, "Rodinia assembled", 0.0),          # Trust centroid
    (750,  None, None, "Rodinia breaking up", 0.0),        # Trust centroid
    (550,  100, -45, "Gondwana assembling", 0.5),          # Guide toward Gondwana core
    (480,  120, -50, "Gondwana assembled", 0.5),           # Center on Australia/India cluster
    (380,    5, -15, "Laurussia forming", 0.4),            # Northern continents merge
    (350,    0, -10, "Pangaea assembling", 0.5),           # Drift to Pangaea center
    (300,    0,  10, "Pangaea coalescing", 0.6),           # Center on Pangaea
    (250,    0,  10, "Pangaea assembled", 0.7),            # Pangaea fully formed
    (200,   20,  15, "Pangaea breaking up", 0.5),          # Central Atlantic opens
    (150,   20,  10, "Atlantic Ocean opening", 0.3),       # Indian Ocean opens too
    (100,   10,  10, "India racing north", 0.2),           # Let centroid lead
    (66,     0,  10, "K-Pg extinction", 0.2),              # Brief geological moment
    (50,     0,  20, "Modern world forming", 0.1),         # Trust centroid
    (0,     15,  25, "Present day", 0.4),                  # Centered on Europe/Africa
]

# Interpolate era overrides to each timestep
from scipy.interpolate import interp1d

era_times = [e[0] for e in ERA_OVERRIDES]
era_weights = [e[4] for e in ERA_OVERRIDES]

# For overrides with None (trust centroid), use the computed centroid
era_lons = []
era_lats = []
for e in ERA_OVERRIDES:
    t_idx = int((TIME_START - e[0]) / TIME_STEP)
    t_idx = max(0, min(t_idx, total_steps - 1))
    era_lons.append(e[1] if e[1] is not None else raw_lons[t_idx])
    era_lats.append(e[2] if e[2] is not None else raw_lats[t_idx])

# Interpolate to all timesteps (reversing because eras go 1000→0 but we want monotonic)
weight_interp = interp1d(era_times[::-1], era_weights[::-1],
                         kind='linear', fill_value='extrapolate')
lon_interp = interp1d(era_times[::-1], era_lons[::-1],
                      kind='linear', fill_value='extrapolate')
lat_interp = interp1d(era_times[::-1], era_lats[::-1],
                      kind='linear', fill_value='extrapolate')

override_weights = weight_interp(times[::-1])[::-1]
override_lons = lon_interp(times[::-1])[::-1]
override_lats = lat_interp(times[::-1])[::-1]

# Blend computed centroid with era overrides
blended_lons = raw_lons * (1 - override_weights) + override_lons * override_weights
blended_lats = raw_lats * (1 - override_weights) + override_lats * override_weights

print(f"✓ Era overrides applied ({len(ERA_OVERRIDES)} keyframes)")

# ── Step 4: Gaussian smoothing ────────────────────────────────
# Smooth the camera path so it doesn't jerk around
from scipy.ndimage import gaussian_filter1d

# Handle longitude wrapping: smooth in Cartesian then convert back
lons_rad = np.radians(blended_lons)
lats_rad = np.radians(blended_lats)

# Convert to Cartesian
cart_x = np.cos(lats_rad) * np.cos(lons_rad)
cart_y = np.cos(lats_rad) * np.sin(lons_rad)
cart_z = np.sin(lats_rad)

# Smooth in Cartesian space
smooth_x = gaussian_filter1d(cart_x, sigma=SMOOTH_SIGMA)
smooth_y = gaussian_filter1d(cart_y, sigma=SMOOTH_SIGMA)
smooth_z = gaussian_filter1d(cart_z, sigma=SMOOTH_SIGMA)

# Convert back to lat/lon
smooth_lats = np.degrees(np.arctan2(smooth_z, np.sqrt(smooth_x**2 + smooth_y**2)))
smooth_lons = np.degrees(np.arctan2(smooth_y, smooth_x))

print(f"✓ Gaussian smoothing applied (σ={SMOOTH_SIGMA} frames = {SMOOTH_SIGMA * TIME_STEP} Ma)")

# ── Step 5: Variable pacing ──────────────────────────────────
# Supercontinents (low dispersal) → more frames (slower)
# Dispersal phases (high dispersal) → fewer frames (faster)
print("\nComputing variable pacing...")

# Smooth the dispersal metric too
smooth_dispersal = gaussian_filter1d(dispersal_norm, sigma=SMOOTH_SIGMA)

# Frame duration multiplier: low dispersal → longer, high dispersal → shorter
# Targeting ~45-60s total video duration
MIN_SPEED = 1.0   # Fastest: 1 frame per timestep (during max dispersal)
MAX_SPEED = 3.0   # Slowest: 3 frames per timestep (during supercontinents)

frame_duration = MIN_SPEED + (MAX_SPEED - MIN_SPEED) * (1.0 - smooth_dispersal)

# Also add extra hold time at key supercontinents
SUPERCONTINENT_HOLD = [
    # (time_ma, extra_hold_frames, label)
    (900, 48, "Rodinia peak"),       # 2s pause at Rodinia
    (480, 36, "Gondwana peak"),     # 1.5s pause at Gondwana
    (250, 60, "Pangaea peak"),      # 2.5s pause at Pangaea
    (0, 60, "Present day"),         # 2.5s pause at present
]

# Convert to frame indices and add hold
hold_frames = {}
for sc_time, extra, label in SUPERCONTINENT_HOLD:
    idx = int((TIME_START - sc_time) / TIME_STEP)
    idx = max(0, min(idx, total_steps - 1))
    hold_frames[idx] = (extra, label)
    print(f"  Hold at {sc_time} Ma ({label}): +{extra} frames")

# Build a lookup: time_ma → era label (for overlay text)
def get_era_label(time_ma):
    """Return the era label for a given time."""
    # Find the era whose time is closest without going past
    best = ERA_OVERRIDES[0]
    for e in ERA_OVERRIDES:
        if e[0] >= time_ma:
            best = e
    return best[3]

# Build final frame mapping
# Each geological timestep maps to a variable number of animation frames
output_frames = []
anim_frame = 0

for i in range(total_steps):
    time_ma = float(times[i])
    era_label = get_era_label(time_ma)

    # Base frame(s) for this timestep
    n_frames = max(1, int(round(frame_duration[i])))
    for sub in range(n_frames):
        # Interpolate position within this timestep if multiple frames
        t = sub / n_frames if n_frames > 1 else 0
        if i < total_steps - 1:
            interp_lon = smooth_lons[i] * (1 - t) + smooth_lons[i + 1] * t
            interp_lat = smooth_lats[i] * (1 - t) + smooth_lats[i + 1] * t
        else:
            interp_lon = smooth_lons[i]
            interp_lat = smooth_lats[i]

        output_frames.append({
            "anim_frame": anim_frame,
            "time_ma": time_ma,
            "geo_frame_idx": i,  # Index into globe_frame_NNNN.png
            "camera_lon": float(interp_lon),
            "camera_lat": float(interp_lat),
            "dispersal": float(smooth_dispersal[i]),
            "era_label": era_label,
        })
        anim_frame += 1

    # Add hold frames at supercontinents
    if i in hold_frames:
        extra, label = hold_frames[i]
        for h in range(extra):
            output_frames.append({
                "anim_frame": anim_frame,
                "time_ma": time_ma,
                "geo_frame_idx": i,
                "camera_lon": float(smooth_lons[i]),
                "camera_lat": float(smooth_lats[i]),
                "dispersal": float(smooth_dispersal[i]),
                "era_label": era_label,
            })
            anim_frame += 1

total_anim_frames = len(output_frames)
print(f"\n✓ Variable pacing computed:")
print(f"  Geological timesteps: {total_steps}")
print(f"  Animation frames: {total_anim_frames}")
print(f"  Duration at 24fps: {total_anim_frames / 24:.1f}s")
print(f"  Duration at 30fps: {total_anim_frames / 30:.1f}s")

# ── Step 6: Export ────────────────────────────────────────────
camera_path = {
    "metadata": {
        "time_range": f"{TIME_START} Ma to {TIME_END} Ma",
        "time_step": TIME_STEP,
        "geological_timesteps": total_steps,
        "animation_frames": total_anim_frames,
        "smooth_sigma": SMOOTH_SIGMA,
        "pacing": f"variable ({MIN_SPEED}x to {MAX_SPEED}x)",
    },
    "eras": [
        {"time_ma": e[0], "label": e[3]} for e in ERA_OVERRIDES
    ],
    "frames": output_frames,
}

with open(OUTPUT_PATH, 'w') as f:
    json.dump(camera_path, f, indent=2)

print(f"\n✓ Camera path exported to: {OUTPUT_PATH}")
print(f"  File size: {os.path.getsize(OUTPUT_PATH) / 1024:.0f} KB")

# ── Summary ───────────────────────────────────────────────────
print(f"\n{'='*60}")
print(f"CAMERA PATH SUMMARY")
print(f"{'='*60}")
print(f"  Start: {times[0]:.0f} Ma → camera at ({smooth_lats[0]:+.1f}°, {smooth_lons[0]:+.1f}°)")
print(f"  End:   {times[-1]:.0f} Ma → camera at ({smooth_lats[-1]:+.1f}°, {smooth_lons[-1]:+.1f}°)")
print(f"  Total animation frames: {total_anim_frames}")
print(f"  Key moments:")
for sc_time, extra, label in SUPERCONTINENT_HOLD:
    idx = int((TIME_START - sc_time) / TIME_STEP)
    idx = max(0, min(idx, total_steps - 1))
    print(f"    {sc_time:4d} Ma ({label}): camera at "
          f"({smooth_lats[idx]:+.1f}°, {smooth_lons[idx]:+.1f}°), "
          f"dispersal={smooth_dispersal[idx]:.2f}")
