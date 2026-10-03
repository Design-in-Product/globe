#!/usr/bin/env python3
"""Rung 5, step 2: camera/timing path for the sequel globe pass.

Reads the texture sidecar (~/globe-render/sequel_frames/sequel_frames.json)
written by generate_sequel_frames.py — the sequence has one owner — and
emits sequel_camera_path.json in the shape render_globe.py and
assemble_globe.py already consume (frames[] of anim_frame/time_ma/
geo_frame_idx/camera_lon/camera_lat/dispersal/era_label; metadata with
time_range/pacing — the keys whose absence KeyError'd the prequel launch).

PACING (plan §6c): anim-frames-per-geo-frame is not constant across the
divergence. Slow at both ends, where dispersal and assembly happen; brisk
through the quiet middle. rate(u) = 1 - 0.22*cos(2*pi*u), so a geo frame
near either end gets ~3.1 anim frames and the middle ~2.0 (base TEMPO 2.4).
Accumulated as a float so rounding never drifts.

HOLDS: departure at present (matches the main film's hold length), the
terminal superposition, each tour stop, and the final cloud. Tour blends
get BLEND_ANIM frames each so the 8-frame texture dissolve lasts ~2 s and
the camera has time to travel.

CAMERA: the first frame's camera is the MAIN FILM'S LAST — read from
camera_path_spin_v8.json, not typed in — so the sequel opens where the
story left off (the prequel's seam trick, mirrored). The divergence drifts
gently west. Each tour stop aims at its scenario's land-centroid
longitude from the sidecar (re-centring as a camera move), reached along
the shortest arc so a 180-degree swing never goes the long way round.
Everything between keys is PCHIP with duplicate keys pinning the holds.

time_ma is stored NEGATIVE for the future; assemble_globe.time_label
renders it "+N Myr".
"""
import json
import os
import sys

import numpy as np
from scipy.interpolate import PchipInterpolator

SIDE = os.path.expanduser(os.environ.get("SEQUEL_SIDECAR", "~/globe-render/sequel_frames/sequel_frames.json"))
MAIN_PATH = "camera_path_spin_v8.json"
OUT = "sequel_camera_path.json"
FPS = 24
TEMPO = 2.4            # base anim frames per divergence geo frame
HOLD = 132             # 5.5 s, the film's established hold length
TOUR_HOLD = 60         # 2.5 s per scenario alone
BLEND_ANIM = 6         # anim frames per blend geo frame -> 8 blends = 48 f = 2 s
DRIFT_LON = -60.0      # gentle westward drift across the divergence
TOUR_LAT = 10.0


def rate(u):
    return 1.0 - 0.22 * np.cos(2 * np.pi * u)


def shortest_arc(prev_lon, target_lon):
    """Unwrap target so the move from prev is the short way round."""
    d = (target_lon - prev_lon + 180.0) % 360.0 - 180.0
    return prev_lon + d


