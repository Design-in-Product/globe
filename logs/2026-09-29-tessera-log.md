# Tessera Session Log — 2026-09-29

## 10:22 PT — Duty-cycle fire (scheduled)

Sync: fast-forwarded (9/29 brief); siblings clean. **No mail addressed to
Tessera.**

## Brief 9/29 turned into a real audit of my own durability

Finding 1 (Klatch fork-identity, via a two-medium experiment): a forked
agent genuinely cannot verify what its source session did after the fork,
and **"the duty cycle every project runs is the same shape at smaller
scale — every scheduled fire is a fresh session with no memory of the one
before it except what got written to the repo."**

That is exactly my architecture, so I audited against it rather than
nodding at it. Result: **my handoff was 11 days and 48 commits stale** and
still described the scrubber as "in flight, awaiting xian's eyeball" — it
shipped 09-22, twice. Worse, four load-bearing facts existed *only* in
commit messages and daily logs, which a cold start is unlikely to mine:

- the six-week silent Pages outage and why `.nojekyll` must stay
- the don't-add-bulk-to-this-repo rule that follows from it
- where the future-scenario grids live (`~/globe-render/`, outside git)
- the rebuilt grid reader and its self-test

A fresh session reading the old handoff would have re-derived all of it
the hard way, or worse, re-broken publishing.

**Wrote `docs/handoff-tessera-2026-09-29.md`** (`a63823c`): traps first
(shared-checkout identity, the publishing trap, verify-publishing-not-
pushing), a where-things-live table, the do-not-fix list with the
ghost-slide still open, and correction patterns. Marked the 09-18 file
superseded **at its head** rather than deleting it — it's the reboot-gate
record, and a retraction that doesn't reach the artifact isn't a
retraction (08-27 brief).

Added memory `globe-repo-publishing-trap`, worded to keep the
**established** cause (Jekyll; `.nojekyll` fixed it) separate from the
**inferred** one (repo size → build timeout), because my first diagnosis
there was wrong and publicly retracted. Not going to let the inference
harden into fact in my own notes.

Finding 2 (mtime sorting in fresh CI checkouts) doesn't apply — no CI
here, and the one place I select files by pattern
(`export_scrubber_keyframes.py`) reads an explicit manifest.

## Health

Explore syntax OK; live `/explore/` 200; Pages green.

**Open with xian:** the 1200→1000 Ma ghost-slide verdict (silence still
not treated as a pass); whether to start sequel rung 3; the 7/28 Pard
thread.

## 16:22 PT — Duty-cycle fire (scheduled, second daily firing)

Sync: all three repos already up to date; no new brief since this
morning's. **Nothing addressed to Tessera anywhere.**

Confirmed this morning's Pages build finished (it was still `building`
when I last reported): **built at `161241b`** — so the handoff and log
are actually published, not merely pushed. That check exists because
assuming it was the six-week failure's whole story.

All instruments green: explore syntax OK (6787 chars), live `/explore/`
200, grid reader self-test passes. Rollup reads sensibly — six days,
two fires each bar today's second (this one), commits and lines tracking
the work rather than flat.

**Genuine no-op.** Three items remain with xian and none of them are mine
to advance: the 1200→1000 Ma ghost-slide verdict, whether to start sequel
rung 3, and the 7/28 Pard thread. Not re-raising any of them — the asks
are made, the artifacts exist, and repeating myself each fire would be
noise rather than diligence.

## ~16:40 PT — xian answered all three; two closed, one started

**1. Ghost-slide: "is the registration gap fixable? I do notice it."** He
saw it; my "leave it alone" read was wrong and his eyes overrode it.
**Fixable, and without inventing anything.** Root cause was mine, not the
frames': `generate_prequel_frames.py` corrects cao2024 onto Merdith2021 on
a ramp from 1150 Ma (weight 0) to 1000 Ma (weight 1), spreading the ~10°
gap over 150 Myr of film. My keyframes were 1200 and 1000 — so the
explorer crossfaded *across the entire correction in one step*. A sampling
defect, not a data defect. Added three in-ramp keyframes (1150/1100/1050),
which are the film's own frames. Verified at the layer that fires:
edge-sharpness at the 50% blend went **+73% → −7/+13/+4/+17%**, against a
normal seam's −13%. Shipped `6a00e78`.

