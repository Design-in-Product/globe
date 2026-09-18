# Handoff: Tessera — Amber reboot gate (fleet-wide, 2026-09-18)

**Why this exists:** Janus's fleet memo (`docs/mail/janus-to-all-non-pm-
residents-...-2026-09-18.md`): 24 red, 0 green, Amber restarts today or
tomorrow, xian intends **fresh sessions with no prior context imported**.
Whatever isn't in this file or the repo is gone. Written for a stranger,
not for future-me.

## Project state, in one paragraph

Tectonic Globe: animated tectonic-plate reconstructions (GPlates/gplately),
shipped as standalone HTML + video on globe.dinp.xyz (GitHub Pages,
`Design-in-Product/globe`, single `main` branch, `CNAME`, no build step).
**Roadmap #1 (main film) and #2 (deep-time prequel) are SHIPPED and live.**
Roadmap #3 (future-projection sequel) is mid-design. Roadmap item 5 (WebGL
scrubber) is scoped and **actively in flight this session** — see below.
Full roadmap: `ROADMAP.md`. Full narrative history: `logs/*-tessera-log.md`
(daily) and `docs/design/`, `docs/research/` (design/research docs, dated).

## Who-owes-what (both directions)

| Counterparty | They owe Tessera | Tessera owes them |
|---|---|---|
| **xian** | Eyeball verdict on the scrubber resolution comparison (blocks Phase-1 asset-export budget — see In Flight #1) | The Phase-0 spike + resolution comparison itself (building now, this fire) |
| **Pard** (mediajunkie, Amber infra) | Advance notice of host changes (reboots, DHCP) when possible | Accurate environment self-reports when asked (schedule mechanism, etc.) |
| **Janus** (DinP curator) | Relaying xian's decisions promptly (track record: reliable — LaMantia heads-up 8/12, four scrubber answers 9/12) | Reading/acting on daily cross-pollination briefs; responding to fleet-wide asks like this one |
| **Dispatch-PM** (Piper Morgan coordinator, one-off) | Nothing ongoing — not a Globe process | Nothing ongoing |

## Deliberately unresolved — do not fix these

1. **The "little oddness at the end" of the globe prequel** (xian flagged
   pre-chain, ~8/9). Registration work done afterward may have fixed it;
   **no explicit verdict was ever given either way.** Don't assume fixed,
   don't re-open uninvited — ask xian if it comes up.
2. **A provisioning-email loose end** from a stranded 7/28 memo (delivered
   28 days late, 8/25, by Dispatch-PM — see `docs/mail/memo-dispatch-pm-
   to-tessera-stranded-memo-delivered-2026-08-25.md`). Almost certainly
   moot given the full migration since, but never explicitly confirmed.
   Leave it; don't chase.
3. **Physical-product (item 7) and biome-painting (item 8) roadmap ideas**
   are xian-confirmed *someday/maybe* — researched, logged, intentionally
   not scoped further. Don't build toward either without a fresh explicit
   go. If biome-painting ever does move: the best dataset found (CESM1.2.2
   540Myr, CC BY 4.0) is fine to use commercially; the more directly
   "paintable" one (Köppen–Geiger set) is **CC BY-NC-ND — do not build a
   commercial/POD product on that one** without separate permission.
4. **The "Wikiglobe" north star** (`layers-platform-framing.md` in agent
   memory, not in this repo — see Environment note below on memory
   survival): xian's framing that tectonics/climate/culture/physical are
   independent layers over one substrate, extensible open-source-style.
   It's a soft architectural bias (prefer layer-separable designs when the
   cost is low/neutral) — **not a scoped direction, don't propose building
   it.**

## Counterparties — what was most recently gotten wrong with each

- **xian**: told him a memory file had been updated to reflect his
  refinement of the "Wikiglobe" framing when the edit tool had not
  actually been called — caught and corrected the next turn. **Lesson:
  don't narrate a write as done without the tool call actually landing in
  the same turn; memory/file edits are silent unless verified.**
- **Pard**: no correction pattern on file. Interactions have been
  protocol execution (stand-down, schedule reporting) without back-and-
  forth corrections, as far as recorded.
- **Janus**: no correction pattern on file. Memos acted on as received
  without needing revision.
- **Dispatch-PM**: not a correction of Tessera's reasoning, but a process
  gap Dispatch-PM surfaced: a memo was treated as "delivered" once
  written+committed to the recipient's repo, but it sat **uncommitted**
  for 28 days and nobody checked. **Fix now in practice: verify delivery
  against `origin/main`** (`git log origin/main -- docs/mail/` or
  `git ls-remote`), not just "I wrote the file" or "I committed it
  locally."

## In flight, named, with who's waiting

1. **WebGL scrubber (roadmap item 5) — active this session.** Scoped
   2026-08-29 (`docs/design/scrubber-scope-2026-08-29.md`). xian answered
   all four open questions 2026-09-12 (`docs/mail/janus-to-tessera-cc-
   xian-pard-all-four-answers-...md`): **alongside placement, main-era-
   first range (1000→0 Ma, 15 eras), eyeball-first on resolution, spike
   first.** Sequence: Phase-0 spike → resolution comparison → **xian's
   eyeball (blocking Phase-1 asset-export budget)** → Phase-1 export at
   confirmed budget. Nothing is blocked on xian until the comparison
   artifact exists — that's the immediate next-action for whoever picks
   this up, unless it was finished later in this same fire (check
   `logs/2026-09-18-tessera-log.md` and git history after this commit for
   whether the spike/comparison landed).
2. **Sequel rung 3 (roadmap #3)**: motion window ~+40–80 Myr, coherent
   scenario-members, not started. OSF-grid-reading code exists only in a
   prior session's scratch space (not durable, not in this repo) — treat
   as needing to be rebuilt from `docs/research/future-plate-models-
   2026-08-10.md` if picked up. Nobody actively waiting.
3. **Social kit posting** (`previews/social/`, built and delivered 8/10):
   posting to social platforms is explicitly **xian's move**, not
   Tessera's — not blocked, just not Tessera's to do.

## Environment (verified 2026-09-18, don't trust older memory blindly)

- LAN IP: `192.168.1.119`. `.venv` (Python 3.12 — 3.14 has no pygplates
  wheel), Blender.app at `/Applications/Blender.app` (not on PATH), ffmpeg
  8.1.2 (no libass — all overlays are PIL-burned, see `render_flat.py`/
  `assemble_globe.py`). Render workspace `~/globe-render/` (frames,
  prequel_frames, prequel_globe_frames, render_frames_v7, camera paths) —
  outside the repo, survives reboots, not git-tracked.
- **Scheduling mechanism has CHANGED since the last handoff era.** A real
  LaunchAgent now exists: `~/Library/LaunchAgents/com.xian.tessera-
  cycle.plist`, label `com.xian.tessera-cycle`, fires **10:22 and 16:22
  daily**, runs `mediajunkie/scripts/seat-cycle-fire.sh tessera`, logs to
  `mediajunkie/logs/tessera-cycle-launchd.{out,err}`. This supersedes the
  old self-report ("session-scoped ScheduleWakeup only, no LaunchAgent") —
  that was accurate as of August, is **not** accurate now. Tessera did not
  set this up and doesn't know who did or exactly when between 9/12 and
  9/18 — Janus's 9/12 memo explicitly flagged the absence of any firing
  mechanism as the blocker, so this was almost certainly built in response
  to that.
- **Agent memory** (`~/.claude/projects/-Users-xian-Development-globe/
  memory/`) is a separate persistence layer from this repo — **it may not
  survive a fresh-session-no-import policy the same way this repo does.**
  If it's gone, the load-bearing content to reconstruct: the "layers
  platform framing" / Wikiglobe north star (see Deliberately Unresolved
  #4), the physical-product someday/maybe status, and the memo-delivery
  verify-against-remote convention (see Counterparties, Dispatch-PM). All
  three are restated in this handoff so the repo alone is sufficient.

## Cold-start reading order

This file → `ROADMAP.md` → most recent `logs/*-tessera-log.md` entries →
`docs/design/scrubber-scope-2026-08-29.md` (if continuing item 5) →
`docs/briefs/cross-pollination/current.md` (ritual, per `CLAUDE.md`).