def main():
    side = json.load(open(SIDE))
    geo = side["frames"]
    n_div = sum(1 for f in geo if f["kind"] == "divergence")
    main_last = json.load(open(MAIN_PATH))["frames"][-1]
    lon0, lat0 = main_last["camera_lon"], main_last["camera_lat"]

    # ---- anim frames per geo frame
    per = []
    acc = 0.0
    for f in geo:
        k = f["kind"]
        if k == "divergence":
            u = f["geo_frame_idx"] / (n_div - 1)
            acc += TEMPO / rate(u)
            n = int(acc); acc -= n
            if f["geo_frame_idx"] in (0, n_div - 1):
                n += HOLD
        elif k in ("tour_blend", "return_blend"):
            n = BLEND_ANIM
        elif k == "tour_hold":
            n = TOUR_HOLD
        elif k == "final_hold":
            n = HOLD
        else:
            raise ValueError(k)
        per.append(max(1, n))

    # ---- camera keys: (anim_index, lon, lat), with duplicates pinning holds
    starts = np.cumsum([0] + per[:-1])
    keys = []
    def key(a, lon, lat): keys.append((int(a), float(lon), float(lat)))
    # departure hold: pinned to the main film's last camera
    key(starts[0], lon0, lat0); key(starts[0] + HOLD - 1, lon0, lat0)
    # divergence drift
    key(starts[n_div - 1], lon0 + DRIFT_LON, lat0 * 0.6 + TOUR_LAT * 0.4)
    key(starts[n_div - 1] + HOLD - 1, lon0 + DRIFT_LON, lat0 * 0.6 + TOUR_LAT * 0.4)
    prev_lon = lon0 + DRIFT_LON
    for f, s, n in zip(geo, starts, per):
        if f["kind"] == "tour_hold":
            lon = shortest_arc(prev_lon, f["centroid_lon"])
            key(s, lon, TOUR_LAT); key(s + n - 1, lon, TOUR_LAT)
            prev_lon = lon
        elif f["kind"] == "final_hold":
            key(s, prev_lon, TOUR_LAT); key(s + n - 1, prev_lon, TOUR_LAT)
    ka = np.array([k[0] for k in keys], float)
    # PCHIP needs strictly increasing x: nudge any exact duplicates by epsilon
    for i in range(1, len(ka)):
        if ka[i] <= ka[i - 1]:
            ka[i] = ka[i - 1] + 1e-6
    lon_i = PchipInterpolator(ka, [k[1] for k in keys])
    lat_i = PchipInterpolator(ka, [k[2] for k in keys])

    # ---- emit frames
    frames = []
    a = 0
    for f, n in zip(geo, per):
        t_ma = -float(f["time_myr"]) if f["kind"] != "divergence" or f["time_myr"] > 0 else 0.0
        era = f["label"] if f["kind"] != "divergence" else "four futures, superposed"
        for _ in range(n):
            lon = float(lon_i(a)); lon = (lon + 180.0) % 360.0 - 180.0
            frames.append({"anim_frame": a, "time_ma": t_ma, "geo_frame_idx": f["geo_frame_idx"],
                           "camera_lon": lon, "camera_lat": float(lat_i(a)),
                           "dispersal": 0.0, "era_label": era})
            a += 1

    out = {
        "metadata": {
            "description": "Future sequel: present -> +200 Myr superposed, then the tour, then back",
            "time_range": "0 Ma to +200 Myr (tour stops to +250)",
            "time_step": 1, "geological_timesteps": len(geo),
            "animation_frames": len(frames), "anim_frames": len(frames), "fps": FPS,
            "duration_sec": round(len(frames) / FPS, 1),
            "pacing": f"eased (rate 1-0.22cos2piu, base {TEMPO}), holds {HOLD}/{TOUR_HOLD}, blends {BLEND_ANIM}/geo",
            "opening_camera_from": MAIN_PATH,
        },
        "eras": [{"time_ma": 0, "label": "Present day"},
                 {"time_ma": -200, "label": "four futures, superposed"}] +
                [{"time_ma": -v["terminus"], "label": v["name"]} for v in side["scenarios"].values()],
        "frames": frames,
    }
    json.dump(out, open(OUT, "w"), indent=1)

    # ---- verification, printed so the log can quote it
    geos = [fr["geo_frame_idx"] for fr in frames]
    assert geos == sorted(geos), "geo index not monotone"
    assert set(geos) == set(range(len(geo))), "some geo frame never referenced"
    lons = np.array([fr["camera_lon"] for fr in frames])
    dl = np.abs((np.diff(lons) + 180) % 360 - 180)
    holds = [(f["label"], s, n) for f, s, n in zip(geo, starts, per) if f["kind"] in ("tour_hold", "final_hold")]
    print(f"anim frames {len(frames)} = {len(frames)/FPS:.1f}s @ {FPS}fps; geo frames {len(geo)}; "
          f"divergence anim {sum(per[:n_div])} (incl. 2 holds)")
    print(f"opening camera = main film's last: lon {lon0:.2f} lat {lat0:.2f}; "
          f"frame0 lon {frames[0]['camera_lon']:.2f} lat {frames[0]['camera_lat']:.2f}")
    for label, s, n in holds:
        seg = lons[s:s + n]; print(f"  hold {label:<28} frames {s}-{s+n-1}  lon spread {np.ptp(seg):.3f}")
    print(f"max per-frame lon step {dl.max():.2f} deg (at frame {int(dl.argmax())})")


if __name__ == "__main__":
    main()
