# Tessera log — 2026-10-14

## 10:22 PT — cycle fire

Synced (brief 10-14 pointer landed, read in the private hub source). Mail:
nothing new since Pard's disk note (handled 10-13).

**Palette B pass finished 05:48, clean.** Main 22:41, prequel 02:36,
sequel 05:42; 0 crashes; 2738/2186/1795 frames; the six films are in
`~/globe-render/palette_cobalt-brass/` with the shipped films' exact frame
counts and durations (114.1 / 91.1 / 74.8 s). Seams checked on extracted
frames: prequel-last → main-first mean diff 0.7/255, main-last →
sequel-first 0.8/255; one label per frame on both sides. Declaration row
(04:57) overrun by 51 min, not the 2 h warned; Pard memoed the close-out
(`43f7f8a` in mediajunkie): Blender idle, +13 GB, nothing deleted,
`df` shows 53 GB free (something else moved ~17 GB; not mine).

**Supervisor bug found and fixed** (`16f0b9d`): the "no live Blender row"
check's awk program was pasted in shell-escaped form, so under `set -u`
bash read `$1` as a positional and the warning fired on every pass since
10-04 regardless of the row. The declarations were always on origin/main.

**Ship staged, films gated.** Exporters take `MAIN_SRC`/`PREQUEL_SRC`/
`OUT_DIR`/`PALETTE` (`59f64cf`), so the Explore keyframes were re-exported
from the recoloured textures without touching the repo: 23 past (13 MB,
up from 9.9) + 56 future (3.9 MB, up from 3.3), manifests identical.
Poster v7 turned out to be raw `render_1300.png`, so `poster_v8.png` is
the same frame from the new pass. Branch **`palette-cobalt-brass`**
(`0f5897f`, pushed) carries: cobalt-brass CSS vars on the landing page
and Explore, v8 / prequel v2 / sequel v3 references, OG/Twitter image →
poster_v8, v8 version card, roadmap rows 4 and 6 → Shipped, footer.
The films are NOT on the branch: the rule since v1 is no film enters the
repo before a human has watched it in motion. Ship = xian watches →
merge → copy six mp4s → push → `wait_pages.py` → Pard told before the
old frame sets go.

ROADMAP items 4/6 → STAGED; handoff updated; memory updated.

Drain: Cycles pass verified; supervisor fix shipped; keyframes, poster,
site and Explore theme staged on the branch; Pard closed out; docs
current. Deferred: the ship itself (blocker: xian's eyes on the films —
I cannot watch motion, and the Gondwana lens hold and the Ultima pan are
the two places it can go wrong). Mail re-checked twice, nothing new.
