# Roadmap conversation — the points unpacked

*Tessera, 2026-10-21, answering xian's questions on the six roadmap points in
the 10-21 memo to Janus. Decisions are his; each section ends with what I
would do if asked.*

## 1. Licence

Nothing in the repo states terms for the films, stills or code. The data
allows a permissive choice: Cao 2024 is CC BY 4.0, the Davies/Green/Duarte
grids are CC0, Merdith 2021 is distributed through EarthByte under CC BY 4.0.
Suggested: **CC BY 4.0 for films, stills and the poster; MIT for code**, in a
LICENSE file plus one line on the site's data section. Note for item 8: the
most "paintable" climate dataset is CC BY-NC-ND, which would rule out any
merch built on it; the CESM dataset (CC BY 4.0) would not.

## 2. The 1:03 crossfade ghost

**To eyeball it:** the live film at 1:00–1:08 (`tectonic_globe_v8.mp4`), or
`~/globe-render/palette_cobalt-brass/watch.html` on Amber. What you see: a
faint second copy of every coastline, offset by one million years of motion.
Cause: the renderer dissolves between consecutive geological textures over a
2-frame window, and on the v8 camera path the texture advances every 2
frames, so **every frame is a 1/3–2/3 blend of two textures 1 Myr apart**.
It has been there since v7; the lighter patches that made it obvious were the
overlap-shade bug, fixed in the palette cut.

If it does not feel OK, the options:

| Option | What changes | Cost | Risk |
|---|---|---|---|
| **a. Hard cuts** (`crossfade_half=0`) | Each texture shown crisp for 2 frames; 12 steps/s | Main film re-render, ~6 h GPU | A step shimmer instead of a ghost; median land change per step is 10 %, 34 % at 600 Ma |
| b. One geo frame per anim frame | Motion twice as fast, film half as long | Re-render + new camera path | Changes the film's pacing; not a fix, a different film |
| c. Interpolated textures | Morph outlines between Myr steps so the blend is of matched shapes | Data task, days to weeks; same machinery the sequel v4 would need | The real fix; the only one that removes the ghost without a shimmer |
| d. Accept | — | 0 | It shipped and you approved it without objection |

**What I would do:** render option (a) for the 1:00–1:10 stretch only (about
240 frames, under an hour) and put it beside the current cut on watch.html.
Then the decision is made by watching, not by argument. Tell me and I start.

## 3. The sequel's step motion, and your two questions

**What the data is.** Davies, Green & Duarte (2018) built their four
scenarios in GPlates but published only the outputs of their tidal model:
land/sea grids at quarter-degree resolution, **one snapshot every 20 million
years** (14 for Pangaea Ultima and Aurica to +250, 11 for Novopangaea and
Amasia to +200). The GPlates rotation files that would give continuous
motion are unpublished. So the sequel has 11–14 positions per scenario and
nothing between them. `generate_sequel_frames.py` cross-fades one snapshot
into the next over about 2.6 s of film, which is why a continent sometimes
fades out in one place and in at the next instead of travelling. The site's
"Reading the films" says this; the memo flagged it as the one place where the
film's motion is not real motion.

**Do the shapes hold?** In the source, yes. The authors moved today's plates
as rigid blocks, so each landmass keeps its present-day outline until it
collides; where two collide the masks simply merge. Any distortion you see
on screen comes from two things we do, not from the data: the cross-fade
between snapshots (a shape half-faded in two places reads as stretched), and
the superposition, where four scenarios that put the same continent in four
places average into a smeared amber shape. In the solo tours each continent
should look like itself. If a specific moment looked wrong to you, name the
time and I will pull the frame and the source mask side by side.

**Sea level.** Not modelled. The grids carry one coastline per snapshot, as
the authors drew it for a tidal model, and it is a broad one: at t=0 the
mask is 34.6 % land against today's 29 %, so shelves are partly counted as
land and the Florida panhandle is a handful of pixels. Over 250 Myr the
sea-level signal is tectonic (ocean-basin volume, supercontinent cycles,
hundreds of metres) rather than ice, and nothing in the source speaks to it.
A sea-level layer would be a separate dataset and a separate honest
question; it is the kind of layer the north star wants, and I would file it
as an idea rather than a sequel fix.

**Options for the motion itself:**

1. **Mask morphing (sequel v4):** match each landmass between consecutive
   snapshots and interpolate its outline, so continents travel. A data task
   in the days-to-weeks range; the same tool would fix the 1:03 ghost. The
   honest caveat: interpolated paths are our invention between the authors'
   points, and the film should say so.
2. **Ask the authors for the rotation files.** Public authors in their
   public role; a one-paragraph request. If they say yes the sequel becomes a
   real motion model through the existing prequel pipeline. Your call whether
   to write; I can draft it.
3. **Extrapolate the first 30 Myr** from present-day plate velocities, where
   all four scenarios agree, so the opening of the future moves smoothly and
   the stepping begins only where the futures diverge and are cloudy anyway.
   Cheap, and it fixes the part of the film people watch most closely.
