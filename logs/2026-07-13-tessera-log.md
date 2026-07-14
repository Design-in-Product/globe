# Tessera Session Log — 2026-07-13

**Session:** Local follow-on session (planned with xian in prior chat). Worktree branch `claude/roadmap-review-planning-418a49`.

**Note:** This is the first session log — Tessera adopts the DinP session-log tradition as of today.

## Session start

- Read cross-pollination brief (`docs/briefs/cross-pollination/current.md`). Brief is dated **2026-06-26** — 17 days stale; no daily delivery since the welcome brief. Worth flagging to Janus/xian.
- Reviewed `ROADMAP.md` (committed 2026-03-09). Six items; suggested sequencing puts the **supercontinent spin reveal** first ("explore next").
- Repo state: clean; last substantive render work was flat v6 + landing page redesign (2026-02-28). June commits were network onboarding only.

## Roadmap review (state as of today)

1. **Spin reveal** — not started. Prototype plan already sketched in roadmap: render Pangaea hold frames three ways (Earth axis, camera-view axis, hybrid tilt+orbit) and compare. ← next up
2. **Deep time prequel** — research phase; needs plate-model availability check (>1 Ga).
3. **Future projection sequel** — research phase; parallel track.
4. **Visual polish (gold/blue)** — not started; can be incremental, site theme first.
5. **WebGL viewer** — blocked-ish on spin-reveal learnings (informs interaction model).
6. **Landing page enhancements** — evolves with content.

## Plan for this session

- [ ] Roadmap review with xian (this conversation)
- [ ] Scope the spin-reveal prototype: read `compute_camera_path.py`, `render_globe.py`, `camera_path.json` hold-frame structure
- [ ] Verify local render prerequisites (Blender availability, source frames for Pangaea holds)
- [ ] Decide prototype cut with xian; begin implementation if time allows

## Work log

