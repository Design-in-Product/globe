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