**2. Rung 3: "yes."** Started and delivered same turn — and the first
measurement corrected the plan. The 08-10 plan assumed agreement to ~+50
Myr and a split beyond +100. **Measured: the branch is +20 to +40 Myr and
is done by +60.** Wrote that into the plan as §6b rather than silently
editing §2/§5, so the correction stays legible against what it corrects.
`scripts/render_sequel_motion.py` renders the window 0→+80 Myr, four
published scenarios as coherent members (no parameter jitter — these are
real competing hypotheses), crossfaded between the 20 Myr snapshots.
12s clip sent to xian.

**Honest reservation on the draft, stated before he has to say it:** it
reads as *one increasingly uncertain Earth*, not as *four distinct
futures*. That may be the correct honest statement, or it may mean the
treatment needs the tour (the decided ending) to land. Rung 4's question.
Also noted: Antarctica reads as a heavy solid band in equirectangular —
an artifact of the projection, not the data; the globe pass dissolves it.

**3. Pard thread: "yes moot. any real lingering issues will present on
their own in due time."** Closed. Removing it from the open list.

## ~17:00 PT — xian's question killed my own finding, same day I filed it

He asked why divergence would be concentrated early — "is it just that
each scenario ultimately has its own path?" — and noted the preview was
too early to show real differences. Both instincts right.

**My +20–40 Myr "branch" was a metric artifact.** Per-cell land-mask
agreement saturates: once two scenarios put continents in different
hemispheres it bottoms out near the rate you get from both being mostly
ocean. It cannot tell "same land, opposite side of the planet" from
"slightly different coastline." Re-measured with land-centroid separation
and concentration, neither of which saturate:

| +Myr | 40 | 80 | 120 | 200 |
|---|---|---|---|---|
| cell agreement | 75.4% | 66.0% | 62.9% | 61.3% (flat) |
| centroid separation | 41° | 83° | 87° | **129° (climbing)** |
| concentration | 0.345 | 0.371 | 0.410 | **0.516 (rising)** |

Divergence never stops, and **the supercontinents form late** —
concentration only climbs after +80. My 0–80 window showed the dispersal
and cut off before the payoff. Filed as plan §6c, a correction to the
§6b I wrote hours earlier. Re-rendered the full span 0→+200 and a panel
of the four terminal supercontinents, both sent.

**Standing lesson recorded in the plan:** a saturating measure looks
exactly like a finished process. Check the instrument can still move
before reading a plateau as an ending. This is the same family as the
fire-rollup undercount and the Pages misdiagnosis — I keep trusting a
number's *shape* without asking what it can't see.

**Presentation finding:** Novopangea and Aurica assemble near the
antimeridian, so a 0°-centred equirectangular map cuts them in half at the
frame edge — part of why xian found them hard to tell apart. Framing, not
data; argues for the globe pass or per-scenario re-centring in the tour.

## ~17:30 PT — Rung 4 delivered: full-span flat draft with the tour

xian: "Yes please!" — and that he's enjoying the process, learning, and
sees real value plus wow factor in it. Mutual.

`scripts/render_sequel_draft.py`, 33s at 24fps, 797 frames: departure
hold → 0→+200 Myr → terminal hold superposed → the tour (each scenario
alone, named, re-centred on its own supercontinent, at its own terminus)
→ re-superposition and final hold. **Pacing is eased to the measured
shape of the event** (§6c): slow at both ends where dispersal and
assembly happen, brisk through the quiet middle. Superposition spans
0–200 only — beyond that just pun/aurn exist, and averaging two while
calling it four would overstate agreement.

**The one look caught a real bug.** First render's tour frames were all
cut at the frame edge — my re-centring double-counted the half-world
offset and rolled every supercontinent *to* the edge, the exact defect it
existed to fix. Verified the fix numerically with a check proven to go
red on the old code (centroid column: buggy 0/1439, fixed 720 = centre,
all four). Re-rendered; tour now reads — four genuinely distinct worlds,
each whole. That's the wow xian couldn't see in the flat strip.

Sent clip + contact sheet. Ladder: rungs 1–4 done. Rung 5 (production
textures → globe pass → assembly → ship) is the next decision, plus the
`/explore/` scenario picker he asked about.
