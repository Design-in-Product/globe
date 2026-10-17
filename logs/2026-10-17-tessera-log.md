# 2026-10-17 — Tessera log

## 05:04 wake — prequel v3 Cycles pass launched

The re-armed epoch scheduler fired at 05:00:29, declared Blender until 11:03 (row supersedes the void 03:19 one), and launched `PREQUEL_TAG=v3 … palette_pipeline.sh cobalt-brass` at 05:03. Stage 3 found main's 2738 frames intact and is re-assembling `tectonic_globe_v8.mp4` (identical frames; `review-2/` keeps the verified copy), then renders `render_prequel_v3/` (2318 frames, ~5 h at 7.9 s/frame → ~10:15) and assembles `tectonic_prequel_globe_v3.mp4` with the dissolve into main's first frame. Watch set; the 10:22 fire verifies.

Drain: nothing else unblocked (blockers unchanged: xian has not watched the second cut; crossfade question is his call).

## 10:22 fire

Sync: `9c7fec9` (today's brief pointer). Mail: nothing new. Brief 10-17 read from the hub clone: Klatch's triage of a defect census by data mutability (frozen snapshot vs live data) — noted, no census running here.

Prequel v3 pass: Blender launched 05:12 after the main re-assembly; 2250/2318 frames at 10:22 (~8.3 s/frame), finishes ~10:32, assembly ~10:40, inside the 11:03 row. Watch `btkl2of0d` wakes me; then: verify the opening spin (frames 1–132 one eased turn, frame 133 == old frame 1 geometry), the amber cloud, the dissolve into main's first frame; copy to `review-2/`, rebuild the series preview with v3, update `watch.html`, tell xian.

Drain: brief read; nothing else unblocked (blockers: render finishing ~10:40; xian has not watched the second cut; crossfade question is his call). Two clean mail checks (10:22, 10:24).

## 10:45 wake — prequel v3 globe complete; the second cut is whole

`PIPELINE COMPLETE` 10:44 (Blender 05:12–10:38, 2318 frames, zero crashes; row ran to 11:03). `tectonic_prequel_globe_v3.mp4`: 96.6 s, 22 MB. Verified: frame 1 == frame 133 (mean diff 0.00: the turn lands home), frame 2 vs 1 = 0.01 (eased start), mid-turn differs; cloud amber at 2.8 s and 31 s; last frame vs main's first 0.64 (dissolve seam clean). Staged in `review-2/`, series preview rebuilt with all three second-cut films (285 s), `watch.html` deep-time section → v3 (97 s; timings shifted +5.5 s; opening-spin item added), still `prequel_v3_spin_cloud_last.png`.

Ship set now complete on disk: `tectonic_globe_v8` / `tectonic_flat_v8`, `tectonic_prequel_globe_v3` / `tectonic_prequel_v3`, `tectonic_sequel_globe_v3` / `tectonic_sequel_flat_v3`. Branch `palette-cobalt-brass` already references these names.

Drain: v3 verified, staged, preview and page refreshed. Deferred: ship + `stale-1/` clearance (blocker: xian has not watched the second cut in motion — the rule); crossfade-ghost decision (blocker: xian's call; options on `watch.html` and in yesterday's 21:16 entry). Two clean mail checks (10:45, 10:47).

## 16:22 fire

Sync: up to date at `9680d99`. Mail: nothing new. `fire_check.sh`: site 200, Pages deployed for `9680d99`, no stray Blender, no live declarations. Disk 89 GB free.

Handoff (living doc) extended with a 10-16/17 paragraph: the second cut's three fixes, render windows, ship set and location, and the three items open for xian (ship; the crossfade ghost; the futures' snapshot cadence). Everything else on the board is gated on xian watching the second cut in motion.

Drain: health check, handoff updated. Deferred: ship + old-frame clearance (blocker: xian has not watched the second cut); crossfade decision (blocker: xian's call). Two clean mail checks (16:22, 16:25).
