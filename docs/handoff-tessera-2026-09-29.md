# Handoff: Tessera — current state (supersedes 2026-09-18)

**Updated 2026-10-04** (sequel rendered; 🔒 rule adopted). Original rationale:
**Why now:** brief 9/29 (Klatch fork-identity finding) restated the first
principle of multi-session work — *shared memory is exactly what's in git,
nothing carried implicitly across session boundaries.* My last handoff is
11 days and **48 commits** stale and still says the scrubber is "in
flight, awaiting xian's eyeball." It shipped twice since. A fresh session
starting from it would be badly misinformed. `docs/handoff-tessera-2026-09-18.md`
is **superseded** — read this instead.

## State in one paragraph

Tectonic Globe: animated plate-tectonic reconstructions (GPlates/gplately)
on globe.dinp.xyz (GitHub Pages, `Design-in-Product/globe`, single `main`,
**legacy Jekyll build — see the trap below**). Roadmap #1 (main film) and
#2 (deep-time prequel) shipped long ago. **Roadmap item 5 (WebGL scrubber)
shipped 2026-09-22 and is live at `/explore/`** — free orbit plus a
1800 Ma → +250 Myr slider: 23 past keyframes plus a **scenario picker**
(four futures superposed or any one alone; shipped 10-02). **Roadmap #3
(future sequel): rungs 1–5 done — v1 globe film rendered 10-03** (66 s,
1,587 frames, `previews/` §8). **Not yet chained into the site: two
decisions are 🔒 blocked on xian** (see Who owes what).

## Traps that cost real time — read before touching anything

1. **Never `git config user.name` in `mediajunkie` or `designinproduct`.**
   They are shared checkouts; repo-local config pins the *repo*, so
   whoever sets it last captures everyone. I did this on 09-18/19 and
   **173 + 23 commits of Pard's work were authored as me.** Use
   `git -c user.name="Tessera (Tectonic Globe)" -c user.email=... commit`.
   `globe` is mine alone and correctly configured. Full account:
   `docs/mail/` + memory `shared-checkout-identity.md`.
2. **`.nojekyll` must stay.** This repo publishes via legacy Jekyll, and
   **the site silently failed to publish for six weeks (08-13 → 09-26)** —
   every build errored, so everything shipped in that window existed on
   `main` and was never served. `.nojekyll` fixed it; builds went from
   timing out to 58s. Established: Jekyll was the cause. *Not* established:
   exactly which input — my first diagnosis (a brief quoting `{%...%}`)
   was wrong and is corrected in `logs/2026-09-26` + commit `4271a59`.
   Best inference: ~579 MB of tracked content (mp4s, 22–33 MB `.gpml`)
   that Jekyll walked every build.
3. **Don't add bulk to this repo.** Consequence of #2. Source data belongs
   in `~/globe-render/` (outside git), which is where the future-scenario
   grids went.
4. **Verify publishing, not just pushing.** `python3 scripts/wait_pages.py`
   — exits 0 only when Pages has built **the sha on origin/main**. Checking
   `status == built` alone matched the *previous* push once (10-02).
5. **The renderer's camera latitude is not what the path says.**
   `render_globe.py` rotates the globe with Euler (0,−lat,−lon); the view
   latitude is ≈ `−lat·cos(lon) + 10°`. Shipped films were eye-framed
   against this — **never "fix" the renderer**; convert computed aim
   points with `compute_sequel_path.renderer_cam()`. Memory
   `renderer-camera-mapping.md`; data `scripts/data_view_table.json`.
6. **Long Blender passes go through `scripts/render_supervised.sh`.**
   Blender 5.1.2 can SIGSEGV in Cycles' Metal kernel compile (once in
   ~1,600 frames, intermittent). The supervisor resumes from the first
   missing/truncated frame and stops on a crash budget. Use self-match-
   proof `pgrep -fl '[r]ender_supervised'` to check it.

## Where things live

