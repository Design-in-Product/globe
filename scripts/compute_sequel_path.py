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
TOUR_HOLD = 84         # 3.5 s per scenario alone (xian 10-03: a slower tour)
DEG_PER_FRAME = 1.2    # tour moves pace by distance (xian 10-03: slower); a big swing ~6-7 s, a hop ~2 s
BLEND_MIN, BLEND_MAX = 48, 168   # anim frames per 8-frame dissolve (2 s .. 7 s)
SEA_BIAS = {"pun": float(os.environ.get("PUN_SEA_BIAS", "1.0"))}           # fraction from the most-land point toward the centroid (the sea); xian 10-06: centroid
# Slow pan during a tour hold: (degrees of view longitude, anim frames), after the
# static hold. xian 10-06 on Ultima: "rotate the globe in a slow pan so people get
# the feel for it ... I assume the other side is almost all ocean" — measured: the
# antipodal hemisphere at +250 is 0.5% land, so a half-turn westward lands on the
# world ocean. 180 deg over 288 f = 0.63 deg/f, half the tour's move pace.
PAN = {"pun": (float(os.environ.get("PUN_PAN_DEG", "180")), int(os.environ.get("PUN_PAN_FRAMES", "288")))}
PAN_STEP = 30.0        # view-lon spacing of the pan's camera keys (renderer_cam is lon-coupled; keys keep the arc honest)
LAT_CLAMP = 75.0   # 45 put the camera UNDER Amasia (land at 60-75N): mostly ocean in frame. A polar mass wants a near-polar look.
DRIFT_LON = -60.0      # gentle westward drift across the divergence
TOUR_LAT = 10.0


def rate(u):
    return 1.0 - 0.22 * np.cos(2 * np.pi * u)


def aim_for(f):
    """Tour camera target: most-land hemisphere, blended toward the centroid by
    the scenario's sea bias (Ultima is a ring; its centroid is the inland sea).
    Lat clamped so a polar mass (Amasia) still reads as a globe."""
    a = f["aim"]; b = SEA_BIAS.get(f["scenario"], 0.0)
    # Scenarios with a sea bias are rings: start from the ring-side view and
    # blend toward the centroid (the sea). Everyone else: most-land hemisphere.
    start = a["ring_side"] if f["scenario"] in SEA_BIAS else a["most_land"]
    (la1, lo1), (la2, lo2) = start, a["centroid"]
    lo2 = lo1 + ((lo2 - lo1 + 180.0) % 360.0 - 180.0)          # blend along the short arc
    lat = la1 * (1 - b) + la2 * b; lon = lo1 * (1 - b) + lo2 * b
    return float(np.clip(lat, -LAT_CLAMP, LAT_CLAMP)), float((lon + 180.0) % 360.0 - 180.0)


def arc_deg(lon_a, lat_a, lon_b, lat_b):
    a, b = np.deg2rad([lat_a, lon_a]), np.deg2rad([lat_b, lon_b])
    return float(np.degrees(np.arccos(np.clip(np.sin(a[0])*np.sin(b[0]) + np.cos(a[0])*np.cos(b[0])*np.cos(a[1]-b[1]), -1, 1))))


# ---- the renderer's view mapping, measured (10-03) ----------------------------
# render_globe.py rotates the GLOBE with Euler (0, -lat, -lon) under a fixed camera
# 10 deg above the equator. Measured with Blender's own sphere (data_view_table.json):
# the view latitude is roughly -lat*cos(lon) + 10 — sign-inverted, longitude-coupled.
# Every shipped film was hand-framed against that behaviour, so it stays; aim points
# computed in TRUE (lat, lon) are converted here. The main film's departure camera is
# already in renderer space and is NOT converted.
_VM = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_view_model.json")))
def _Rz(a): c, s_ = np.cos(a), np.sin(a); return np.array([[c, -s_, 0], [s_, c, 0], [0, 0, 1]])
def _Ry(a): c, s_ = np.cos(a), np.sin(a); return np.array([[c, 0, s_], [0, 1, 0], [-s_, 0, c]])
_D = np.array([np.cos(np.deg2rad(_VM["elev"])), 0, np.sin(np.deg2rad(_VM["elev"]))])
def view_of(cam_lat, cam_lon):
    A, B = _Ry(_VM["sy"] * np.deg2rad(cam_lat)), _Rz(_VM["sz"] * np.deg2rad(cam_lon))
    M = B @ A if _VM["order"] == "zy" else A @ B
    p = (M.T if _VM["transpose"] else M) @ _D
    return float(np.degrees(np.arcsin(np.clip(p[2], -1, 1)))), float(np.degrees(np.arctan2(p[1], p[0])))
