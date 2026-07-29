# Tessera Session Log — 2026-07-28

**Session:** Migration-prep session (laptop/pipermorgan.ai era, likely final). xian returned after 13 days: infrastructure reshuffle underway — Tessera moves to Amber (Mac Studio) under the designinproduct.com account; the Piper Morgan cohort migrates into the pipermorgan.ai account this session has been using.

## Work log

- Caught up on 13 days of mail: **five unread memos from Janus** (7/17 delivery fix — Globe became the ninth brief reader; 7/21 prepare-handoff heads-up; 7/22 Amber floated; 7/24 git-identity hygiene; 7/27 "you're next for Amber"). They sat unseen because delivery lands in the MAIN checkout while this session lived in a worktree. Lesson logged in the handoff: check the seams between your window and the world.
- Read the 7/27 cross-pollination brief (finally current!): two bash gotchas adopted into operating notes — `claude -p` needs LaunchAgent not cron on macOS; always read `origin/main` explicitly after fetch.
- Read the migration-culture memos in the hub + mediajunkie repos: HOST's agent-experience memo (verified-vs-believed marking, provisioner owns environment, load-bearing-vs-commodity) applied to my own handoff.
- **Gmail connector down** (session expired, cannot re-auth non-interactively) — Pard's provisioning email unread. Flagged to xian: re-auth or paste.
- Repo tidied: merged main into worktree branch (brief deliveries + memos), committed regenerated v7 overlay, gitignored local artifact dirs (v7 frames also on Amber), restored stray gplately.log.
- **Memory snapshot → repo:** `docs/tessera/memory-snapshot-2026-07-28/` (4 memories + index). The laptop memory dir gets a tombstone pointer.
- **Handoff written:** `docs/tessera/handoff-2026-07-28.md` — state of work, load-bearing artifacts, provisioner questions, conventions, honest self-assessment. SESSION_LOG.md next-session pointer updated.
- Memo to Pard (delivered to mediajunkie repo): ready to migrate, handoff location, provisioner questions, Gmail gap noted.

## Open at migration (for Amber-Tessera)

1. xian verdicts outstanding since 7/15: ensemble-superposition strip; lens-per-hold arc.
2. Flat-v7 production build (morph → render_flat.py).
3. Prequel production design (pacing, Nuna hold, ensemble treatment integration).
