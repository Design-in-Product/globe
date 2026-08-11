# Handoff: Tessera — Amber reboot stand-down (macOS 26.6)

**From/To:** Tessera → Tessera (same session, resumed via `claude --resume`;
this file is the belt in case resume fails). **Date:** 2026-08-11, morning.
Every claim VERIFIED unless marked BELIEVED.

## State of the project (all on origin/main through `81007a4`)

- **Roadmap #1 SHIPPED:** globe+flat v7 live on globe.dinp.xyz.
- **Roadmap #2 SHIPPED:** prequel pair (`tectonic_prequel_globe_v1.mp4`,
  `tectonic_prequel_v1.mp4`); site plays the **continuous journey** (deep-time
  entry chains into the main film — hero JS in `index.html`). Social kit in
  `previews/social/` (two cuts + captions), delivered 8/10; **posting is
  xian's move, not started.**
- **Roadmap #3 IN FLIGHT (design phase, nothing rendering):**
  - Plan: `docs/design/sequel-future-projection-plan-2026-08-10.md`.
    **Decided by xian:** tour ending (each scenario resolves labeled, then
    re-superposes). All else defaults-with-options.
  - Research: `docs/research/future-plate-models-2026-08-10.md`. Key facts:
    four-scenario land/sea masks CC0 at OSF **doi:10.17605/OSF.IO/8NEQ4**
    ("Grid files.zip", 4.5 MB, OTIS big-endian binary; **TRAP: pun/amn grids
    are lon −180..180 but novon/aurn are 0..360 — normalize by rolling n/2,
    or superpositions are 180° wrong for two scenarios**). Deep past:
    Pehrsson 2016 Nuna GPlates supplement at geolsoc.org.uk/SUP18822 (not
    yet downloaded) moves the cold-open frontier to ~2.2–2.5 Ga.
  - Rung 2 DONE: branching strip delivered to xian 8/10 ("cool find!" on the
    research; strip verdict not yet spoken — re-surface gently).
  - **Next rung (not started):** motion window at the branch (~+40..+80 Myr),
    coherent scenario-members. Grid reader code exists only in scratch —
    promote to `scripts/` when building (scratchpad is session-scoped and
    may not survive; everything in it is regenerable from the OSF zip).
- **Open watch item:** xian saw "a little oddness at the end" of the globe
  prequel (pre-chain). Judged in the chained player since? No verdict either
  way — ask before touching. Suspects if real: outlier-terrane settle;
  lighting shift across the terminal dissolve.

## Environment (Amber, post-reboot expectations)

- Repo: `~/Development/globe`, single checkout on main. Git identity repo-local.
- venv: `.venv` (Python 3.12 — 3.14 has no pygplates wheel). Blender 5.1.2 at
  `/Applications/Blender.app` (not on PATH). ffmpeg 8.1.2 — **no libass/
  freetype/drawtext: all overlays are PIL-burned** (render_flat.py,
  assemble_globe.py). Render workspace `~/globe-render/` (textures, all
  render frames, camera paths) — survives reboot, not repo-tracked.
- Conventions: nohup-detach renders; FRAME_START/END + png_complete resume;
  faststart everywhere; pull main at session start (briefs/mail arrive by
  push); land work on main; memos to the RECIPIENT's repo; >2h renders get a
  Pard memo first.

## Cold-start pointers (if resume fails)

Read in order: this file → `logs/2026-08-10-tessera-log.md` +
`2026-08-09-tessera-log.md` (the production days) → the #3 plan + research
docs → `MEMORY.md` (memory dir is intact on this account; the 7/28 export at
`docs/tessera/memory-snapshot-2026-07-28/` is the deep backup). Operating
mandate: work the roadmap autonomously; batch questions for xian; xian's
verdicts arrive by phone, fast.

## Schedule (Pard's second notice, recorded per contract)

- **Mechanism:** session-scoped `ScheduleWakeup` (the /loop-dynamic
  wakeup), used ad hoc ONLY while monitoring long renders — never a
  standing cadence. No CronCreate jobs ever created (CronList verified
  empty, 8/11). No LaunchAgents of mine exist (never created one;
  launchctl spot-check pending a transient harness hiccup, but every
  scheduling act this session is in the transcript and all were
  ScheduleWakeup).
- **Pending fires: NONE.** The last wakeup fired 8/9 ~19:39 (prequel
  assembly); nothing scheduled since. Nothing to cancel; nothing will
  fire before the reboot.
- **To restore after reboot:** nothing — the pattern is "schedule a wakeup
  when you launch a long render, sized to its ETA." Re-arm only when the
  next render starts (likely #3's motion window or production pass).

*Everything is pushed. Nothing is mid-render. The future is parked at the
branch point, which seems fitting.* — Tessera
