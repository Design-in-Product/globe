# Tessera Session Log — 2026-07-29

**Session:** Second Amber day. xian at 5:36 am with verdicts and the boil question.

## Morning drop from xian

- **All four prequel design questions answered — defaults confirmed:** 1 Ma/frame
  cadence (tempo-matched) · Proterozoic era labels, same overlay style · static
  holds for the draft (revisit after) · no extra confidence-annotation cue
  (may reconsider after seeing the render). Design doc updated OPEN → DECIDED.
- **Boil vs coherent:** xian sees the appeal of both — boiling feels "honest,"
  coherent may be easier to read. Asked my instinct. Argued for coherent as MORE
  honest (reconstruction error is time-correlated; the boil falsely implies
  ~1 Myr decorrelation; a film asserts continuity, so the joint-distribution
  sample is the truthful one). Building the coherent variant of the same
  1550→1500 Ma window for a stacked side-by-side rather than deciding in the
  abstract.
- Predecessor note relayed — moot in the best way: both verdicts landed 7/28,
  `~/globe-render/` survived intact. Memory export offer declined: the git
  export already carried me across (re-seeded 7/28).

## Work log

- 7/28 log closed; this one opened.
- Design doc: four decisions recorded; ICS Proterozoic period boundaries added
  for the era-label track (Statherian → Stenian).
- `test_ensemble_motion.py --coherent`: per-member perturbations drawn once
  (unit-scale, scaled by u(t)) — nine smooth parallel worlds. Rendered the same
  1550→1500 Ma window (~7 min) and delivered a stacked **boil-vs-coherent
  comparison** to xian. Stills are statistically identical between modes, as
  they should be — the difference exists only in motion.
- **Coherence verdict: coherent wins** ("agreed smooth is better") — recorded
  in the design doc; production renders use `--coherent`.
- `test_ensemble_motion.py` generalized (`--start/--end/--step/--fps/--tag`).
- **Step 2 launched**: full-span pacing draft, 1800→1000 Ma, 4 Ma cadence,
  201 frames × 9 coherent members, nohup-detached (~27 min). Deliverables:
  flipbook + tempo-matched previews, Nuna hold-time candidates.
- **Step 2 DELIVERED**: full-span draft complete (201/201 frames, ~30 min).
  Two cuts to xian (flipbook 20 s; tempo-matched 80 s at ~10 Ma/s) + three
  Nuna hold candidates (1600 / 1520 / 1452 Ma; my pick 1452, peak
  consolidation). Confirmed the cluster reaches toward the antimeridian —
  hand-framing required, as lesson 4 predicted. Awaiting xian: pacing verdict
  + hold pick. Then step 3: production texture render (801 × 9 coherent).
## Production day — all three verdicts in

xian (mid-morning): lens arc plays well · no compression (1 Ma stands) ·
Nuna hold at 1452 Ma. Every gate open.

- **Prequel step 3 LAUNCHED**: `scripts/generate_prequel_frames.py` — 801
  frames × 9 coherent members to `~/globe-render/prequel_frames/`.
  Perturbations now derived from `SeedSequence((seed, member, plate_id))`,
  not draw order — resume/split renders are byte-identical (VERIFIED by cmp
  on a deleted-and-re-rendered frame; the motion script's lazy draws would
  have silently broken coherence on resume). Measured ~600 f/h → ~80 min.
- **Flat-v7 production LAUNCHED**: morph math promoted to `scripts/flat_morph.py`
  (canonical); `render_flat.py` gained env paths + hold detection + lens-arc
  assignment (24f morph / 84f rotate / 24f morph inside each 132-frame v8
  hold). Production mesh 1024×512: ortho limb clean at 1920×960, 0.4 s/frame.
  Building `tectonic_flat_v7.mp4` from `~/globe-render/frames/`.
- `previews/` page added: globe.dinp.xyz/previews (unlisted, noindex) after
  xian asked where previews live. (Chat cards DO play — page kept as the
  durable review surface.) xian on the full-span draft: "super cool."
- 7/29 brief read: our `| tail` exit-masking incident from last night is the
  corroborating instance for PM's `grep -q`/SIGPIPE finding (the network saw
  it before I filed anything). Audited repo scripts for `| grep -q` / `| tail`
  / `| head` under pipefail: **no hits** — all pipeline logic is Python-side.
  My own harness habit is the fix that matters: capture-then-test, no verdicts
  through pipes. CLAUDE.md finding (operative rules, not records): ours is
  lean and already shaped that way; no action.
