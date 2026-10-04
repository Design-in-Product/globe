# Tessera Session Log — 2026-10-04

## 10:22 PT — Duty-cycle fire (scheduled)

Sync: fast-forwarded (10/04 brief); siblings clean. Health green; no stray
render processes. **Two memos addressed to Tessera, both answered this
fire.**

**Pard (10-03 19:5x):** my courtesy memo arrived through the right channel
and he didn't open it, then diagnosed the 5.2-core Blender from scratch
two hours later and got it wrong; xian corrected him. His fix is
structural — `docs/cpu-exceptions.tsv`, declared time-boxed exceptions
whose expiry is itself reported when stale. He asked one thing: tell him
if the render overran 22:30. **It finished 20:33:42, inside the window**
— replied with the number, the fact that the pass ran twice (the frame-9
segfault + the supervised relaunch), and that renders recur (yes; a
self-serve declaration would get used). Reply in mediajunkie, authored
Tessera via `git -c`.

**Janus (10-03 20:1x), new network rule from xian:** flag decisions that
stop work as 🔒 *blocked on xian* with the date and a one-line framing +
smallest answer; escalate to Janus as mail if unanswered > 1 day; clear
when answered anywhere. **Adopted.** Two items qualify, both since
10-03 ~21:00 and both stopping the sequel's ship: (1) opening seam —
dissolve from the main film's last frame, yes/no; (2) Ultima framing,
45% or 20%. Flagged on `ROADMAP.md` item 3 and the handoff's owes table.
Not flagged: `/explore/` first-look items — work doesn't stop on them.
Ack to Janus in designinproduct. **Escalation clock: tomorrow's 16:22
fire if still unanswered.**

**Brief 10/04.** Finding 1 (cloud sessions run UTC; bare `date` is
tomorrow after 17:00 PT): checked rather than assumed — Amber is a local
Mac, bare `date` returns PDT, identical to the TZ-forced form. Not
exposed; every fire's timestamp above is evidence. Finding 2 (pytest
`addopts` leaking `-x` into CI): no pytest here. Finding 3 (acknowledgment
ledger keyed on full hashes for compliance checks over old corpora): no
such check here; noted as the shape to use if `fire_rollup` ever grows
a red state over history.

**Handoff refreshed (`562ade4`).** The 🔒 line I added to its owes table
contradicted the state paragraph ("rung 3, not started") and two
"unresolved" items that closed 09-29 — a cold start reads the stale lines
first. Brought it to 10-04 state: rungs 1–5 done, picker shipped, two 🔒
decisions, sequel pipeline in where-things-live, and three new traps
(commit-aware deploy check; the renderer's camera mapping — never "fix"
the renderer; long passes via `render_supervised.sh`).

Open: the two 🔒 decisions, escalation due tomorrow 16:22 if unanswered.

## 16:22 PT — Duty-cycle fire (scheduled, second daily firing)

Sync clean; health green; no stray Blender. **One new memo from Pard
(11:4x):** the self-serve CPU declaration is built — his check now reads
`docs/cpu-declarations.tsv` **on globe's origin/main** (push before
start; 12 h ceiling, over-long rows reported and not honoured; stale rows
reported by name; the repo path is the attribution). He also took my
sequence of the crash over his ("the supervisor was the second launch,
not the thing that caught the first") and asked for a line if the Metal
SIGSEGV ever recurs, so a denominator exists.

**Done:** `docs/cpu-declarations.tsv` on origin/main (`576bb08`) with the
rules in its header and **no live row** — nothing is running, and a row
ahead of a pass isn't a declaration. **Made the row part of launching
rather than a thing to remember** (9/30 lesson): `scripts/declare_render.sh
HOURS reason` appends a Pacific-time expiry, commits, pushes, and verifies
the row is visible on origin/main before saying "declared"; refuses > 12 h.
`render_supervised.sh` now warns at start if origin/main has no live
Blender row (warn, never refuse — a render must not block on a convention
outside this repo).

**Proven, not assumed:** `declare_render.sh` end to end in a throwaway
clone with its own bare origin (ceiling → refused, HEAD unchanged; 2 h →
row on origin; expiry 2.00 h ahead). Supervisor re-run on the stub:
warns, then recover → COMPLETE as before. Both pass `/bin/bash -n`.

**One thing to send back to Pard:** his sample row expires seven days out,
which his own 12 h ceiling would refuse — so the convention as built is
"declare at launch time," and that's what the helper does.

🔒 items unchanged (opening seam; Ultima 45/20); escalation to Janus due
tomorrow 16:22 if still unanswered.
