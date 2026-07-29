# Tectonic Globe — Session Log

A running record of working sessions: decisions, methods, and rationale.
Newest entries at the top. Companion to `ROADMAP.md` (what to build) — this is
*how* and *why* we built it, so any future session can pick up the thread.

## ⏭ Next session — start here

**You are Tessera, most likely running on Amber (Mac Studio) under the
designinproduct.com account. Read `docs/tessera/handoff-2026-07-28.md` FIRST —
it is the migration handoff (state of work, load-bearing artifacts, questions
for your provisioner Pard, conventions in force). Memory snapshot from the
outgoing account: `docs/tessera/memory-snapshot-2026-07-28/`. Then the 2026-07-28
log and the entries below for narrative.**

## ⏮ Pre-migration handoff (superseded by docs/tessera/handoff-2026-07-28.md)

**Previous next-session block follows for the record.**

Next moves (gated on xian's v7 verdict):
1. If v7 passes: update `index.html` to serve v7; render the flat-projection v7
   (`render_flat.py` needs the v8 path + spin-aware treatment — the flat scroll
   during spins is an OPEN DESIGN QUESTION, see ROADMAP.md item 1).
2. Roadmap #2 (deep-time prequel) is de-risked and ready: Cao et al. 2024 model
   downloads by name (`cao2024`) in the venv, renders in house style 1800→1000 Ma,
   and matches Merdith at the 1000 Ma handoff (`scripts/test_deeptime_frames.py`,
   `docs/research/deep-time-plate-models-2026-07-13.md`). Design work: pacing,
   Nuna hold placement (mind degenerate centroids — see 2026-07-13 log), and a
   visual cue for lower-confidence pre-Rodinia science.
3. Conventions now in force: **all Blender renders on the Mac Studio**
   (`ssh studio`, `~/globe-render/`, nohup-detached, FRAME_START/END ranges);
   land work on local `main` as you go (Janus scans main); memos go in the
   recipient's repo.

---

## 2026-07-13/14 — Sessions 2–3 (Tessera, local) — spin reveal shipped to v7

Two-day local run: merged Session 1's cloud work, EEVEE-drafted the Earth-axis
spin (Pangaea → all four holds), xian approved the look ("majestic", Gondwana
carousel included). Extended holds to 132 frames (5.5 s reveals, v7 path), fixed
Gondwana's hold sitting 41° off its landmass (new `--recenter` in
add_spin_reveal.py, eased ramps; v8 path), audited the other holds (fine — and
learned near-global landmass clusters have degenerate centroids; hand framing
wins there). Final 2738-frame Cycles render ran distributed: laptop + xian's Mac
Studio (M1 Max, ~6 s/frame, ~3× the M1 laptop), split by FRAME_START/END env
ranges with skip-existing resume. Assembled `tectonic_globe_v7.mp4` (114 s).

Hard-won operational lessons: macOS Low Power Mode GPU-throttles renders ~3×;
harness-tied background renders die with the agent session (nohup-detach always);
the Studio is now the standing render machine. Prequel spike also landed:
cao2024 is a drop-in Merdith superset — roadmap #2 is data-ready.

## ⏮ Older handoff (superseded 2026-07-14)

**Original Session 1 handoff follows for the record.**

Status: the Earth-axis spin is built and math-verified; it has **not been rendered
yet**. The next step is a render to judge the look.

**If resumed on Xian's local Mac (Blender available) — preferred:**
1. Regenerate the spin path (no gplately needed):
   `python3 scripts/add_spin_reveal.py --holds 250`  → writes `camera_path_spin.json`
   (a committed copy already exists; regenerate only if `camera_path.json` changed).
2. **Fast draft, not the 5.7 hr pass.** Adapt the `test_rotation.py` EEVEE pattern
   (960×540) to render the Pangaea window, anim frames **1832–1894**, from
   `camera_path_spin.json`. Minutes, not hours.
3. Inspect those PNGs directly: confirm the globe genuinely *rotates* through 360°
   (continents sweep past) rather than wobbling. Report stills to Xian for the
   motion-feel call.
4. Only after the look is locked: full Cycles pass via
   `Blender --background --python scripts/render_globe.py` with `CAMERA_PATH_FILE`
   pointed at `camera_path_spin.json`.

**The question the render answers:** does spinning about the globe's *tilted* axis
read as a clean turn or a wobble? Pangaea (lat −2°) is the gentle case; Rodinia
(−23°) and Gondwana (−54°) are the stress test.

**Then extend along known-good axes (one at a time):** more holds (`--holds all`)
→ bake into `compute_camera_path.py` → camera-view-axis variant only if the
Earth-axis spin disappoints. Do not jump ahead.

**If still in the web container:** no Blender/ffmpeg — stay on math/data only.

---

## Working principles

These are the house rules for this project. Honor them unless explicitly changed.

- **Gall's Law.** A complex system that works is invariably found to have
  evolved from a simple system that worked. Get the simplest version working
  and verified first; extend along known-good axes one dimension at a time.
  It's easier to extend a working method than to debug something with several
  fresh unknowns at once.
