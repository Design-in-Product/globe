#!/usr/bin/env python3
"""
Prepend an eased 360° orientation spin to a camera path (xian, 2026-10-16:
"a full globe spin at the very start, to orient people" — the prequel).

The new frames hold the first frame's geological state (geo_frame_idx,
time_ma, era_label) while camera_lon sweeps one full turn with smootherstep
easing — the same convention as add_spin_reveal.py, direction +1 — and land
exactly on the original first frame, so the join is seamless. anim_frame is
renumbered; metadata.anim_frames / duration_sec are updated.

    python3 scripts/add_opening_spin.py prequel_camera_path.json prequel_camera_path_v3.json [--frames 132] [--direction 1]

Flat parity: the flat film renders the same window as a pan,
PAN_SCROLL=0:<frames>:360 (render_flat.py skips lens-morph detection inside a
pan window).
"""
import argparse, json


def smootherstep(t):
    return t * t * t * (t * (t * 6 - 15) + 10)


def wrap_lon(lon):
    return ((lon + 180.0) % 360.0) - 180.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("dst")
    ap.add_argument("--frames", type=int, default=132, help="spin length (132 ≈ 5.5 s at 24 fps, as the v8 holds)")
    ap.add_argument("--direction", type=int, choices=[-1, 1], default=1)
    a = ap.parse_args()
    d = json.load(open(a.src))
    first = d["frames"][0]
    spin = []
    for k in range(a.frames):
        f = dict(first)
        f["camera_lon"] = wrap_lon(first["camera_lon"] + a.direction * 360.0 * smootherstep(k / a.frames))
        spin.append(f)
    frames = spin + d["frames"]
    for i, f in enumerate(frames):
        f["anim_frame"] = i
    d["frames"] = frames
    meta = d.setdefault("metadata", {})
    fps = meta.get("fps", 24)
    meta["anim_frames"] = len(frames)
    meta["duration_sec"] = round(len(frames) / fps, 1)
    meta["opening_spin"] = {"frames": a.frames, "direction": a.direction, "easing": "smootherstep",
                            "source": a.src, "added": "2026-10-16"}
    json.dump(d, open(a.dst, "w"), indent=1)
    print(f"{a.dst}: {len(frames)} frames ({len(frames)/fps:.1f} s); spin {a.frames} frames at "
          f"{first['time_ma']:.0f} Ma, lon {first['camera_lon']:.1f} → +{a.direction*360}° → {frames[a.frames]['camera_lon']:.1f}")


if __name__ == "__main__":
    main()
