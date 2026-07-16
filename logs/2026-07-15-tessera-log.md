# Tessera Session Log — 2026-07-15

**Session:** Continuation on worktree branch `claude/roadmap-review-planning-418a49`.

## Session start

- xian's verdict on the Mollweide morph concept draft: **"That is very cool!"** — motion approved.
- Two queued artifacts to produce: (1) production-quality morph (per-pixel-scale mesh + bilinear sampling, 1920×960) to prove crispness; (2) prequel fuzziness test strip (graduated haze/blur on Nuna-era frames).

## Work log

- 09:53 — xian checked in; closed out the 07-14 log, pushed main.
- 09:55 — **Mail/brief check:** no new incoming mail. Brief still June 26 — but hub log claims "receipt 2026-07-14 — 8/8 delivered" while nothing reached our repo (origin has no new commits). Delivery mechanism vs receipt disagree; my 07-13 memo to Janus also sits unprocessed (hub pulse-log shows cron trouble: missed STOP, re-armed twice). Flagged to xian to raise with Janus.
- 10:00 — Upgraded `test_flat_morph.py` to production quality: argparse (res/mesh/source/out), per-pixel-scale mesh, bilinear texture sampling (scipy map_coordinates, grid-wrap). HD render (1920×960) running in background.
- 10:05 — **Fuzziness test strip delivered**: 6 cao2024 frames 1800→1000 Ma with graduated blur + desaturation + contrast haze (100%→0%), labeled strip. New `scripts/test_fuzziness_strip.py`. Tunables: MAX_BLUR 6px, MAX_DESAT 0.45, MAX_DECONTRAST 0.25, haze tint (60,80,100) @ 0.18 max.
- 10:20 — **HD morph delivered** (~10 min render, 288 frames): per-pixel mesh + bilinear sampling is crisp — rotation midpoint frame (Panthalassa centered, Pangaea wrapped around the ellipse rim) is a stunner. Flat-v7 technique proven end-to-end.

- 18:48 — xian (remote): HD morph video wouldn't play. Diagnosis: `moov` atom at end of file (no faststart) → streaming/mobile players fail. Remuxed (`-c copy -movflags +faststart`) and resent. **Convention: always `-movflags +faststart` on preview MP4s** (the v6/v7 site videos already stream fine — GitHub Pages serves range requests — but previews sent to xian's phone must be faststart).

- 19:05 — xian: **HD morph "very smooth action"** — flat-v7 technique approved. Fuzziness strip hadn't reached them (remote-session change dropped the file); resent.

- 19:20 — **xian redirected the uncertainty treatment, decisively better**: blur = "vision fails at a distance"; what the science says is *positions become a probability cloud* — superposition of possibilities, fuzzy edges because they're far from the probability locus (particle metaphor, "fourier superimposition"). Implementation: **ensemble rendering** — N perturbed reconstructions averaged (per-plate rotation-pole jitter σ=5°·u incoherent + coherent time jitter σ=25 Ma·u so smear follows true trajectories). New `scripts/test_ensemble_uncertainty.py` (9 members × 6 times, cao2024), running in background.
- Lens question answered (xian asked count + opinion): ~12 morph-viable projections (continuous forward mapping; interrupted ones like Dymaxion can't morph — though "map tears apart" noted for someday). Pitched **one lens per hold, arc from map-ness to globe-ness**: Rodinia sinusoidal → Gondwana south-polar azimuthal (flat cousin of the polar carousel) → Pangaea Mollweide (proven) → **Present orthographic — the flat map becomes a globe, the two videos converge at the present**.

- 19:45 — Ensemble spike debugging: first pass rendered a wall of continent color — naive `ax.fill`+Geodetic wraps antimeridian-crossing polygons around the whole map (bug present even unperturbed; the old `render_frame_pygplates` fallback shares it). Fix: `pygplates.DateLineWrapper`. Second pass: geometry right, ocean white — figure facecolor isn't inherited by the `buffer_rgba` grab path; fixed with explicit `facecolor=` on the figure. Third pass ✓.
- 20:00 — **Ensemble-superposition strip delivered.** 1800 Ma reads as true probability clouds (cratonic cores dense, fringes dissolving); collapses to single crisp reality at 1000 Ma. Exactly xian's particle metaphor, rendered from real perturbed reconstructions rather than image filters. Known nit: "1 superimposed possibilities" label grammar.

## Awaiting xian

1. Ensemble-superposition strip verdict (supersedes blur strip).
2. Lens-per-hold pitch: sinusoidal → polar azimuthal → Mollweide → orthographic (flat map becomes the globe at present day).
