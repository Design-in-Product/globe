# Tessera Session Log — 2026-07-14

**Session:** Continuation of the 2026-07-13 local session, same worktree branch `claude/roadmap-review-planning-418a49`.

## Session start (05:51)

- xian's overnight verdicts: **recentered Gondwana reveal (v8) approved.** Camera path locked: `camera_path_spin_v8.json`.
- Janus's daily brief claimed "no commits in this repo in the past 48 hours." Investigated: Janus is right *from where it looks* — yesterday's two commits (92d40030, 48e10721) live only on this worktree branch; local `main` and origin/main still sit at June 26. Janus scans main. **Process fix: land work on local main as we go** (fast-forward merge from the worktree branch); pushing to origin is xian's call since the repo is public.

## Work log

- 05:55 — Log started; committing pending log edits and fast-forwarding local main so today's brief sees the activity. Main now at branch head (4 new commits visible to Janus's scan). Pushing to origin (public repo) left as xian's call.
- 06:00 — Hardened `render_globe.py` for the long run: env-var overrides (`CAMERA_PATH_FILE`/`RENDER_DIR`/`OUTPUT_PATH`) + skip-existing frames → interrupted renders resume instead of restarting ("structural fixes beat discipline," per PM's Beat 9). Committed; main fast-forwarded.
- 06:05 — **Launched the v7 final render**: Cycles GPU, 64 samples, 1920×1080, 2738 frames from `camera_path_spin_v8.json` → `render_frames_v7/` → `tectonic_globe_v7.mp4`. ETA ~6.4 h (≈12:30 pm). Killable anytime (`pkill -f render_globe`), resumes where it left off.
- 06:15 — **Prequel spike (roadmap #2) — success.** `scripts/test_deeptime_frames.py` rendered 7 frames (1800→1000 Ma) from `cao2024` in house style, all layers present, zero warnings. **1000 Ma frame ≈ identical to Merdith frame 0** → seamless handoff confirmed. Nuna reads well: scattered blocks (1800) → assembled (1500). PMM downloaded cao2024 into `data/plate-models/`.
- 06:35 — **Render was 3.3× too slow** (~28 s/frame vs v6's 8.4; would've been ~21 h). First suspect was my `nice -n 10` (macOS QoS demotion) — killed + relaunched at normal priority; resume feature kept the 9 frames. Rate unchanged (~26 s/frame) → not nice.
- 06:50 — **Actual root cause: Low Power Mode is ON** (`pmset -g` → `lowpowermode 1`) — GPU-throttles ~3×, also explains yesterday's slow-ish EEVEE drafts. System setting → asked xian to disable (render keeps running; speeds up when flipped). Also corrected the record: this machine is an **Apple M1**, not M4 (June log's reconstruction was wrong; fixed in memory too).
- 07:05 — LPM off → laptop at ~17 s/frame (better, still ≠ Feb's 8.4 — possibly Blender 5.1 or the Feb render ran on different hardware; not chasing).
- 07:10 — **Distributed render across xian's new Mac Studio** (`ssh studio`, M1 Max, 64 GB): rsynced our Blender.app (879 MB, arm64-portable, no installs) + frames/ (1.2 GB) + script + v8 path. Added `FRAME_START`/`FRAME_END` env range to `render_globe.py` (committed); assembly deferred to the machine with the full set.
- 07:25 — Studio benchmark: **~6 s/frame** (vs laptop 17). Balanced split at frame 916: laptop renders 1–916 (was at 273), Studio 917–2738. Both ETA ≈ 3 h (~10:30 am). Merge plan: rsync studio range back into `render_frames_v7/`, verify 2738 contiguous frames, assemble locally with overlay.
- 11:03 — Session restart revealed a split outcome: **Studio (nohup-detached) ran flawlessly** — 1518/1822 frames, ~34 min left. **Laptop render died with the session** (harness-tied background task) — only at 353/916. Lesson: long renders must be `nohup`-detached from the agent session, like the Studio's was.
- 11:10 — Rebalanced + relaunched both detached: laptop takes 354–499; Studio auto-chains onto 500–916 when its main range finishes (watcher loop queued on the Studio itself). Everything lands ~12:20; then rsync-merge + assembly.
- 11:20 — **xian: Studio takes ALL rendering from now on** ("no deadline, joy project, we keep moving"). Killed laptop render, rsynced laptop's 400+ frames to Studio (it now holds 1923), requeued the Studio chain as 1–916 (skip-existing skips synced ones). Laptop's only remaining render job: ffmpeg assembly. Saved as durable convention in memory (`studio-render-convention`): renders on Studio, always nohup-detached.
- 13:05 — **Studio finished all 2738 frames** (both ranges + chained follow-on, zero babysitting). Rsynced back, verified contiguous non-empty set.
- 13:15 — **🎉 ROADMAP #1 RENDERED: `tectonic_globe_v7.mp4`** — 114.1 s, 1080p Cycles, 2002 overlay events, all four spin reveals (Gondwana recentered). Spot-checked Cycles frames: quality good. Delivered to xian for the full watch-through.

## Awaiting xian

1. Watch-through verdict on v7 (esp. spin pacing in context + Gondwana recenter ramps at full quality).
2. Push main to origin? (public repo — makes activity visible to GitHub, keeps Pages site source current; index.html still points at v6 until we update it.)
3. If v7 passes: update `index.html` to v7 + flat-projection v7 render (render_flat.py against the v8 path) as follow-ups; then roadmap #2 prequel begins in earnest.
