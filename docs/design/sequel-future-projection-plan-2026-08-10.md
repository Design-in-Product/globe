# Sequel: Future Projection — Plan (Roadmap #3)

*Tessera, 2026-08-10. Status: PLAN for xian review. Everything measured is
from prequel production (7/29–8/9); everything about future-model data is
RESEARCH-TO-VERIFY until the research pass runs.*

## 1 · What carries over, proven

The prequel built and battle-tested every piece this film needs:

- **Pipeline:** gplately/pygplates frame generation (`generate_prequel_frames.py`
  generalizes), camera-path generator (PCHIP, pinned holds), Blender globe pass
  (~5.9 s/frame measured), PIL-overlay assembly (`assemble_globe.py`), flat
  companion (`render_flat.py`), terminal-blend seam machinery, resumable
  renders with deterministic ensembles.
- **The seam:** the sequel's FIRST frame is the main film's LAST (present day)
  — the exact trick that welded the prequel on, run in mirror. The site's
  chained player already accommodates a third film (~10 lines of JS).
- **The uncertainty language:** viewers of the series have already learned
  that *blur = the science's honest spread*. The sequel speaks it natively.

## 2 · The design inversion (the centerpiece)

The prequel: nine possible pasts **converging** into the known map.
The sequel: the known map **diverging** into possible futures.

And the divergence is not parameter jitter — it's *discrete hypotheses*. The
literature offers four named future supercontinents (roadmap notes; ~200–250
Myr out):

| Scenario | Mechanism |
|---|---|
| **Pangaea Ultima/Proxima** (Scotese) | Atlantic reopens→closes; ring supercontinent |
| **Novopangea** | Pacific closes; Americas meet Asia–Australia |
| **Aurica** | Both oceans close; centered on the vanished Pacific+Atlantic |
| **Amasia** | Northern amalgamation over the Arctic |

**Proposed treatment — scenario superposition:** all available scenarios
rendered as coherent members (the prequel's coherent-worlds decision, reused),
weighted equally, diverging from the shared present. Near-future (~+50 Myr)
they largely agree (Africa–Eurasia suture, Australia's march north) and the
film stays crisp; beyond ~+100 Myr they split and the world genuinely
*branches* on screen — four ghost Earths sliding apart. u-ramp inverted:
0 at present → 1 at the terminal hold.

## 3 · The hard design question: how does a diverging film END?

Options (xian's call, eventually — the drafts will inform it):

- **(a) End on the superposition** — four ghost supercontinents at +250 Myr,
  held. The honest statement: "we don't know which; we know it happens."
  My lean: this is the thematically correct mirror of the prequel's opening.
- **(b) Crystallize one** — dissolve the cloud into the best-supported
  scenario as a "most likely future" ending. Legible, but overclaims.
- **(c) Tour then cloud** — during the terminal hold, briefly resolve each
  scenario alone (labeled), then let them re-superpose. Longest, most
  didactic; possibly the most satisfying.

## 4 · Research pass (gate for everything downstream)

Scope, mirroring the deep-time research doc that found cao2024:

1. Which scenarios have **GPlates-consumable rotation + polygon files**?
   Candidates to run down: Scotese's PALEOMAP future model (Pangaea
   Proxima, 0→+250 Ma); the Davies/Green/Duarte future-tides work, which
   built GPlates reconstructions of all four scenarios — did they publish
   the files, and under what license?
2. **Present-day handoff:** does each model's 0 Ma match our Merdith present
   (same shapes/frame), or does the registration machinery need to run again?
   (We now have the measured-rotation tooling if so.)
3. Coverage gaps: if only ONE scenario is obtainable, the design falls back
   to single-track with parameter-jitter uncertainty (prequel-style ensemble
   on one model) — still honest, less dramatic.

## 5 · Film structure (defaults, adjustable after research)

- **Span:** present → +250 Myr (or the obtainable models' common horizon).
- **Cadence:** 1 Myr/frame, tempo-matched. 250 geo frames ≈ 10.4 s raw —
  too short. Default: **0.25 Myr/frame** (1000 frames ≈ 42 s + holds ≈ 50 s),
  which also flatters the near-future where all scenarios agree. OPEN.
- **Holds:** departure hold at present day (mirroring the main film's
  present-day hold, possibly with its ortho lens in the flat version), and
  the terminal hold per §3. A mid-film hold at ~+120 Myr (Africa–Eurasia
  suture complete — the last thing all scenarios agree on) is a candidate.
- **Era labels:** no ICS periods exist for the future; label as "+N Myr"
  with scenario names appearing only if/when design (c) is chosen. OPEN.
- **Both formats:** globe + flat, same as the siblings; chained player gains
  "Continue into the future" and the journey becomes ~4¼ min, −1800 → +250.

## 6 · Budget (measured basis)

At 1000 geo frames × N-scenario members: member renders ≈ prequel's rate
(~1 s each warm) → texture pass ≈ 1–2 h. Blender pass ≈ 2400 anim frames ×
5.9 s ≈ 4 h. Assembly minutes. **One render-day total**, same as the prequel.

## 7 · Draft ladder (the discipline, unchanged)

1. Research pass → model availability report → xian reads.
2. Static strip: present → +250 at 6 stops, superposed scenarios — does the
   branching READ? → xian.
3. Motion window (~40 Myr around the split, coherent members) → xian.
4. Full-span flat draft (pacing + hold placement + ending options) → xian.
5. Production textures → globe pass → assembly → ship.

## Addendum: the other direction — how far before 1800 Ma? (xian, 8/10)

The 7/13 research doc's finding stands: **1.8 Ga is the frontier for
continuous full-plate models** — cao2024 is the deepest topological
reconstruction published. But "nothing continuous" ≠ "nothing":

- Individual cratons carry paleomagnetic poles back to ~3 Ga (with enormous
  gaps); the literature proposes discrete cratonic clusterings — **Kenorland /
  Superia / Sclavia (~2.7–2.4 Ga)** and the two-craton **Vaalbara (~3.6–2.8
  Ga)** hypothesis — as *static snapshots*, not motion models.
- So pre-1.8 Ga can't be film in the same sense: there is no defensible
  interpolation between snapshots. What IS honest: a **cold open** — a few
  anchor moments (say 2.7 Ga, 2.1 Ga) rendered as near-total cloud with only
  the paleomag-constrained cratons even present, holding briefly, with darkness
  (not ocean — *ignorance*) between them, before the continuous film begins at
  1800 Ma. "Before the film can run, glimpses."
- Where "just noise" begins is then a data question: the u-level at which the
  ensemble stops encoding measurement and starts encoding nothing. The
  research pass (§4) should scope this too: what pole compilations exist
  per-craton pre-1.8 Ga, and whether any are GPlates-loadable.

Filed as a candidate **cold-open extension to the prequel**, separate from
the sequel — either could go first.

## Immediate next step (on xian's go)

Fire the research pass (step 1). It gates everything; it's also the only
step with real uncertainty — the four scenarios' file availability ranges
from "published on Zenodo" to "personal communication with the authors."
The deep-past probe (addendum) can ride along in the same pass at little
extra cost.
