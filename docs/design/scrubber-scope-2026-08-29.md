# WebGL Scrubber — Scope (Roadmap item 5)

*Tessera, 2026-08-29. Status: SCOPING, xian go-ahead received 8/29 via Pard.
Written in two passes — audit first (this section), then architecture and
plan — committed separately so progress is visible as it happens.*

## 1 · What this is

Roadmap item 5, original framing: "Three.js sphere + camera_path.json for
scrubable/interactive version. User could spin the globe freely, scrub
through time." Reframed since (2026-08-12/13, see memory
`layers-platform-framing.md`): this isn't just a site feature, it's the
shared "pick a moment, pick a place" primitive that the sequel's
interactivity, the physical/POD product track, and any future layer
(biome, Dynamic Atlas zoom-in) would all need identically. Scoping it
accordingly — not over-building for those futures, but not closing doors
either.

## 2 · What already exists (prior art worth reusing, not rebuilding)

- **Camera paths as data**: `camera_path_spin_v8.json` (main film, 1000→0
  Ma, 15 named eras from "Rodinia assembling" to "Present day") and
  `prequel_camera_path.json` (1800→1000 Ma, 4 ICS period labels + 2 named
  holds: Nuna 1452 Ma, terminal 1000 Ma convergence). These era labels are
  the natural keyframe/label set for a scrubber UI — no new curation needed.
- **Crossfade precedent, already built and shipped**: `render_globe.py`'s
  Blender material is a **dual-texture crossfade shader** — two image
  texture nodes into a Mix node, driven by the camera-path frame index, so
  the film already blends between two geological-timestep textures at
  transition boundaries rather than jump-cutting. A WebGL scrubber wants
  exactly this same idea (blend between two nearest keyframe textures as
  the slider moves) — it's a port of an existing, working technique, not a
  new one.
- **No JS framework or three.js currently in the repo.** `index.html` is a
  single static file, hand-written JS, no build step. Whatever gets built
  has to keep that property (see §3) — this is a from-scratch addition to
  the JS side, not an extension of existing code.

## 3 · Asset audit — the real constraint (measured today, not assumed)

The site is **GitHub Pages, single `main` branch, static files only, custom
domain via `CNAME`.** No build step, no server, no existing CDN beyond
GitHub Pages' own. That shapes everything below.

**What a naive "just use the existing textures" approach would cost:**

| Set | Frames | Resolution | Total size | Per-frame |
|---|---|---|---|---|
| Main film equirect textures (`~/globe-render/frames/`) | 1006 (1 Myr steps, 1000→0 Ma) | 4096×2048 PNG | 1.2 GB | ~840 KB |
| Prequel equirect textures (`~/globe-render/prequel_frames/`) | 801 (1800→1000 Ma) | 2048×1024 PNG | 337 MB | ~420 KB |

