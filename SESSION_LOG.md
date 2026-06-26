# Tectonic Globe — Session Log

A running record of working sessions: decisions, methods, and rationale.
Newest entries at the top. Companion to `ROADMAP.md` (what to build) — this is
*how* and *why* we built it, so any future session can pick up the thread.

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

**Handoff / next step**
- Xian renders the **full path** (not descoped) with `render_globe.py` pointed at
  `camera_path_spin.json`, and judges the Pangaea spin.
- Open question the render answers: does spinning about the globe's *tilted* axis
  read as a clean turn, or as a wobble? Pangaea (near-equatorial) is the gentle
  test; Rodinia (lat −23°) and Gondwana (lat −54°) are the real stress test.
- If it looks good, extend along known-good axes: more holds (`--holds all`) →
  bake into `compute_camera_path.py` → only then consider the camera-view-axis
  variant. One fresh dimension at a time.
