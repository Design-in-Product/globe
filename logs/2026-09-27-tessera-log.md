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
