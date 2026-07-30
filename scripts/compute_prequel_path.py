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


frames = []
anim = 0
for geo_idx in range(T_START - T_END + 1):          # 0..800
    time_ma = float(T_START - geo_idx)
    # Tempo-matched repeat count (2/3 alternation averaging TEMPO) …
    n = int((geo_idx + 1) * TEMPO) - int(geo_idx * TEMPO)
    # … plus a static hold extension at the hold frames.
    if geo_idx in HOLDS:
        n += HOLD_FRAMES
    for _ in range(n):
        frames.append({
            "anim_frame": anim,
            "time_ma": time_ma,
            "geo_frame_idx": geo_idx,
            "camera_lon": 0.0,   # flat film; globe pass hand-frames holds later
            "camera_lat": 0.0,
            "dispersal": 0.0,
            "era_label": era_label(time_ma, geo_idx),
        })
        anim += 1

path = {
    "metadata": {
        "description": "Prequel 1800->1000 Ma, tempo-matched, static holds "
                       "at Nuna 1452 Ma and the 1000 Ma convergence",
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
