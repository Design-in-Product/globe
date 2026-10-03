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

## ~17:00 PT — xian: "rung 5, sure! picker first, yes." Picker shipped.

**Data:** `scripts/export_future_keyframes.py` — the four scenarios each
to their own terminus (pun/aurn +250, novon/amn +200) plus the
superposition to +200, at the OSF 20 Myr snapshots, as **negative
`time_ma`** so the whole axis is one number line (1800 … 0 … −250). 56
keyframes, 3.3 MB, WebP q90, own manifest (`keyframes-future.json`) —
each exporter owns its manifest and the page merges, which is the
layer-separable shape the north star asks for. The t=0 snapshots are
deliberately not exported: the shared Merdith present is the origin and
0→+20 is the honest seam between two datasets.

**Page:** keyframe handling rewritten around layers. Active set = PAST +
one future layer; picker buttons from the manifest; slider spans
1800→−250 with per-layer clamp (a +200 scenario can't show +250);
textures load on demand and cache by file (79 total now, past eagerly);
ticks/labels rebuild per layer; `fmt()` renders `+N Myr` for the future;
End key goes to the far future. Shader untouched.

The syntax checker caught a duplicate `MAJOR` declaration left over from
the old code on the first pass — the gate paying for itself on a real
edit. Fixed; no dead references to the old names remain.

Hero copy: "1.8 billion years back, 250 million ahead."

**First-look items for xian (can't browser-test from Amber):** the 0→+20
style seam (Merdith relief dissolving into a flat mask); whether the
picker reads as a control over the future only; mobile layout with the
extra row.

**Rung 5 is next** — Pard courtesy memo before the >2h Blender pass.
