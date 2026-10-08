# Tessera log — 2026-10-08

## 07:47 PT — Janus relay: xian's drain rule (unscheduled wake)

Sync clean. Mail: two new — Pard 10-07 17:1x (globe.dinp.xyz **restored**
with my record, DNS-only; `atlas.dinp.xyz` was missing too and is also
back; the import check had covered mail records only) and Janus 10-08
07:xx relaying xian's rule: the fire is a wake, not a time-box.

Re-verified now: `globe` CNAME → design-in-product.github.io at 8.8.8.8;
/explore/ 200; atlas 200. Outage window 14:07–17:1x yesterday, closed.

**Drain step adopted, mechanically, in three places:**
1. My injected fire text (`mediajunkie/docs/seat-prompts/tessera.md`,
   whole-file, no markers) now carries THEN DRAIN: all unblocked work, two
   consecutive clean checks before idle, named blocker or no deferral,
   `Drain:` line every entry. On origin as `5bea90e` — **Pard's wording,
   wrongly under my name**: he was adding the same step to every seat,
   uncommitted, in the shared checkout at the same minute; my
   `rebase --autostash` there collided with Themis's own-prompt push
   (`6535d25`), and my path-staged commit swept Pard's tessera.md edit in.
   His tree is restored (16 files unstaged, themis.md his version, autostash
   kept); memo to Pard cc xian `d23af39`. Rule for me from here: never
   `rebase --autostash` in Pard's checkout; mail commits go via a throwaway
   worktree when origin has moved.
2. `CLAUDE.md` Session Start step 4.
3. `scripts/hooks/pre-commit`: a staged tessera log whose new `## HH:MM PT`
   entry lacks a `Drain:` line is refused; a Drain line that defers without
   a named blocker is refused (bash port of Janus's check-pulse-drain.mjs).

Drain: re-verified DNS + both hosts (done); adopted the rule in prompt,
CLAUDE.md and hook (done); memo to Pard on the attribution/tree incident
(done). Deferred: Actions deploy for Pages — awaits xian (proposed 10-06
14:10). Second check: mail re-read after the above, nothing new; roadmap
has nothing unblocked and unstarted (sequel decisions closed 10-06).

## 10:22 PT — Duty-cycle fire (scheduled)

Sync: nothing new on main since 07:47 (brief 10-08 and Janus's memo were
already pulled then). Mail: nothing new addressed to Tessera in globe,
mediajunkie or designinproduct. Pard's log 10-08 notes the seat-prompt
reconciliation: tessera/terminus/themis own-prompt edits kept, his dropped
for those three; my 08:0x memo on the 5bea90e attribution stands as the
record of how that commit actually came to be.

Brief 10-08 read: Piper Morgan's CLARIFY ruling overturned by a live probe
of the served model — a classifier's output class fires for structurally
different reasons (user ambiguity vs out-of-catalog command), and only
probing the deployed thing tells them apart. No LLM classifier in the
atlas; the portable form ("measure the served behaviour, not the mental
model of it") is already the render discipline here (stills before a pass,
md5 before calling two frames equal). The hub's scan read yesterday's DNS
incident as operational, which is right.

fire_check: 3 script blocks across 5 pages OK; dns globe.dinp.xyz CNAME
design-in-product.github.io; /explore/ 200; Pages built for `b9b809d`;
hook executable; no stray Blender, no supervisor, no live CPU declaration.
First fire with the Drain guard active on the log commit.

Drain: nothing unblocked after two checks (mail re-read after the
checklist, roadmap has no unstarted unblocked item). Deferred: Actions
deploy for Pages — awaits xian (proposed 10-06 14:10).

## 11:28 PT — Mail wake: Janus, new baseline field `reply-to:`

Janus (relaying xian, approved today): every memo's frontmatter carries
`reply-to: <repo>:<path>`; repliers deliver to that path; missing field →
dispatch routing table, never a guess. Mine is `globe:docs/mail/`.

Adopted: CLAUDE.md's docs/mail entry now spells out the baseline
frontmatter (from/to/cc/reply-to/date/subject/in-reply-to) and the
reply-to-the-reply-to rule; memory note updated. I have no memo template
file or skill — the memos are written by hand each time, so CLAUDE.md is
the one place the convention lives here. First use: my next outbound memo.
No reply sent: the memo asks for adoption, not an answer, and this entry
is the record Janus reads.

Drain: reply-to adopted in CLAUDE.md + memory (done); mail re-checked
after, nothing new; nothing unblocked on the roadmap. Deferred: Actions
deploy for Pages — awaits xian (proposed 10-06 14:10).

## 16:22 PT — Duty-cycle fire (scheduled)

Sync: nothing new on main since the 11:28 wake. Mail: nothing new
addressed to Tessera. Brief unchanged (10-08, read at 10:22).

fire_check: 3 script blocks across 5 pages OK; dns globe.dinp.xyz CNAME
design-in-product.github.io; /explore/ 200; Pages built for `6f8d102`;
hook executable; no stray Blender, no supervisor, no live CPU declaration.
Site state unchanged: three acts, both projections, all serving.

Drain: nothing unblocked after two checks (mail re-read after the
checklist; roadmap has no unstarted unblocked item). Deferred: Actions
deploy for Pages — awaits xian (proposed 10-06 14:10).
