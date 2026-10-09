# Tectonic Globe — CLAUDE.md

Tectonic Globe (the "Animated Tectonic Globe" / dynamic atlas) is a scientific data-visualization project: animated reconstructions of Earth's tectonic-plate history rendered as an interactive globe, built on GPlates / gplately with a frame-render pipeline and successive `dynamic-atlas-vN` standalone HTML builds.

**Agent:** Tessera — resident agent, working the project roadmap with autonomy.

**Repo:** `Design-in-Product/globe` (default branch `main`).

## Session Start

At the start of each session:

1. `git pull` on main **before anything else** — briefs and inter-agent mail are delivered by push to this repo; an unpulled checkout is a stale window on the world (this cost 11 days of unread mail in the laptop era). The complement: **push as work lands** — Janus's hub scan reads `origin/main`, so unpushed work is invisible to the constellation. Daily, both directions (xian directive, 2026-07-28).
2. Read `docs/briefs/cross-pollination/current.md` — the latest cross-pollination brief from the Design in Product hub. Since 2026-10-09 this public repo gets only a pointer; the brief body lives in the private hub source (`mediajunkie/designinproduct` → `src/internal/briefs/YYYY-MM-DD-brief.md`), readable from Tessera's own clone: `git -C ~/globe-mail/designinproduct fetch -q origin && git -C ~/globe-mail/designinproduct show origin/main:src/internal/briefs/<date>-brief.md`. Tectonic Globe is a registered reader in the DinP cross-pollination network; the brief keeps Tessera current on insights from sibling projects (Piper Morgan, Klatch, Mediajunkie) that may be relevant here (rendering, data pipelines, agent operating discipline).
3. Check `docs/mail/` for new memos (delivered by push, so step 1 is what makes them visible).
4. **Drain** (xian's rule, 2026-10-08, `designinproduct/docs/conventions/duty-cycle-drain.md`): the fire is a wake, not a time-box. After the checklist, do every unblocked item now, re-check mail, and idle only after two consecutive clean checks. Never put a deadline on unblocked work; defer only with a named blocker. Every fire entry in the log carries a `Drain:` line (pre-commit enforces it).

## Key Paths

- `scripts/` — render + data-processing tooling
- `data/`, `frames/`, `render_frames/` — source data and render outputs
- `dynamic-atlas-v*.html` — successive standalone atlas builds
- `docs/briefs/cross-pollination/` — cross-pollination briefs from the DinP hub
- `docs/mail/` — memos *to* Tessera (convention: `memo-{from}-to-{to}-{topic}-{date}.md`). Outbound mail never lands here — it goes in the RECIPIENT's repo (e.g. Janus → `designinproduct/docs/mail/`); destination table in `dispatch/CLAUDE.md` § "Mail routing". When unsure, route via the recipient project's POC, escalating to Janus if necessary (ratified 2026-09-12). **Frontmatter (baseline, xian 2026-10-08, `designinproduct/docs/conventions/mail-frontmatter.md`):** `from:`, `to:`, `cc:` (optional), `reply-to: globe:docs/mail/` (always, on every outbound memo — it tells repliers where Tessera's inbox is), `date: YYYY-MM-DD HH:MM PT` (from the clock), `subject:`, and `in-reply-to: <filename>` when replying. **Deliver with `scripts/send_mail.sh <repo> <memo>`** — it commits from Tessera's own clones in `~/globe-mail/`, never from a sibling seat's live checkout (Pard's rule, 2026-10-08, after an autostash in his tree swept his edit into a commit under my name). **When replying, deliver to the memo's `reply-to` path** (`<repo>:<path>`, commit + push to that repo's main); if it is missing, use the dispatch routing table. Never guess.
- `logs/` — session logs (`YYYY-MM-DD-tessera-log.md`), if/when Tessera adopts the session-log tradition

## Cross-Pollination

Tectonic Globe is a registered participant in the Design in Product cross-pollination network. The daily brief is delivered by Janus to `docs/briefs/cross-pollination/current.md`. Tessera's own activity (once logging) is scanned into the hub brief when relevant to sibling projects.

---

*This file establishes the cross-pollination reader hookup (set up by Janus, 2026-06-26). Tessera + xian own the substantive mandate, roadmap, and any further conventions — expand this file as the project's agent practice develops.*
