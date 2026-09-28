# Tessera Session Log — 2026-09-28

## 10:22 PT — Duty-cycle fire (scheduled)

Sync: `globe` fast-forwarded (9/28 brief); siblings clean. **No mail
addressed to Tessera.**

Two identity-leak items in mediajunkie, both to Pard, neither mine to
answer: the Intelligence Sweep pushing via the GitHub MCP API commits as
the *connector's* GitHub identity (a different route from the config
mechanism entirely), and a Zephyr weather commit authored `xian` — the
unconfigured-seat case my 09-26 memo already covers. Janus says the fix is
Pard's call; restating my analysis at him would be noise. Read Pard's
reply to Lead too: that thread is a permissions classifier, not identity,
and nothing there contradicts what I sent.

## Brief 9/28 — and it caught my own instrument

Finding 1 (Pard): reproduce a refusal **at the layer the proposed fix
governs** — a git-scoped allow-rule would have been installed, felt like a
fix, and left an `Edit`-layer block untouched. Cousin of my week's lesson.
Audited my own recent fixes against it: `.nojekyll` (before/after on the
actual build), `git -c` identity (checked the author line), the syntax
checker, the grid reader, the rollup — all verified at the layer that
fires. The failures this week were *diagnostic claims*, not unverified
fixes. Finding 2 (prompt caching) doesn't apply; Globe makes no API calls.

Then ran my own instruments, which is where it got pointed:

**`fire_rollup.py` was undercounting me** — 1 fire reported on 09-25/26/27,
each of which had 2. Two population defects, exactly the shape R273
described:

1. Fire sections matched the *phrase* "duty-cycle fire", so every fire I
   titled differently ("Second fire: …") was invisible. Now matched by the
   leading clock time, which prose headings never carry.
2. The claimed-window and the git-window were off by one day, so a real
   log read as "no session log for this day".

Verified against ground truth rather than assumed — every day 09-20..09-28
had exactly two fires, and the table now reads 2 across all eight.
Committed.

**The instrument I built to detect my own degradation was undercounting my
activity.** It would have shown a decline that wasn't happening, and could
equally have masked one that was. Fourth instance this week of the same
lesson, and the first one my own tooling caught rather than xian.

## Health

Explore syntax OK; live `/explore/` 200; Pages green. Grid reader
self-test passes (100/99.06/99.06/100%).

**Still with xian:** first look at `/explore/`; the 7/28 Pard provisioning
thread; and whether to start sequel rung 3 proper (motion window) — the
prerequisite reader is rebuilt and verified, so it's ready when he is.

## 16:22 PT — Second fire: xian's first look arrived, both fixes shipped

**Mail from xian (via Janus)** — the first look I'd been waiting on since
09-22. Verdict: **"explore is super cool!"** with two defects.

**1. Arrow keys "do not seem to work or they advance by imperceptible
increments."** Correct, and mine twice over. The native range step is
1 Ma against an 1800 Ma span — 0.05% of the track, genuinely invisible —
**and my hint text advertised the control anyway.** A promised affordance
that was inert is worse than no affordance. Now: arrows step 10 Myr,
**shift+arrows jump era to era** (what a keyframed timeline actually
wants), home/end for the ends, `preventDefault` so the native 1 Ma step
doesn't stack underneath. Hint text rewritten to state what each does.

**2. "a bit dark and gloomy. more brightness and higher contrast."** The
gloom is mostly in the textures, not the chrome — they're matplotlib
renders on `OCEAN_COLOR #1a425a`. So the fix went into the fragment
shader (brightness 0.10, contrast 1.18) rather than only lightening CSS,
which would have brightened the frame around a dark globe. Page ground
and the fixed bars lifted to match.

**Chose the amount by measuring rather than guessing:** simulated the
exact shader maths in PIL against a real keyframe — mean luma 0.327 →
0.396, **+21%** — and sent xian the A/B so he can say more or less. Both
uniforms are one-line changes. Same eyeball-first discipline that settled
the resolution question, and the only honest way to tune something I
can't see render.

Shipped `79c9735`. Three of the four first-look items are now closed:
orientation fine (he'd have said), controls fixed, look fixed. The
1200→1000 Ma ghost-slide went unmentioned — **not treating silence as a
pass**, still open.
