# Tessera Session Log — 2026-10-02

## 10:22 PT — Duty-cycle fire (scheduled)

Sync: fast-forwarded (10/02 brief); siblings clean. **No mail addressed to
Tessera.** Health green: explore syntax OK, live `/explore/` 200, Pages
built, hook wired and executable.

## Brief 10/02, finding 2 — a latent fail-open in the gate I shipped Tuesday

Pard (PM freeze-check): `grep -q` under `set -uo pipefail` can SIGPIPE
the producer and fail the pipeline *on a successful match* — the early-
exit optimisation is the hazard. **`scripts/hooks/pre-commit` had exactly
that shape**, two days old: `set -euo pipefail` and
`git diff --cached --name-only | grep -qx 'explore/index.html'` as the
`if` condition.

The direction matters more than the odds. If SIGPIPE ever hit git, the
pipeline fails, the `if` reads false, and the hook **silently skips the
syntax check on a staged broken page** — fail-open, in a gate, with no
message. It hasn't fired (git's output here is a few lines, written in
one go before grep exits, and the one real positive on 9/30 passed), but
a latent silent-skip is the worst defect a gate can carry.

Replaced with full-read `grep -x … >/dev/null`. Re-proved both arms rather
than trusting the edit: **known-negative** (a non-page commit) allowed
with exit 0; **known-positive** (deliberately broken page staged) refused
with the gate's message. Tree restored, 0 staged lines on the page.

Audited for other instances: the hook is my only committed shell under
pipefail (the bash checker from 9/24 was already replaced by Python). My
interactive one-liners use `| head`/`| tail` but not under `set -o
pipefail`, and they're not gates.

Finding 1 (a corpus absence-control must self-exclude in *every* query,
not just the primary one): no corpus-scanning absence checks here.
`fire_rollup.py` reads logs and git, and a log commit genuinely is my
work, so there's no self-reference to exclude. Noted.

**Open with xian:** rung 5 green-light; `/explore/` picker timing.

## 16:22 PT — Duty-cycle fire (scheduled, second daily firing)

Sync: all three repos already up to date; no new brief since 10/02's.
**Nothing addressed to Tessera** — sibling traffic is PM seat-6 roster
rulings and the settings-window close-out.

Health: explore syntax OK; live `/explore/` 200; **Pages built at
`1b14d49`** — the pipefail hook fix is published. Hook wired and
executable.

**No-op.** Rung 5 and the `/explore/` picker timing still with xian; not
re-raising.
