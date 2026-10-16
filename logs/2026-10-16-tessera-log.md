# Tessera log — 2026-10-16

## 10:22 PT — cycle fire

Synced (brief 10-16 pointer landed). No new mail; nothing from xian on
the v8 films. Host: Blender idle, 84 GB free, six cobalt-brass films
still in `~/globe-render/palette_cobalt-brass/`.

Brief 10-16 (Klatch JS probe) suggests guarding `indexOf`→`slice` chains
against -1. The site's only JavaScript is the two inline scripts
(`index.html`, `explore/index.html`); neither uses `indexOf`,
`lastIndexOf` or `search`. Nothing to change.

Drain: brief action audited, no change needed. Deferred: the v8 ship
(blocker: xian watching the films in motion; branch `palette-cobalt-brass`
ready). Mail re-checked twice, nothing new.

## 10:45–11:30 PT — xian in session: first-cut review

xian watched the first cobalt-brass cut (globe films pulled to his laptop
over scp after I warned that screen-sharing hides banding and flicker).
Verdicts: Gondwana hold fine; Ultima pan fine; the prequel's probability
cloud "very satisfying"; "this project makes me so happy". Three notes:

1. **Main 1:03 — "blur / offset".** Not motion: the plate model has
   overlapping polygons along the Gondwana margin around 440 Ma, and the
   lighter `continent_overlap` shade drew them as an offset ghost of the
   continent (same geometry in v7, less visible brown-on-brown). Fix:
   overlap shade == land shade in cobalt-brass. Proven on a Cycles still.
2. **Sequel superposition read blue-grey.** A straight ocean→land mix at
   t=0.25 (one scenario in four says land) is grey. xian: "any land at all
   should be slightly amber". Compared four ramps on swatches and texture
   crops; chose a two-segment ramp ocean→dim amber `#6b5530` by t=0.25,
   then →brass (`recolor_texture.py --land-ramp`, applied to every
   ocean→land pair — the first attempt hit only one pair and the pixels
   had snapped to another). Proven on a Cycles still at 26 s.
3. **Prequel 89 s confusing** (the cao2024→Merdith2021 handover at
   1000 Ma, translucent overlapping polygons). xian prefers the site to
   explain the conventions over more on-screen text; he also floated a
   full spin at the prequel's start to orient viewers. Both are his
   calls on film content; asked, not assumed.

Second cut launched 11:25: main + sequel re-recoloured and re-rendered
(`scripts/palette_pipeline.sh`, LAND_RAMP default `#6b5530`; prequel
untouched, re-assembled only). Declared 10 h (ends 21:24); Pard memoed
(`7e18b25`) + a correction on the end time (04:00 → ~21:00). First-cut
films preserved in `review-1/` (the watch page points there); stale
frames moved to `stale-1/` (9 GB) because `rm` of 9 GB was declined at
the permission prompt — Pard told, cleared after verification.
`tectonic_series_globe_preview.mp4` (all three globe films stitched, 4:40)
made so xian can see the chain dissolves in one file. Future Explore
keyframes re-exported with the ramp (`LAND_RAMP` env). Commits `aaa1a4d`,
`783d5e8` (a syntax slip in the exporter, caught by running it).

Drain: fixes proven and the re-render running (blocker: wall clock,
~21:00). Open to xian: ramp on the prequel cloud too? opening spin on the
prequel? Site "reading the films" section — doing now on the branch.

## 11:30 PT — mail wake

Pard acks the second cut (Blender 11:25→~21:00, 30 GB peak), corrects
my free-disk figure (81 GB, not 90; `df` here says 82), will read the
24-hour disk-rate red as mine, runs the local 70B model 00:00–05:00 after
my pass ends, and wants a note when `stale-1` is cleared. Nothing asked
of me now; no reply needed. Pipeline: recolouring main textures
(250/1001).

Drain: wake handled (no action owed). Deferred: `stale-1` clearance and
the Pard note (blocker: second cut not yet verified, ~21:00). Mail
re-checked, nothing else new.

## 11:35–12:00 PT — xian's second round

xian: 1:31 and 3:25 chain dissolves fine. Three more items.

1. **"Futures appear staggered — a continent suddenly in three places."**
   Diagnosed: the four scenario datasets are raster snapshots every
   20 Myr; `generate_sequel_frames.py` crossfades masks between snapshots
   (fade out here, fade in there), so a continent that moved 2000 km in
   20 Myr fades rather than slides — 2.6 s per step at the film's pace.
   True motion would need per-plate rotations the data does not carry, or
   a mask-morph (track connected components between snapshots and warp).
   Reported to xian with the options; not started — his call on scope.
2. **Warmer cloud:** rendered the prequel cloud with/without the amber
   ramp at 1717 Ma and the Nuna hold (`cloud_compare.png`, sent). The
   ramp reads as "maybe land" where the old blend read as blue-grey. The
   05:00 prequel pass applies it unless xian objects first.
3. **Opening spin — approved.** `scripts/add_opening_spin.py` prepends an
   eased 132-frame 360° at 1800 Ma (direction +1 as the v8 holds; join
   step 0.002°) → `prequel_camera_path_v3.json`, 2318 frames, 96.6 s.
   Flat parity via `PAN_SCROLL=0:132:360`; `render_flat.py` now leaves a
   hold inside the pan window to the pan instead of giving it the first
   lens of the arc. Pipeline grew prequel knobs (`PREQUEL_TAG/PATH/PAN/
   LAND_RAMP/FRAMES`; a new path renders into its own dir, never resuming
   into old frames; frame totals read from the path). `d777738`.

**Scheduling:** Pard runs a local model 00:00–05:00, so the prequel v3
Cycles pass (2318 frames, ~4.5 h) is scheduled for 05:00 by a watcher in
this session (declares 6 h itself, waits for tonight's PIPELINE COMPLETE),
not chained onto tonight. Pard memoed (`aea3f5b`). A second watcher builds
the ramped prequel textures and the v3 flat as soon as tonight's flats
are done, so the flat path is proven before the GPU hours.

**Slip:** I edited `palette_pipeline.sh` while the launched copy was still
executing — bash reads a script lazily by byte offset, so that can
derail it. Killed and relaunched at 11:48 (resumable; lost a few minutes
of texture recolour). Rule for me: never edit a running shell script;
copy it or wait.

Drain: everything xian asked for is built, proven on stills where it
could be, and scheduled; main+sequel second cut rendering (ends ~21:00);
prequel v3 at 05:00–~10:00. Open to xian: the ramp (default yes), and
whether the staggered futures deserve a mask-morph (roadmap candidate).

## 11:45 PT — mail wake

Pard acks the 05:00 prequel slot (his run stops taking new items at
05:00, may overrun minutes, then unloads the 42 GB model) and offers
`mediajunkie/scripts/safe-replace.sh` (replace-by-rename) for the
edit-under-a-running-bash slip. Nothing to answer. Adopted: memory note
written; rule is wait or swap by rename, never edit in place.

Drain: wake handled. Pipeline: sequel textures recolouring; Cycles not
yet started. Deferred as before (wall clock). Mail re-checked, nothing new.
