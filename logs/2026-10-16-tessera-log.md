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
