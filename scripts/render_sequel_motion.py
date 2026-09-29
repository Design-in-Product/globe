#!/usr/bin/env python3
"""Rung 3: motion window across the future branch (scenario superposition).

Ladder position: rung 1 research done, rung 2 static strip delivered 08-10,
this is rung 3 — "motion window around the split, coherent members" — for
xian's read on whether the branching reads in motion. xian: "yes" (09-29).

WINDOW CHOSEN BY MEASUREMENT, NOT BY THE PLAN. The 08-10 plan assumed the
scenarios "largely agree to ~+50 Myr" and "split beyond ~+100". Measuring
pairwise land-mask agreement across all six scenario pairs says otherwise:

    +0   99.4%      +60  67.9%
    +20  96.3%      +80  66.0%
    +40  75.4%     +200  61.3%

The branch is +20 to +40 Myr and is essentially complete by +60; everything
later is slow drift. So the window is 0 -> 80, which contains the whole
event. Recorded because the plan's §5 defaults would have put the film's
drama in the wrong place.

Treatment: the four published scenarios ARE the ensemble members (the
prequel's coherent-members decision, reused — no parameter jitter, these
are real competing hypotheses). Averaging their land masks gives the
probability cloud for free: agreed land renders solid, contested land
renders ghostly in proportion to how many scenarios claim it.

Sources are 20 Myr snapshots, so between them we crossfade — the same
honest approximation the scrubber and the film's own transitions make.

Usage: python3 scripts/render_sequel_motion.py [--end 80] [--fps 24]
"""
import argparse
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from read_future_grids import SCENARIOS, available_times, grid_path, read_grid  # noqa: E402

OUT_DIR = os.path.expanduser("~/globe-render/sequel_motion")
OCEAN = np.array([0x1a, 0x42, 0x5a], dtype=np.float32)      # film palette
CONTINENT = np.array([0xa0, 0x7c, 0x5a], dtype=np.float32)
W, H = 1920, 960


def load_masks():
    """-> {t: (4, h, w) float array of land masks}, on the shared snapshot times."""
    times = sorted(set.intersection(*[set(available_times(s)) for s in SCENARIOS]))
    out = {}
    for t in times:
        stack = []
        for s in SCENARIOS:
            g = read_grid(grid_path(s, t))
            # grids are (n_lon, m_lat); transpose to image orientation, flip lat
            stack.append(np.asarray(g["mask"], dtype=np.float32).T[::-1])
        out[t] = np.stack(stack)
    return times, out


def frame(cloud, t_myr, agree):
    """cloud: (h,w) in 0..1 = fraction of scenarios calling this cell land."""
    img = OCEAN[None, None, :] + (CONTINENT - OCEAN)[None, None, :] * cloud[..., None]
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)
    d = ImageDraw.Draw(im)
    d.text((28, 24), f"+{t_myr:,.0f} Myr", fill=(242, 247, 251))
    d.text((28, 44), f"scenario agreement {agree*100:.0f}%", fill=(194, 212, 226))
    d.text((28, H - 36), "Pangaea Ultima · Novopangea · Aurica · Amasia — "
                         "solid where all four agree, ghostly where they differ",
           fill=(160, 124, 90))
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--end", type=float, default=80.0)
    ap.add_argument("--fps", type=int, default=24)
    ap.add_argument("--seconds", type=float, default=12.0)
    a = ap.parse_args()

    times, masks = load_masks()
    os.makedirs(OUT_DIR, exist_ok=True)
    n = int(a.fps * a.seconds)
    print(f"snapshots {times[0]}..{times[-1]} every 20 Myr; "
          f"rendering 0..{a.end:.0f} Myr in {n} frames")

    for i in range(n):
        t = a.end * i / (n - 1)
        lo = max([x for x in times if x <= t])
        hi = min([x for x in times if x >= t])
        f = 0.0 if hi == lo else (t - lo) / (hi - lo)
        stack = masks[lo] * (1 - f) + masks[hi] * f          # crossfade between snapshots
        cloud = stack.mean(axis=0)
        # agreement = fraction of cells where all four say the same thing
        agree = float(((stack > 0.5).all(0) | (stack <= 0.5).all(0)).mean())
        frame(cloud, t, agree).save(f"{OUT_DIR}/f{i:04d}.png")
        if i % 40 == 0:
            print(f"  {i:>4}/{n}  t=+{t:5.1f} Myr  agreement {agree*100:.0f}%")

    out = os.path.expanduser("~/globe-render/sequel_motion_window.mp4")
    r = subprocess.run(["ffmpeg", "-y", "-framerate", str(a.fps), "-i", f"{OUT_DIR}/f%04d.png",
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
                        "-movflags", "+faststart", out], capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-800:], file=sys.stderr); sys.exit(1)
    print(f"\nwrote {out} ({os.path.getsize(out)/1e6:.1f} MB, {n} frames, {a.seconds:.0f}s)")


if __name__ == "__main__":
    main()
