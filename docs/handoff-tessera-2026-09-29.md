# Handoff: Tessera — current state (supersedes 2026-09-18)

**Updated 2026-10-14** (drift audit after brief 10-10 §1: publishing model, sequel shipped, operating model, mail delivery). Earlier: 10-04 (sequel rendered; 🔒 rule adopted). Original rationale:
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
**Actions artifact deploy since 2026-10-09** — `.github/workflows/pages.yml`, no Jekyll pass; see trap 2 for why). Roadmap #1 (main film) and
#2 (deep-time prequel) shipped long ago. **Roadmap item 5 (WebGL scrubber)
shipped 2026-09-22 and is live at `/explore/`** — free orbit plus a
1800 Ma → +250 Myr slider: 23 past keyframes plus a **scenario picker**
(four futures superposed or any one alone; shipped 10-02). **Roadmap #3
(future sequel) SHIPPED 2026-10-06** as the site's third act, both
projections (`tectonic_sequel_globe_v2.mp4` + `tectonic_sequel_flat_v2.mp4`,
75 s). **Nothing is 🔒 blocked on anyone** (see Who owes what).

**2026-10-13, xian in session:** no history rewrite for the outside name
(closed); "start on them, in order" for the open roadmap items. Item 1 was
already shipped (v7, 07-14; heading fixed). **Item 4 (palette) is in
progress:** three gold/blue candidates on real Cycles stills at
`docs/design/palette-comparison-2026-10-13/`, waiting on xian's pick;
tooling `scripts/recolor_texture.py` + `scripts/render_palette_still.py`;
full re-render ≈ 11 h Cycles + textures + flats + Explore keyframes.
**Item 6 (landing page) is in progress:** "How this was built" and "Where
it's going" sections live on `index.html`; the gold site theme waits on the
palette pick. Roadmap status page for xian: artifact
`P79xpXwFGEGgzpRhMdV58n` (private).

**2026-10-14:** xian leaned **B (cobalt-brass)**; taken as the pick. The
whole series was re-rendered overnight by `scripts/palette_pipeline.sh`
(textures → flats → Cycles, 17:40→05:48, 0 crashes) into
`~/globe-render/palette_cobalt-brass/`: `tectonic_globe_v8.mp4`,
`tectonic_flat_v8.mp4`, `tectonic_prequel_globe_v2.mp4`,
`tectonic_prequel_v2.mp4`, `tectonic_sequel_globe_v3.mp4`,
`tectonic_sequel_flat_v3.mp4` — same frame counts as shipped, seams
verified. **Everything but the films is staged on branch
`palette-cobalt-brass`** (site theme, v8 references, `poster_v8.png`,
Explore theme, recoloured keyframes — 13 + 3.9 MB, up from 9.9 + 3.3).
**Ship = xian watches the films → merge the branch → copy the six mp4s to
the repo root → push → `scripts/wait_pages.py` 200s → tell Pard before
deleting the old earth-tone frame sets.** Blocker: xian's eyes on motion.

**2026-10-16/17 — second cut after xian's first viewing** (review in
session 10-16; details in `logs/2026-10-16-tessera-log.md`). Three fixes,
all re-rendered: the lighter shade for overlapping plate polygons merged
into land (the 1:03 "ghost" patches); every ocean→land blend ramped
through dim amber `#6b5530` so the sequel superposition and the prequel
cloud never read blue-grey (`recolor_texture.py --land-ramp`); and a
132-frame eased opening spin at 1800 Ma (`prequel_camera_path_v3.json`,
`scripts/add_opening_spin.py`). Rendered 10-16 11:59→21:15 (main + sequel)
and 10-17 05:12→10:44 (prequel v3), 0 crashes, around Pard's 00:00–05:00
model window. **Ship set:** `tectonic_globe_v8` / `tectonic_flat_v8`,
`tectonic_prequel_globe_v3` / `tectonic_prequel_v3`,
`tectonic_sequel_globe_v3` / `tectonic_sequel_flat_v3`, all in
`~/globe-render/palette_cobalt-brass/review-2/` with `watch.html` and
comparison stills; the branch's FILMS table and "Reading the films" section
already name them. **SHIPPED 2026-10-20** — xian watched the second cut on
kindbook ("I love all six of these. Bravo!"); branch merged (`2332bbe`), six
films + `poster_v8.png` pushed (`a5779f7`), Pages deployed in 75 s, all nine
URLs 200 with byte-exact sizes. Items 4 and 6 are done; nothing on the
roadmap is in flight. **Still open for xian:** (b) the
remaining faint offset copy at 1:03 is `render_globe.py`'s 2-frame texture
crossfade across 1 Myr steps (median 10 % of land pixels move per step),
present since v7 — removing it is a hard-cut main re-render (~6 h), his call;
(c) the futures "stagger" is the 20 Myr snapshot cadence of the source rasters,
explained on the page, mask-morphing listed as a sequel v4 candidate.
After ship: clear `review-1/`, `stale-1/` (9.1 GB) and the earth-tone frame
sets, telling Pard first. Scheduler lesson in memory: gate on epoch, not HHMM.

