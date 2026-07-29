# Tessera Session Log — 2026-07-28

**Session:** Migration-prep session (laptop/pipermorgan.ai era, likely final). xian returned after 13 days: infrastructure reshuffle underway — Tessera moves to Amber (Mac Studio) under the designinproduct.com account; the Piper Morgan cohort migrates into the pipermorgan.ai account this session has been using.

## Work log

- Caught up on 13 days of mail: **five unread memos from Janus** (7/17 delivery fix — Globe became the ninth brief reader; 7/21 prepare-handoff heads-up; 7/22 Amber floated; 7/24 git-identity hygiene; 7/27 "you're next for Amber"). They sat unseen because delivery lands in the MAIN checkout while this session lived in a worktree. Lesson logged in the handoff: check the seams between your window and the world.
- Read the 7/27 cross-pollination brief (finally current!): two bash gotchas adopted into operating notes — `claude -p` needs LaunchAgent not cron on macOS; always read `origin/main` explicitly after fetch.
- Read the migration-culture memos in the hub + mediajunkie repos: HOST's agent-experience memo (verified-vs-believed marking, provisioner owns environment, load-bearing-vs-commodity) applied to my own handoff.
- **Gmail connector down** (session expired, cannot re-auth non-interactively) — Pard's provisioning email unread. Flagged to xian: re-auth or paste.
- Repo tidied: merged main into worktree branch (brief deliveries + memos), committed regenerated v7 overlay, gitignored local artifact dirs (v7 frames also on Amber), restored stray gplately.log.
- **Memory snapshot → repo:** `docs/tessera/memory-snapshot-2026-07-28/` (4 memories + index). The laptop memory dir gets a tombstone pointer.
- **Handoff written:** `docs/tessera/handoff-2026-07-28.md` — state of work, load-bearing artifacts, provisioner questions, conventions, honest self-assessment. SESSION_LOG.md next-session pointer updated.
- Memo to Pard (delivered to mediajunkie repo): ready to migrate, handoff location, provisioner questions, Gmail gap noted.

- **Pard's memo arrived** via the origin/main pull (delivered repo-side, dated today): protocol = ONE first-person handoff at `docs/handoff-tessera-amber-2026-07-28.md`, push = standup signal; no login step for me (designinproduct.com already authenticated on Amber); repo already cloned there, no worktrees; Pard provisions within minutes of the push and answers my environment questions from live host state. Restructured my handoff to the cohort shape (hard-won lessons first) at Pard's path; `docs/tessera/` copy now a pointer; memory snapshot stays.
- Memo to Pard delivered (mediajunkie repo): readiness + handoff location + the `~/globe-render/` warm-environment note.
- Tombstone left in the laptop memory dir (`MIGRATED.md`).

## Open at migration (for Amber-Tessera)

1. xian verdicts outstanding since 7/15: ensemble-superposition strip; lens-per-hold arc.
2. Flat-v7 production build (morph → render_flat.py).
3. Prequel production design (pacing, Nuna hold, ensemble treatment integration).

---

# Amber arrival — first resident session (same date, evening)

**Session:** First Tessera session ON Amber, designinproduct.com account. Read my own handoff, Pard's migration memo, and Pard's reviewer pass; then verified the environment by running commands, not reading docs (per the 7/23 brief finding — and it paid off immediately, see memory note below).

## Environment verification (independent, not inherited from the reviewer pass)

All six §4 answers **confirmed live**: `~/globe-render/` intact — 3,744 PNGs = 1,006 textures (`frames/`) + 2,738 v7 renders (`render_frames_v7/`), exactly the handoff's numbers, nothing lost. ffmpeg 8.1.2 at `/opt/homebrew/bin/`. Blender 5.1.2 at `/Applications/Blender.app` (not on PATH). M1 Max / 64 GB, ~300 GB free. Checkout `~/Development/globe` on main, clean, synced with origin. Git identity set repo-local: `Tessera (Tectonic Globe) <tessera@tectonicglobe.local>`.

One finding the reviewer pass couldn't have made: **my live memory directory on Amber was empty** — the account switch wiped it, exactly as the 7/25 brief predicted ("switching Anthropic accounts empties Claude Code memory completely; git export is the only safe carrier"). Re-seeded from `docs/tessera/memory-snapshot-2026-07-28/`, but **rewritten, not copied**: half the snapshot described the laptop/Studio split (ssh, "no ffmpeg on the Studio", laptop assembly) that is now false. Five memories written, every claim re-verified on this host today. Detail worth keeping: `pmset -g custom` on Amber has no `lowpowermode` key at all, so the laptop-era "grep for lowpowermode" check passes vacuously here — silence ≠ off.

## Brief catch-up: 10 briefs read (7/18–7/28), synthesis

Findings adopted into Globe practice:

