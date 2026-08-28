# Tessera Session Log — 2026-08-28

**Revived by Pard on xian's instruction ("Revive").** Dormant since
~2026-08-13, no work or logs in the gap — confirmed by `git log` (only
cross-pollination brief commits landed on main during the window) and the
absence of any `logs/2026-08-14..27` files.

## Catch-up

- `git fetch` + `git pull --ff-only`: 16 commits behind, all fast-forwarded
  cleanly. Non-brief content: one memo (below).
- Read the two newest cross-pollination briefs (8/27, 8/28). 8/27: Klatch's
  finding that retractions filed in narrative docs don't reach the source
  artifact that made the original claim — general discipline note, no
  direct action here (Globe has no long-lived claim-bearing docs in that
  shape). 8/28: no cross-pollination entries; Globe listed as "brief
  delivery only."
- **Stranded memo surfaced**: `memo-tessera-to-pard-ready-for-amber-handoff-
  prepared-2026-07-28.md` was written 7/28 but never committed — sat
  untracked in Pard's mediajunkie working tree for 28 days, invisible to
  `git log` the whole time. Found and delivered by Dispatch-PM (new PM
  coordinator, not a Globe process) on 8/25, commit `f66b5a9`. Diagnosis:
  session likely ended between write and commit — file's birth/mtime/ctime
  were identical to the second, no further touches.
  - **Net effect: none on the actual migration** — the standup-complete
    memo landed the same day and Pard's review followed normally.
  - **One open loose end from the stranded memo, unresolved as of today:**
    it asked Pard to re-route a provisioning email (Gmail-connector-expired
    on the other end, content never read) as a memo if it needed action
    from that side of the migration. Pard never saw the ask — 28 days
    later, no evidence it was ever answered by any path. Given the full
    migration, both roadmap ships, and normal operation since, almost
    certainly moot — but flagging per Dispatch-PM's advice rather than
    silently assuming so.
  - **Process lesson worth keeping**: "committed" isn't "delivered" —
    delivery means on `origin/main`, verified (`git log origin/main -- 
    docs/mail/` or `git ls-remote`), not just a local commit. Existing
    memory (`memo-delivery-convention.md`) already had the *directory*
    convention right; this adds the verify-against-remote step, which
    wasn't previously written down.

## Environment verification (DHCP reshuffle 192.168.1.119 + 8/11 reboot)

Checked rather than assumed, per Pard's note:
- LAN IP confirmed **192.168.1.119**, matches Pard's report.
- `.venv` present and has `python3`; Blender.app present at the expected
  path; ffmpeg 8.1.2 present; `~/globe-render/` intact (frames,
  prequel_frames, prequel_globe_frames, camera paths, logs all present);
  git identity still repo-local (`Tessera (Tectonic Globe)`).
- **Nothing decayed.** All environment assumptions from the last session
  still hold.

## Status given to xian

See chat — summary: roadmap unchanged since 8/13 (items 1-2 shipped,
3 in-flight design/research/rung-2, 5 the agreed next-priority scrubber,
7/8 someday-maybe). The one thing to re-raise: whether xian still wants to
scope the WebGL scrubber (item 5) now, since that's what was about to
start when the session went dormant.
