#!/usr/bin/env python3
"""Camera/timing path for the prequel film (1800 -> 1000 Ma).

Schema-compatible with camera_path.json so render_flat.py (and later the
Blender pass) consume it unchanged. Decisions encoded (xian, 7/29):
tempo-matched to the main film (~2.4 anim frames per 1 Ma geo frame),
static holds (no spins) at Nuna 1452 Ma and the 1000 Ma Rodinia
convergence, ICS Proterozoic period labels.

Usage: python3 scripts/compute_prequel_path.py   -> prequel_camera_path.json
"""

import json

T_START, T_END = 1800, 1000
TEMPO = 2.4          # anim frames per geo frame ≈ main film's average
HOLD_FRAMES = 132    # matches the v8 hold length (5.5 s at 24 fps)
FPS = 24

HOLDS = {
    348: "Nuna/Columbia assembled",   # 1452 Ma (xian's pick)
    800: "Rodinia assembling",        # 1000 Ma — convergence into the main film
}

PERIODS = [  # ICS Proterozoic periods covering the span
    (1800, 1600, "Statherian Period"),
    (1600, 1400, "Calymmian Period"),
    (1400, 1200, "Ectasian Period"),
    (1200, 1000, "Stenian Period"),
]


def era_label(time_ma, geo_idx):
    if geo_idx in HOLDS:
        return HOLDS[geo_idx]
    for hi, lo, name in PERIODS:
        if lo < time_ma <= hi:
            return name
    return PERIODS[-1][2]


# Camera track (hand-framed, Tessera 2026-08-09; xian delegated the framing).
# Keys are (geo_idx, lon, lat); lon unwrapped westward so the sweep crosses
# the antimeridian WITH the migrating landmass (mass stays near lon -110
# through ~1250 Ma, then crosses to +115-ish by 1100 — verified against the
# full-span draft frames). Terminal camera = v8's opening exactly, so the
# globe prequel hands into the main globe film's first shot.
# Hold cameras are pinned constant by duplicate keys at hold start/end.
CAM_KEYS = [
    (0,   -110.0, 10.0),                       # 1800 Ma — early cluster
    (348, -120.0, 15.0),                       # Nuna hold (hand-framed)
    (548, -115.0, 10.0),                       # 1252 Ma — mass still west
    (700, -240.0, -8.0),                       # 1100 Ma — crossed with the mass
    (800, 115.054649 - 360.0, -12.341535),     # 1000 Ma — v8 opening, exact
]


frames = []
anim = 0
geo_anim_range = {}   # geo_idx -> (first_anim, last_anim)
for geo_idx in range(T_START - T_END + 1):          # 0..800
    time_ma = float(T_START - geo_idx)
    # Tempo-matched repeat count (2/3 alternation averaging TEMPO) …
    n = int((geo_idx + 1) * TEMPO) - int(geo_idx * TEMPO)
    # … plus a static hold extension at the hold frames.
    if geo_idx in HOLDS:
        n += HOLD_FRAMES
    geo_anim_range[geo_idx] = (anim, anim + n - 1)
    for _ in range(n):
        frames.append({
            "anim_frame": anim,
            "time_ma": time_ma,
            "geo_frame_idx": geo_idx,
            "camera_lon": 0.0,   # filled below from CAM_KEYS
            "camera_lat": 0.0,
            "dispersal": 0.0,
            "era_label": era_label(time_ma, geo_idx),
        })
        anim += 1

# ── Camera interpolation over ANIM frames (smooth, holds pinned) ──
from scipy.interpolate import PchipInterpolator

knots, lons, lats = [], [], []
for geo_idx, lon, lat in CAM_KEYS:
    first, last = geo_anim_range[geo_idx]
    knots.append(first); lons.append(lon); lats.append(lat)
    if geo_idx in HOLDS or geo_idx == T_START - T_END:
        # duplicate key at hold/film end pins the camera through it
        knots.append(last); lons.append(lon); lats.append(lat)
lon_f = PchipInterpolator(knots, lons)
lat_f = PchipInterpolator(knots, lats)
for f in frames:
    a = min(max(f["anim_frame"], knots[0]), knots[-1])
    f["camera_lon"] = ((float(lon_f(a)) + 180.0) % 360.0) - 180.0  # rewrap
    f["camera_lat"] = float(lat_f(a))

path = {
    "metadata": {
        "description": "Prequel 1800->1000 Ma, tempo-matched, static holds "
                       "at Nuna 1452 Ma and the 1000 Ma convergence",
        # keys render_globe.py prints at startup
        "time_range": "1800 Ma to 1000 Ma",
        "pacing": "tempo-matched (2.4x) + static 132f holds",
        "geo_frames": T_START - T_END + 1,
        "anim_frames": len(frames),
        "fps": FPS,
        "duration_sec": round(len(frames) / FPS, 1),
    },
    "eras": [{"start_ma": hi, "end_ma": lo, "label": name}
             for hi, lo, name in PERIODS],
    "frames": frames,
}

out = "prequel_camera_path.json"
with open(out, "w") as f:
    json.dump(path, f)
print(f"✓ {out}: {len(frames)} anim frames "
      f"({len(frames) / FPS:.1f} s at {FPS} fps), "
      f"{path['metadata']['geo_frames']} geo frames, "
      f"holds at {sorted(HOLDS)} (+{HOLD_FRAMES}f each)")
