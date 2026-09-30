#!/usr/bin/env python3
"""Rung 4: full-span flat draft of the future sequel — pacing, holds, the tour.

xian approved 2026-09-29 with two things baked in from the rung-3 round:
the full span (rung 3's 0–80 window stopped before the payoff) and
per-scenario framing (Novopangea and Aurica assemble near the antimeridian,
so a 0°-centred map cuts them in half).

PACING follows the measured shape of the event, not a constant rate. From
plan §6c: dispersal runs +20→60 (centroid separation 41°→71°), then a
quiet middle, then assembly +80→200 (concentration 0.371→0.516, steepest
at the end). A linear ramp would spend equal time on the quiet stretch and
on the supercontinents forming. So time is eased: brisk through the middle,
slow at both ends where the structure changes.

STRUCTURE
  1  departure hold     present day, superposed (all four agree here)
  2  the divergence     0 → +200, eased pacing
  3  terminal hold      four futures superposed — "we don't know which"
  4  the tour           each scenario alone, named, re-centred on its own
                        supercontinent, at its own terminus (250 for pun/
                        aurn, 200 for novon/amn — honest about which models
                        reach further)
  5  re-superposition   back to the cloud, final hold

Superposition spans 0–200 only: beyond that just pun/aurn exist, and
averaging two scenarios while calling it four would overstate agreement.

Usage: python3 scripts/render_sequel_draft.py [--fps 24] [--scale 1.0]
"""
import argparse
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from read_future_grids import SCENARIOS, available_times, grid_path, read_grid  # noqa: E402

OUT_DIR = os.path.expanduser("~/globe-render/sequel_draft")
OCEAN = np.array([0x1a, 0x42, 0x5a], dtype=np.float32)
CONTINENT = np.array([0xa0, 0x7c, 0x5a], dtype=np.float32)
W, H = 1920, 960
SUPER_END = 200.0          # all four scenarios exist to here


def load():
    times = sorted(set.intersection(*[set(available_times(s)) for s in SCENARIOS]))
    masks = {}
    for t in times:
        masks[t] = np.stack([np.asarray(read_grid(grid_path(s, t))["mask"],
                                        dtype=np.float32).T[::-1] for s in SCENARIOS])
    termini = {s: max(available_times(s)) for s in SCENARIOS}
    term = {s: np.asarray(read_grid(grid_path(s, termini[s]))["mask"],
                          dtype=np.float32).T[::-1] for s in SCENARIOS}
    return times, masks, term, termini


def centre_on_land(m):
    """Roll longitude so the land centroid sits at frame centre — otherwise a
    supercontinent that assembles near the antimeridian is cut in half."""
    col = (m * np.cos(np.linspace(np.pi/2, -np.pi/2, m.shape[0]))[:, None]).sum(0)
    ang = np.linspace(-np.pi, np.pi, m.shape[1])
    cx, cy = (np.cos(ang) * col).sum(), (np.sin(ang) * col).sum()
    centre = np.arctan2(cy, cx)
    # column of the centroid is (centre/2pi + 0.5)*ncols; moving it to ncols/2 is a
    # roll of -centre/2pi*ncols. The earlier '+ ncols//2' double-counted the half
    # world and rolled every supercontinent TO the frame edge (caught on the first
    # look, 09-29 — the tour frames were all cut in half).
    return np.roll(m, -int(round(centre / (2*np.pi) * m.shape[1])), axis=1)


def ease(u):
    """Slow at both ends, brisk through the quiet middle (plan §6c)."""
    # d/du = 1 - 0.22*cos(2*pi*u): 0.78 at both ends, 1.22 through the middle.
    return u - 0.22 * np.sin(2 * np.pi * u) / (2 * np.pi)


def cloud_at(t, times, masks):
    lo = max([x for x in times if x <= t]); hi = min([x for x in times if x >= t])
    f = 0.0 if hi == lo else (t - lo) / (hi - lo)
    return masks[lo] * (1 - f) + masks[hi] * f


def draw(cloud, title, sub, foot):
    img = OCEAN[None, None, :] + (CONTINENT - OCEAN)[None, None, :] * cloud[..., None]
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)
    d = ImageDraw.Draw(im)
    d.text((30, 26), title, fill=(242, 247, 251))
    if sub:
        d.text((30, 48), sub, fill=(194, 212, 226))
    d.text((30, H - 38), foot, fill=(160, 124, 90))
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fps", type=int, default=24)
    a = ap.parse_args()
    fps = a.fps
    times, masks, term, termini = load()
    os.makedirs(OUT_DIR, exist_ok=True)
    frames, SUPER = [], "Pangaea Ultima · Novopangea · Aurica · Amasia — superposed"

    # 1 departure hold
    for _ in range(int(1.8 * fps)):
        frames.append(draw(masks[0].mean(0), "Present day", "all four futures begin here", SUPER))

    # 2 the divergence, eased
    n = int(16 * fps)
    for i in range(n):
        t = float(SUPER_END * ease(i / (n - 1)))
        st = cloud_at(t, times, masks)
        agree = float(((st > 0.5).all(0) | (st <= 0.5).all(0)).mean())
        frames.append(draw(st.mean(0), f"+{t:,.0f} Myr",
                           f"scenario agreement {agree*100:.0f}%", SUPER))

    # 3 terminal hold, superposed
    endc = masks[int(SUPER_END)]
    for _ in range(int(2.2 * fps)):
        frames.append(draw(endc.mean(0), f"+{SUPER_END:,.0f} Myr",
                           "four futures at once — the honest state", SUPER))

    # 4 the tour: each alone, named, re-centred on its own supercontinent
    for s, name in SCENARIOS.items():
        alone = centre_on_land(term[s])
        cross = int(0.5 * fps)
        for i in range(cross):                       # dissolve out of the cloud
            f = i / (cross - 1)
            frames.append(draw(endc.mean(0) * (1 - f) + alone * f, name,
                               f"+{termini[s]} Myr — resolved alone",
                               "the tour: one future at a time, re-centred on its own supercontinent"))
        for _ in range(int(2.0 * fps)):
            frames.append(draw(alone, name, f"+{termini[s]} Myr — resolved alone",
                               "the tour: one future at a time, re-centred on its own supercontinent"))

    # 5 re-superposition
    last = centre_on_land(term[list(SCENARIOS)[-1]])
    cross = int(0.9 * fps)
    for i in range(cross):
        f = i / (cross - 1)
        frames.append(draw(last * (1 - f) + endc.mean(0) * f, "and back",
                           "we know it happens; we don't know which", SUPER))
    for _ in range(int(2.4 * fps)):
        frames.append(draw(endc.mean(0), "One of these is next",
                           "we know it happens; we don't know which", SUPER))

    print(f"rendering {len(frames)} frames ({len(frames)/fps:.1f}s @ {fps}fps)")
    for i, im in enumerate(frames):
        im.save(f"{OUT_DIR}/f{i:05d}.png")
        if i % 100 == 0:
            print(f"  {i}/{len(frames)}")

    out = os.path.expanduser("~/globe-render/sequel_fullspan_draft.mp4")
    r = subprocess.run(["ffmpeg", "-y", "-framerate", str(fps), "-i", f"{OUT_DIR}/f%05d.png",
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
                        "-movflags", "+faststart", out], capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-800:], file=sys.stderr); sys.exit(1)
    print(f"wrote {out} ({os.path.getsize(out)/1e6:.1f} MB, {len(frames)/fps:.1f}s)")


if __name__ == "__main__":
    main()
