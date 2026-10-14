# Tessera log — 2026-10-13

## 10:22 PT — cycle fire

Sync: ff-merged origin/main to 402153c (Janus's 10-13 brief pointer). Mail:
nothing new addressed to me (newest real memo is xian's 10-12 people rule,
already applied). Health (`fire_check.sh`): brief age 0 d; 3 inline script
blocks across 5 pages OK; DNS CNAME present; /explore/ 200; Pages deployed
(workflow) for 402153c; build_type still `workflow`; no stray render
processes.

Brief 10-13 (read from the private source): correcting a computed value does
not correct hand-authored prose that explains the arithmetic — a Klatch
probe went 12/12 green while printing a stale derivation. Checked here:
no `echo`/`print` in `scripts/` spells out a derivation by hand
(`fire_check.sh` computes its "N blocks across M pages" line from the live
count); the only page prose that looked like a hardcoded count was a grep
artifact ("cao2024 keyframes"). No exposure; nothing to change.

ROADMAP.md: no unstarted unblocked item (items 1/4/6 remain exploratory
and wait on xian's finalization, as recorded 10-10 to 10-12). Handoff
"Who owes what": nothing owed either direction.

Drain: brief applied (checked, clean); health check (done); mail re-read
after the checklist, nothing new; roadmap has no unstarted unblocked item.
No deferrals.

## 16:22 PT — cycle fire

Sync: origin/main unchanged since the 10:22 fire (2f73930); working tree
clean. Mail: nothing new. Health (`fire_check.sh`): brief age 0 d; 3 inline
script blocks across 5 pages OK; DNS CNAME present; /explore/ 200; Pages
deployed (workflow) for 2f73930; build_type still `workflow`; no stray
render processes. Brief 10-13 already applied at 10:22 (no stale-derivation
exposure). ROADMAP.md unchanged: no unstarted unblocked item.

Drain: health check (done); mail re-read after the checklist, nothing new;
roadmap has no unstarted unblocked item. No deferrals.

## 16:30 PT — xian in session: roadmap directive (drain continues)

xian: (1) no history rewrite for the outside name — closed; (2) "Roadmap:
please start on them, in order!" for items 1, 4, 6; (3) asked for a roadmap
status update as an artifact for a globe-atlas aficionado.

Item 1 turned out to be SHIPPED already (v7, 2026-07-14, spin reveals at all
four holds; flat-v7 morph) — the ROADMAP.md heading still said "explore
next". Fixed: items 1 and 2 (prequel, commit 03d27b6, 2026-08-10) now carry
SHIPPED markers; 4 and 6 marked IN PROGRESS.

Item 4 (cinematic gold/blue palette): rather than re-render three films
blind, built `scripts/recolor_texture.py` (remaps the six colour roles of an
existing texture by nearest-segment decomposition; anti-aliased edges keep
their blend; 2,088 unique colours out vs 3,850 in; ~8 s/frame) and
`scripts/render_palette_still.py` (one Cycles still with the production
sphere/camera/lights/world). Rendered 8 stills (current + 3 candidates ×
Pangaea/present holds, 64 s total) and published the comparison at
`docs/design/palette-comparison-2026-10-13/` (1.0 MB WebP) with site-chrome
mocks, my read (A midnight-gold recommended; C ink-ember loses the limb
against space) and the cost table (6,719 Cycles frames ≈ 11 h + 2,048
textures + flats + Explore keyframes + theme). Waits on xian's pick.

Item 6 (landing page): added "How this was built" (lessons from the README
plus the Amber era: renderer mapping, publishing outage) and "Where it's
going" (status list, north star, link to ROADMAP.md) to `index.html`;
footer dates to October 2026. Gold theme on the page waits on the palette.

Roadmap status artifact: a forked subagent researched ROADMAP/logs/handoff
and published https://claude.ai/artifact/P79xpXwFGEGgzpRhMdV58n (private);
one stale phrase fixed and republished.

Handoff "Updated 2026-10-13" paragraph added; memory
`roadmap-execution-mandate` rewritten with today's decisions.

Drain: items 1/2 headings (done); item 4 comparison (done, awaits xian's
palette pick — blocker: xian's choice); item 6 sections (done; theme
awaits the same pick); artifact (done); mail re-read, nothing new.

## 16:50 PT — xian: "I lean toward B" (cobalt-brass) — re-render launched

Taken as the pick (said so; he can stop it). Verified the recolour holds on
the prequel's probability cloud and the sequel's scenario superposition
(both blend ocean→#a07c5a continuously; added a `continent_full` basis so
opaque land and the main film's alpha-0.9 land map to the same gold).
`recolor_texture.py` gained `--pattern` and `--jobs` (8-way, atomic
`.part` rename). New `scripts/palette_pipeline.sh <palette>`: textures →
flats (main v8; prequel v2 with terminal blend into main's first frame;
sequel v3 with initial blend out of main's last frame, PAN_SCROLL
890:288:360 read from the sequel path, LENS_HOLDS=0) → globe films via
`render_supervised.sh` + `assemble_globe.py` with the same seam blends.
Everything lands in `~/globe-render/palette_cobalt-brass/`; the repo is
untouched until xian has watched. First launch failed at once (PIL refused
the `.part` extension; the driver did not stop) — both fixed, relaunched
16:58, 56 textures in the first 80 s. Declared 12 h on origin/main; Pard
memoed (mediajunkie `62ad00b`).

xian also asked whether we would ever show greenery vs desert — that is
roadmap item 8 (he asked 08-12; research done, not scoped). Answered in
session: datasets exist (CESM 540 Myr, CC BY), registration onto
Merdith/cao2024 is the hard part, and it would arrive as an Explore layer
before it touches the films.

Drain: pipeline running (textures ~35 min, flats minutes, Cycles ~11 h —
blocker: wall clock); background watch set to check the flats when they
land; mail re-read, nothing new. No other deferrals.

## 17:04 PT — mail wake: Pard's "render is fine; one disk note"

Already read at 17:00 (it arrived while I was pushing). Sized the run
against his note: ~13 GB of new files in a fresh directory (4.8 + 3.6 +
2.8 GB of globe frames + 1.6 GB of textures), no overwrites, so no
Time Machine doubling; under his 20 GB threshold, so per his memo no
reply is needed. Pipeline still in the texture stage.

Drain: nothing new to do; mail re-read, nothing else. No deferrals beyond
the running render (blocker: wall clock).

## 17:08 PT — xian: give Pard the disk heads-up anyway

He is watching volume fluctuations; an unlabelled 13 GB curve would read
as a red herring. Sent the footprint by stage and time (textures ~1.6 GB
now, globe frames ~11 GB over ~11 h, fresh directory, nothing deleted
tonight) — mediajunkie `7dccd5f`.

Drain: memo sent (done); pipeline at 230/1001 main textures. No
deferrals beyond the running render (blocker: wall clock).

## 17:30 PT — pipeline: textures done, flat stage restarted on the venv

All 2,048 textures recoloured by 17:28 (main 1,001 / prequel 801 /
sequel 246, ~30 min). The flat stage then died at once: `flat_morph.py`
imports matplotlib, which the Homebrew python3 lacks — the shipped flats
were built with the repo `.venv` (3.12, mpl 3.11). Pipeline now prefers
`.venv/bin/python3`; the failure message also reports the real exit code
(it printed 0). Relaunched 17:28:51, textures skipped as present, main
flat rendering (1,884 crossfade frames). Background watch reset.

Drain: fix + relaunch (done); waiting on the flats (blocker: wall clock,
minutes). Mail re-read, nothing new.
