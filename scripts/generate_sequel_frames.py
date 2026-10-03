#!/usr/bin/env python3
"""Rung 5, step 1: production textures for the future sequel's globe pass.

xian: "rung 5, sure!" (2026-10-02). Produces clean 2048x1024 equirect
textures — no text, the film palette — one per GEO FRAME, named
sequel_frame_NNNN.png so render_globe.py picks them up via
FRAMES_DIR/FRAME_PREFIX exactly as it did the prequel's.

GEO-FRAME SEQUENCE (what the camera path will pace and hold):
  divergence   0 -> +200 Myr at 1 Myr per geo frame (201 frames), each a
               crossfade of the bracketing OSF 20 Myr snapshots, four
               scenarios superposed. Pacing (eased per plan §6c) belongs
               to the camera path, not here — textures are uniform in time.
  tour         for each scenario: BLEND frames dissolving the cloud into
               the scenario alone (so the Blender pass's 2-frame crossfade
               becomes a real dissolve), then one HOLD frame the path
               holds. Re-centring is NOT done to the texture: on a globe
               it is a camera move, so each tour frame records the
               scenario's land-centroid longitude for the path to aim at.
  return       BLEND frames from the last scenario back to the cloud, then
               a final HOLD on the superposition.

A sidecar sequel_frames.json describes every geo frame (kind, time,
scenario, label, centroid lon) so compute_sequel_path.py reads the
structure instead of re-deriving it — one owner for the sequence.

Superposition covers 0..200 only (all four exist); each scenario tours at
its own terminus (pun/aurn +250, novon/amn +200). Honest accounting at the
end; exits non-zero if the set is incomplete.

Env: SEQUEL_OUT (default ~/globe-render/sequel_frames).
"""
import json
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from read_future_grids import SCENARIOS, available_times, grid_path, read_grid  # noqa: E402

OUT = os.path.expanduser(os.environ.get("SEQUEL_OUT", "~/globe-render/sequel_frames"))
PREFIX = "sequel_frame_"
SIZE = (2048, 1024)
OCEAN = np.array([0x1a, 0x42, 0x5a], dtype=np.float32)
CONTINENT = np.array([0xa0, 0x7c, 0x5a], dtype=np.float32)
SUPER_END = 200
BLEND_FRAMES = 8          # geo frames per dissolve; the path gives each ~2-3 anim frames


def grid_mask(s, t):
    return np.asarray(read_grid(grid_path(s, t))["mask"], dtype=np.float32).T[::-1]


def to_image(m):
    img = OCEAN[None, None, :] + (CONTINENT - OCEAN)[None, None, :] * m[..., None]
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).resize(SIZE, Image.BILINEAR)


def _unit_vectors(m):
    """Area-weighted unit vectors of land cells, on a coarse grid (speed)."""
    h, w = m.shape
    mm = m[::4, ::4]                                   # 1440x721 -> ~360x181
    lat = np.deg2rad(np.linspace(90, -90, mm.shape[0]))[:, None]
    lon = np.deg2rad(np.linspace(-180, 180, mm.shape[1]))[None, :]
    wgt = (mm * np.cos(lat)).ravel()
    x = (np.cos(lat) * np.cos(lon)).ravel(); y = (np.cos(lat) * np.sin(lon)).ravel(); z = np.broadcast_to(np.sin(lat), mm.shape).ravel()
    keep = wgt > 0
    return np.stack([x[keep], y[keep], z[keep]], 1), wgt[keep]


def aim_points(m):
    """Two candidate camera targets for a tour stop, both (lat, lon) in degrees.

    centroid   — the land centroid. For a RING supercontinent (Pangaea Ultima)
                 this sits in the inland sea: the camera stares into the hole.
    most_land  — the hemisphere centre that sees the most land area
                 (sum of area-weighted dot products clipped at 0, searched on a
                 5-degree grid). For a compact mass this ~= the centroid; for a
                 ring it moves onto the ring. xian (10-03): aim Ultima here,
                 "perhaps at a locus nearer to the sea" — the path script blends
                 toward the centroid by a per-scenario sea bias.
    """
    U, wgt = _unit_vectors(m)
    c = (U * wgt[:, None]).sum(0); c /= np.linalg.norm(c)
    centroid = (float(np.degrees(np.arcsin(c[2]))), float(np.degrees(np.arctan2(c[1], c[0]))))
    best, best_pt, ring_best, ring_pt = -1.0, None, -1.0, None
    for lat in range(-60, 61, 5):
        for lon in range(-180, 180, 5):
            la, lo = np.deg2rad(lat), np.deg2rad(lon)
            v = np.array([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)])
            vis = (wgt * np.clip(U @ v, 0, None)).sum()
            if vis > best:
                best, best_pt = vis, (float(lat), float(lon))
            # ring_side: best view at least 35 deg away from the centroid. For a
            # ring the unconstrained optimum IS the centroid (measured 10-03:
            # Ultima's most_land == centroid), so this is the view that sits on
            # the ring with the sea entering from one side.
            if np.degrees(np.arccos(np.clip(v @ c, -1, 1))) >= 35.0 and vis > ring_best:
                ring_best, ring_pt = vis, (float(lat), float(lon))
    return {"centroid": centroid, "most_land": best_pt, "ring_side": ring_pt}


