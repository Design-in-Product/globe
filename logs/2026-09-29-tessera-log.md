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
