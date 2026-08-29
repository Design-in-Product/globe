# Tessera Session Log — 2026-08-29

**xian's go-ahead relayed via Pard: scope the WebGL scrubber (roadmap item
5), commit as work lands.**

## Scrubber scoping — two committed passes

Audited before designing rather than assuming the roadmap note ("frames
already texture-ready") meant "ready to ship": measured the actual asset
sets on Amber. Main-film equirect textures are 1006 frames @ 4096×2048,
1.2 GB; prequel's are 801 frames @ 2048×1024, 337 MB. The site is static
GitHub Pages (single `main` branch, `CNAME`, no build step, no server) —
1.5 GB of PNGs is not a committable asset set for that hosting model,
independent of which JS renders it.

Recommended approach (`docs/design/scrubber-scope-2026-08-29.md`): sparse
keyframes at the film's own already-named eras (~21 across both films,
free — the labels already exist in `camera_path_spin_v8.json` and
`prequel_camera_path.json`), crossfaded via a shader that ports the
technique `render_globe.py`'s Blender material already uses at texture
transitions (dual-texture Mix node → GLSL two-texture blend). Free spin
via Three.js OrbitControls; time-scrub feels continuous via the crossfade
even though the keyframe data is sparse — same approximation the shipped
film already makes, not a new compromise.

Phased: spike (throwaway feel-test) → sparse-keyframe MVP (~21 textures,
few MB, no LFS/CDN needed) → denser sampling if wanted → true per-Myr
density as an explicit future infra decision (external hosting), not
bundled into this scope.

Four open questions left for xian in the doc (§7): placement (new mode vs.
hero replacement), Phase 1 range (main film only vs. both films from the
start), resolution/format budget (2048×1024 WebP working default), and
whether to see the Phase 0 spike before committing to the real export
pipeline. Cleared to start the spike under the existing go-ahead; holding
the asset-export commitment (Phase 1 proper) for an answer since the
resolution/range choice is mildly annoying to redo.

`ROADMAP.md` item 5 updated to point at the scope doc and mark it scoped.