def centroid_lon_deg(m):
    return aim_points(m)["centroid"][1]


def main():
    os.makedirs(OUT, exist_ok=True)
    times = sorted(set.intersection(*[set(available_times(s)) for s in SCENARIOS]))
    masks = {t: np.stack([grid_mask(s, t) for s in SCENARIOS]) for t in times if t <= SUPER_END}
    term = {s: grid_mask(s, max(available_times(s))) for s in SCENARIOS}
    termini = {s: max(available_times(s)) for s in SCENARIOS}

    frames = []   # sidecar entries, in geo order

    def emit(m, **meta):
        idx = len(frames)
        to_image(m).save(os.path.join(OUT, f"{PREFIX}{idx:04d}.png"))
        frames.append({"geo_frame_idx": idx, **meta})
        return idx

    # ---- divergence: 0..200 Myr, 1 Myr per geo frame, crossfaded between snapshots
    for t in range(0, SUPER_END + 1):
        lo = max(x for x in masks if x <= t); hi = min(x for x in masks if x >= t)
        f = 0.0 if hi == lo else (t - lo) / (hi - lo)
        cloud = (masks[lo] * (1 - f) + masks[hi] * f).mean(0)
        emit(cloud, kind="divergence", time_myr=t, label=f"+{t} Myr", scenario=None,
             centroid_lon=None)
    end_cloud = masks[SUPER_END].mean(0)

    # ---- tour: dissolve cloud -> scenario, then a hold frame; camera aims at the centroid
    prev = end_cloud
    for s, name in SCENARIOS.items():
        alone = term[s]; aim = aim_points(alone); lon = aim["centroid"][1]
        for i in range(1, BLEND_FRAMES + 1):
            f = i / (BLEND_FRAMES + 1)
            emit(prev * (1 - f) + alone * f, kind="tour_blend", time_myr=termini[s],
                 label=name, scenario=s, centroid_lon=lon, aim=aim)
        emit(alone, kind="tour_hold", time_myr=termini[s], label=name, scenario=s, centroid_lon=lon, aim=aim)
        prev = alone

    # ---- return to the cloud, final hold
    for i in range(1, BLEND_FRAMES + 1):
        f = i / (BLEND_FRAMES + 1)
        emit(prev * (1 - f) + end_cloud * f, kind="return_blend", time_myr=SUPER_END,
             label="four futures, superposed", scenario=None, centroid_lon=None)
    emit(end_cloud, kind="final_hold", time_myr=SUPER_END, label="four futures, superposed",
         scenario=None, centroid_lon=None)

    side = {"prefix": PREFIX, "size": SIZE, "super_end": SUPER_END, "blend_frames": BLEND_FRAMES,
            "scenarios": {s: {"name": n, "terminus": termini[s]} for s, n in SCENARIOS.items()},
            "frames": frames}
    with open(os.path.join(OUT, "sequel_frames.json"), "w") as f:
        json.dump(side, f, indent=1)

    # honest accounting
    expected = (SUPER_END + 1) + len(SCENARIOS) * (BLEND_FRAMES + 1) + BLEND_FRAMES + 1
    on_disk = len([f for f in os.listdir(OUT) if f.startswith(PREFIX) and f.endswith(".png")])
    kinds = {}
    for fr in frames:
        kinds[fr["kind"]] = kinds.get(fr["kind"], 0) + 1
    print(f"geo frames: {len(frames)} emitted, {on_disk} on disk, {expected} expected  {kinds}")
    for s in SCENARIOS:
        a = aim_points(term[s])
        print(f"  aim {s:<6} centroid (lat,lon) {tuple(round(v,1) for v in a['centroid'])}  "
              f"most-land hemisphere {tuple(round(v,1) for v in a['most_land'])}")
    if not (len(frames) == on_disk == expected):
        print("INCOMPLETE"); sys.exit(1)


if __name__ == "__main__":
    main()