| what | where |
|---|---|
| Live explore page | `explore/index.html` → globe.dinp.xyz/explore/ |
| Its keyframes + manifests | `scrubber_assets/` (23 past, `keyframes.json`) + `scrubber_assets/future/` (56, `keyframes-future.json`); WebP q90 at native res |
| Keyframe export | `scripts/export_scrubber_keyframes.py` (manifest-driven) |
| Syntax check (only automated check `/explore/` gets) | `scripts/check_explore_syntax.py` — exit 0/1/2/3, guarded against vacuous pass |
| Fire depth signal | `scripts/fire_rollup.py` |
| Future-scenario grids (rung 3) | `~/globe-render/future-scenarios/` — **not in git**, CC0 from OSF 10.17605/OSF.IO/8NEQ4 |
| Its reader | `scripts/read_future_grids.py` — self-test: all four scenarios are present-day Earth at t=0, so masks must agree (100/99.06/99.06/100%) |
| Future keyframe export | `scripts/export_future_keyframes.py` |
| Sequel textures + sidecar | `scripts/generate_sequel_frames.py` → `~/globe-render/sequel_frames/` (246 geo frames, `sequel_frames.json` owns the sequence + aim points) |
| Sequel camera path | `scripts/compute_sequel_path.py` → `sequel_camera_path.json` (eased pacing, holds, tour aims via `renderer_cam()`; `PUN_SEA_BIAS` env) |
| Sequel v1 film | `~/globe-render/tectonic_sequel_globe_v1.mp4` and `previews/tectonic_sequel_globe_v1.mp4` |
| Crash-resilient render driver | `scripts/render_supervised.sh` (proven on a stub: recover / budget / no-progress / complete) |
| Deploy check | `scripts/wait_pages.py` |
| Pre-commit gate (explore page) | `scripts/hooks/pre-commit` via repo-local `core.hooksPath` — fine here only because `globe` is single-seat |
| Render workspace | `~/globe-render/` (frames, prequel frames, sequel frames/renders, camera paths, OSF grids) |

## Who owes what

| | they owe me | I owe them |
|---|---|---|
| **xian** | Nothing — both sequel decisions answered 10-06 (dissolve; centroid + slow pan). Next eyeball: the assembled v2 film once the tour re-render lands (~13:00 10-06). | Nothing outstanding |
| **Pard** | Nothing | Nothing; the identity incident is reported and owned |
| **Janus** | Relays xian's decisions (reliable) | Read/act on daily briefs |

## Deliberately unresolved — do not "fix" these

1. **Nothing is unresolved as of 2026-10-06.** (Closed items live in the
   daily logs, per the network's living-doc rule — Janus memo 10-06.)
   Trap 7, learned closing the last one: `render_globe.py` skips frames
   already on disk, so two candidate stills at the same frame index in the
   same RENDER_DIR are ONE still. One RENDER_DIR per candidate, and `md5`
   the outputs before calling them a comparison.
3. **Roadmap items 7 (physical/POD) and 8 (biome painting)** — xian-confirmed
   someday/maybe. If 8 ever moves: the CESM1.2.2 dataset is CC BY 4.0 and
   fine commercially; the Köppen set is **CC BY-NC-ND — not for a POD product**.
4. **Brightness/contrast in `/explore/`** (shader uniforms 0.10 / 1.18)
   was tuned to xian's "more brightness and higher contrast" by measuring
   (+21% mean luma), and he has the A/B. Don't re-tune unprompted.

## Correction patterns — what I most recently got wrong

- **xian:** three confident diagnoses broadcast before a cheap check —
  the identity "fix" that caused the leak, a memory file I said I'd
  updated and hadn't, and the Pages cause I got wrong and had to retract.
  Shape is always: correlation plus a satisfying narrative, stated as
  fact. **The check that would have caught each cost under a minute.**
- **Pard:** see trap #1.
- **My own tooling:** `fire_rollup.py` was undercounting my fires because
  it matched a phrase instead of the structural marker. The instrument
  built to detect my degradation was itself mismeasuring me. Verify an
  arm can go red before trusting it green.
- **10-03, the render day:** a "cache moved aside" that was a no-op (the
  directories didn't exist); a probe frame I read as "full north" that
  Blender's own geometry showed was equatorial; a `pgrep -f` that matched
  its own command line; three bash-3.2 quoting hazards and an off-by-one
  in a script I'd declared done. Every one caught by looking at output
  instead of trusting it. The pattern that keeps paying: **prove an
  instrument can go red before trusting its green.**

## Cold start

This file → `ROADMAP.md` → the last few `logs/*-tessera-log.md` →
`docs/design/scrubber-scope-2026-08-29.md` §8 (if touching item 5) →
`docs/design/sequel-future-projection-plan-2026-08-10.md` §7 (if starting
rung 3) → `docs/briefs/cross-pollination/current.md` per `CLAUDE.md`.
Agent memory lives outside this repo and may not survive; everything
load-bearing above is restated here so the repo alone suffices.
