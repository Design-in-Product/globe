# Tectonic Globe Roadmap

## Captured from working sessions (Feb 2025 – Feb 2026)

### 1. Supercontinent "spin reveal" ← explore next

During the variable-pacing hold frames at major supercontinents (Rodinia, Gondwana, Pangaea, present day), add a slow 360° rotation to reveal the full surface. Worth exploring BEFORE the deep-time prequel, since it affects the overall animation feel.

**Globe render (Blender):**
- Preferred approach: rotate on an axis derived from the current camera view ("orbit the interesting side"). We're flying a magic camera through space — any flight path is valid.
- The hold frames already exist in camera_path.json (48-60 extra frames per supercontinent). Could extend them and sweep camera_lon through 360° instead of holding constant.
- Prototype idea: render just the Pangaea hold frames three ways (Earth axis, camera-view axis, hybrid tilt+orbit) and compare.

**Flat projection (PIL/ffmpeg):**
- A straight horizontal scroll smears badly at the poles on equirectangular projection.
- Ideas to explore:
  - Sinusoidal or figure-8 path through lat/lon space for a more even "tour"
  - Temporary projection switch during the reveal (e.g., Mollweide or orthographic snapshot)
  - Some geometric path that works well for BOTH globe and flat simultaneously — worth investigating whether such a path exists (e.g., an orbit that traces a great circle maps to a sinusoid on the flat projection)
- Open question: does the reveal need to look the same in both views, or can they diverge?

**Implementation lives in:** `compute_camera_path.py` (camera targeting), `render_globe.py` (Blender rotation), `render_flat.py` (flat frame assembly)

---

### 2. Deep time — prequel series

Extend further into the past beyond 1 Ga (Rodinia).

- Strategy: series of videos that connect end-to-end, not one massive file
- Needs research into plate models covering >1 Ga (e.g., Li et al. 2008 goes to ~1.1 Ga, some extend to ~1.8 Ga)
- This was where Xian left off in a prior Claude session (Cowork or Code)
- Pipeline is parameterized (TIME_STEP, time range) so the code changes are small; the bigger question is data availability and model compatibility

---

### 3. Future projection — sequel

Speculative plate tectonics going forward from present day.

- Published models: Pangaea Ultima (~250 Ma future), Amasia (~200 Ma), Novopangaea (~200 Ma), Aurica (~250 Ma)
- Would be a "sequel" video connecting from present day forward
- Xian: "supercurious" about this direction
- Same pipeline, different data source

---

### 4. Visual polish — cinematic color palette

Shift from current earth tones to gold/blue movie-poster aesthetic.

- CSS custom properties already in place on the landing page (--bg, --accent, etc.) for easy theming
- Render-side changes: Blender lighting energy/color, background color, continent fill in generate_frames.py
- Could be done incrementally — site theme first, then re-render frames to match

---

### 5. Interactive WebGL viewer — SCOPED 2026-08-29, xian go-ahead given

Equirectangular frames are already texture-ready (4096x2048) — **but not
web-deliverable at that density**: full audit in
`docs/design/scrubber-scope-2026-08-29.md`. 1006 main-film + 801 prequel
frames (1.5 GB) can't reasonably be committed to a static GitHub Pages
site. Recommended approach: sparse keyframes at the film's own named eras
(~21 total) + a crossfade shader porting the technique the Blender render
pipeline already uses at texture transitions — spin is real (Three.js
OrbitControls), time-scrub feels continuous via the crossfade even though
the underlying data is sparse.

- Three.js sphere + camera_path.json for scrubable/interactive version
- User could spin the globe freely, scrub through time
- The spin reveal work (item 1) would directly inform the interaction model here
- Phased: spike → sparse-keyframe MVP → denser sampling → (stretch) true
  per-Myr density, which would need external asset hosting, not just more
  scoping. Open questions for xian in the scope doc §7 (placement, range,
  resolution budget, spike-first-or-not).

---

### 6. Landing page enhancements

- Roadmap section on the site (once this list is finalized by Xian)
- Case study / "How This Was Built" — the README narrative is already written for an audience, could become its own expanded page section
- Gold/blue color theme when render palette is ready

---

### 7. Physical product — someday/maybe

Joe LaMantia (xian's call, 2026-08-11): turn this into an actual physical
product — a globe on the desk, display or mechanical (a steampunk
crank-and-wooden-plates version came up too), Kickstarter-funded, possibly
merged with Dynamic Atlas (xian's sibling project) on the same hardware.

**Xian's read (2026-08-12): loves the idea, lacks the bandwidth — someday/
maybe, not now.** Two things do carry forward:

- **The WebGL scrubber (item 5) is the shared prerequisite either way** —
  hardware or not, "pick a moment and a camera angle" has to exist in
  software first. Xian agrees this is needed regardless of the hardware
  decision, which raises its priority independent of this item.
- **Lesser stepping-stone idea, xian's: print-on-demand.** User scrubs to
  the still they want (needs item 5) and orders it printed — globe gores,
  a flat print, whatever POD format is feasible — no display/mechanical
  R&D, no fulfillment risk beyond a standard POD vendor integration.
  Framed as a possible way to raise money toward the bigger physical-globe
  version rather than a competing scope.

No work started. Revisit once item 5 exists.

---

### 8. Biome/paleoclimate painting — someday/maybe, speculative

Xian (2026-08-12): does the roadmap ever paint landmasses with real detail
— Pangaea's central desert, its forested fringes — instead of one flat
fill color? It doesn't currently (`CONTINENT_COLOR` is a single flat tone
in `generate_prequel_frames.py` and the main-film scripts; item 4 is a
palette shift, not per-region variation).

**Research done** (`docs/research/paleoclimate-biome-painting-2026-08-12.md`,
speculative, not scoped): real deep-time paleoclimate/vegetation datasets
exist and are downloadable now. Best fit: **CESM1.2.2 540 Myr dataset**
(55 snapshots, 10 Myr steps, temp/precip + vegetation via dynamic global
vegetation model, CC BY 4.0, Scotese & Wright 2018 paleogeography). A more
directly "paintable" Köppen–Geiger classification dataset also exists but
is CC BY-NC-ND (noncommercial, no-derivatives — a real constraint given
the Kickstarter/POD conversation in item 7). Both ride on Scotese
paleogeography, not Merdith2021/cao2024 — same *kind* of registration
problem the prequel's terminal-seam fix solved, but harder (raster grid
onto plate boundaries, not plate-polygon onto plate-polygon).

No work started, purely speculative per xian's request to open up ideas
without committing.

---

## Suggested sequencing

1. **Spin reveal** — small scope, high visual impact, informs everything else
2. **Deep time prequel** — Xian's prior momentum, extends the core content
3. **Future projection** — natural sequel, parallel research track
4. **Visual polish** — can happen anytime, incremental
5. **WebGL viewer** — builds on all of the above; also the shared
   prerequisite for item 7's physical-product path (scrubber = the
   software both the display and the print-on-demand version need)
6. **Landing page** — evolves as content grows
7. **Physical product** — someday/maybe, gated on item 5
