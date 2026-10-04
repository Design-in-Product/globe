# Handoff: Tessera — current state (supersedes 2026-09-18)

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
1800→0 Ma slider crossfading 20 era keyframes. Roadmap #3 (future sequel)
is at rung 3 of its ladder, unblocked and not started.

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
4. **Verify publishing, not just pushing.** `git push` succeeding says
   nothing about the site. `gh api repos/Design-in-Product/globe/pages/builds/latest`.

## Where things live

| what | where |
|---|---|
| Live explore page | `explore/index.html` → globe.dinp.xyz/explore/ |
| Its 20 keyframes + manifest | `scrubber_assets/` (WebP q90 at native res) |
| Keyframe export | `scripts/export_scrubber_keyframes.py` (manifest-driven) |
| Syntax check (only automated check `/explore/` gets) | `scripts/check_explore_syntax.py` — exit 0/1/2/3, guarded against vacuous pass |
| Fire depth signal | `scripts/fire_rollup.py` |
| Future-scenario grids (rung 3) | `~/globe-render/future-scenarios/` — **not in git**, CC0 from OSF 10.17605/OSF.IO/8NEQ4 |
| Its reader | `scripts/read_future_grids.py` — self-test: all four scenarios are present-day Earth at t=0, so masks must agree (100/99.06/99.06/100%) |
| Render workspace | `~/globe-render/` (frames, prequel frames, camera paths) |

## Who owes what

| | they owe me | I owe them |
|---|---|---|
| **xian** | 🔒 **since 2026-10-03**: (1) sequel opening seam — dissolve from the main film's last frame, yes/no; (2) Ultima framing 45% or 20%. Both stop the sequel shipping. (Ghost-slide fixed 09-29; rung 3–5 done; Pard thread closed moot 09-29.) | Nothing outstanding |
| **Pard** | Nothing | Nothing; the identity incident is reported and owned |
| **Janus** | Relays xian's decisions (reliable) | Read/act on daily briefs |

## Deliberately unresolved — do not "fix" these

1. **The 1200→1000 Ma ghost-slide in `/explore/`.** Crossfading an
   unregistered cao2024 keyframe into Merdith2021, ~10° apart. xian's
   first look didn't mention it — **silence is not a pass**, he may not
   have scrubbed there. If he does object, the fix is a registered
   intermediate keyframe, not a rewrite.
2. **The 7/28 provisioning thread with Pard.** Two months old, delivered
   28 days late, never answered. xian's call to nudge or drop.
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

## Cold start

This file → `ROADMAP.md` → the last few `logs/*-tessera-log.md` →
`docs/design/scrubber-scope-2026-08-29.md` §8 (if touching item 5) →
`docs/design/sequel-future-projection-plan-2026-08-10.md` §7 (if starting
rung 3) → `docs/briefs/cross-pollination/current.md` per `CLAUDE.md`.
Agent memory lives outside this repo and may not survive; everything
load-bearing above is restated here so the repo alone suffices.
