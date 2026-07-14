# Deep-Time Plate Reconstruction Models (>1 Ga) — Research Report

*Researched 2026-07-13 (Tessera, background research agent) for Roadmap #2, the deep-time prequel.*

## Bottom line

There is a single, clear best answer for the prequel: **Cao et al. (2024), "Earth's tectonic and plate boundary evolution over 1.8 billion years"** (*Geoscience Frontiers*). It is a full-plate **topological** model spanning **1800 → 0 Ma** that was built by taking **Merdith et al. (2021) as its 1.0 Ga → present base** and extending it back to 1.8 Ga. Because the current animation already uses Merdith 2021, this model is a drop-in superset — the stitching problem is solved by construction (same reference frame, same lineage). Files are on Zenodo under CC-BY-4.0 and it is already integrated into the GPlates ecosystem as model ID `CAO2024`.

## 1. Models older than 1 Ga

| Model | Span | Type | Plate polygons + rotations? | Files available |
|---|---|---|---|---|
| **Cao et al. 2024** | 1800–0 Ma | **Topological (full-plate)** | Yes — rotations, topologies, continental/static polygons, coastlines, COBs | Zenodo [13628813](https://zenodo.org/records/13628813) (`1.8Ga_model_GSF.zip`, ~20.7 MB); supplementary [13340841](https://zenodo.org/records/13340841). CC-BY-4.0 |
| **Merdith et al. 2021** | 1000–0 Ma | **Topological (full-plate)** | Yes — rotations, topologies, static polygons, coastlines, cratons | Zenodo [4485738](https://zenodo.org/records/4485738); bundled in GPlates 2.3+ |
| Merdith et al. 2017 | ~1000–520 Ma | Full-plate (earlier version) | Yes | Superseded by Merdith 2021 |
| **Li et al. 2008** (Rodinia synthesis) | 1100–530 Ma | **Static / continental-drift** | Rotations + static polygons only; no evolving boundaries | GPlates sample data as `Li2008` |
| Pisarevsky et al. 2014 | ~1.8–1.0 Ga | Continental-drift (paleomag frame) | Blocks + rotations, no topologies | Used as a base model *inside* Cao 2024 |
| Condie et al. 2021 | late Paleoproterozoic–Mesoproterozoic | Continental-drift | Continental blocks | Also folded into Cao 2024 |
| Li et al. 2023 | 2.0–0.54 Ga | Paleomag continental reconstruction | Blocks + rotations; not full-plate | Paper-level; contested (published Comment). Not recommended |
| PALEOMAP (Scotese) | ~1100–0 Ma | Static, paleogeographic | Coastlines + static polygons; no topologies | Widely distributed but not full-plate |

Key distinction: only **Cao 2024** and **Merdith 2021** are *continuous topological* full-plate models in this depth range. Everything else pre-1 Ga is a static/continental-drift reconstruction — rigid blocks without the evolving plate-boundary topologies needed for full-plate velocity/age-grid work. Cao 2024's achievement is precisely that it built topologies over those older continental-drift inputs.

## 2. gplately / pygplates consumability

- **Cao 2024** — Yes. Standard EarthByte GPlates layers (`.rot` rotations + `.gpml/.gpmlz` topologies, continents, coastlines, static polygons). Loadable directly in pygplates/gplately; registered in the GPlates Web Service as `CAO2024` (StaticPolygons, Coastlines, ContinentalPolygons, Topologies, COBs), so DataServer access works too. Topological → supports plate velocities, plate IDs, age-grid workflows across the full 1.8 Ga.
- **Merdith 2021** — Yes, fully; first-class gplately built-in (`MERDITH2021`).
- **Li 2008** — Loadable as static polygons + rotations, but **not topological** — snapshot-style only.

## 3. Stitching / reference-frame compatibility at 1000 Ma

Cao et al. 2024 **explicitly adopts Merdith et al. (2021) for the 1.0 Ga → present interval** (minor Neoproterozoic adjustments), using Pisarevsky 2014 / Condie 2021 as the pre-1.0 Ga base. Both are in a **paleomagnetic reference frame**. So:

- No merge needed — **Cao 2024 already contains the Merdith-based 0–1000 Ma portion**, continued seamlessly to 1800 Ma. It *is* the published combined/extended model.
- Practical implication: **replace** the current Merdith-2021 dataset with Cao 2024 and get 1.8 Ga → present in one continuous timeline. Verify the 0–1000 Ma frames still match current renders (should be near-identical, minor Neoproterozoic tweaks).

Caveat to check at build time: confirm the current pipeline uses Merdith 2021's *paleomagnetic* rotation frame (not a mantle/absolute frame like Müller 2022). Cao 2024 is paleomagnetic; any mantle-frame or TPW correction must be handled consistently across the boundary.

## 4. Recommendation

**Use Cao et al. (2024) as the prequel, and treat it as a full replacement for Merdith 2021 rather than a bolt-on.**

- Download: https://zenodo.org/records/13628813 (`1.8Ga_model_GSF.zip`, CC-BY-4.0). Supplementary: https://zenodo.org/records/13340841
- Paper: Cao, X., Collins, A.S., Pisarevsky, S., Flament, N., Li, S., Hasterok, D., Müller, R.D. (2024), *Geoscience Frontiers*, 101922. DOI: https://doi.org/10.1016/j.gsf.2024.101922
- EarthByte landing page (context + errata): https://www.earthbyte.org/geoscience-frontiers-earths-tectonic-and-plate-boundary-evolution-over-1-8-billion-years/
- GPlates Web Service model ID: `CAO2024` (https://gwsdoc.gplates.org/models/)

Suggested integration path: unzip the Zenodo archive, load the `.rot` + topology/continent `.gpml(z)` into the existing gplately pipeline exactly as Merdith 2021 loads now, extend the frame range to 1800 Ma, and spot-check the 900–1000 Ma handoff frames against current output.

## Uncertainty flags

- **Confirm exact layer filenames on unzip** — the Zenodo web listing shows only the single 20.7 MB zip; internal `.rot`/`.gpml` names couldn't be enumerated remotely (errata reference `shapes_continents.gpmlz`, `Paleomagnetic_poles.gpml`; GWS registration confirms full topological layers).
- **Pre-1.0 Ga is genuinely lower-confidence science.** Paleomagnetic control thins before Rodinia; Nuna/Columbia (~1.8–1.3 Ga) configurations are actively debated. Affects scientific accuracy, not GPlates compatibility. Consider a visual/annotation cue that pre-1 Ga is more schematic.
- **1.8 Ga is the current frontier** — nothing published extends a topological full-plate model reliably beyond it.
