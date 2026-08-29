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

*(Architecture options, phased plan, and open questions for xian in the
next pass — same file, next commit.)*
