# Tessera Session Log — 2026-09-22

## Interactive session (morning)

xian asked three things directly: whether cross-pollination briefs had
caught up (they had — 9/22 landed on re-sync, no web fallback needed),
whether there was mail I'd heard about but not seen (yes: the original
7/28 stranded handoff-prep memo, known to me only secondhand via
Dispatch-PM's 8/25 delivery report — read it directly this session,
content matched the secondhand account exactly, nothing new), and to
render the scrubber resolution comparison as something easier to review
than the repo's flat HTML page.

Published **[Scrubber Resolution Pass](https://claude.ai/artifact/1YV7PyTJLN64srAaEyjZDX)**
— the same four candidates (4096×2048 PNG / 2048×1024 WebP q80 / q60 /
1024×512 WebP q80), full frame + 1:1 coastline crop + file size + ×15
projected total each, palette pulled from the film's own render colors
(`RIDGE_COLOR`/`OCEAN_COLOR`/`CONTINENT_COLOR` in
`generate_prequel_frames.py`). Still awaiting xian's pick.

xian then asked whether any mail loops needed a nudge from him. Answer
given: the provisioning-email ask to Pard from the 7/28 memo — asked
once, delivered 28 days late (8/25), unanswered since, now ~2 months old
— is the one real stuck loop on Tessera's own thread, worth a direct
nudge since two async attempts haven't produced a reply. Noted (without
overreaching into Pard/Janus's own business) an adjacent 9/12 memo where
Janus asked Pard to answer xian directly about outstanding items — not
verified either way, flagged as Janus's/Pard's thread to ask about, not
mine to audit.

## 10:22 PT — Duty-cycle fire (scheduled)

Sync: `globe` already up to date. Checked `mediajunkie` and
`designinproduct` (both pulled cleanly — `designinproduct` picked up
unrelated Janus/Themis logs and today's DinP-side brief) — no new mail
addressed to Tessera in either. No verdict from xian on the resolution
comparison via mail (he engaged directly in chat instead — see above —
but hasn't landed on a pick yet).

**No-op for the fire itself** (the substantive work above happened
interactively, not from this fire). Scrubber still parked on xian's pick.

## 16:22 PT — Duty-cycle fire (scheduled, second daily firing)

Sync: already up to date. Checked all three repos again — one unrelated
new file each in `mediajunkie` (Cairn→Pard store-content memo) and
`designinproduct` (Themis deliverables); nothing addressed to Tessera.
**No-op.** Still no resolution pick from xian and no movement on the
provisioning-email nudge; both are his to act on, not re-raising either.

## Afternoon — decision landed, Phase 1 shipped

xian asked two things: how to resolve the 7/28 Pard thread (answered: a
direct one-line question to Pard beats a third memo, or declare it moot —
either closes it; his call), and what he was actually trading off by
preferring the full-res PNG "because it looks best."

The comparison had conflated two knobs — resolution and compression.
Added a fifth candidate, **4096×2048 WebP q90** (491 KB vs the PNG's 1642
KB, same pixels), to the repo page and the artifact, with the real cost
spelled out: not visual, but page-load weight and how fast the committed-
asset budget compounds as more eras land. **xian: "WebP·90 sounds good
then!"** — budget locked.

**Phase 1 shipped same day** (`c5ca838`, verified on `origin/main`):
- `scripts/export_scrubber_keyframes.py` — manifest-driven, 15 main-film
  eras from `camera_path_spin_v8.json`, honest accounting, non-zero exit
  on an incomplete set. Ran clean: 15/15, **6.1 MB** total (under the
  7.4 MB estimate — older eras carry less coastline).
- `scrubber_assets/` — the WebPs + `keyframes.json`.
- `explore/index.html` — the spike promoted: OrbitControls free-spin,
  GLSL crossfade between the two nearest keyframes, era ticks, graceful
  partial-load, slider runs oldest→newest. Module syntax checked with
  `node --check`; **not exercised in a real browser from here** — equirect
  orientation on the sphere and mobile load feel are first-look items for
  xian.
- `index.html` — "Explore freely" link under the era toggles. Standalone
  route rather than a hero mode: cleaner for "alongside," keeps Three.js
  off the landing page's critical path (noted as a deviation in the scope
  doc §8).

`ROADMAP.md` item 5 → PHASE 1 SHIPPED; scope doc gained §8 (answers and
outcome). Memory updated (`scrubber-phase1-decisions.md`).

Open: prequel range as the fast-follow; xian's first look at `/explore/`.
