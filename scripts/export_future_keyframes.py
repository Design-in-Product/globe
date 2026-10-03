#!/usr/bin/env python3
"""Future-layer keyframes for /explore/'s scenario picker.

xian, 2026-09-29: "maybe we need a way for the user to choose one" of the
four future scenarios. Picker approved 10-02, ahead of the film (rung 5).

Layers written (each a set of keyframes at the OSF 20 Myr snapshots,
future times stored as NEGATIVE time_ma so the past/future axis is one
number line: 1800 ... 0 ... -250):

    future:super   mean of all four masks, 0..200 (all four exist there)
    future:pun     Pangaea Ultima  0..250
    future:novon   Novopangea      0..200
    future:aurn    Aurica          0..250
    future:amn     Amasia          0..200

The t=0 snapshot of every layer is deliberately NOT exported: the shared
present-day keyframe (Merdith, from the past layer) is the common origin,
and the 0 -> +20 crossfade is the honest seam between two datasets, the
same kind of seam the prequel->main join is. Two keyframes at the same
time cannot be crossfaded anyway.

Resolution: the grids are 1440x721. Rendered at 2048x1024 so the shader
sees the same texture size as the prequel layer; that is a resize, not
information, and the budget rule (WebP q90, no upscaling for detail)
still holds in spirit — these are flat masks with no detail to invent.

Writes scrubber_assets/future/<layer>_<t>.webp and
scrubber_assets/future/keyframes-future.json. Separate manifest from the
past layer's keyframes.json: each exporter owns its own, the page merges.
That is the layer-separable shape the "Wikiglobe" north star asks for.
"""
import json
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from read_future_grids import SCENARIOS, available_times, grid_path, read_grid  # noqa: E402

OUT_DIR = "scrubber_assets/future"
SIZE = (2048, 1024)
WEBP_QUALITY = 90
OCEAN = np.array([0x1a, 0x42, 0x5a], dtype=np.float32)
CONTINENT = np.array([0xa0, 0x7c, 0x5a], dtype=np.float32)
SUPER_END = 200  # all four scenarios exist to here


def mask_image(m):
    """m: (lat, lon) float 0..1 land fraction -> PIL image in the film palette."""
    img = OCEAN[None, None, :] + (CONTINENT - OCEAN)[None, None, :] * m[..., None]
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).resize(SIZE, Image.BILINEAR)


def grid_mask(s, t):
    return np.asarray(read_grid(grid_path(s, t))["mask"], dtype=np.float32).T[::-1]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    entries, n_written = [], 0

    def write(layer, t, label, m):
        nonlocal n_written
        fn = f"{layer.replace(':', '_')}_{t:03d}.webp"
        mask_image(m).save(os.path.join(OUT_DIR, fn), "WEBP", quality=WEBP_QUALITY)
        entries.append({"layer": layer, "time_ma": -t, "label": label, "file": fn,
                        "width": SIZE[0], "height": SIZE[1]})
        n_written += 1
        print(f"wrote {layer:<14} +{t:3d} Myr  {os.path.getsize(os.path.join(OUT_DIR, fn))/1024:5.0f} KB")

    # superposition: only where all four exist, t>0
    common = sorted(set.intersection(*[set(available_times(s)) for s in SCENARIOS]))
    for t in common:
        if t == 0 or t > SUPER_END:
            continue
        m = np.mean([grid_mask(s, t) for s in SCENARIOS], axis=0)
        write("future:super", t, f"+{t} Myr — four futures superposed", m)

    # each scenario alone, to its own terminus
    for s, name in SCENARIOS.items():
        for t in available_times(s):
            if t == 0:
                continue
            write(f"future:{s}", t, f"+{t} Myr — {name}", grid_mask(s, t))

    manifest = {
        "budget": f"{SIZE[0]}x{SIZE[1]} WebP q{WEBP_QUALITY}, flat masks (OSF 1440x721 resized)",
        "source": "OSF 10.17605/OSF.IO/8NEQ4 (Davies, Green & Duarte), CC0",
        "layers": {
            "future:super": "All four, superposed",
            **{f"future:{s}": name for s, name in SCENARIOS.items()},
        },
        "keyframes": sorted(entries, key=lambda k: (k["layer"], -k["time_ma"])),
    }
    with open(os.path.join(OUT_DIR, "keyframes-future.json"), "w") as f:
        json.dump(manifest, f, indent=2)

    expected = (len([t for t in common if 0 < t <= SUPER_END])
                + sum(len([t for t in available_times(s) if t > 0]) for s in SCENARIOS))
    total = sum(os.path.getsize(os.path.join(OUT_DIR, e["file"])) for e in entries) / 1e6
    print(f"\n{n_written} written, {expected} expected; {total:.1f} MB")
    if n_written != expected:
        print("INCOMPLETE"); sys.exit(1)


if __name__ == "__main__":
    main()