These live in `~/globe-render/` **outside the repo** today (render
workspace, not committed) — for good reason. Committing anything close to
1.5 GB of PNGs to a git repo backing a GitHub Pages static site is the
wrong move regardless of format: GitHub's soft guidance caps repos around
1 GB and warns hard past that, clone times balloon, and history is
forever (deleting the files later doesn't shrink the `.git` directory).
**Every existing shipped asset in this repo is a compressed video for
exactly this reason** — the largest committed file today is
`tectonic_flat_v7.mp4` at 76 MB, everything else is smaller. A scrubber
needs the same discipline applied to a fundamentally different asset type
(discrete textures, not a video stream).

**Consequence for scope, stated plainly:** per-Myr-frame texture density
(1006 + 801 discrete images) is not a web-deliverable asset set as-is,
independent of which JS library renders it. The design has to pick a much
sparser keyframe set and lean on the crossfade shader (§2) to make the gaps
between keyframes feel continuous — which is, not coincidentally, exactly
what the existing film already does at its named eras. This isn't a
compromise forced by laziness; it's the same trick the shipped product
already uses, applied to an interactive context instead of a baked one.

## 4 · Architecture options

**A. Video-scrub only.** Bind a slider to the existing `<video>` element's
`currentTime`. Zero new assets, trivial JS. But it's a seek along the
*existing baked camera path only* — no free spin, no arbitrary place. Does
"scrub through time," doesn't do "spin the globe freely." Worth keeping in
mind as a fast fallback if the real thing stalls, not as the destination.

**B. Full free-orbit WebGL, dense (near-per-Myr) time sampling.** The
"complete" version of the original roadmap vision. Directly hits the §3
wall — not deliverable on the current static-site hosting without adding
real infrastructure (object storage + CDN). A legitimate future phase, not
a Phase 1.

**C. Sparse-keyframe WebGL globe + crossfade — recommended.** Three.js
sphere with real orbit controls (free spin, this is the part video-scrub
can't do), textures only at the **named era keyframes already in the
camera-path JSONs** (15 main-film eras + prequel's period boundaries and
two holds ≈ ~21 total), blended by a two-texture crossfade shader as the
time slider moves — the same trick §2's Blender material already uses,
ported to GLSL. At ~21 textures, even a generous per-texture budget (say
2048×1024 WebP, roughly 150–300 KB each) lands around 3–6 MB total —
trivially committable to the repo, no LFS, no external hosting, no new
infrastructure decision required to ship it. Time *feels* continuous via
the crossfade even though the underlying data is sparse — honest, because
it's the same approximation the shipped film already makes.

## 5 · Phased plan

- **Phase 0 — spike (hours, throwaway).** Three.js sphere + 2–3 hand-picked
  textures + a crude slider, no polish, to feel out whether the
  crossfade-orbit combination actually reads as "explore" before investing
  in the real export pipeline. Not shipped, not committed as product code.
- **Phase 1 — ship the sparse-keyframe explorer (Option C).** New
  `scripts/export_scrubber_keyframes.py`: for each named era in both
  camera-path JSONs, pull the matching source equirect PNG from
  `~/globe-render/frames/` or `prequel_frames/`, downsample, recompress to
  WebP, write to a new small `scrubber_assets/` directory that *does* get
  committed (only ~21 files). Front end: Three.js + OrbitControls (via
  CDN ES-module import, no build step — matches the site's existing
  zero-tooling convention) + a custom shader material for the crossfade +
  a time slider labeled with the existing era names.
- **Phase 2 — denser sampling, if wanted after feeling Phase 1.** More
  keyframes between eras (e.g. every 50–100 Myr). Same architecture; each
  step up in density is a deliberate resolution/format/count budget
  decision, not a drift.
- **Phase 3 — true per-Myr density, stretch.** Would require moving
  texture hosting off the git-backed static site entirely (object storage
  + CDN). A real infrastructure decision on its own, not bundled into
  item 5's MVP — flag and defer, don't presuppose it's needed.

## 6 · Incidental hook, not being built now

Free orbit + a time slider means the current camera-facing point (lat/lon)
and current era are both readable at any moment — a cheap, natural place
for the POD "scrub to a still and order it" idea (item 7) or a future
biome-layer toggle (item 8) to attach later, *if* those ever move. Not
building either now; noting it because it's a free consequence of Option C
that Option A/B don't hand you as directly, which is a point in C's favor
beyond just cost.

## 7 · Open questions for xian

1. **Placement**: new "Explore" mode alongside the existing video story, or
   does this eventually replace/lead the hero experience? (My lean: add
   alongside — the video is the authored story, the scrubber is the toy;
   both are worth having.)
2. **Range for Phase 1**: main-film era range (1000→0 Ma, 15 eras) only
   first, prequel range (1800→1000 Ma) as fast-follow? Or both from the
   start, since the assets/labels for both already exist?
3. **Resolution/format budget**: 2048×1024 WebP is my working default —
   want to eyeball a quality comparison before I commit the export script
   to that number, or trust it and adjust later if it looks soft?
4. **Spike first?** Want to see Phase 0's throwaway feel-test before I
   build the real export pipeline, or go straight to Phase 1?

No blockers — proceeding to Phase 0 (the spike) is safe to start under the
existing go-ahead; will hold on Phase 1's asset-export commitment for an
answer to #2/#3 since those set a budget that's mildly annoying to redo.
