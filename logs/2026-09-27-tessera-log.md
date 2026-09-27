# Tessera Session Log — 2026-09-27

## 10:22 PT — Duty-cycle fire (scheduled)

Sync: `globe` fast-forwarded (9/27 brief); `mediajunkie` and
`designinproduct` clean. **Mail: nothing addressed to Tessera.**

## Checked yesterday's finding before spreading it — and it collapsed

Yesterday I offered to tell Janus that the 08-13 brief had likely broken
Pages builds across eleven reader repos. Before sending, I checked. Nine
sibling repos scanned for the offending file and their Pages status:

- **Most carry the identical brief and build fine.** `klatch` is the
  decisive case: same file, same `build_type=legacy`, same `main:/`
  source, **no `.nojekyll`** — and green.
- Only `nyt-crossword` is also errored, and I have **not** verified it is
  the same cause. Not claiming it.

So the memo I was about to send would have told eleven teams to go looking
for a defect that isn't there. **The fleet-wide alarm was wrong, and the
per-repo diagnosis was wrong with it.** Full correction appended to
yesterday's log and committed at the source of the claim (`4271a59`),
because commit `82c9cbc`'s message carries the wrong version and a
retraction elsewhere doesn't change it.

What survives: Jekyll was the problem, `.nojekyll` fixed it, site is live.
What died: the tidy story that the brief describing methodology-49
reproduced it here. The failure signature is a **timeout** (829s–21,578s
before erroring; 58s after the fix), and a Liquid parse error fails in
seconds. Likely driver is the ~579 MB of tracked binaries Jekyll walks
every build — inferred, not proven, and I am not toggling `.nojekyll` on a
live site to find out.

**Third confident-diagnosis miss this week** (git-identity "fix", the
memory file I said I'd updated, this). Common shape: correlation plus a
narrative too satisfying to interrogate, broadcast before running a check
that costs under a minute. The check caught it this time only because
xian's 404 forced me back into the evidence.

## Routine

Brief 9/27 present, read. Explore page health-checked clean; live
`/explore/` returns 200. Nothing else pending on my side.

**Still with xian:** first look at `/explore/` (orientation, mobile load,
the 1200→1000 Ma ghost-slide); the 7/28 Pard provisioning thread; and
whether to pick up sequel rung 3 (motion window), which needs nothing
from him to start.

## 16:22 PT — Second fire: project work resumed, rung-3 prerequisite rebuilt

Sync clean; no mail for Tessera in any of the three repos.

The project has been idle a week while I cleaned up process messes, so
this fire did the bounded piece of sequel rung 3 that was genuinely lost.
Checked first: **no OSF data on disk, no committed scenario script,
August's scratch gone** — matching the handoff's warning that the rung-2
grid reader was scratch-only and would need rebuilding.

Re-fetched the CC0 data (OSF doi:10.17605/OSF.IO/8NEQ4) into
`~/globe-render/future-scenarios/` — **deliberately not the repo.** Source
data doesn't belong in a tree whose bulk just cost six weeks of
un-published site.

`scripts/read_future_grids.py` rebuilt from the authors' `grd_in.m`
(big-endian OTIS, column-major MATLAB layout). What the data holds:

| scenario | | snapshots | span |
|---|---|---|---|
| pun | Pangaea Ultima | 14 | 0–250 Myr |
| novon | Novopangea | 11 | 0–200 Myr |
| aurn | Aurica | 14 | 0–250 Myr |
| amn | Amasia | 11 | 0–200 Myr |

1440×721, 34.6% land at t=0. Carries the trap that cost a 180° error in
August: pun/amn are lon −180..180, novon/aurn are 0..360.

**Self-test uses a fact the data provides rather than a fixture:** all
four scenarios *are* present-day Earth at t=0, so their masks must agree.
They do — 100 / 99.06 / 99.06 / 100%. And per R262 I verified the arm can
go red rather than assuming: with normalisation disabled, novon/aurn
collapse to 67.93%. The test detects exactly the failure it exists for.

Committed `c712510`. Rung 3 proper (motion window, ~40 Myr around the
split, coherent scenario-members) is now unblocked whenever it starts —
that part is a render job, not a fire's worth of work, and xian hasn't
said go on it yet.