def renderer_cam(view_lat, view_lon):
    """Invert view_of numerically: the (camera_lat, camera_lon) that shows (view_lat, view_lon)."""
    from scipy.optimize import minimize
    def cost(x):
        vl, vo = view_of(x[0], x[1])
        dlo = (vo - view_lon + 180) % 360 - 180
        return (vl - view_lat) ** 2 + (np.cos(np.deg2rad(view_lat)) * dlo) ** 2
    best = None
    for lat0 in (-view_lat, view_lat, 0.0):
        for lon0 in (view_lon, view_lon + 180):
            r = minimize(cost, [lat0, lon0], method="Nelder-Mead", options={"xatol": 1e-3, "fatol": 1e-6})
            if best is None or r.fun < best.fun: best = r
    cl, co = best.x; co = (co + 180) % 360 - 180
    assert best.fun < 0.25, f"renderer_cam could not reach view ({view_lat},{view_lon}): residual {best.fun}"
    return float(cl), float(co)


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

    # ---- camera targets per tour stop, and the arc each dissolve must cover
    stops = {}                                   # scenario -> (lat, lon)
    cur_lat, cur_lon = lat0 * 0.6 + TOUR_LAT * 0.4, lon0 + DRIFT_LON
    blend_len = {}                               # scenario (or "return") -> anim frames per blend geo frame
    pan_keys = {}                                # scenario -> [(cam_lat, cam_lon), ...] after the static hold
    for f in geo:
        if f["kind"] == "tour_hold":
            vlat, vlon = aim_for(f)                      # TRUE view coordinates
            lat, lon = renderer_cam(vlat, vlon)          # -> renderer camera_lat/lon
            stops[f["scenario"]] = (lat, lon); views = globals().setdefault("_views", {}); views[f["scenario"]] = (vlat, vlon)
            arc = arc_deg(cur_lon, cur_lat, lon, lat)
            total = int(np.clip(arc / DEG_PER_FRAME, BLEND_MIN, BLEND_MAX))
            blend_len[f["scenario"]] = max(1, round(total / side["blend_frames"]))
            cur_lat, cur_lon = lat, lon
            if f["scenario"] in PAN:                     # pan keys in renderer space, westward from the stop
                deg, _ = PAN[f["scenario"]]
                steps = int(round(deg / PAN_STEP))
                pan_keys[f["scenario"]] = [renderer_cam(vlat, vlon - deg * j / steps) for j in range(1, steps + 1)]
                cur_lat, cur_lon = pan_keys[f["scenario"]][-1]   # the next move departs from the pan's end
    blend_len["return"] = max(1, round(BLEND_MIN / side["blend_frames"]))

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
        elif k == "tour_blend":
            n = blend_len[f["scenario"]]
        elif k == "return_blend":
            n = blend_len["return"]
        elif k == "tour_hold":
            n = TOUR_HOLD + (PAN[f["scenario"]][1] if f["scenario"] in PAN else 0)
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
    prev_lon, prev_lat = lon0 + DRIFT_LON, lat0 * 0.6 + TOUR_LAT * 0.4
    for f, s, n in zip(geo, starts, per):
        if f["kind"] == "tour_hold":
            lat, lon = stops[f["scenario"]]
            lon = shortest_arc(prev_lon, lon)
            pk = pan_keys.get(f["scenario"], [])
            key(s, lon, lat); key(s + TOUR_HOLD - 1, lon, lat)   # static hold, then the pan keys spread over the rest
            for j, (plat, plon) in enumerate(pk, 1):
                lon = shortest_arc(lon, plon); lat = plat
                key(s + TOUR_HOLD - 1 + round((n - TOUR_HOLD) * j / len(pk)), lon, lat)
            if not pk:
                key(s + n - 1, lon, lat)
            prev_lon, prev_lat = lon, lat
        elif f["kind"] == "final_hold":
            key(s, prev_lon, prev_lat); key(s + n - 1, prev_lon, prev_lat)
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
            "pacing": f"eased (rate 1-0.22cos2piu, base {TEMPO}), holds {HOLD}/{TOUR_HOLD}, tour dissolves {BLEND_MIN}-{BLEND_MAX}f by arc at {DEG_PER_FRAME} deg/f, pans {PAN}",
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
    for sc, (lat, lon) in stops.items():
        vl, vo = globals()["_views"][sc]; cl, co = view_of(lat, lon)
        print(f"  stop {sc:<6} want view ({vl:6.1f},{vo:7.1f}) -> cam ({lat:6.1f},{lon:7.1f}) -> model view ({cl:6.1f},{co:7.1f})   dissolve {blend_len[sc]*side['blend_frames']/FPS:.1f}s")
    print(f"max per-frame lon step {dl.max():.2f} deg (at frame {int(dl.argmax())})")


if __name__ == "__main__":
    main()
