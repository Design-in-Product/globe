#!/usr/bin/env python3
"""
Recolor an equirectangular texture frame into a named palette — WITHOUT
re-running the gplately pipeline (roadmap item 4, cinematic palette).

The source textures are flat-colour maps: ocean, continent (two shades where
polygons overlap), coastline, ridge/transform and trench, plus anti-aliased
edge pixels that blend two of those. Each pixel is decomposed as the nearest
point on the segment between two basis colours (t along a→b), and the same t
is applied to the target palette's a'→b'. Edges stay anti-aliased; the five
roles keep their meaning.

Usage:
    python3 scripts/recolor_texture.py --palette midnight-gold \
        ~/globe-render/frames/globe_frame_1000.png out.png
    python3 scripts/recolor_texture.py --list

A directory as input recolours every globe_frame_*.png into the output dir
(skip-existing, so a batch is resumable).
"""
import argparse, glob, os, sys
import numpy as np
from PIL import Image

# Source basis, as the pixels actually appear in ~/globe-render/frames
# (continent is #a07c5a at alpha 0.9 over the ocean; overlaps stack lighter).
# "continent" is the main film's land as rendered (#a07c5a at alpha 0.9 over
# the ocean); "continent_full" is the same role drawn opaque — the prequel's
# probability cloud and the sequel's scenario superposition blend ocean→
# #a07c5a continuously, and both land shades map to the one target gold.
ROLES = ["ocean", "continent", "continent_full", "continent_overlap", "coastline", "ridge", "trench"]
SOURCE = {
    "ocean":             "#1a425a",
    "continent":         "#92765a",
    "continent_full":    "#a07c5a",
    "continent_overlap": "#9e7b5a",
    "coastline":         "#5c442e",
    "ridge":             "#ff6b35",
    "trench":            "#e63946",
}

PALETTES = {
    # Deep navy ocean, warm gold land, amber/coral boundaries.
    "midnight-gold": {
        "ocean": "#0b1f3a", "continent": "#c9a24a", "continent_full": "#c9a24a", "continent_overlap": "#d6b25e",
        "coastline": "#6e5218", "ridge": "#ffb347", "trench": "#ff5f6d",
    },
    # Cobalt ocean, brass land — lower-contrast, more "atlas" than "poster".
    "cobalt-brass": {
        "ocean": "#10294d", "continent": "#b8923e", "continent_full": "#b8923e", "continent_overlap": "#c7a252",
        "coastline": "#5f4a1c", "ridge": "#ffd166", "trench": "#ef476f",
    },
    # Near-black ink ocean, bright gold land — highest contrast; keeps the
    # original trench red so the subduction teeth read the same.
    "ink-ember": {
        "ocean": "#071426", "continent": "#d4a84b", "continent_full": "#d4a84b", "continent_overlap": "#e2ba5f",
        "coastline": "#8a6a24", "ridge": "#ff9f1c", "trench": "#e63946",
    },
}


def hex2rgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float32)


def recolor(img, palette):
    src = np.stack([hex2rgb(SOURCE[r]) for r in ROLES])        # (R,3)
    dst = np.stack([hex2rgb(palette[r]) for r in ROLES])       # (R,3)
    px = np.asarray(img.convert("RGB"), dtype=np.float32)      # (H,W,3)
    flat = px.reshape(-1, 3)
    best_res = np.full(flat.shape[0], np.inf, dtype=np.float32)
    out = np.zeros_like(flat)
    n = len(ROLES)
    for a in range(n):
        for b in range(a, n):
            sa, sb = src[a], src[b]
            da, db = dst[a], dst[b]
            d = sb - sa
            dd = float(d @ d)
            if dd == 0:
                t = np.zeros(flat.shape[0], dtype=np.float32)
            else:
                t = np.clip(((flat - sa) @ d) / dd, 0.0, 1.0)
            proj = sa + t[:, None] * d
            res = np.sum((flat - proj) ** 2, axis=1)
            better = res < best_res
            if better.any():
                best_res[better] = res[better]
                out[better] = da + t[better, None] * (db - da)
    return Image.fromarray(np.clip(out + 0.5, 0, 255).astype(np.uint8).reshape(px.shape))


def _job(t):
    f, o, name = t
    tmp = o + ".part"
    recolor(Image.open(f), PALETTES[name]).save(tmp, format="PNG", optimize=True)
    os.replace(tmp, o)   # never leave a truncated PNG under the final name


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--palette", choices=sorted(PALETTES), default=None)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--pattern", default="globe_frame_*.png", help="glob inside a src dir (prequel_frame_*.png, sequel_frame_*.png)")
    ap.add_argument("--jobs", type=int, default=1)
    ap.add_argument("src", nargs="?")
    ap.add_argument("dst", nargs="?")
    args = ap.parse_args()
    if args.list:
        for name, pal in PALETTES.items():
            print(name, " ".join(f"{r}={pal[r]}" for r in ROLES))
        return
    if not (args.palette and args.src and args.dst):
        ap.error("--palette, src and dst are required (or --list)")
    pal = PALETTES[args.palette]
    if os.path.isdir(args.src):
        os.makedirs(args.dst, exist_ok=True)
        files = sorted(glob.glob(os.path.join(args.src, args.pattern)))
        todo = [(f, os.path.join(args.dst, os.path.basename(f))) for f in files
                if not os.path.exists(os.path.join(args.dst, os.path.basename(f)))]
        if args.jobs > 1 and todo:
            from multiprocessing import Pool
            with Pool(args.jobs) as pool:
                for k, _ in enumerate(pool.imap_unordered(_job, [(f, o, args.palette) for f, o in todo]), 1):
                    if k % 50 == 0:
                        print(f"  {k}/{len(todo)} recoloured", flush=True)
        else:
            for k, (f, o) in enumerate(todo, 1):
                _job((f, o, args.palette))
                if k % 50 == 0:
                    print(f"  {k}/{len(todo)} recoloured", flush=True)
        print(f"recolor {args.palette}: {len(todo)} written, {len(files) - len(todo)} already present, of {len(files)}")
    else:
        recolor(Image.open(args.src), pal).save(args.dst, optimize=True)
        print(f"recolor {args.palette}: {args.dst}")


if __name__ == "__main__":
    main()
