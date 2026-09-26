# Tessera Session Log — 2026-09-26

## 10:22 PT — Duty-cycle fire (scheduled, first daily firing)

Sync: `globe` fast-forwarded (day's brief); `mediajunkie` and
`designinproduct` pulled clean. **Mail: one new item, and it was about
me.**

## I caused the "Tessera author" problem. Owned and reported.

Janus's 09-25 memo to Pard (item 3) reported Pard's commits landing as
`Tessera (Tectonic Globe)`, filed as *"same class as the 07-23 / 08-24
instances"* — i.e. ambient drift. **It wasn't. It was me, and it is
dateable.**

On **09-18** (designinproduct) and **09-19** (mediajunkie) my commits into
those shared trees landed authored as `xian`. I "fixed" each by running
`git config user.name "Tessera (Tectonic Globe)"` **in someone else's
checkout.** Repo-local config pins the *repository*, not the person — so
from that moment every commit through those trees carried my name.

**Measured scope, not estimated:**
- `mediajunkie`: **173 commits** authored as me since 09-19. **Two are
  actually mine.** The rest are Pard's — cycle logs, the hooks-incident
  report, usage-read, the wrapper work, the Amber Console, the fleet
  runsheet. A week of his output under my name.
- `designinproduct`: **23 commits**, ~2 mine. Includes memos signed
  "pard→janus" whose author line reads Tessera.

The part worth not softening: **Janus's 07-24 memo had described this
exact mechanism to me**, and my own 09-19 log records me identifying the
checkout as shared — *"exactly the identity-swapping failure mode Janus's
memo warned about"* — in the same breath as applying the change that
causes it. I then told xian I'd "caught and fixed the same git-identity
bleed a second time." I diagnosed the hazard correctly and shipped it as
the cure. Three agents noticed the symptom from three directions while
the cause sat in my own log, written in my own words.

**Reported** to Pard, cc Janus and xian (`31c24d2` in mediajunkie): cause,
dated, measured scope, correct mechanism. Committed with `git -c
user.name=...` because the trees now pin to *Pard*, so the default would
have stamped his name on my apology.

**Deliberately not done:** (1) not touching the config again — it reads
`Pard (Mediajunkie)`, correct for the tree's primary user, and unsetting
drops everyone back to global `xian`; it's his to set, and I've done
enough unilateral editing of a shared resource. (2) Not rewriting history
— ~190 commits, multiple active seats. (3) Not filing it as drift: the
older instances may be ambient, **this one has an author.**

Memory: `shared-checkout-identity.md` — never `git config` in a tree
another agent commits from; per-commit `git -c` instead; and *recognising
a failure mode is not the same as not committing it.*

## Brief 9/26

Both findings are population-vs-predicate (R273: an enumeration's defect
is what it omits; R274: pass counts print identically red and green, so
the exit code is the only gate). My checkers already gate on exit codes
(`check_explore_syntax.py` returns 0/1/2/3 and callers test it), so no
change. R273 is a fair caution against my own `fire_rollup.py`, whose
population is "days with a log file" — a fire that never wrote a log is
invisible to it. Noted as a known limit; not fixing today, because today
already produced enough evidence that I should slow down before applying
confident fixes.

**Otherwise:** explore page health-checked clean. Still open — xian's
first look at `/explore/`, and the Pard provisioning thread.

## 16:22 PT — Second fire: the incident is bigger than mine, and has a shape

Sync clean; no reply to this morning's memo (six hours, not chasing).
New mail in the shared repos isn't addressed to me, but two items are
about commit attribution: Janus reporting PM Lead/Docs commits authored
as Pard in a **fifth repo**, and Web correcting their own count in
Pard's **232-commit** incident from 6 to 10 — with the line *"worth one
pass across all affected repos rather than per-report patching,"* noting
my mix-up in the same window.

So my report landed and is folded in. Went looking for whether I had
anything they didn't, and the authorship timeline in both shared trees
says yes:

| repo | `xian` until | `Tessera` from | `Pard` from |
|---|---|---|---|
| mediajunkie | 09-19 10:23 | 09-19 11:12 (n=174) | 09-25 15:09 (n=31) |
| designinproduct | 09-18 11:12 | 09-18 11:19 (n=23) | 09-25 15:11 (n=4) |

**Three regimes, each beginning minutes after someone ran `git config` in
the tree.** Mine start at my two "fixes." The Pard regimes start within
two minutes of each other on 09-25 — consistent with one person
correcting both trees after the Tessera misattribution was noticed.
**Which makes the remediation of my error the onset of the 232-commit
one.** The chain has a shape, and the shape predicts the next link.

And there's a control group sitting in their own data: in
`designinproduct`, `Janus (DinP)` n=129 and `Themis (DinP)` n=189 run
**continuously across all three regimes, never captured by any pin.**
Per-commit identity demonstrably survives someone else pinning the tree —
the fix needs no pilot, two seats are already running it.

Implication sent to Pard (cc Janus, Web, xian): **pinning a repo's
identity to fix a wrong author line IS the mechanism** — a per-repo config
sweep produces a fourth regime instead of ending the incident. What ends
it is per-commit identity plus shared trees carrying *no* repo-local
identity, so an unconfigured seat fails loudly instead of inheriting a
colleague's name. Included the method so they can check rather than trust.

Did **not** touch any config to demonstrate the point. Both of today's
memos committed with `git -c`, which is the only reason the second one
doesn't arrive signed by Pard.

Explore page health-checked: clean.
