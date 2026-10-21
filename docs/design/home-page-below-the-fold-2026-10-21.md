# Home page below the fold — proposal

*Tessera, 2026-10-21, at xian's request (relayed by Janus). Proposal only: the
live page does not change until xian says yes. Companion: the blog draft in
`docs/drafts/blog-post-tectonic-globe-first-edition-2026-10-21.md`.*

## The read

The hero is right: tagline, film, the three era buttons, the Explore link, the
two one-line notes. Everything below it still reads as a build log. A visitor
who scrolls past the film today meets, in order: a two-paragraph "What is
this?" that describes only the main film (Rodinia to the present) and ends in a
pipeline diagram of script names; eight version cards, each with its own
video, five of them earth-tone films the page no longer looks like, two of them
described by their bugs; a "How this was built" that spends two paragraphs on
a sign-inverted camera, a Jekyll outage and a dropped DNS record; then the one
section written for a viewer, "Reading the films", in fifth position; then a
roadmap with status badges; then a footer that says "Six of eight roadmap items
are shipped. More to come."

That is the page of a project in progress. For a finished thing the order
should answer a viewer's questions in the order they arise: what am I
watching, how do I read it, where does the data come from, who made it, and
where can I learn more. The making-of material stays on the site, on its own
page, one link away.

## Proposed structure

| # | Section | Now | Proposed |
|---|---------|-----|----------|
| 1 | **What you're watching** | "What is this?" (main film only, pipeline diagram) | Three short paragraphs covering the whole span and the three ways to watch, plus a chapter list with timestamps |
| 2 | **How to read it** | "Reading the films", fifth | Same text, moved up to second; one precision fix (below) |
| 3 | **The data** | none | New: the three plate models, the tools, licences |
| 4 | **Who made it** | "How this was built" (four paragraphs, two operational) | Two paragraphs: the collaboration and the method; link to the making-of page |
| 5 | **The making of** (new page, `making-of/`) | "How it evolved": eight version cards on the home page | Moves whole to its own page with the pipeline diagram and the full build narrative; home page carries one sentence and a link |
| 6 | **What's next** | "Where it's going": eight rows with status badges | Two sentences, no badges, pending the roadmap conversation |
| 7 | Footer | "Six of eight roadmap items are shipped. More to come." | "Built by Xian & Claude · February 2025 – October 2026 · Source on GitHub" |

Also in the `<head>`: the `og:description` and `twitter:description` still say
"1 billion years of tectonic plate movement in two minutes", which is the v6
pitch. Proposed: "1.8 billion years of continental drift, and 250 million more,
on a globe" to match the tagline. The `og:image` stays `poster_v8.png`.

## Proposed copy

### 1. What you're watching

> Earth's continents, moving. Three films, one timeline: deep time from 1800
> to 1000 million years ago, the main film from the assembly of Rodinia to the
> present day, and a future that runs 250 million years ahead. The plates
> move at one-million-year steps, drawn from published plate reconstructions
> and rendered onto a globe, so the continents genuinely slide rather than
> jump.
>
> Every era exists in two projections that share every frame: the globe, and a
> flat map for when you want to see the whole surface at once. Press play from
> any of the three starting points and the series runs straight through; the
> seams between films are dissolves, not cuts.
>
> If you would rather hold a moment still, **Explore** puts the same span under
> a scrubber: spin the globe, pick a time, and after today pick a future or
> hold all four.
>
> **Chapters in the main film** (click to jump): Rodinia · 0:09 — Gondwana ·
> 0:54 — Pangaea · 1:24 — Today · 1:49.

The chapter times are the four hold starts in `camera_path_spin_v8.json` at
24 fps (frames 227, 1300, 2008, 2606). Clicking sets the hero video's
`currentTime`; a small script, no new assets.

### 2. How to read it

The current "Reading the films" text, unchanged, under the new heading. One
precision fix in the deep-time paragraph: it says the prequel "draws an
ensemble of them" as if of several reconstructions. The ensemble is nine
variants of one model (Cao et al. 2024), each jittered within the uncertainty
of its paleomagnetic poles, averaged. Proposed wording:

> Before about a billion years ago no reconstruction is certain, so the
> prequel draws nine versions of the same model, each nudged within the
> published uncertainty of where the continents were, and averages them.
> Where they agree the land is solid brass; where they scatter, it is a dim
> amber haze over the ocean.

### 3. The data

> **1000 million years ago to today:** Merdith et al. 2021, *Extending
> full-plate tectonic models into deep time: Linking the Neoproterozoic and the
> Phanerozoic* (Earth-Science Reviews), via the EarthByte GPlates ecosystem.
> **1800 to 1000 million years ago:** Cao et al. 2024, *Earth's tectonic and
> plate boundary evolution over 1.8 billion years* (Geoscience Frontiers),
> which extends Merdith's model back; CC BY 4.0. **The next 250 million
> years:** the four supercontinent scenarios of Davies, Green & Duarte 2018
> (Global and Planetary Change), from their published land–sea grids, 20
> million years apart; CC0.
>
> Reconstructions were turned into frames with gplately and pygplates, rendered
> in Blender Cycles, assembled with ffmpeg; Explore is Three.js. The pipeline
> and every frame-generating script are in the repository.

A licence line belongs here too, and there is none to write: the repository
has no LICENSE file and the films carry no stated terms. See the roadmap
points. Suggested, for xian's decision: CC BY 4.0 for the films and stills,
MIT for the code.

### 4. Who made it

> Tectonic Globe began in February 2025 as a four-day collaboration between
> Xian and Claude: six versions, each built, watched, fixed and built again.
> Xian brought the idea and watched every render; Claude wrote the code. That
> division was the method, not a convenience: an AI can inspect a frame but
> cannot watch a film, and the bugs that mattered only showed in motion.
>
> Since July 2026 the project has had a resident agent, Tessera, working a
> roadmap Xian set: the spin reveals at each supercontinent, the deep-time
> prequel, Explore, the future sequel, and the cobalt-and-brass palette. The
> rule did not change: no film ships until a person has watched it in motion.
> The full story, version by version, is on the [making-of page](making-of/).

### 5. The making of (new page)

`making-of/index.html`, same theme: the eight version cards with their films
exactly as they are now, the pipeline diagram, and the four-paragraph "How
this was built" including the renderer-sign discovery, the Jekyll outage and
the DNS record, which are honest and interesting but not front-page material.
The README's narrative is linked from there as before. Nothing is deleted;
the old films stay on the site at their current URLs.

### 6. What's next

Pending the roadmap conversation. The proposed text assumes the first
edition is declared complete and the two someday items stay someday:

> This is the first complete edition: three eras, two projections, Explore.
> Two ideas are on the table and neither has started: painting climate and
> vegetation onto the plates, and putting the animation on a physical globe.
> The north star behind all of it is a globe other people can extend: shared
> layers, open data, any era. Nothing here is allowed to foreclose that.

If xian would rather keep the roadmap list on the page, the alternative is to
keep it but drop the status badges and the "six of eight" framing: shipped
things are simply described, open ideas are simply listed.

## What does not change

The hero, the films, Explore, the theme, the URLs. No asset is re-rendered.
The page gets lighter: eight `<video>` elements leave the home page.

## Next step

On a yes to the direction, I build it on a branch and put a preview at
`previews/home-2026-10-21/` so xian can see it live before `index.html`
changes. Copy edits welcome at any stage; the quoted text above is a first
draft of each section, not the final.
