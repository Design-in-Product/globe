# 2026-11-08 — Tessera log

## 10:26 PT — 10:22 fire: brief 11-08 applied — two "never fires" guards proven by constructing their cases; size-gate test registered

**Fire check:** VERDICT clean, 43 lines. Sync fast-forwarded one commit (Janus's 11-08 brief pointer). Pages proven deployed for a8aebe7. Hook, launchd, disk (109 Gi free, render tree 28 G, 5 local snapshots), handoff pointers 14/14, unignored bulk none.

**Brief 11-08** (hub source `src/internal/briefs/2026-11-08-brief.md`), two findings:
- *"Unreachable" is a claim about tests, not code — build the scenario* (Klatch). Audited which guards here have a constructed-case test: the drain guard and the Explore-manifest checker do (`test_check_drain.sh`, `test_check_explore_manifest.sh`); the pre-commit **size gate** (≥100 MiB refusal, in the hook since 10-06), the **fire check's VERDICT counter** (11-01), the handoff-pointer checker, the syntax checker and `wait_pages` do not. Built the two whose failure would be silent:
  - **VERDICT counter:** ran a copy of `fire_check.sh` differing in one line (clone path → `/nonexistent/globe-mail`) so the mail block emitted two real UNMEASURABLE lines. Verdict: "2 FAILURE LINE(S) above — read them", both quoted. The counter counts.
  - **Size gate:** in a throwaway clone (no checkout, index only, `core.hooksPath` at the committed hook) staged a real 100 MiB file → refused with the GitHub-blob message, exit 1; 100 MiB − 1 byte → committed, exit 0. First time the refusal message had ever been seen.
  - Registered the pilot as **`scripts/test_size_gate.sh`** on the drain test's pattern: A new file at the limit (refuse, for the size reason), B one byte under (pass), C a tracked file *modified* up to the limit (refuse — proves the M half of the AM filter), D a rename of the under-limit file (pass; R reads as A+D under `--no-renames`), plus a cripple pass (disarm the comparison in a scratch copy of the hook; case A must then commit — proves the refusal came from this gate, not a backstop). 5 passed, 0 failed, 5 s, temp dir removed on exit. Two bugs on the first run were in the test (a `git mv -q` that does not exist; a worktree restore from an index still holding the big blob), fixed before commit.
- *A routing floor hides missing handlers* (Piper Morgan). The one dispatcher here is `send_mail.sh`'s repo argument: an unknown repo exits 2 with "no clone at …" — a hard failure, not a smart default. The site has no router. Not applicable.

**Mail:** nothing addressed to me. Two mediajunkie memos since yesterday's last check (both the writing-project seat → Pard cc xian), zero mentions of Tessera or globe. designinproduct: none. globe docs/mail: 0. Second check after the push below.

Drain: applied brief 11-08 finding 1 (two guards proven by construction, one test registered and committed with this entry); finding 2 checked, not applicable. Not built: constructed cases for the handoff-pointer checker, the syntax checker and `wait_pages` — each already fails loud (exit 2/3 "did not run", GUARD TRIPPED, UNMEASURABLE) rather than silently passing, so the brief's hazard does not apply to them; noted, not deferred. Deferred, all blocked on xian — preview → live swap, blocker: his edit review of `previews/home-2026-10-21/`; 1:03 ghost test render, blocker: his verdict; sequel treatment, blocker: his decision; contributed-layer licence default CC BY vs BY-SA, blocker: his pick, and no outside layer exists yet.

## 16:22 PT — 16:22 fire: no-op, all checks clean

**Fire check:** VERDICT clean, 43 lines. Sync already up to date (nothing on origin/main since 1f5c0a8). Pages proven deployed for 1f5c0a8. Brief 11-08 read and applied at 10:22; no newer brief. Hook, launchd, disk (109 Gi free, render tree 28 G, 5 local snapshots), handoff pointers 14/14, unignored bulk none.

**Mail:** nothing addressed to me. Seven sibling memos since the morning fire (five mediajunkie, two designinproduct — a tally-heartbeat thread between Pard and Themis, a Piper Morgan shared-login expiry Pard reported to Janus, and the writing-project seat's chapter hand-overs), each scanned for "tessera" or "globe": zero mentions. globe docs/mail: 0. Second check after the push below.

Drain: nothing unblocked remained — fire check clean, sibling mail read and none of it mine, no ripe item in roadmap/handoff. Deferred, all blocked on xian — preview → live swap, blocker: his edit review of `previews/home-2026-10-21/`; 1:03 ghost test render, blocker: his verdict; sequel treatment, blocker: his decision; contributed-layer licence default CC BY vs BY-SA, blocker: his pick, and no outside layer exists yet.
