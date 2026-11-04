# NOTICE — third-party data, libraries and tools

Tectonic Globe's own licences are in `LICENSE` (MIT, code) and
`LICENSE-MEDIA.md` (CC BY 4.0: films, stills, keyframes, poster). This file lists what the project is
built on and the terms each piece carries. Licences below were read from the
hosting record on 2026-11-03 (Zenodo / Figshare / OSF API), not from memory.

## Plate reconstructions redistributed in `data/plate-models/`

| Dataset | Used for | Licence | Record |
|---|---|---|---|
| Merdith et al. 2021, *Extending full-plate tectonic models into deep time: Linking the Neoproterozoic and the Phanerozoic* (Earth-Science Reviews) | Main film, 1000 Ma → today; Explore keyframes | **CC BY 4.0** | https://doi.org/10.5281/zenodo.10346399 (v1.2.4 as downloaded: 10.5281/zenodo.13635864) |
| Cao et al. 2024, *Earth's tectonic and plate boundary evolution over 1.8 billion years* (Geoscience Frontiers) | Prequel, 1800 → 1000 Ma | **CC BY 4.0** | https://doi.org/10.5281/zenodo.11536686 (v2.4 as downloaded: 10.5281/zenodo.13628813) |

Both are distributed through the EarthByte GPlates ecosystem and fetched by
`plate_model_manager`; the copies under `data/plate-models/` are unmodified.
Attribution is required when they are passed on; this file and the site's
data section carry it.

## Data used but not redistributed

| Dataset | Used for | Licence | Record |
|---|---|---|---|
| Davies, Green & Duarte 2018, four supercontinent scenarios (land–sea grids at 20 Myr steps) | Sequel, today → +250 Myr; Explore future keyframes | **CC0 1.0** | https://doi.org/10.17605/OSF.IO/8NEQ4 (grids live in `~/globe-render/future-scenarios/`, not in git) |

## Surveyed for the biome/climate layer (roadmap item 8, not in use)

| Dataset | Licence | Record |
|---|---|---|
| CESM1.2.2 540 Myr climate + vegetation dataset (Zhang et al., *Scientific Data* 2022) | **CC BY 4.0** | https://doi.org/10.6084/m9.figshare.19920662 |
| Phanerozoic Köppen–Geiger climate classes (Zenodo, 3 versions, all 2022-03-31) | **CC BY 4.0** — the *Data in Brief* article describing it is CC BY-NC-ND 4.0; the dataset is not | https://doi.org/10.5281/zenodo.6402040 |
| Scotese & Wright 2018, PALEOMAP PaleoDEMs (the paleogeography both of the above ride on) | **CC BY 4.0** | https://doi.org/10.5281/zenodo.5460860 |
| BRIDGE/Bristol Phanerozoic ensemble (Valdes et al.) | not verified | — |

## Libraries and tools

| Component | Role | Licence | Note |
|---|---|---|---|
| pygplates 1.0.0, gplately 2.0.0, plate_model_manager | Reconstruction → equirectangular frames | GPL-2.0 | Imported by the Python scripts; not redistributed here. The scripts are MIT; a bundled distribution that shipped these libraries would carry the GPL for that bundle. |
| matplotlib, numpy, cartopy, xarray, netCDF4, Pillow | Frame generation, grid reading | PSF / BSD-style | |
| Three.js 0.160.0 | Explore page | MIT | Loaded from a CDN |
| Blender (Cycles) | Rendering | GPL | Output images are not covered by Blender's licence |
| ffmpeg + libass | Assembly, burned-in time and era labels (Arial, from the host system) | LGPL/GPL | Output video is not covered |
