# Tessera Session Log — 2026-10-06

## 10:22 PT — Duty-cycle fire (scheduled)

Sync pulled the 10/06 brief; otherwise clean. **No mail addressed to
Tessera**; **no answer to the two 🔒 decisions** anywhere in the three
repos since yesterday's escalation to Janus (tight grep, own mail
excluded). Health green: brief age 0 d, site 200, Pages built, hook live,
no stray Blender, 0 live CPU declarations.

**Brief 10/06, both findings audited against this repo.**

Finding 1 (macOS `sed -i -E` silently takes `-E` as a backup suffix, runs
BRE, exits 0): no `sed -i` in any tracked script; no `*-E` / `*-i`
artefacts tracked or untracked. Clean.

Finding 2 (a CI health check that hardcodes one workflow name is a
coverage claim for one file; derive the list and print the denominator):
**this one I had.** Three HTML pages carry inline scripts
(`index.html`, `explore/index.html`, `previews/scrubber-spike/index.html`);
the pre-commit gate covered exactly one path, and the checker's regex
matched only `type="module"` — so `index.html`'s classic script, the JS
that drives the live hero and the film chaining, **had no gate at all**.
A syntax error there would have shipped the landing page broken while
every check I run said green.

Fixed, structurally: the checker now extracts every inline `<script>`
block (module or classic, skipping `src=` includes and non-JS types),
checks each, and prints the denominator ("3 script block(s) across 3
page(s)"); the hook gates every staged `.html`, not a hardcoded path;
`fire_check.sh` passes `git ls-files "*.html"` rather than defaulting to
one page. **Proven before trusted:** real run 3/3 OK; a deliberate break
in `index.html`'s classic script → checker exit 1 and the hook refuses
the commit; tree restored (0 staged lines).

Same shape as the 9/28 rollup undercount and the 10/02 deploy poll: an
instrument that measured one thing and read as "the site." The lesson
that keeps paying is the denominator — say what was checked, and derive
that list from the thing itself.

**Postscript, 10:35 — a slow Pages build, recorded rather than glossed.**
The "Pages built" in the 10:22 health block was the *pre-push* check
(`3e0d2d6`). The push of `6c59b74` registered a build at 10:24 that sat
in `building` ~11 min against a 20–93 s norm; `wait_pages.py` timed out
at 300 s (exit 2, its honest code — not "built"). Ruled out my side
first: `.nojekyll` still on origin/main, the commit touched four script/
log files. A 25-min background waiter saw it reach **built at 10:35**,
live `/explore/` 200. GitHub-side slowness, transient; nothing to fix.
Worth having: the wait script's timeout is a state, not a failure, and I
didn't write "built" until it was.

## 10:55 — xian's two decisions; one answered, one I had broken

xian, 10:50: Decision 1 = **dissolve** ("the jump-cut is too abrupt").
And: the Ultima "45 vs 20" image "shows the same image twice."

**It did.** `md5` of `sequel_preview3/pun.png` and `pun_b20.png`: byte-
identical. Cause: `render_globe.py` skips frames already intact on disk;
the 10-03 loop rendered both candidates at frame 837 into the same
`RENDER_DIR`, so the second run was "0 rendered, 1 already on disk" and
I copied the 45% frame under the 20% name. I then *recommended 45%* over
an image I had never seen. The recommendation is withdrawn — not because
it's wrong, but because it was made on nothing.

Then I did it again: the first corrected 3-up (0% / 45% / 100%) had A ≡ C
for the identical reason — same dir, same frame index — caught by eye
before sending, confirmed by md5 and "already on disk" in the log. One
RENDER_DIR per candidate fixed it; `md5 | sort -u | wc -l` → 3 of 3
distinct before it went out. Trap 7 added to the handoff.

Also: the "20%" candidate was a 9° nudge from 45% — too subtle to be a
real choice even rendered. The 3-up now spans the actual range: A ring-
side (0%), B as rendered (45%), C centroid over the inland sea (100%).
🔒 Decision 2 reframed as A/B/C, clock restarted 10-06 11:10.

Decision 1 shipped: `INITIAL_BLEND_SRC/_FRAMES` in `assemble_globe.py`
(mirror of the terminal blend, 24 frames, a runs 1→0); v1 re-assembled
from `render_2738.png`. Previews §8, ROADMAP item 3, handoff updated.

Seam verified from the re-assembled mp4 (frames at 0/0.5/1.0/1.5 s: boundaries → half → clean sequel). Janus memo pushed to designinproduct (`1122ae0`).

## 11:05 — Decision 2: centroid, plus a slow pan

xian (mid-turn): "I actually like centroid the best. Probably we should
also rotate the globe in a slow pan so people get the feel for it? I
assume the other side of the globe is almost all ocean?"

Measured before answering: at +250 the hemisphere centred on C is 54.5%
land; the antipodal hemisphere is **0.5%** land (global 27.5%). The far
side is the world ocean — the assumption holds exactly.

Pan: `PAN = {"pun": (180°, 288 f)}` in `compute_sequel_path.py` — 3.5 s
static hold at the centroid, then a westward half-turn over 12 s, camera
keys every 30° of view-lon through `renderer_cam` (the renderer's lon is
coupled, so a two-key pan would not be an honest arc). Max lon step
1.12°/f. Film 66.1 → 74.8 s. The next stop (Novopangea) departs from the
pan's END, not the stop. Five stills across the pan, one RENDER_DIR each,
md5 5/5 distinct, sent 11:07: C → ring edge → coastline sliding off →
open ocean. "Lon spread 359" in the hold print is the ±180 wrap, not a
spin.

Re-render: old/new paths agree through anim frame 755 (the divergence and
the departure to the tour are untouched); 756..1794 = 1,039 frames ≈ 1.6 h.
Prefix hardlinked into `sequel_render_v2/`; declared; supervisor launched.

## 12:48 — v2 tour render complete

Supervisor: `COMPLETE: 1795/1795 intact after 0 crash(es)`, 11:07:49 →
12:47:48 (100 min for 1,039 frames, 5.8 s/frame), inside the 13:07
declaration. Metal SIGSEGV denominator now 1 in ~3,700 frames across three
supervised passes. Assembling v2 with the dissolve; then the site chain.

## 13:05 — sequel v2 assembled; chained into the site as the third act

`tectonic_sequel_globe_v2.mp4`: 1,795 frames, 74.8 s, 8.5 MB, opening
dissolve in. Checked in motion at 36/39/42/45/48/51/54 s: centroid →
ring edge → coast sliding off → last land → open ocean → Novopangea's
dissolve arrives. Reads as intended.

Site: `FILMS.future` (globe only, `flat: null`), `NEXT_ERA` chain
deep→main→future on `ended`, third era button "Continue into the
future", Flat button disabled while in the future (no flat sequel; the
chain stops at the present in flat view), tagline + chain-note updated.
Checker: 1 block OK. The film lives at the site root like its siblings;
previews §8 points at `../`; the v1 draft is removed from the tree
(history keeps it) so the repo carries one sequel, not two.
