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

### 5. Interactive WebGL viewer

Equirectangular frames are already texture-ready (4096x2048).

- Three.js sphere + camera_path.json for scrubable/interactive version
- User could spin the globe freely, scrub through time
- The spin reveal work (item 1) would directly inform the interaction model here

---

### 6. Landing page enhancements

- Roadmap section on the site (once this list is finalized by Xian)
- Case study / "How This Was Built" — the README narrative is already written for an audience, could become its own expanded page section
- Gold/blue color theme when render palette is ready

---

## Suggested sequencing

1. **Spin reveal** — small scope, high visual impact, informs everything else
2. **Deep time prequel** — Xian's prior momentum, extends the core content
3. **Future projection** — natural sequel, parallel research track
4. **Visual polish** — can happen anytime, incremental
5. **WebGL viewer** — builds on all of the above
6. **Landing page** — evolves as content grows