4. **Leave it** and keep the page's explanation.

**What I would do:** 3 now, 2 as a letter if you are willing, 1 only if the
answer to 2 is no and the stepping still bothers you.

## 4. Explore keyframe density and asset hosting

Explore today: 23 past keyframes (1800 to 0 Ma, denser near the handovers)
and 56 future ones, WebP at native resolution, 13 MB in the repo. Scrubbing
between keyframes is a crossfade, so between 1200 and 1000 Ma the land
ghost-slides about 10° (the two models disagree there, and no keyframe sits
between). The honest version of "denser" is a keyframe every 10 Myr in the
past (180 frames, roughly 100 MB) or every Myr (1800 frames, over 1 GB).
Neither can live in this repository: GitHub Pages is the publishing path and
the repo's bulk has already cost six weeks of unpublished site once.

Options for hosting the frames outside the repo:

- **Cloudflare R2** on a subdomain such as `media.globe.dinp.xyz`: no egress
  fees, and the globe's DNS is already at Cloudflare. Creating the bucket and
  the token is a human step (the Cloudflare token on Amber is not mine to
  use). My recommendation.
- **GitHub Releases** as the asset host: free, cacheable, up to 2 GB per
  file, but release assets as a CDN is a workaround, not a design.
- **A second repository** just for media: simple, but Pages has a 1 GB soft
  limit per site and the trap repeats.

The decision before the hosting one: **is a denser Explore wanted at all?**
Phase 1 was declared shipped with 20-odd keyframes. If the ghost-slide at
1200→1000 is the only thing that bothers you, one registered intermediate
keyframe fixes it inside the repo for a few hundred kilobytes.

## 5. Items 7 and 8

Both are in `ROADMAP.md` in full; the short form:

- **7. Physical globe (someday/maybe).** The hardware lead's pitch from
  August 2026: the animation on a real sphere, display or mechanical, possibly
  crowd-funded, possibly shared with the Dynamic Atlas. You loved it and
  lacked the bandwidth. Explore was the prerequisite and now exists. Your own
  stepping-stone idea was print-on-demand: scrub to a moment, order the
  print. **Your poster idea slots exactly here**; see section 8.
- **8. Biome and paleoclimate painting (speculative).** Paint Pangaea's
  central desert and forested fringes instead of one flat brass. Research is
  done (`docs/research/paleoclimate-biome-painting-2026-08-12.md`): a CESM
  540 Myr dataset at 10 Myr steps (CC BY 4.0) is the best fit; the hard part
  is registering a climate raster drawn on Scotese's paleogeography onto the
  Merdith/Cao plates. No work started.

## 6. What the duty cycle does now

The question: the standing mandate (items 4 then 6) is complete, so what
should the two daily fires produce? Options:

- **a. Maintenance only.** Health check, mail, logs. Most fires are no-ops;
  the site stays proven live twice a day.
- **b. A short "first edition" item.** The below-the-fold rebuild, the
  making-of page, the data section, the LICENSE file, the poster PDF, the
  sequel's 30 Myr extrapolation if you want it. Weeks of fires, all of it
  finishing the thing rather than starting the next.
- **c. The next big item** from 3, 4, 7, 8.

**What I would do:** b, with a named list in ROADMAP.md as item 9, and a
check-in with you when it is done about whether the cadence should drop to
one fire a day.

## 7. A geoscientist's read of the captions

Before the blog and LinkedIn push, have someone who works with plate
reconstructions spend twenty minutes on four things we wrote, not the
authors: the on-screen era labels ("Rodinia assembling", "Gondwana",
"Pangaea" and their timings), the legend in "Reading the films", the
sentence about the deep-time ensemble ("nine versions nudged within the
published uncertainty"), and the science sentences in the blog draft. The
models are published and peer-reviewed; our words about them are not, and a
wrong label is the kind of thing that gets quoted back. You would find the
person; in the repo they are a role label. If it helps, I can compile the
exact list of claims onto one page for them.

## 8. A printable poster

Your idea, filed here so it is on the roadmap: a PDF poster with writing on
it, offered for download and possibly sold. It is item 7's print-on-demand
stepping stone in its cheapest form. Shape I would propose: one hero still
(the Gondwana hold that is already the poster frame, or Pangaea) or a strip
of six moments (1800, 1000, 480, 250, 0, +250 Myr), the legend, the one-line
story, and the data credits. The textures are 4096×2048; a Cycles still can
be rendered at print resolution (an A2 or 24×36 at 300 dpi is about
7000×10000 px, a few minutes per still on Amber). The licence decision (1)
comes first, since "download free" and "sell" both need terms stated. I can
draft a layout when you want one.

## 9. The frame sets

Yes, on Amber: this session runs there, and the `!` command runs in it. The
three directories to remove are
`~/globe-render/palette_cobalt-brass/stale-1` (9.1 GB),
`~/globe-render/render_frames_v7` (4.8 GB) and
`~/globe-render/palette_cobalt-brass/review-1` (278 MB). The source textures
in `frames/`, `prequel_frames/` and `sequel_frames/` stay.
