#!/usr/bin/env python3
"""Projection-morph library for the flat film's lens-per-hold reveals.

Canonical implementation of the xian-approved flat-v7 technique (drafted in
test_flat_morph.py, approved 2026-07-28): during a supercontinent hold the
equirectangular map morphs into a target "lens" projection, the planet rotates
360° UNDER the fixed projection, then morphs back.

Lenses (the approved arc): sinusoidal → azimuthal-s → mollweide → ortho.
Display frame is 2:1; circular lenses scale x by 0.5 to render as true circles.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
from scipy.ndimage import map_coordinates

LENSES = ("sinusoidal", "azimuthal-s", "mollweide", "ortho")


def smootherstep(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * t * (t * (t * 6 - 15) + 10)


def mollweide_theta(lat_rad):
    """Solve 2θ + sin 2θ = π sin(lat) by Newton iteration (vectorized)."""
    theta = lat_rad.copy()
    target = np.pi * np.sin(lat_rad)
    for _ in range(10):
        f = 2 * theta + np.sin(2 * theta) - target
        fp = 2 + 2 * np.cos(2 * theta)
        step = np.where(np.abs(fp) > 1e-9, f / fp, 0.0)
        theta = theta - step
    return theta


class FlatMorph:
    """Precomputed mesh + texture sampler for one lens at one resolution."""

    def __init__(self, lens, nlon=1024, nlat=512, resx=1920, resy=960,
                 ocean='black'):
        # 'ocean' is the surround outside the morphed map; the approved draft
        # look is black (the map's own ocean color lives in the texture).
        assert lens in LENSES, lens
        self.lens = lens
        self.resx, self.resy = resx, resy
        self.ocean = ocean

        lon_edges = np.linspace(-180, 180, nlon + 1)
        lat_edges = np.linspace(-90, 90, nlat + 1)
        LON, LAT = np.meshgrid(lon_edges, lat_edges)

        self.EQ_X = LON / 180.0
        self.EQ_Y = LAT / 90.0

        if lens == "mollweide":
            theta = np.repeat(mollweide_theta(np.radians(lat_edges))[:, None],
                              nlon + 1, axis=1)
            self.TG_X = np.radians(LON) * np.cos(theta) / np.pi
            self.TG_Y = np.sin(theta)
        elif lens == "sinusoidal":
            self.TG_X = (LON / 180.0) * np.cos(np.radians(LAT))
            self.TG_Y = LAT / 90.0
        elif lens == "azimuthal-s":
            r = np.sin(np.radians((90.0 + LAT) / 2.0))
            self.TG_X = 0.5 * r * np.sin(np.radians(LON))
            self.TG_Y = r * np.cos(np.radians(LON))
        elif lens == "ortho":
            self.TG_X = 0.5 * np.cos(np.radians(LAT)) * np.sin(np.radians(LON))
            self.TG_Y = np.sin(np.radians(LAT))

        lon_c = (lon_edges[:-1] + lon_edges[1:]) / 2
        lat_c = (lat_edges[:-1] + lat_edges[1:]) / 2
        self.LON_C, self.LAT_C = np.meshgrid(lon_c, lat_c)
        self.NEAR = np.abs(self.LON_C) < 90.0 if lens == "ortho" else None

        self.img = None
        self.ROW_F = None

    def load_texture(self, path):
        self.img = np.asarray(Image.open(path).convert('RGB'),
                              dtype=np.float32) / 255.0
        H = self.img.shape[0]
        self.ROW_F = np.clip((90 - self.LAT_C) / 180.0 * H - 0.5, 0, H - 1)

    def _sample(self, lon0):
        H, W = self.img.shape[:2]
        col_f = (((self.LON_C + lon0 + 180.0) % 360.0) / 360.0 * W - 0.5) % W
        coords = np.stack([self.ROW_F.ravel(), col_f.ravel()])
        out = np.empty((*self.LON_C.shape, 3), dtype=np.float32)
        for c in range(3):
            out[..., c] = map_coordinates(
                self.img[..., c], coords, order=1,
                mode='grid-wrap').reshape(self.LON_C.shape)
        return out

    def render(self, s, lon0, out_png):
        """Render one frame: morph factor s (0=equirect, 1=lens), planet
        rotated lon0 degrees under the projection."""
        X = (1 - s) * self.EQ_X + s * self.TG_X
        Y = (1 - s) * self.EQ_Y + s * self.TG_Y
        C = self._sample(lon0)

        fig = plt.figure(figsize=(self.resx / 100, self.resy / 100), dpi=100)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_xlim(-1.03, 1.03)
        ax.set_ylim(-1.03, 1.03)
        ax.set_axis_off()
        fig.patch.set_facecolor(self.ocean)
        if self.NEAR is None:
            ax.pcolormesh(X, Y, C, shading='flat', rasterized=True)
        else:
            # Ortho: far hemisphere fades with the morph, near side on top.
            far = np.empty((*C.shape[:2], 4), dtype=np.float32)
            far[..., :3] = C
            far[..., 3] = np.where(self.NEAR, 0.0, 1.0 - s)
            near = np.empty_like(far)
            near[..., :3] = C
            near[..., 3] = np.where(self.NEAR, 1.0, 0.0)
            ax.pcolormesh(X, Y, far, shading='flat', rasterized=True)
            ax.pcolormesh(X, Y, near, shading='flat', rasterized=True)
        fig.savefig(out_png, dpi=100, facecolor=self.ocean)
        plt.close(fig)


def hold_schedule(n_frames, morph_frames=24):
    """Per-frame (s, lon0) for an n_frames hold: morph out, rotate 360°,
    morph back. Default 24+f+24 split (132-frame v8 holds → 84-frame spin)."""
    spin = n_frames - 2 * morph_frames
    assert spin > 0, "hold too short for morph windows"
    sched = []
    for k in range(morph_frames):
        sched.append((float(smootherstep((k + 1) / morph_frames)), 0.0))
    for k in range(spin):
        sched.append((1.0, float(360.0 * smootherstep((k + 1) / spin))))
    for k in range(morph_frames):
        sched.append((float(1.0 - smootherstep((k + 1) / morph_frames)), 0.0))
    return sched
