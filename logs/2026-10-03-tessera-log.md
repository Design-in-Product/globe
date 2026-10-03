# Tessera Session Log — 2026-10-03

## 10:22 PT — Duty-cycle fire (scheduled)

Sync: fast-forwarded (10/03 brief); siblings clean. **No mail addressed to
Tessera.** Health green — explore syntax OK, live `/explore/` 200, Pages
built for origin/main (checked by commit via `wait_pages.py`), hook wired.

Brief 10/03: finding 2 is my own `wait_pages.py` fix reported back to the
constellation; finding 1 (routing adapters must carry the registry's
description text) has no routing layer here to apply to. Noted.

## Rung 5, step 1: production textures for the sequel globe pass

Pipeline contracts pulled from the code rather than remembered:
`render_globe.py` globs `FRAMES_DIR/FRAME_PREFIX*.png` as the texture list
and maps anim→texture via the camera path's `geo_frame_idx` (2-frame
crossfade at transitions); the path needs `metadata.time_range/pacing`
(August's KeyError); `assemble_globe.py` stamps `time_ma`/`era_label`.

`scripts/generate_sequel_frames.py` → `~/globe-render/sequel_frames/`
(**outside the repo**, 66 MB): **246 geo frames** at 2048×1024, no text.
201 divergence frames (0→+200 at 1 Myr, crossfaded between the 20 Myr
snapshots, four scenarios superposed), then the tour as 8 blend frames +
1 hold per scenario (32+4), 8 return blends, 1 final hold. Honest
accounting: 246 emitted = 246 on disk = 246 expected.

**Design call:** re-centring is *not* baked into the textures. On a globe
it's a camera move, so each tour frame records its scenario's land-
centroid longitude (pun −27°, novon 152°, aurn −177°, amn 48°) in a
sidecar `sequel_frames.json` that owns the sequence; the camera-path
script will consume it rather than re-derive it (detect, don't enumerate).
Blend frames exist so the Blender pass's 2-frame crossfade becomes a real
dissolve. Pacing/holds belong to the path, not the textures.

Contact sheet looked at once: present crisp → cloud → terminal cloud →
mid-blend → four holds → final. Novopangea/Aurica are edge-cut in the
flat sheet, as expected — the camera handles that.

`assemble_globe.py`: `time_label()` stamps negative times as `+N Myr`
(would otherwise have printed "−200 Ma" — wrong, not just ugly). Tested
on −250/−200/0/66/1000; compiles.

**Next:** `compute_sequel_path.py` (eased tempo per §6c, holds, tour
camera keys from the sidecar), then the Pard courtesy memo, then Blender.
