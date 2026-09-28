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
