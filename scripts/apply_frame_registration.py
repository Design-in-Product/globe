#!/usr/bin/env python3
"""Register the prequel's terminal approach onto the main film's frame.

cao2024's reference frame at 1000 Ma is rigidly rotated 9.8475° (pole
37.24N, 130.03W) from Merdith2021's — measured directly from the rotation
models (R_corr = R_mer(1000,P) ∘ R_cao(1000,P)⁻¹, identical across all
major cratons; a few small terranes differ per-plate and settle in the
blend). Over the crystallization window (1150 -> 1000 Ma, frames 651-800)
this script drifts each composited frame by w(t)·R_corr — ~0.16 px/frame,
imperceptible — so the terminal frame lands pixel-registered on the main
film's opening and a smooth dissolve works.

Raster-level (inverse-mapped bilinear resample with longitude wrap); reads
originals from prequel_frames_precorr/, writes into prequel_frames/.
Idempotent: originals are moved to the precorr dir on first run.
"""

import os
import shutil
import numpy as np
from PIL import Image
from scipy.ndimage import map_coordinates

POLE_LAT, POLE_LON, ANGLE_DEG = 37.238544, -130.032507, 9.847544
FADE_START_T, T_END = 1150.0, 1000.0
IDX_FIRST, IDX_LAST = 651, 800

FRAMES = os.path.expanduser("~/globe-render/prequel_frames")
PRECORR = os.path.expanduser("~/globe-render/prequel_frames_precorr")
os.makedirs(PRECORR, exist_ok=True)


def rot_matrix(pole_lat, pole_lon, angle_deg):
    """Rodrigues rotation matrix about the given Euler pole."""
    la, lo, th = map(np.radians, (pole_lat, pole_lon, angle_deg))
    k = np.array([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)])
    K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
    return np.eye(3) + np.sin(th) * K + (1 - np.cos(th)) * (K @ K)


def register(img, w):
    """Rotate the equirect raster by w·R_corr (inverse pixel mapping)."""
    H, W = img.shape[:2]
    lon = (np.arange(W) + 0.5) / W * 360.0 - 180.0
    lat = 90.0 - (np.arange(H) + 0.5) / H * 180.0
    LON, LAT = np.meshgrid(np.radians(lon), np.radians(lat))
    xyz = np.stack([np.cos(LAT) * np.cos(LON),
                    np.cos(LAT) * np.sin(LON),
                    np.sin(LAT)])
    Rinv = rot_matrix(POLE_LAT, POLE_LON, -ANGLE_DEG * w)
    v = np.einsum('ij,jhw->ihw', Rinv, xyz)
    src_lat = np.degrees(np.arcsin(np.clip(v[2], -1, 1)))
    src_lon = np.degrees(np.arctan2(v[1], v[0]))
    row = np.clip((90.0 - src_lat) / 180.0 * H - 0.5, 0, H - 1)
    col = ((src_lon + 180.0) / 360.0 * W - 0.5) % W
    coords = np.stack([row.ravel(), col.ravel()])
    out = np.empty_like(img)
    for c in range(img.shape[2]):
        out[..., c] = map_coordinates(img[..., c], coords, order=1,
                                      mode='grid-wrap').reshape(H, W)
    return out


n = 0
for idx in range(IDX_FIRST, IDX_LAST + 1):
    name = f"prequel_frame_{idx:04d}.png"
    src = os.path.join(PRECORR, name)
    if not os.path.exists(src):
        shutil.move(os.path.join(FRAMES, name), src)
    t = 1800 - idx
    w = min(1.0, max(0.0, (FADE_START_T - t) / (FADE_START_T - T_END)))
    img = np.asarray(Image.open(src).convert("RGB"), dtype=np.float32)
    Image.fromarray(register(img, w).astype(np.uint8)).save(
        os.path.join(FRAMES, name))
    n += 1
    if idx % 30 == 0:
        print(f"  [{idx}] w={w:.2f}", flush=True)

print(f"✓ registered {n} frames "
      f"({IDX_FIRST}-{IDX_LAST}; w ramps 0→1 over 1150→1000 Ma)")