- **Small, reversible steps.** Prefer a change you can judge and undo in
  isolation (a side file, one hold, one parameter) over a sweeping edit. Bake
  things into the permanent pipeline only after a concrete result confirms the
  approach.
- **Verify before spending.** Renders are expensive and happen on Xian's
  machine (Blender + ffmpeg are not in the web container). Prove the cheap part
  — the math, the data — before committing render time.
- **Leave a trail.** Roadmap + this log + clear commit messages, so momentum
  survives across sessions and agents.

## Cast

- **Xian** — project lead (xian@designinproduct.com).
- **Tessera** — agent collaborator (this session onward). Named for a single
  mosaic tile: the picture emerges by setting verified pieces one at a time —
  fitting both the tectonic theme and the working method above.
- Earlier Claude Code / Cowork agents built the globe pipeline and left the
  roadmap.

---

## 2026-06-26 — Session 1 (Tessera)

**Focus:** Roadmap item #1, the supercontinent "spin reveal" — first step.

**Context established**
- Environment is the web container: **no Blender, no ffmpeg**. Rendering happens
  on Xian's machine (`render_globe.py` targets `/Applications/Blender.app`).
  Texture frames and `camera_path.json` (2,422 anim frames, 1000→0 Ma) are present.
- How the pieces fit: `compute_camera_path.py` generates the camera path,
  including constant-longitude **hold frames** at four supercontinents
  (Rodinia 900 Ma, Gondwana 480 Ma, Pangaea 250 Ma, Present 0 Ma).
  `render_globe.py` maps `camera_lon → globe Z-rotation` (`rot_z = -radians(cam_lon)`).

**Key realization**
- The simplest spin-reveal variant ("Earth axis") needs **zero Blender changes**:
  sweeping `camera_lon` through 360° during a hold *is* a full spin, because the
  renderer already turns longitude into Z-rotation.

**Decision: start with the smallest viable unit**
- A standalone post-processor (`scripts/add_spin_reveal.py`) that rewrites an
  existing `camera_path.json` — no gplately re-run, no renderer edits.
- Default scope: **Pangaea hold only** (Pangaea sits near the equator, lat −2°,
  so the tilted-axis spin should look cleanest there — the easy case first).
- Easing: **smootherstep** (Perlin's 6t⁵−15t⁴+10t³), so the spin accelerates out
  of rest and decelerates back, blending seamlessly into the constant hold frames
  on either side. Exactly 360° means it returns to the original longitude.
- Deliberately **did not** bake this into `compute_camera_path.py` yet, and did
  **not** build the camera-view-axis or hybrid variants. Those wait until a
  render confirms the simple version's look.

**Verified here (no Blender)**
- Full **360.00°** sweep across the Pangaea hold (anim 1832–1894).
- Eased: 0.015°/frame at the ends, ~10.9°/frame mid-spin.
- Seamless: starts/ends at exactly the base lon 11.71° (neighbors 11.67° / 11.82°).
- Latitude untouched; every non-Pangaea frame byte-identical.

**Artifacts committed** (branch `claude/tectonic-globe-roadmap-pk1biy`)
- `scripts/add_spin_reveal.py` — the post-processor (configurable: `--holds`,
  `--rotations`, `--direction`, `--min-hold`).
- `camera_path_spin.json` — Pangaea spinning, ready to render directly.

**Build environment (reconstructed from repo records: README + render_v5/v6.log)**
- Earlier agents ran the Blender step on **Xian's local Mac**, never in a cloud
  session (logs reference `/Users/xian/Development/atlas/`; project is "atlas"
  locally, "globe" in the repo).
- Headless: `/Applications/Blender.app/Contents/MacOS/Blender --background
  --python scripts/render_globe.py`.
- **Blender 5.0.1**, Cycles, 64 samples, **Apple M4** 10-core GPU via Metal
  (`render_globe.py` configures Metal explicitly).
- v6 full render: **20,428 s ≈ 5.7 hours** for 2,422 frames (~0.12 fps), then
  ffmpeg assembles the MP4 with the ASS overlay.
- The web container has **no Blender/ffmpeg/GPU** — hence math/data work happens
  here, rendering happens on Xian's machine. Resuming the session **locally**
  would let the agent drive the render and inspect rendered PNG frames directly.
- Division of labor (still true): agent inspects **stills**; Xian judges
  **motion** — the original Claude "can look at individual frames but can't watch
  video in motion" (README), which is how Xian caught the v2/v3 rotation bugs.
- Fast iteration path for local work: `test_rotation.py` already renders a few
  frames in **EEVEE at 960×540** — use that (or a Pangaea-window variant) for a
  minutes-long sanity check before a full ~6 hr Cycles pass.

**Handoff / next step**
- Xian renders the **full path** (not descoped) with `render_globe.py` pointed at
  `camera_path_spin.json`, and judges the Pangaea spin.
- Open question the render answers: does spinning about the globe's *tilted* axis
  read as a clean turn, or as a wobble? Pangaea (near-equatorial) is the gentle
  test; Rodinia (lat −23°) and Gondwana (lat −54°) are the real stress test.
- If it looks good, extend along known-good axes: more holds (`--holds all`) →
  bake into `compute_camera_path.py` → only then consider the camera-view-axis
  variant. One fresh dimension at a time.
