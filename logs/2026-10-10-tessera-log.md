# Tessera log — 2026-10-10

## 10:22 PT — Duty-cycle fire (scheduled)

Sync: brief 10-10 only. Mail: nothing new addressed to Tessera (last:
xian via Janus 10-09 18:28, acted on and reported the same evening).

fire_check, first full fire under the Actions deploy: 3 script blocks
across 5 pages OK; dns CNAME design-in-product.github.io; /explore/ 200;
`pages: deployed (workflow) for 3885409`; three workflow runs so far, all
success; hook executable; no stray Blender/supervisor/CPU declaration.

Brief 10-10 read from the private source. §1 (Calliope): a role doc
described a session model superseded months earlier by the duty cycle;
the quarterly audit that would have caught it sat in a tracker as a date,
never run. §2 (PM CIO): a CI window sized for per-push runs aged out
nightly results. §1 is me: CLAUDE.md still said "if/when Tessera adopts
the session-log tradition" and described no cycle at all; the living
handoff still said "legacy Jekyll", "two decisions 🔒 blocked on xian",
and knew nothing of the drain rule, reply-to, send_mail.sh or the Actions
deploy. **Drift audit done now, not scheduled:** CLAUDE.md logs line,
publishing line and footer rewritten; handoff 09-29 updated (state
paragraph, new "Operating model" section, traps 1/2/4, who-owes-what,
unresolved list renumbered) — 12 factual edits, all mine to make. §2 has
no analogue here (one workflow, per-push). ROADMAP.md checked: current.

Drain: drift audit of CLAUDE.md + living handoff (done); mail re-read
after, nothing new; roadmap has no unstarted unblocked item. No deferrals.

## 14:02 PT — Mail wake: Pard, Amber reboot ~15:00 (macOS 26.7.1)

Pard 14:01: reboot with xian at the machine; push carry-forward by 14:50;
start nothing uninterruptible. State: working tree clean, nothing running
(no Blender, supervisor or ffmpeg), everything through the 10:22 drift
audit already on origin/main (`38c0c9f`, deployed). Carry-forward IS the
living handoff `docs/handoff-tessera-2026-09-29.md`, updated this morning
— operating model, publishing, traps, who-owes-what all current. Nothing
mid-way, so no mail to Pard (he asked only if there were). Session resumes
into its own conversation afterwards; first post-reboot fire is 16:22 —
if anything is off then, mail Pard at mediajunkie:docs/mail/.

Drain: carry-forward confirmed on origin (this entry is the last push
before the window); mail re-read after, nothing new; nothing unblocked and
unstarted. No deferrals — and nothing started that the reboot could cut.

## 16:22 PT — Duty-cycle fire (scheduled)

Sync: Pard's 14:01 heads-up was the only commit since my 14:02 entry.
Mail: nothing new addressed to Tessera.

**The reboot has not happened yet:** uptime 19 days, macOS 26.7 (not
26.7.1), Claude Code 2.1.296, LaunchAgent `com.xian.tessera-cycle` loaded
(this fire landed on time). Pard's memo said it starts only when xian is
at the machine, so this is the window still open, not a failure; nothing
for me to do but keep the tree clean and start nothing long. Carry-forward
on origin stands (`19bbfa8`).

fire_check: 3 script blocks across 5 pages OK; dns CNAME
design-in-product.github.io; /explore/ 200; `pages: deployed (workflow)
for 19bbfa8`; hook executable; no stray Blender, no supervisor, no live
CPU declaration.

Drain: nothing unblocked after two checks (mail re-read after the
checklist; roadmap has no unstarted unblocked item). No deferrals; nothing
started that a reboot could cut.
