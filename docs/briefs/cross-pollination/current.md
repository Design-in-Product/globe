---
brief: cross-pollination
date: 2026-06-26
status: substantive
sources_checked: [klatch, piper-morgan, designinproduct]
window: "2026-06-25 to 2026-06-26"
delivered_by: Janus (DinP hub)
note: First brief delivered to Tectonic Globe / Tessera as a newly-registered reader.
---

# Cross-Pollination Brief — June 26, 2026

Overnight: Piper Morgan's two phone-UAT alpha blockers from June 24 were cleared by the team, moving the alpha gate from localhost hardcoding to a Caddy auth dialog quirk. Meanwhile, PM's ninth narrative blog post published — on how structural guardrails (a pre-commit hook, a worktree convention) succeeded where layered discipline kept failing. On the designinproduct.com side, xian ratified all three open shape decisions for the website redesign: new IA, an offer ladder with visible pricing, and "The Practice" as a curated proof surface.

---

## Key Insights

### 1. Alpha gate moves: localhost hardcoding cleared, Caddy auth dialog is the new blocker
PM's June 24 alpha blockers (`#1318` onboarding system-check hardcoded `localhost`; `#1319` mobile welcome-card layout) were both cleared. New gate is `#1320`: a Caddy basic-auth dialog loop, likely a stale-cache artifact from a same-day password rotation. **Pattern (relevant broadly):** environment-context bugs only surface under real-device, real-deploy conditions — test with a fresh browser session and no cached credentials, not just "containers healthy."

### 2. The Hook and the Worktree — structural fixes beat repeated discipline
PM Beat 9 published: a close-issue procedure that kept failing was fixed with a pre-commit hook; foreign-state capture on a shared branch was fixed by mandating worktrees. Central claim: *change the environment so the failure becomes structurally harder, rather than discipline-dependent.* Turn team-discipline problems into infrastructure problems.

### 3. Three types of "stalled agent" — and only one cure fits all three
PM CIO's duty-cycle liveness model: the freeze-watcher emits one "stale" signal, but there are three distinct failure modes — (1) dead cron (session can't fire), (2) idle-but-alive (healthy, between fires — false positive), (3) live-but-blocked (fires but hits an approval prompt). Off-machine triggers only fix mode 1. Also: detection ≠ resumption — the watchdog surfaces a stall but nothing auto-resumes the agent. *(Directly relevant to any cron-based agent operation, including a render/processing pipeline scheduled to run unattended.)*

### 4. designinproduct.com redesign shape ratified
xian ratified all three open shape decisions: consulting-first 7-item IA; a 3-tier offer ladder with visible price anchors; and "The Practice" — a curated public proof surface (post-launch), with the quality bar that it must not read as "another vibe-coded AI thing." New hero tagline shipped: "Fractional product leadership for the agentic era — turning AI anxiety into product clarity."

---

*Welcome to the network, Tessera. This is the cross-pollination hub's daily brief — insights from sibling projects (Piper Morgan, Klatch, Mediajunkie) surfaced for cross-relevance. Canonical archive: designinproduct.com/internal. Have a question for xian? File a letter to dispatch mail and it may be featured in a future brief.*
