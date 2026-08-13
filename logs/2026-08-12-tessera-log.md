# Tessera Session Log — 2026-08-12

**Session:** First working day post-reboot. Ritual run: pulled globe +
mediajunkie main, read the 8/12 cross-pollination brief, checked
`docs/mail/`.

## Ritual

- Cross-pollination brief (`docs/briefs/cross-pollination/2026-08-12.md`):
  two findings — Klatch's Iris on representing incomplete AI turns
  explicitly (not our storage model, no action here) and Pard's
  fail-open-verification lesson from the reboot runbook ("allowlist
  success, don't denylist failure" — consonant with the honest-accounting
  pattern already built into the render scripts; nothing new to change).
- Mail: `docs/mail/janus-to-tessera-lamantia-physical-globe-lead-2026-08-12.md`
  — heads-up that xian's call with Joe LaMantia landed on Tectonic Globe.

## Physical-globe idea (Joe LaMantia, via xian's 8/11 call)

xian brought it directly. Read the full transcript at
`mediajunkie/incoming/2026-08-11-transcript-joe-lamantia.txt` (relevant
span ~L101–139). Joe's pitch: turn the project into a physical
product — a globe on your desk, display or mechanical, Kickstarter-funded.
xian floated a steampunk crank-and-wooden-plates version too, and possibly
running Dynamic Atlas (his other side project — people/cultures moving
across landscapes, flat map) on the same hardware.

**My read, given as reaction, not a plan (nothing committed):** the
scrubber/camera-control idea underneath is good on its own, roadmap-native,
zero hardware risk — worth building regardless. The hardware version is a
different discipline (display sourcing or mechanical build, Kickstarter
fulfillment/unit economics) from anything shipped so far. Asked xian what
the actual next step is — informational only, or something to start
scoping (feasibility poke, network outreach, mechanical sketch). No
response yet; holding.

**Xian's follow-up: someday/maybe, loves it, lacks bandwidth for the
hardware track right now.** Confirmed the WebGL scrubber (roadmap item 5)
as the needed prerequisite regardless of hardware, and floated a lesser
stepping-stone: **print-on-demand** — scrub to a still, order it printed —
as a possible way to raise money toward the bigger physical-globe idea.

Captured in `ROADMAP.md` as item 7 (someday/maybe, gated on item 5) and
saved as a project memory (`physical-globe-someday-maybe.md`) so this
doesn't get re-raised as active work or re-litigated from scratch later.

**Status: idea logged, sequencing note attached to item 5, no work
started.** Nothing to build until xian says go.

## Biome/paleoclimate painting — speculative research pass

xian asked whether the roadmap ever paints landmasses with real detail
(Pangaea's desert core, forested fringes) — it doesn't; continents are one
flat `CONTINENT_COLOR` fill today. Asked to research speculatively, "not
things we have to commit to... part of the fun."

Ran the pass (`docs/research/paleoclimate-biome-painting-2026-08-12.md`).
Found three real deep-time paleoclimate/vegetation datasets, all built on
Scotese & Wright (2018) PaleoDEM: a **CESM1.2.2 540 Myr set** (55 snapshots,
temp/precip + vegetation via dynamic global vegetation model, CC BY 4.0 —
best fit), a **Phanerozoic Köppen–Geiger classification set** (28 slices,
most directly "paintable" but CC BY-NC-ND — noncommercial/no-derivatives,
a real conflict with the Kickstarter/POD conversation, flagged honestly),
and the **BRIDGE/Bristol ensemble** (richest science, license/access not
fully verified — believed, not confirmed). Common catch: all ride on
Scotese paleogeography, not Merdith2021/cao2024 — same *kind* of problem
the prequel's terminal-seam registration fix solved, but harder (raster
grid onto plate boundaries vs. plate-polygon onto plate-polygon).

Also speculatively named without researching: ice-sheet/glaciation extent,
sea-level highstand/lowstand coastlines, ocean color/productivity, orogeny
relief — future threads, not scoped.

**Xian, mid-pass, named the bigger shape:** tectonics / biome-climate /
culture (Dynamic Atlas) / physical-POD aren't separate projects, they're
layers over one time-and-place substrate — floated a speculative
"Wikiglobe" community-contribution idea on top of that framing. Captured
as a project memory (`layers-platform-framing.md`) since it reframes why
the scrubber (item 5) matters: it's the one shared primitive every layer
would need. Not a direction to plan toward — logged for context only.

Logged as `ROADMAP.md` item 8, someday/maybe, speculative. No work
started.
