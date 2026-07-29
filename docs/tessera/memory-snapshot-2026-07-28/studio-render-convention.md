---
name: studio-render-convention
description: "All Blender rendering runs on the Mac Studio (ssh studio), nohup-detached — never harness-tied, never on the laptop"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1b2ec6f6-37e2-43d3-9f24-caf747003efc
---

As of 2026-07-14, all Blender render work goes to xian's **Mac Studio** (`ssh studio`, M1 Max, 64 GB RAM, ~6 s/frame Cycles 1080p/64-samples vs the M1 laptop's ~17). Blender 5.1.2 lives at `/Applications/Blender.app` there (copied from the laptop); render workspace is `~/globe-render/` (frames/, scripts/render_globe.py, camera paths). No brew/ffmpeg on the Studio — ffmpeg assembly happens on the laptop after rsyncing frames back.

**Why:** xian, 2026-07-14: "shall we give the studio all the rendering work from now on?" after the Studio outperformed the laptop 3× and survived a session restart that killed the laptop's render.

**How to apply:** launch renders via `ssh studio 'nohup ... &'` — **always nohup-detached, never as a harness background task** (those die with the agent session; cost ~3 h on 2026-07-14). Use `FRAME_START`/`FRAME_END` env vars for ranges, skip-existing makes reruns free. Keep `~/globe-render/frames/` and scripts in sync with the repo before launching (rsync).

Related: [[render-environment-status]]
