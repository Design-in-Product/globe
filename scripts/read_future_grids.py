#!/usr/bin/env python3
"""Reader for the Davies/Green/Duarte future-supercontinent grids (OTIS format).

Data: OSF doi:10.17605/OSF.IO/8NEQ4, "Grid files.zip" (CC0), 50 grids across
four scenarios at 20 Myr snapshots — pun (Pangaea Ultima), novon
(Novopangea), aurn (Aurica), amn (Amasia). Lives in
~/globe-render/future-scenarios/ rather than this repo: it is source data,
and the repo's bulk already cost six weeks of un-published site.

Format from the authors' own grd_in.m (big-endian):
    @4     n, m           int32       grid dimensions
           lats[2]        float32     south, north
           lons[2]        float32     west, east
           dt             float32     timestep (sec)
           nob            int32       open-boundary count
           (+20 if nob==0, else +8, iob[2,nob] int32, +8)
           hz[n,m]        float32     bathymetry, COLUMN-major (MATLAB)
           +8
           mz[n,m]        int32       mask: 0 = land, nonzero = ocean

THE TRAP (cost a 180-degree error in the August rung-2 strip): the
scenarios do not share a longitude convention. pun/amn are -180..180;
novon/aurn are 0..360. Superposing them raw puts two scenarios half a
world out. `read_grid` normalises everything to -180..180.

Self-test: all four scenarios are the SAME present-day Earth at t=0, so
their t=0 masks must agree. That is a check the data itself provides, and
it goes red precisely when the longitude handling is wrong — which is the
failure this file exists to prevent. Run it:  python3 scripts/read_future_grids.py
"""
import os
import struct
import sys

import numpy as np

DATA_DIR = os.path.expanduser("~/globe-render/future-scenarios/Grid files")
SCENARIOS = {"pun": "Pangaea Ultima", "novon": "Novopangea",
             "aurn": "Aurica", "amn": "Amasia"}


def read_grid(path):
    """-> dict(lons, lats, mask, hz, shape). mask: True = land."""
    with open(path, "rb") as f:
        raw = f.read()
    if len(raw) < 44:
        raise ValueError(f"{path}: too small to be an OTIS grid ({len(raw)} B)")

    o = 4
    n, m = struct.unpack_from(">ii", raw, o); o += 8
    if not (0 < n < 10000 and 0 < m < 10000):
        raise ValueError(f"{path}: implausible grid dims {n}x{m} — wrong endianness or offset?")
    lat0, lat1 = struct.unpack_from(">ff", raw, o); o += 8
    lon0, lon1 = struct.unpack_from(">ff", raw, o); o += 8
    dt, = struct.unpack_from(">f", raw, o); o += 4
    nob, = struct.unpack_from(">i", raw, o); o += 4
    o += 20 if nob == 0 else 8 + 8 * nob + 8

    hz = np.frombuffer(raw, dtype=">f4", count=n * m, offset=o).reshape((n, m), order="F")
    o += 4 * n * m + 8
    mz = np.frombuffer(raw, dtype=">i4", count=n * m, offset=o).reshape((n, m), order="F")

    lons = np.linspace(lon0, lon1, n)
    lats = np.linspace(lat0, lat1, m)

    # Normalise to -180..180 so scenarios can be superposed (see THE TRAP).
    if lons.max() > 180.0:
        lons = ((lons + 180.0) % 360.0) - 180.0
        roll = int(np.argmin(lons))
        lons = np.roll(lons, -roll)
        mz = np.roll(mz, -roll, axis=0)
        hz = np.roll(hz, -roll, axis=0)

    return {"lons": lons, "lats": lats, "mask": (mz == 0),
            "hz": hz, "shape": (n, m), "dt": dt, "path": path}


def grid_path(scenario, t):
    return os.path.join(DATA_DIR, f"{scenario}1_{t}")


def available_times(scenario):
    pre = f"{scenario}1_"
    return sorted(int(f[len(pre):]) for f in os.listdir(DATA_DIR)
                  if f.startswith(pre) and f[len(pre):].isdigit())


def _agreement(a, b):
    """Fraction of cells where two land masks agree, on a common grid."""
    if a["mask"].shape != b["mask"].shape:
        return float("nan")
    return float((a["mask"] == b["mask"]).mean())


def self_test():
    """All four scenarios are the same Earth at t=0 -> their masks must agree."""
    if not os.path.isdir(DATA_DIR):
        print(f"FAIL: no data at {DATA_DIR}", file=sys.stderr); return 2

    print("scenario spans (Myr into the future):")
    grids = {}
    for s, name in SCENARIOS.items():
        ts = available_times(s)
        print(f"  {s:<6} {name:<16} {len(ts):>2} snapshots  {min(ts)}..{max(ts)}")
        grids[s] = read_grid(grid_path(s, 0))

    ref = grids["pun"]
    print(f"\ngrid {ref['shape'][0]}x{ref['shape'][1]}, "
          f"lon {ref['lons'].min():.1f}..{ref['lons'].max():.1f}, "
          f"lat {ref['lats'].min():.1f}..{ref['lats'].max():.1f}, "
          f"land {ref['mask'].mean()*100:.1f}%")

    print("\nt=0 agreement with pun (all four are present-day Earth):")
    ok = True
    for s in SCENARIOS:
        a = _agreement(ref, grids[s])
        flag = "ok" if a > 0.95 else "MISMATCH"
        if a <= 0.95:
            ok = False
        print(f"  {s:<6} {a*100:6.2f}%  {flag}")

    if not ok:
        print("\nFAIL: t=0 masks disagree — longitude convention or layout is wrong.",
              file=sys.stderr)
        return 1
    print("\nPASS: all four scenarios agree at t=0.")
    return 0


if __name__ == "__main__":
    sys.exit(self_test())
