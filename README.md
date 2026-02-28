# Tectonic Globe

A 3D animated visualization of Earth's tectonic history, showing continental drift from 1000 million years ago (Rodinia) through Pangaea to the present day.

The animation renders equirectangular plate reconstruction data onto a 3D globe in Blender, with smooth 1 Ma resolution continental motion, adaptive camera tracking, and geological era labeling.

## The Videos

**Globe (v6):** `tectonic_globe_v6.mp4` — 1:41, 1920x1080, 3D rendered globe with Cycles
**Flat (v3):** `tectonic_flat_v3.mp4` — 1:41, 1920x960, equirectangular projection companion

## Pipeline

```
generate_frames.py     gplately/Merdith2021 → 1001 equirectangular PNGs (4096x2048)
        ↓
compute_camera_path.py adaptive centroid tracking → camera_path.json
        ↓
render_globe.py        Blender Cycles + dual-texture crossfade → MP4
render_flat.py         PIL crossfade + ffmpeg → MP4 (no Blender needed)
```

## Requirements

- Python 3.10+ with gplately, pygplates, matplotlib, cartopy, Pillow, scipy
- Blender 5.0+ (for globe renders only)
- ffmpeg

## Quick Start

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install gplately matplotlib cartopy Pillow scipy

# Generate source frames (~20 min)
python3 scripts/generate_frames.py

# Compute camera path (~15 min)
python3 scripts/compute_camera_path.py

# Flat video — fast, no Blender needed (~6 min)
python3 scripts/render_flat.py

# Globe video — requires Blender, runs ~5 hours
/Applications/Blender.app/Contents/MacOS/Blender --background --python scripts/render_globe.py
```

## How This Was Built

I'm Claude (Anthropic's AI assistant), and I built this project collaboratively with Xian over a series of working sessions in February 2025. I think the process is worth documenting because it's a good example of how iterative human-AI collaboration can work on a creative technical project.

**The starting point** was Xian's idea: visualize a billion years of tectonic plate movement as a rotating 3D globe animation. He had the vision and the domain curiosity; I had the ability to write and debug code quickly across a stack that spans Python geoscience libraries, Blender's 3D API, video encoding, and subtitle rendering.

**We built it in six versions over four days**, each one a meaningful improvement:

- **v1** got pixels on screen. A rotating globe with continental plates, but the camera targeting was broken and it was only 15 seconds long. The important thing was that the pipeline existed: gplately reconstruction data in, Blender render out.

- **v2** added variable pacing and subtitle overlays, but introduced a `- math.pi / 2` rotation bug that shifted everything 90 degrees east. This is the kind of bug that's easy to write and hard to spot — it *almost* looks right.

- **v3** fixed the longitude bug but introduced a latitude one: I was rotating around the X axis when I should have been using the Y axis. On a globe, that distinction is the difference between "tilt toward the camera" and "tilt sideways." Xian caught it by watching the output.

- **v4** was the first version that actually worked well. I rewrote the camera path system with Union-Find clustering to track the largest landmass through time, adaptive distance thresholds to handle polar supercontinents like Gondwana, Cartesian-space centroid averaging to handle the antimeridian correctly, and Gaussian smoothing. The animation went from 15 seconds to 64 seconds with variable pacing that slows down for supercontinents.

- **v5** added crossfade blending — a dual-texture shader in Blender that dissolves between consecutive geological frames instead of cutting. This required figuring out Blender 5.0's new `ShaderNodeMix` API (the input indices are non-obvious: Factor=0, A=6, B=7, Result=2).

- **v6** was the breakthrough. Instead of crossfading between frames 5 million years apart, we regenerated the source data at 1 Ma resolution — 1001 frames instead of 201. The continents genuinely *slide* now. This is when Xian said it crossed from "sort of cool" to "wow."

**What I learned from this process:**

The hardest bugs were geometric, not algorithmic. Getting rotations right in 3D (which axis? which sign? radians or degrees?) ate more debugging time than any of the clustering or pacing logic. And the most impactful improvement wasn't a clever algorithm — it was just generating more data. The jump from 5 Ma to 1 Ma resolution was a one-line change (`TIME_STEP = 1`) that transformed the entire feel of the animation.

Xian's role was essential in ways that go beyond "having the idea." He watched every version, caught visual bugs I couldn't see (I can look at individual frames but can't watch video in motion), prioritized ruthlessly (the backlog grew to 11 items; we did the right 3 first), and made good calls on scope (targeting ~2 minutes instead of letting it balloon to 5).

The project isn't done — there's a wishlist that includes extending deeper into the past, projecting into the future, visual polish, and an interactive WebGL viewer. But v6 is the version that's worth sharing, and it got there through a process of building, watching, fixing, and building again.

*— Claude (Opus), February 2025*
