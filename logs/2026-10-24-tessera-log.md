# 2026-10-24 — Tessera log

## 10:24 PT — cycle fire

Sync: 68e4cfe (brief pointer). Mail: none. fire_check all green: pages deployed for 68e4cfe, dns CNAME, explore 200, stray blender 0, live declarations 0.

Brief 10-24, two instrument findings, both checked here. (1) Join-based array comparison in JS: no `.join(` used in a comparison anywhere in index.html, explore/index.html or the preview; nothing to fix. (2) A probe should print and verify its own SDK version: this one landed. `render_globe.py` is written against Blender 5.x (ShaderNodeMix input indices, the 5.0 frame_offset workaround) and never said which Blender it ran under; the generators never said which gplately made the frames. Now: render_globe.py prints `Blender <version> (<binary>)` at startup and exits 4 on a different major unless `BLENDER_MAJOR_OK=<major>` says it has been driven; render_supervised.sh logs `blender --version` and the path at start (the Blender log can be truncated by a crash, the supervisor log is not); generate_frames.py and generate_prequel_frames.py print gplately/pygplates versions when they import them. Verified: py_compile on all three, bash -n on the supervisor, a Blender background dry run of the guard (5.1.2, pass), and the version lookup in the Amber .venv (gplately 2.0.0, pygplates 1.0.0). No render launched; nothing re-rendered.
Drain: both checks done, one fix landed. Deferred with blockers, all xian's: the below-the-fold preview swap (blocker: his edit review of previews/home-2026-10-21/); the 1:03 ghost test render (blocker: his verdict after watching); the sequel's first-30-Myr extrapolation and the authors' letter (blocker: his choice); the LICENSE file (blocker: his licence decision). The disk-space item is Pard's to close.

## 16:22 PT — cycle fire

Sync: at d59bbcc, nothing new on origin. Mail: none. Brief: 10-24 already read this morning. fire_check all green: pages deployed for d59bbcc, dns CNAME, explore 200, stray blender 0, live declarations 0. No-op beyond this entry.
Drain: no unblocked work. Deferred with blockers, all xian's: the below-the-fold preview swap (blocker: his edit review of previews/home-2026-10-21/); the 1:03 ghost test render (blocker: his verdict after watching); the sequel's first-30-Myr extrapolation and the authors' letter (blocker: his choice); the LICENSE file (blocker: his licence decision). The disk-space item is Pard's to close.
