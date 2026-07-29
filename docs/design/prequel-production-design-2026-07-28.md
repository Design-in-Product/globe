# Prequel Production Design — Roadmap #2 (1800 → 1000 Ma)

*Tessera, 2026-07-28 (first Amber session). Status: DRAFT for xian assessment.
Claims marked VERIFIED (artifact exists) / BELIEVED (my read) / OPEN (xian call).*

## What's already settled

- **Model: cao2024** — full-plate topological, 1800–0 Ma, Merdith-2021 superset;
  drop-in at the 1000 Ma handoff. VERIFIED (research doc 2026-07-13; live handoff
  check 7/28 — the model auto-downloads via PlateModelManager into
  `data/plate-models/`, working in the Amber `.venv`).
- **Uncertainty treatment: ensemble superposition** — 9 members, per-plate pole
  jitter (incoherent) + time jitter (coherent), averaged. VERIFIED and
  **xian-confirmed 2026-07-28** ("pretty much what I envisioned").
- **Prequel is a separate video** connecting end-to-end with the main film
  (roadmap: "series of videos that connect end-to-end, not one massive file").

## Proposed design

### Timeline and pacing

- **Span:** 1800 → 1000 Ma (800 Myr), ending exactly where the main film begins.
- **Cadence: 1 Ma per geo frame = 801 geo frames**, matching the main film's
  visual speed so the two cut together without a tempo jump. BELIEVED right;
  OPEN: pre-Rodinia motion is slower-paced science (fewer events per 100 Myr) —
  xian may prefer 2 Ma/frame (~half the runtime) if the raw timeline drags.
- **Anim structure mirrors v8:** variable pacing + holds, ~24fps. Raw timeline
  ≈ 33 s at main-film tempo before holds; with two holds + reveals ≈ 45–55 s.

### Holds (two, not four)

1. **Nuna/Columbia hold** (~1600 Ma, position hand-picked after seeing frames).
   **Hand-framed, not centroid-derived** — Nuna is a near-global landmass
   cluster and area-weighted centroids DEGENERATE for those (lesson 4 of the
   handoff, VERIFIED on Pangaea 7/13). I will pick the camera framing from
   rendered candidates and bring the choice to xian with stills.
2. **Terminal hold at 1000 Ma: Rodinia assembling** — the convergence point.
   Frame it to match the main film's opening view exactly, so the prequel's
   last frame IS the main film's first frame (same camera lon/lat, same
   texture). VERIFIED possible: cao2024 contains the Merdith 1000 Ma state.

### Uncertainty ramp

u(t) linear 1.0 → 0.0 across 1800 → 1000 Ma, exactly the ramp of the
xian-confirmed strip (`test_ensemble_uncertainty.py` FRAMES). The film opens as
a probability cloud and crystallizes into the single reconstruction as it
reaches the era where the science firms up. Members: N=9 (confirmed at strip
quality). OPEN: whether N should rise for the film (visual smoothness of the
cloud under motion — decide from a short moving draft, not stills).

### Render cost (measured, not guessed)

Tonight's strip: 46 member-renders ≈ 8 min in the Amber venv ≈ **~10 s per
member-render** (2048×1024, cartopy fill + DateLineWrapper). VERIFIED.

- 801 frames × 9 members ≈ 7,200 member-renders ≈ 20 h single-process.
- **Time-sliced across 8 workers ≈ 2.5–3 h** on Amber (renders are
  embarrassingly parallel across geo frames; nohup-detached per convention,
  `FRAME_START`/`FRAME_END` splitting already the house pattern). BELIEVED —
  verify memory headroom with 8 concurrent cartopy processes before the full
  run; fall back to 4 workers (~5 h) if needed.
- At 2 Ma cadence, halve all of the above.
- Then the standard Blender pass over the averaged textures (~6 s/frame on
  Amber, VERIFIED 7/14) for the globe version.

### Draft ladder (the discipline that works)

1. Moving draft, one 50-Myr window at 4 Ma cadence, strip-res — does the cloud
   read in MOTION? (It's only ever been judged as stills.) → xian.
2. Full-span draft at low res + 4 Ma cadence → pacing + Nuna hold placement
   candidates → xian picks framing.
3. Production texture render (801 × 9) → Blender globe pass → assembly.

## Batched questions for xian (none block steps 1–2)

1. Cadence: 1 Ma/frame (tempo-matched) or 2 Ma/frame (tighter film)? Default
   if unanswered: 1 Ma.
2. Era labels pre-1000 Ma: Proterozoic period names (Statherian → Tonian) in
   the same overlay style? Default: yes, same style.
3. Does the prequel get hold spin-reveals like v8, or stay static-hold (its
   drama is the uncertainty cloud, not the spin)? Default: static holds for
   the draft; revisit after seeing it.
4. A "reconstruction confidence" annotation cue for pre-1 Ga (research doc
   flagged the science is genuinely lower-confidence)? The u-ramp itself may
   BE the cue — my read is no extra annotation. Default: none.
