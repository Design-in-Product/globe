#!/usr/bin/env python3
"""
Add a "spin reveal" to the supercontinent hold frames of an existing
camera_path.json — WITHOUT re-running the gplately pipeline.

During the variable-pacing holds at the major supercontinents (Rodinia,
Gondwana, Pangaea, present day) the camera currently sits still. This script
sweeps camera_lon through a full 360° during each hold so the globe performs a
slow, eased rotation that reveals the whole surface, then returns to rest.

This is the "Earth axis" variant of the spin reveal (roadmap item #1): a pure
camera_lon sweep. render_globe.py already maps camera_lon → globe Z-rotation
(rot_z = -radians(cam_lon)), so NO Blender changes are needed — just re-render
with the new camera path.

Because the sweep is exactly 360° and eased with smootherstep (zero velocity at
both ends), each hold starts and ends at its original longitude: the reveal
blends seamlessly into the constant frames on either side.

Usage:
    python3 scripts/add_spin_reveal.py \
        [--in camera_path.json] [--out camera_path_spin.json] \
        [--rotations 1.0] [--direction 1] [--holds 250,0,480,900] \
        [--min-hold 20]

Then point render_globe.py's CAMERA_PATH_FILE at the output and re-render.
"""

import os
import sys
import json
import argparse


def smootherstep(t):
    """Ken Perlin's smootherstep: 6t^5 - 15t^4 + 10t^3.

    Eases in and out with zero first derivative at t=0 and t=1, so the spin
    accelerates out of the hold and decelerates back to rest — no visible
    velocity discontinuity where the reveal meets the constant hold frames.
    """
    t = max(0.0, min(1.0, t))
    return t * t * t * (t * (t * 6 - 15) + 10)


def find_hold_runs(frames, min_hold):
    """Return [(start_idx, end_idx_inclusive, time_ma)] for each hold.

    A hold is a maximal run of frames sharing one geo_frame_idx whose length
    exceeds min_hold. Normal timesteps produce 1-3 frame runs; supercontinent
    holds add 36-60 extra frames, so they stand out clearly.
    """
    runs = []
    n = len(frames)
    i = 0
    while i < n:
        j = i
        while j + 1 < n and frames[j + 1]["geo_frame_idx"] == frames[i]["geo_frame_idx"]:
            j += 1
        if (j - i + 1) >= min_hold:
            runs.append((i, j, frames[i]["time_ma"]))
        i = j + 1
    return runs


def apply_spin(frames, run, rotations, direction):
    """Rewrite camera_lon across a hold run to perform an eased 360°*rotations sweep.

    The base longitude is taken from the run's first frame; latitude is left
    untouched (the globe spins about its tilted axis, revealing the surface
    while keeping the supercontinent's vertical framing).
    """
    start, end, _ = run
    base_lon = frames[start]["camera_lon"]
    length = end - start
    if length <= 0:
        return 0
    for k in range(start, end + 1):
        t = (k - start) / length
        offset = direction * 360.0 * rotations * smootherstep(t)
        new_lon = base_lon + offset
        # Normalize to [-180, 180] to match the rest of the path's convention
        new_lon = ((new_lon + 180.0) % 360.0) - 180.0
        frames[k]["camera_lon"] = new_lon
        frames[k]["spin_reveal"] = True
    return length + 1


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(here)

    ap = argparse.ArgumentParser(description="Add a spin reveal to camera_path.json holds.")
    ap.add_argument("--in", dest="inp", default=os.path.join(root, "camera_path.json"))
    ap.add_argument("--out", dest="out", default=os.path.join(root, "camera_path_spin.json"))
    ap.add_argument("--rotations", type=float, default=1.0,
                    help="Number of full turns during each hold (default 1.0).")
    ap.add_argument("--direction", type=int, choices=[-1, 1], default=1,
                    help="Spin direction: 1 or -1 (default 1).")
    ap.add_argument("--holds", default="all",
                    help="Comma-separated time_ma values to spin (e.g. '250' for Pangaea "
                         "only), or 'all' (default).")
    ap.add_argument("--min-hold", type=int, default=20,
                    help="Minimum run length to be treated as a hold (default 20).")
    args = ap.parse_args()

    with open(args.inp) as f:
        data = json.load(f)
    frames = data["frames"]

    runs = find_hold_runs(frames, args.min_hold)
    if not runs:
        print(f"No holds >= {args.min_hold} frames found in {args.inp}. Nothing to do.")
        return

    if args.holds.strip().lower() == "all":
        wanted = None
    else:
        wanted = {float(x) for x in args.holds.split(",") if x.strip() != ""}

    print(f"Source: {args.inp}  ({len(frames)} frames)")
    print(f"Detected {len(runs)} hold(s) >= {args.min_hold} frames:")
    spun = 0
    for run in runs:
        start, end, time_ma = run
        era = frames[start].get("era_label", "")
        selected = wanted is None or float(time_ma) in wanted
        if selected:
            length = apply_spin(frames, run, args.rotations, args.direction)
            spun += 1
            mark = "→ SPIN"
        else:
            length = end - start + 1
            mark = "  skip"
        print(f"  {mark}  {int(time_ma):4d} Ma  anim {start}-{end}  "
              f"({length} frames)  {era}")

    data.setdefault("metadata", {})["spin_reveal"] = {
        "variant": "earth_axis",
        "rotations": args.rotations,
        "direction": args.direction,
        "holds_spun": spun,
        "easing": "smootherstep",
    }

    with open(args.out, "w") as f:
        json.dump(data, f, indent=2)
    print(f"\n✓ Wrote {args.out}  ({spun} hold(s) given a {args.rotations}× spin)")
    print(f"  Point render_globe.py CAMERA_PATH_FILE at this file and re-render.")


if __name__ == "__main__":
    main()
