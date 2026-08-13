# Paleoclimate / Biome Painting — Research Report (speculative)

*Tessera, 2026-08-12. Same discipline as the future-models and deep-past
passes: Verified = checked against the live source today; Believed =
inference. Explicitly speculative — nothing here is scoped or committed.*

## The question

Right now every landmass renders as one flat `CONTINENT_COLOR` at every
time and every place — Pangaea's central desert and forested fringes are
real published science we're not showing. Is there data that would let us
*paint* the landmasses instead of filling them?

**Bottom line: yes, more than expected, and multiple independent groups
have already done the hard part (running deep-time GCMs and turning the
output into classified climate/vegetation maps).** Three candidates found,
in order of fit:

## 1. CESM1.2.2 540 Myr dataset — best fit (vegetation + permissive license)

**VERIFIED** via PMC/Figshare. 55 snapshots, 540 Ma → present, 10 Myr
intervals, 0.9°×1.25° grid. Built on **Scotese & Wright (2018) PaleoDEM**
(paleogeography). Outputs monthly temperature and precipitation, **plus
vegetation via a dynamic global vegetation model (CNDV) that generates
plant functional types** — the actual biome signal, not just climate
proxies.

- License: **CC BY 4.0** — permissive, commercial use fine with
  attribution. Matters given this project's Kickstarter/POD conversation.
- Repository: Figshare, DOI `10.6084/m9.figshare.19920662.v1`, single
  NetCDF file (`High_Resolution_Climate_Simulation_Dataset_540_Myr.nc`).
- Paper: Y. Zhang et al., *Scientific Data* 2022 (the "540 million years"
  climate dataset — distinct from the Bristol/Valdes dataset below, same
  headline number, different group and model).

## 2. Phanerozoic Köppen–Geiger classification — most directly "paintable," but license-constrained

**VERIFIED** via Data in Brief 2022 (Beaufort/Wolf-Sacks et al.) + Zenodo
record. 28 time slices at 20 Myr intervals, 540 Ma → present, on the same
**Scotese & Wright (2018) PaleoDEM** paleogeography, FOAM GCM. Output is
**already classified** into Köppen–Geiger climate letter-codes (tropical /
arid / temperate / cold / polar, with desert/steppe/monsoon/savanna
sub-types) — closer to a direct paint-by-zone map than raw temperature
fields would be.

- Repository: Zenodo `10.5281/zenodo.6620748`, NetCDF or CSV, per-slice or
  zipped.
- Resolution: 2.8°×1.4°.
- **License: CC BY-NC-ND 4.0 — noncommercial, no derivatives.** This is a
  real constraint, not a formality: a POD/Kickstarter product built on a
  *derivative* of this data would need separate permission or a different
  source. Flagging honestly rather than quietly working around it.

## 3. BRIDGE/Bristol (Valdes et al.) Phanerozoic ensemble — richest science, least turnkey

**VERIFIED exists, license/vegetation-variable specifics NOT verified.**
109 time-slice HadCM3L simulations (coupled atmosphere-ocean-**vegetation**
model), whole Phanerozoic, also on Scotese paleogeography. This is the
dataset the deep-time paleoclimate community treats as most authoritative
— DeepMIP builds on the same lineage — but the public page documents a
web-interface + "email Paul Valdes for raw netCDF" workflow rather than a
one-shot open archive. Believed to be usable for research/attribution
purposes; would need direct contact to confirm terms, same as the
Davies/Duarte future-scenario rotations in the sequel research.

## The catch common to all three: paleogeography mismatch

All three ride on **Scotese & Wright (2018) PaleoDEM** — a different
lineage from **Merdith2021** (main film) and **cao2024** (prequel), the
same kind of mismatch the prequel's terminal-seam bug came from (cao2024
vs. Merdith2021 at 1000 Ma). That fix — measure the discrepancy, build
per-plate registration with a displacement cap — is **proven, reusable
tooling** (`generate_prequel_frames.py`'s `registration_rotation`). But
it's a bigger job here: the prior fix registered *rotated plate polygons*
onto each other; this would mean registering a *raster elevation/climate
grid* (not plate-indexed) onto our plate boundaries at each timestep — closer
to an image-warping problem than a rotation problem. Not a blocker, just a
different and probably larger piece of work than the rotation fix was.

## Speculative extensions (per xian's ask — casting wide, not scoping)

None of these are researched beyond naming them:

- **Ice sheets / glaciation extent** — Snowball Earth episodes, Pleistocene
  ice ages — would be a dramatic, well-attested visual layer (bright white
  caps waxing/waning) with data likely adjacent to the same GCM outputs.
- **Coastlines at sea-level highstand/lowstand** — PaleoDEM already carries
  bathymetry; distinguishing "shallow flooded continent" from "true
  coastline" is a known paleogeography visualization technique (epeiric
  seas were huge for most of the Phanerozoic).
- **Ocean color/productivity** — speculative; deep-time ocean
  biogeochemistry models exist but are a much longer research thread.
- **Orogeny visualization** — mountain belts forming/eroding is implicit in
  the topology data we already render (trenches, collisions) but isn't
  currently painted as elevation/relief.

## The bigger shape this is pointing at

Worth naming since it changes how item 8 should be scoped later, not
because it's decided now: tectonics (shipped), climate/biome (this
research), culture (Dynamic Atlas, xian's sibling project, itself a
zoom-in on the present-day terminal frame), and the physical/POD track
(item 7) are independent *layers* over the same time-and-place substrate,
not separate projects competing for the same slot. The scrubber (item 5)
is the one piece all of them need first — "pick a moment, pick a place" is
the shared primitive climate-layer toggling, Atlas zoom-in, and POD
still-picking would all use identically. If a biome layer gets built, it
slots in as a toggle/blend against the existing texture, not a rewrite.

## Recommendation

No action needed now — this was requested as speculative, idea-generating
research, not a commit. If/when it becomes real work: start with the
CESM1.2.2 dataset (permissive license, has vegetation, single clean file)
over the Köppen set (better-looking output, worse license) unless the
NC-ND terms turn out not to matter for the eventual use.

## Sources

- CESM1.2.2 540 Myr dataset (Scientific Data 2022): https://www.nature.com/articles/s41597-022-01490-4
  · full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC9240078/
  · data: https://doi.org/10.6084/m9.figshare.19920662.v1
- Phanerozoic Köppen–Geiger dataset (Data in Brief 2022): https://doi.org/10.1016/j.dib.2022.108424
  · full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC9278035/
  · data: https://zenodo.org/record/6620748
- BRIDGE/Bristol Phanerozoic ensemble (Valdes et al. 2021): https://www.paleo.bristol.ac.uk/ummodel/scripts/papers/Valdes_et_al_2021.html
- Scotese & Wright (2018) PaleoDEM (the shared paleogeography basis): https://www.earthbyte.org/paleodem-resource-scotese-and-wright-2018/
