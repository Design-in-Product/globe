---
name: render-environment-status
description: "What the local machine can/can't run for the globe render pipeline (updated 2026-07-13 evening)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 1b2ec6f6-37e2-43d3-9f24-caf747003efc
---

As of 2026-07-13 (evening), xian's local machine runs the **full** globe render pipeline: **Blender 5.1.2 installed** via `brew install --cask blender` (xian-approved, 2026-07-13) at `/Applications/Blender.app`, plus ffmpeg (homebrew) and Python 3.12 with Pillow. Prior renders (v6, Feb 2026) used Blender 5.0.1 on this same machine; 5.1.2 runs the existing scripts unmodified. **gplately is not importable** in system python — only needed to regenerate source frames or for the deep-time prequel (roadmap item 2). All prior outputs exist in-repo: 1001 source equirectangular frames in `frames/`, 2422 rendered globe frames in `render_frames/`, and `camera_path.json` (2422 anim frames, 1000 Ma → 0). Fast-draft pattern: EEVEE at 960×540 vs full Cycles pass (~8.4 s/frame, ~5.7 h for 2422 frames at full speed). **The machine is an Apple M1** (June session log's "M4" was a wrong reconstruction). **Check Low Power Mode before renders** (`pmset -g | grep lowpowermode`) — it GPU-throttles renders ~3×; ask xian to disable it (system setting).

Related: [[roadmap-execution-mandate]]
