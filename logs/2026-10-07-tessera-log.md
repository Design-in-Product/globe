# Tessera log — 2026-10-07

## 10:22 PT — Duty-cycle fire (scheduled)

Sync: one commit overnight, Janus's brief for 10-07 (`828f0cc`). Mail:
nothing new addressed to Tessera in globe, mediajunkie or
designinproduct — the newest items under my name in the other two repos
are my own outbound memos (10-04/05/06), all answered or closed.

Brief 10-07 read: (1) Piper Morgan ADR-080 — LLM decides meaning, code
decides permission, enumerate-and-confirm before destructive ops;
(2) Haiku prompt caching needs a ≥4,096-token prefix. Neither lands on
this project (no LLM in the atlas, no Haiku calls); the portable piece
of (1) — "show before you act" as a mandatory step, not a nicety — is
already how renders and comparisons run here after 10-06 (stills before
a 1.5 h pass; md5 before calling two images a comparison). The hub's scan
read yesterday's shipping of the sequel in both projections as
"operational… not brief-worthy", which is its call to make.

fire_check: 3 script blocks across 5 pages OK; /explore/ 200; Pages
built for `828f0cc`; hook executable; no stray Blender, no supervisor,
no live CPU declaration. Site state unchanged: three acts, both
projections, all serving. No-op fire; the one open item still awaits
xian (Actions deploy for Pages, proposed 10-06 14:10).

## 16:22 PT — Duty-cycle fire (scheduled) — SITE DOWN, DNS

Sync: nothing new on main since 10:22. Mail: nothing new addressed to me;
Pard→Janus 11:0x names me only as a trust dialog to clear before this fire
(it was cleared — this fire ran; restart confirmed on `claude-fable-5-1`).

**fire_check: `live /explore/: 000`** — curl exit 6, cannot resolve.
Root-caused before anything else: `globe.dinp.xyz` is **NXDOMAIN** at
8.8.8.8 and 1.1.1.1, SOA from arch.ns.cloudflare.com. dinp.xyz moved from
Hover DNS to Cloudflare at 14:07 today (Pard + xian; Pard's record lists
the imported Hover records as 5 MX + TXT + `mail` CNAME — no `globe`).
GitHub Pages side intact: cname globe.dinp.xyz, https_enforced, built;
github.io origin still 301s to the custom domain. So: one missing CNAME,
site dark since ~14:07–14:25, all three acts + both projections + /explore/.

Fix is `globe CNAME design-in-product.github.io`, DNS-only, on the
Cloudflare zone. The token is xian's, scoped to Pard, and my permission
layer declined the credential read — correctly; not mine to touch. Memo to
Pard cc xian in mediajunkie (`0083503`,
`tessera-to-pard-cc-xian-globe-dinp-xyz-is-nxdomain-since-the-cloudflare-move-add-the-globe-cname-2026-10-07.md`)
with the evidence, the exact record, verification commands, and a request
to diff Hover's full zone against Cloudflare's before anything else at
Hover is deleted. fire_check now prints the CNAME lookup ahead of the HTTP
probe so NXDOMAIN and a Pages failure stop looking alike.

Rest of the check: 3 script blocks across 5 pages OK; Pages built for
`2b3f2ac`; hook executable; no stray Blender/supervisor/CPU declaration.
Open: (1) DNS record — Pard; (2) Actions deploy for Pages — xian, since
10-06 14:10. Re-verify DNS first thing next fire.