- 16:57 — Session opened. Log created; roadmap review prepared for xian.
- 17:05 — Memo to Janus delivered to `~/Development/designinproduct/docs/mail/` (mail goes in the *recipient's* repo — noting for future sends). Includes the stale-brief flag.
- 17:08 — **Found the missing Session 1 record**: remote branch `claude/tectonic-globe-roadmap-pk1biy` (cloud, 2026-06-26) had `SESSION_LOG.md`, `scripts/add_spin_reveal.py`, and `camera_path_spin.json`. Merged into this worktree branch. Log convention to reconcile: Session 1 used root `SESSION_LOG.md` (newest-first); today started `logs/` per CLAUDE.md. Keeping both for now — SESSION_LOG.md as the cross-session narrative, logs/ for dailies.
- 17:12 — Re-verified spin path locally: anim window 1832–1894 is 63 Pangaea frames (250 Ma, lat −2.16°), lon sweeps exactly 360.0° and returns to base 11.71°, single texture geo_frame 750 (present in `frames/`).
- 17:15 — Wrote `scripts/test_spin_pangaea.py`: EEVEE 960×540 draft of the spin window per the Session 1 handoff, adapted from `test_rotation.py`. Ready to run headless.
- **Blocker:** No Blender on this machine (`/Applications/Blender.app` absent, no brew cask, not in PATH). ffmpeg ✓, frames ✓ (1006 textures), path ✓. Asked xian: install Blender or point me at it.
- 17:20 — Mystery resolved: `render_v6.log` shows v6 rendered on *this* machine from `~/Development/atlas` (Blender 5.x-era deprecation warnings). Blender was removed sometime after February. xian approved reinstall → `brew install --cask blender` running in background.
- 17:22 — Launched background research agent: deep-time plate models >1 Ga (roadmap #2) — coverage, gplately compatibility, stitchability to Merdith 2021 at 1000 Ma.
- Log convention decision (xian): dailies in `logs/` are fine — keep them consistent. `SESSION_LOG.md` stays as cross-session narrative; add a summary entry there at session end.
- 17:30 — Blender 5.1.2 installed via brew cask (`/Applications/Blender.app`, xian-approved). Note: prior renders used 5.0.1; 5.1.2 rendered the test scripts without changes.
- 17:35 — Parallel-session note from xian: an earlier restart attempt landed on branch `claude/globe-roadmap-execution-3e7714` (one commit, 17:00: its own kickoff log + memo). No code/render work there; xian will stand it down. Its memo never reached Janus (was written to our repo, not delivered).
- 17:45 — **First spin-reveal render complete.** `test_spin_pangaea.py` ran clean on Blender 5.1.2: 63 EEVEE frames, ~15 min. Stills verified: genuine 360° rotation (Pangaea face-on → Panthalassa antipode at midpoint → seamless return; first/last frames identical). No wobble apparent in stills — near-equatorial lat (−2°) as predicted the gentle case. Preview MP4 assembled and sent to xian for the motion call.
- 17:45 — Deep-time research (roadmap #2) returned: **Cao et al. 2024** is the clear prequel answer — full-plate topological model 1800→0 Ma, built ON Merdith 2021 (same frame, drop-in superset; stitching solved by construction). Report saved to `docs/research/deep-time-plate-models-2026-07-13.md`.

## xian's calls (18:00)

1. Pangaea spin **approved** ("looks good").
2. Stress tests green-lit.
3. Cao 2024 download green-lit.

- 18:05 — Reconciled shared memory after the parallel session stood down: updated `render-environment-status` (Blender now installed), fixed memo convention in `roadmap-execution-mandate`, added `memo-delivery-convention`, removed the resolved orphaned-commit breadcrumb. Branch `claude/globe-roadmap-execution-3e7714` still exists locally — deletion is xian's call (nothing on it we need).
- 18:10 — Generated `camera_path_spin_all.json` (`add_spin_reveal.py --holds all`): 4 spin windows — Rodinia 227–276 (50f, lat −23.4°), Gondwana 1218–1255 (38f, lat −54.2°), Pangaea 1832–1894 (63f, −2.1°), Present 2361–2421 (61f, +28.8°).
- 18:12 — Wrote `scripts/test_spin_window.py` (parameterized draft renderer, supersedes the Pangaea-only script). Rodinia + Gondwana EEVEE drafts running in background; Cao 2024 zip downloading to `data/deep-time/`.
- 18:20 — **Cao 2024 downloaded + unzipped** (`data/deep-time/1.8Ga_model_GSF/`, 115 MB unpacked): rotations split 1800–1000 + 1000–0, era-sliced plate-boundary topologies, static polygons/coasts/continents/COB, GPlates project file. Filenames confirmed (research uncertainty resolved).
- 18:25 — **Prequel integration will be tiny**: `generate_frames.py` loads its model via `plate_model_manager.get_model("Merdith2021")`, and the working venv (`~/Development/atlas/.venv`, gplately 2.0.0) already registers **`cao2024`** as an available model name. Swap the name + extend the time range ≈ the whole code change. (venv note: gplately imports fine there; PyGMT warning is nonfatal.)
- 18:30 — **Stress tests rendered** (Rodinia 227–276, Gondwana 1218–1255; both clean runs). Stills: Rodinia reads as a clean tilted turn; Gondwana (−54°) reads as a "polar carousel" — looking down toward the pole while land wheels around. Previews sent to xian for the motion call.
- 18:40 — xian's verdict: **"majestic"** — all three spin looks approved. Proceeding to pacing.
- 18:45 — Extended `add_spin_reveal.py` with `--target-hold`: pads holds to uniform length before spinning. Generated **`camera_path_spin_v7.json`**: 132-frame holds (5.5 s/reveal), 2738 total frames (~114 s @ 24fps), all four sweeps verified (exact 360°, seamless return, contiguous renumbering). Note: uniform holds trade away the original per-supercontinent pause weighting (48/36/60/60) — flagged for xian.
- 18:50 — Overlay-timing check: both `render_globe.py` and `render_flat.py` **generate** their ASS overlays from the camera-path JSON at assembly time — no stale-timing risk with the new path.
- 18:52 — Committed day's work to branch (spin scripts, v7 path, research doc, log). Held `data/deep-time/` (136 MB) out of git pending xian's vendoring call (`data/plate-models` 90 MB *is* committed, so either way is defensible).
- 18:55 — Extended-Gondwana pacing draft (anim 1300–1431 from v7 path) rendering in background.
- 19:20 — Pacing draft done (132 frames, clean run; padded rest frames + gradual sweep verified in stills). Preview sent to xian.

- 19:30 — xian: pacing good; **Gondwana hold not centered**. Minor calls resolved per Tessera's leans (keep deep-time data git-ignored; uniform holds) unless a reason emerges.
- 19:40 — Root-caused the off-center hold: computed true land centroids at all four hold times (scratchpad, venv). Gondwana pose was **41° lon off centroid**; Rodinia ~5° (fine); Pangaea/Present deliberately framed (raw centroid at 0 Ma = Siberia). Fix: new `--recenter time:lat,lon` in `add_spin_reveal.py` with smootherstep ramps (default 24f). **v8 path** = v7 + Gondwana hold at (−51.2, 142.5). Verified: exact sweep, smooth ramps. Single-frame check: Gondwana now centered, night-and-day. Committed.
- 19:45 — v8 Gondwana reveal (incl. entry/exit ramps, anim 1276–1455) rendering for xian's confirmation.

- 20:00 — **Hold-framing audit** (xian: "double-check the others"): rendered current-vs-centroid stills for Rodinia/Pangaea/Present. Verdict: current framing wins or ties everywhere; **Gondwana was the only broken hold**. Key finding: for near-global clusters (Pangaea 93%, Present 91% of land) the area-weighted centroid **degenerates** — it can land in open ocean between continents; it's only meaningful for compact clusters (Gondwana 63%). Relevant later for prequel hold placement (Nuna). v8 stands. (Also: zsh doesn't word-split unquoted vars — a `set -- $spec` loop silently no-opped; explicit commands fixed it.)

## Open calls for xian (end of day)

1. Confirm the recentered Gondwana reveal (v8 preview, incl. ramps).
2. When to launch the full Cycles re-render with `camera_path_spin_v8.json` (~6.4 h for 2738 frames) — overnight candidate. Prequel spike (cao2024 in the venv) can run alongside.