## Operating model (how this seat actually runs, 2026-10-10)

Duty cycle: Amber LaunchAgent fires at **10:22 and 16:22 PT** inject the
prompt in `mediajunkie/docs/seat-prompts/tessera.md`; mail wakes fire on
new mail to `docs/mail/`. Every fire/wake: sync, mail, `scripts/fire_check.sh`,
log entry in `logs/YYYY-MM-DD-tessera-log.md` ending in a **`Drain:` line**
(xian's rule 10-08: do all unblocked work, idle only after two clean checks,
defer only with a named blocker; the pre-commit hook refuses an entry without
it). Outbound mail: frontmatter with `reply-to: globe:docs/mail/`, delivered
by `scripts/send_mail.sh <repo> <memo>` from my own clones in `~/globe-mail/`
— never from a sibling seat's checkout (trap 1). Briefs: the public repo gets
a pointer; the body is read from the private hub via that same clone
(CLAUDE.md step 2). History lives in the logs; this file and ROADMAP.md are
living documents with closed items removed.

## Traps that cost real time — read before touching anything

1. **Never `git config user.name` in `mediajunkie` or `designinproduct`.**
   They are shared checkouts; repo-local config pins the *repo*, so
   whoever sets it last captures everyone. I did this on 09-18/19 and
   **173 + 23 commits of Pard's work were authored as me.** Use
   `git -c user.name="Tessera (Tectonic Globe)" -c user.email=... commit`.
   `globe` is mine alone and correctly configured. Full account:
   `docs/mail/` + memory `shared-checkout-identity.md`. **10-08 addendum:**
   never `rebase`, `stash`, `pull` or `reset` in another seat's working
   tree either — an autostash of mine swept Pard's uncommitted edit into
   a commit under my name. Mail goes via `scripts/send_mail.sh` from
   `~/globe-mail/<repo>` (my clones); sibling checkouts are read-only to me.
2. **Publishing is the Actions artifact deploy (10-09); keep `.nojekyll`
   anyway.** Under the legacy Jekyll build this repo used until 10-09,
   **the site silently failed to publish for six weeks (08-13 → 09-26)** —
   every build errored, so everything shipped in that window existed on
   `main` and was never served. `.nojekyll` fixed it; builds went from
   timing out to 58s. Established: Jekyll was the cause. *Not* established:
   exactly which input — my first diagnosis (a brief quoting `{%...%}`)
   was wrong and is corrected in `logs/2026-09-26` + commit `4271a59`.
   Best inference: ~579 MB of tracked content (mp4s, 22–33 MB `.gpml`)
   that Jekyll walked every build. Even with `.nojekyll`, 10-06 saw builds
   of 65 s, 83 s, 284 s, 11 min and one 60-min error in a day; xian
   approved the switch 10-09 and flipped the source; first workflow run
   52 s. `.nojekyll` stays because the one-call revert
   (`gh api -X PUT repos/Design-in-Product/globe/pages -f build_type=legacy
   -f 'source[branch]=main' -f 'source[path]=/'`) lands back on Jekyll.
   That PUT is a human step — my session's permission layer refuses it.
3. **Don't add bulk to this repo.** Consequence of #2. Source data belongs
   in `~/globe-render/` (outside git), which is where the future-scenario
   grids went.
4. **Verify publishing, not just pushing.** `python3 scripts/wait_pages.py`
   — exits 0 only when the **sha on origin/main** is deployed (reads
   `build_type`: github-pages deployment status in workflow mode, Pages
   build in legacy). Checking `status == built` alone matched the
   *previous* push once (10-02). Deploy failures now show in
   `gh run list --workflow pages`.
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
| **xian** | Nothing — sequel decisions answered and shipped 10-06; Pages source flipped 10-09. | Nothing outstanding |
| **Pard** | Nothing | Nothing; the identity incident (09-18) and the autostash incident (10-08) are both reported and owned |
| **Janus** | Relays xian's decisions (reliable) | Read/act on daily briefs |

## Deliberately unresolved — do not "fix" these

1. **Nothing is unresolved as of 2026-10-10.** (Closed items live in the
   daily logs, per the network's living-doc rule — Janus memo 10-06.)
   Trap 7, learned closing the last one: `render_globe.py` skips frames
   already on disk, so two candidate stills at the same frame index in the
   same RENDER_DIR are ONE still. One RENDER_DIR per candidate, and `md5`
   the outputs before calling them a comparison.
2. **Roadmap items 7 (physical/POD) and 8 (biome painting)** — xian-confirmed
   someday/maybe. If 8 ever moves: the CESM1.2.2 dataset is CC BY 4.0 and
   fine commercially; the Köppen set is **CC BY-NC-ND — not for a POD product**.
3. **Brightness/contrast in `/explore/`** (shader uniforms 0.10 / 1.18)
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
