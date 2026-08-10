# Future Plate Models (+ deep-past addendum) — Research Report

*Tessera, 2026-08-10, for the Roadmap #3 sequel plan. Verified = checked
against the live source today; Believed = inference, test before relying.*

## Bottom line

**There is no turnkey GPlates future model** — nothing like the cao2024 gift
the prequel got. But the film is buildable now, from three obtainable pieces:

1. **Davies, Green & Duarte's four-scenario data — CC0, downloadable today.**
   Their OSF repository (doi:10.17605/OSF.IO/8NEQ4) publishes the tidal-model
   grids derived from their GPlates reconstructions: **land/sea masks for all
   four scenarios (Pangea Ultima `pun`, Novopangea `novon`, Aurica `aurn`,
   Amasia `amn`) at 20 Myr snapshots** across each scenario's span. VERIFIED
   (file listing + readme fetched via OSF API; license CC0 per the ESD paper's
   data statement; article CC-BY 4.0). These are *masks, not rotations* —
   renderable directly in our filled-continent style at snapshot cadence.
2. **Near-future smoothness from velocity extrapolation.** For roughly the
   first 20–30 Myr all scenarios agree (Africa–Eurasia closure, Australia
   northward); smooth motion there can come from extrapolating present-day
   stage rotations from our existing model forward. BELIEVED reasonable;
   standard practice in the scenario papers themselves.
3. **The GPlates constructions themselves exist but are unpublished** — the
   2018 Global & Planetary Change paper built all four scenarios in GPlates
   (VERIFIED the paper did; the files are not in the OSF repo, the GPlates
   Web Service — VERIFIED no future model listed — or any standard channel).
   **On-request path:** email Davies/Duarte (and/or Scotese, whose future
   "Atlas … Modern World to Pangea Proxima" exists as a PDF/animation; his
   site currently serves a broken TLS cert). xian's call whether to write.

## Consequences for the design (plan §2–§5)

- **Scenario superposition works from the masks**: 4 scenarios × ~10–13
  snapshots each. Between snapshots, honest options are (a) crossfade-morph
  under rising cloud (the u-ramp itself absorbs the coarse cadence — by the
  time scenarios diverge, positions are cloudy anyway) or (b) hold-step
  pacing. Draft rung 2 (static strip) can run **immediately** from the grids.
- The tour ending (xian-decided) needs each scenario's terminal mask — all
  four are in the repo. VERIFIED naming convention supports it.
- If author rotations arrive later, they slot into the exact prequel pipeline
  (coherent members, registration tooling) as an upgrade, not a redesign.

## Deep-past addendum: how far before 1800 Ma?

- **The frontier moves to ~2.2–2.5 Ga**: Pehrsson et al. 2016 ("Metallogeny
  and its link to orogenic style during the Nuna supercontinent cycle",
  GSL SP424) published their **GPlates model as supplementary data
  (geolsoc.org.uk/SUP18822)** — Euler poles, plate polygons, the works;
  continental-drift class (blocks, no topologies), covering the Nuna cycle
  with timeslices from ≥2.2 Ga. VERIFIED the supplement exists and contains
  GPlates files; exact span/format to verify on download.
  - No topologies = no plate boundaries = **exactly consistent with our
    crystallization language** — that far back, the map hasn't earned its
    boundaries anyway.
- Before ~2.5 Ga: per-craton paleomagnetic poles with enormous gaps;
  Kenorland/Superia/Sclavia and Vaalbara are discrete, contested hypotheses
  with no motion models. **That is where "just noise" begins** — film there
  would encode nothing. The honest artifact: the cold open's earliest glimpse
  sits ~2.5 Ga, near-total cloud, darkness between glimpses.

## Recommendation

Proceed on two tracks, no author contact required to start:
1. **Sequel rung 2 now**: pull the OSF grids, render the four-scenario
   superposition strip (present → each terminus) — does the branching read?
2. **Cold-open probe when convenient**: pull SUP18822, load the Pehrsson
   model, render test frames at 2.1/1.9 Ga — does the extended deep past
   connect to cao2024's 1800 Ma without a lie?
3. Optionally, xian emails Duarte's group for the scenario rotations — the
   upgrade path if they answer.

## Sources

- OSF repo (Davies et al. 2020 data): https://doi.org/10.17605/OSF.IO/8NEQ4
- ESD paper (CC-BY, data statement): https://esd.copernicus.org/articles/11/291/2020/
- Scenarios paper: https://www.sciencedirect.com/science/article/abs/pii/S0921818118302054
- GPlates Web Service model list (no future models): https://gwsdoc.gplates.org/models/
- Pehrsson Nuna model paper: https://www.lyellcollection.org/doi/abs/10.1144/SP424.5
  (supplement: http://www.geolsoc.org.uk/SUP18822)
- Scotese future atlas (PDF): https://www.researchgate.net/publication/323511465
