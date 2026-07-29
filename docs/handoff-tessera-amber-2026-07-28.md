# Handoff: Tessera, laptop era → Tessera on Amber

**From:** Tessera (final pipermorgan.ai session, 2026-07-28)
**To:** Tessera (first Amber session) · **cc:** Pard (provisioner), xian, Janus
**Shape:** cohort standard per Pard's 2026-07-28 memo. Every claim VERIFIED (artifact exists) or BELIEVED (my read — test before building on it).

---

## §1 Hard-won lessons — the judgment that dies with this session if unwritten

1. **Draft cheap, judge, extend one axis.** Every good thing this stint produced went EEVEE-draft → xian's eye → one new dimension → production. Both times I was tempted to skip a rung (the 5.7 h Cycles pass before pacing was locked; the ensemble before the blur strip framed the question) the discipline paid for itself instead. VERIFIED by the whole 7/13–7/15 arc.

2. **Assuming your window on the world IS the world costs real things.** Twice: a harness-tied background render died silently with the session (~3 h lost, 7/14 log — always `nohup` long jobs); and eleven days of mail sat unread because delivery lands on main while I lived in a worktree (7/28 log). On Amber, with eleven residents and shared infrastructure, check the seams FIRST: where does mail land, what does your checkout track, what dies when your session does. VERIFIED, painfully.

3. **Root-cause before restarting.** The slow-render saga (7/14): my first theory (`nice` → QoS throttle) was wrong; killing/relaunching cost a restart and changed nothing. The real cause was macOS Low Power Mode (~3× GPU throttle) — found by measuring, not pattern-matching. Related finds that will recur: `moov` atom placement breaks phone playback (always `-movflags +faststart` on previews, VERIFIED); Blender renders ~6 s/frame on Amber vs ~17 on the M1 laptop (VERIFIED 7/14).

4. **Area-weighted centroids DEGENERATE for near-global landmass clusters** — the "center" of a hemisphere-spanning supercontinent can land in open ocean. Hand-frame those holds; trust computed centroids only for compact clusters (Gondwana 63% ✓, Pangaea 93% ✗). This cost a full audit to learn (7/13 log) and WILL recur when placing the prequel's Nuna hold. VERIFIED with comparison stills.

5. **Antimeridian polygons need `pygplates.DateLineWrapper`** — naive fill+Geodetic wraps the whole map in continent color. The old fallback renderer in `generate_frames.py` still carries this latent bug. VERIFIED (3-pass debug, 7/15).

6. **xian's design instincts outrank my first implementations — solicit them early.** The probability-cloud concept (ensemble superposition, not blur) and the rotate-under-the-projection idea both came from xian reacting to a cheap draft. The drafts' job is to provoke exactly that. VERIFIED twice in one day.

## §2 Load-bearing vs commodity

**Load-bearing:**
- `camera_path_spin_v8.json` — THE approved path (four spins, 132-frame holds, Gondwana recentered). Source of the shipped v7. VERIFIED.
- `scripts/add_spin_reveal.py` — `--target-hold` and `--recenter` encode xian-approved design decisions. VERIFIED.
- `scripts/test_flat_morph.py` — approved flat-v7 technique (projection morph + rotate-under, per-pixel mesh, bilinear). VERIFIED at HD ("very smooth action" — xian).
- `scripts/test_ensemble_uncertainty.py` — superposition uncertainty treatment. VERIFIED at strip quality; awaiting xian verdict.
- `docs/research/deep-time-plate-models-2026-07-13.md` — cao2024 decision + rationale.
- Unencoded design state: the lens-per-hold pitch (sinusoidal → S-polar azimuthal → Mollweide → orthographic-as-globe-convergence, 7/15 log) — pitched, no verdict.
- `docs/tessera/memory-snapshot-2026-07-28/` — persistent memories off the old account.

**Commodity:** all test_*/check_* dirs, verify PNGs, render logs, draft strips — regenerable from scripts above.

## §3 In-flight state

- **Roadmap #1 SHIPPED:** v7 live at globe.dinp.xyz since 7/14 (spin reveals; faststart-remuxed 7/15). VERIFIED.
- **Flat-v7:** technique approved, production build not started. Open design call: lens-per-hold arc (no verdict). Then wire into `render_flat.py`.
- **Prequel (#2):** data solved (cao2024 = drop-in Merdith superset, VERIFIED at 1000 Ma handoff); uncertainty treatment built (no verdict); production design open (pacing across 1.8 Gyr, Nuna hold placement — see lesson 4).
- **Owed to the brief pipeline:** nothing formally; a distributed-render writeup was queued 7/14, never sent, likely moot now.
- **Two xian verdicts outstanding since 7/15:** ensemble strip; lens arc. Re-surface gently.
- **First moves on Amber, from xian directly (2026-07-28):** (a) catch up on the missed cross-pollination briefs — dated copies live in `docs/briefs/cross-pollination/` from 7/18 onward, none read after 7/27 by the laptop era; (b) make sure your working checkout syncs with main DAILY, both directions — pull so briefs/mail reach you (see lesson 2), push so Janus's scan sees your work. Not urgent, but before settling into roadmap work.

## §4 Amber, as questions (I've only ever seen it through ssh)

1. Does `~/globe-render/` survive from the 7/14 distributed render (Blender 5.1.2, 1006 textures, v8 path, 2738 v7 frames)? BELIEVED intact — verify count before relying.
2. GPU/disk budget: is a multi-hour Blender run acceptable alongside eleven residents, and where should frame output live?
3. ffmpeg: absent on 7/14 (VERIFIED then). Installed since? If not, where does assembly run?
4. gplately/pygplates/cartopy env: never existed on Amber (renders needed only Blender). The prequel's frame generation NEEDS one — provision or point me at it. (Laptop's was `~/Development/atlas/.venv`.)
5. Git identity for my commits on a shared host (per Janus's 7/24 hygiene memo)?
6. Where do cross-pollination briefs + mail land relative to the checkout I'll work in? (See lesson 2 — I won't repeat the worktree blind spot, but tell me the seams.)

## §5 Conventions in force (xian-ratified, all VERIFIED in use)

Renders nohup-detached, never harness-tied · `FRAME_START`/`FRAME_END` + skip-existing for resumable/splittable renders · `-movflags +faststart` on every preview · land work on main as you go (Janus scans main; read `origin/main` explicitly on sibling repos) · outgoing mail to the RECIPIENT's repo · daily logs in `logs/`, narrative in `SESSION_LOG.md`.

---

*The picture emerges one verified tile at a time. See you on the other side.* 🌍

— Tessera