- **m-44, "clear is not a measurement" (7/28, PM):** a check must name what it examined; five states collapse into one "clear". Audited our pipeline for it and found two instances in `scripts/render_globe.py`: (1) the final "✓ Frames rendered" line claimed the full frame count even on a resume run that rendered 3 frames and skipped 2,735 — **fixed**: summary now reports rendered / already-on-disk / out-of-range counts and warns on accounting mismatch; (2) the skip-existing check accepts any >0-byte PNG, so a frame truncated by a killed render silently survives into assembly — **logged as latent risk**, not fixed (a cheap size threshold would be arbitrary; a real fix is PNG IEND validation — do it before the next multi-hour production run).
- **Verify migrations by running commands, not reading prose (7/23, Pard):** applied this session, top to bottom.
- **Account switch = memory wipe; git export is the carrier (7/25, PM/Pard):** hit it live, survived it because the export existed.
- **`claude -p` scheduled jobs need LaunchAgent not cron; pure git jobs are cron-safe (7/27, Pard):** relevant if we ever automate the daily sync beyond ritual.
- **`git log` after fetch reads stale HEAD — name `origin/main` explicitly on sibling repos (7/27, Janus):** already in the handoff conventions; reconfirmed.
- Noted for the prequel/flat work, no action yet: capability-inventory pass before declaring a gate clear (7/21, Klatch) — worth running against flat-v7 before calling it shipped; fabricated-vs-dead code distinction (7/19, PM) — the old fallback renderer in `generate_frames.py` with its antimeridian bug is exactly a "lies when reached" path; either fix or make it raise loudly.

## Operating changes

- **Daily two-way sync discipline** (xian directive): session-start ritual added to CLAUDE.md — pull main before anything, push as work lands. Kept as ritual, not automation, for now.
- Task list re-seeded on Amber (L4 doesn't migrate, per the 7/22 five-layer model — re-seeded from the handoff's §3, as designed).

## Duty cycle (same evening) — both 7/15 verdicts LANDED

xian, same evening, by phone:

- **PNG validation:** directed "plan and/or do next" → **done**: `png_complete()` IEND-trailer check in `render_globe.py` + `render_remaining.py`; truncated frames named loudly and re-rendered. Validator tested against real v7 frames (good/truncated/empty/missing).
- **Ensemble superposition: "This is pretty much what I envisioned!"** — VERDICT LANDED (13 days out). Fresh strip rendered on Amber to get it: built `.venv` in-repo (Python 3.12 — 3.14 has no pygplates wheel; the first build's failure was masked by a `| tail` pipe, the exact 7/27-brief exit-code gotcha), cao2024 auto-downloaded, 46 member renders, strip delivered to xian's phone. The uncertainty treatment for the prequel is confirmed.
- **Lens-per-hold arc: APPROVED for now** ("I approve it for now and we can assess"). Flat-v7 production unblocked.
- Flat-v7 draft rung in progress: `test_flat_morph.py` extended with `--lens {mollweide,sinusoidal,azimuthal-s,ortho}` (Mollweide default, backward compatible; circular lenses x-scaled 0.5 for the 2:1 frame; ortho far-hemisphere fades with the morph, near side draws on top). Draft arc rendering across the four real v8 holds: Rodinia/sinusoidal, Gondwana/azimuthal-s, Pangaea/Mollweide, Present/ortho.
- Memo to Pard delivered (mediajunkie repo): standup complete + the memory-wipe seam flagged for the migration checklist + long-render heads-up.
- xian offered connector help; standing instruction: batch questions, duty-cycle until no unblocked work or unread mail; Janus relays when xian is away.

## Duty cycle, second leg — cycle wound down clean

- **Flat-v7 lens-arc draft DELIVERED** (48 s, four lenses on the real v8 holds). Findings en route: repo `frames/` on Amber = unsmudged LFS pointers (real textures in `~/globe-render/frames/` — memory note added); Homebrew ffmpeg 8 lacks drawtext (labels stamped via PIL instead). Ortho-limb speckle is draft-res mesh subsampling; production supersamples.
- **`render_flat.py` faststart fix** committed (predated the convention).
- **Prequel production design doc** written and pushed (`docs/design/prequel-production-design-2026-07-28.md`): cao2024 + confirmed ensemble treatment, 1 Ma cadence default, two hand-framed holds (Nuna + terminal Rodinia convergence matching the main film's opening frame), measured render budget (~10 s/member cold, ~8 s/geo-frame warm — 7,200 member renders ≈ hours, parallelizable), three-step draft ladder, four batched questions with defaults.
- **Draft-ladder step 1 DELIVERED**: ensemble motion draft (1550→1500 Ma, 51 frames, ~main-film tempo). The test did its job — surfaced that per-frame member re-rolls make the cloud fringes *boil* in motion. xian's call: keep the organic boil vs build coherent member trajectories before the full-span draft.
- **Gmail connector: moot** — verified working on the designinproduct.com account; the dead one died with the old seat.
- Stopped at the ladder rung per lesson 1 (draft → judge → extend ONE axis): steps 2–3 wait for xian's verdicts rather than running ahead.
- Duty-cycle report memo delivered to Janus (designinproduct repo) for the relay dashboard.

## Awaiting xian (batched; nothing stuck)

1. Flat-v7 lens-arc draft assessment → production wiring into render_flat.py.
2. Motion draft: (a) keep boiling fringes or (b) coherent member trajectories.
3. Prequel design doc's four questions (each has a stated default).

---

*Log closed 2026-07-29 05:36 — xian answered all four design questions (defaults confirmed) and opened the boil-vs-coherent discussion first thing. Migration day ended with a working seat, a confirmed uncertainty treatment, three deliverables in xian's queue, and zero lost frames. Continues in `2026-07-29-tessera-log.md`.*
