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

## 16:22 PT — Second fire: rung 5 step 2, the camera path

Routine: no mail for Tessera, no new brief, health green, 246 textures
still on disk.

`scripts/compute_sequel_path.py` → `sequel_camera_path.json`. Reads the
texture sidecar (one owner for the sequence); eased pacing per §6c
(rate 1−0.22·cos2πu over the divergence, accumulated as a float so
rounding can't drift); holds at departure, terminal, each tour stop, and
the final cloud; tour blends get 6 anim frames per texture so an 8-frame
dissolve lasts 2 s and the camera can travel; **opening camera read from
the main film's last frame** (25.32°, 28.75°) rather than typed in; tour
stops aim at each scenario's land-centroid lon from the sidecar along
the shortest arc. PCHIP between keys, duplicates pinning holds.

**The first run printed nothing and exited 0** — I'd defined `main()`
and never called it. A silent tool read as success is exactly the
vacuous-pass shape I've been auditing for; caught because I look at
output, not exit codes. Fixed.

Verified (printed by the script): 1,371 anim frames = 57.1 s; opening
camera equals the main film's last; all five holds lon-spread 0.000;
geo index monotone and complete. **Watch item:** max per-frame lon step
5.48° at frame 890 — the Pangaea Ultima → Novopangea swing (179°) inside
a 48-frame blend. Likely too brisk on a globe; `BLEND_ANIM` 6→12 halves
it. Leaving it for a motion preview to decide rather than tuning blind.

xian asked mid-fire how to preview the latest — answering at the break
with real frames rather than a description.

### Preview stills rendered through the real pipeline (xian: "how might I preview the latest?")

Answered with frames, not prose. Six single-frame Blender runs via
`FRAME_START=FRAME_END=k` (the range mode skips assembly): present (f1),
~+60 (f380), +200 superposed (f760), Pangaea Ultima (f807), Novopangea
(f915), final cloud (f1239). ~8 s a frame, all six on disk in
`~/globe-render/sequel_preview/`. **The sequel path drives render_globe.py
unchanged** — no KeyError, texture discovery found all 246, honest
accounting line printed per run. Sheet sent to xian.

Read of the stills: opening frame is Africa-centred on the main film's
last camera, as designed; divergence and terminal cloud read as a ghosted
globe; Novopangea centres cleanly. **Finding: Pangaea Ultima is a ring
around an inland sea, so its land centroid sits in the hole and the
camera stares into the sea (f807).** Mechanism, not a bug; the knob is
the aim target (e.g. hemisphere-of-most-land instead of centroid). Left
for xian's eye — the inland sea *is* PU's defining feature.

Not launching the full pass yet: two cheap-now/expensive-later calls are
in front of xian (PU framing; the 5.5°/frame tour swing). Pard memo goes
out the moment he says go.

### xian's two calls, applied — and a measurement that changed the plan

**Ultima: "center on the hemisphere with the most land, perhaps nearer to
the sea than the precise center."** Implemented a most-land-hemisphere
search (area-weighted visible land, 5° grid). **It landed on (15°, −25°)
— the same point as the centroid.** The ring is wide enough that the view
centred on its hole sees the most land, so that criterion alone keeps the
camera over the sea. The faithful reading of his intent: the best view
*constrained to the ring side* (≥35° from the centroid → (30°, −60°)),
then blended toward the sea by a bias. Rendered at 45% and 20% for his
eye; `PUN_SEA_BIAS` env, default 0.45. For compact masses most-land ≈
centroid (novon/aurn within 5°); Amasia's lat clamped to 45° so a polar
mass still reads as a globe.

**"A slower tour if it makes sense geographically."** It does: dissolves
now pace by the arc the camera travels (1.2°/frame, 2–7 s), tour holds
3.5 s. Peak lon step 5.48 → **2.40°/frame**; film 57 → 65 s. Big swings
(cloud→Novopangea 4.3 s, Aurica→Amasia 4.0 s) are leisurely; short hops
stay 2 s.

Sidecar now carries `aim.{centroid,most_land,ring_side}`; the path owns
the choice. `render_globe.py` has no per-frame camera distance, so a
pulled-back ring shot isn't a knob without renderer work — noted, not
built.

**Caught on the look, before xian saw it:** Amasia's stop was mostly
ocean. My `LAT_CLAMP = 45` — meant to keep a polar mass "reading as a
globe" — put the camera *under* a supercontinent whose land sits at
60–75°N. The clamp did the opposite of its intent. Raised to 75; aim now
(60°, 30°); re-rendered. One more instance of a protective constant that
needed to be looked at, not reasoned about.

### The renderer's camera latitude was never what the path said it was

Amasia's stop stayed mostly ocean after raising the clamp, and the frame
barely changed between clamp 45 and 75 — so the latitude wasn't reaching
the render. Probed empirically (same texture, `camera_lat=60`, five
longitudes) and then asked Blender itself: rebuilt the renderer's UV
sphere, applied its exact `rotation_euler=(0,-lat,-lon)`, read the UV of
the vertex facing the camera. **`render_globe.py` rotates the globe, not
the camera, with an Euler order that spins the tilt axis: the view
latitude is roughly `-lat·cos(lon) + 10°`** (the 10° is the fixed camera
elevation). Sign-inverted and longitude-coupled. The main film's
`(28.75, 25.3)` looks at lat −11; my Ultima stills were well-framed by
accident. Every shipped film was hand-framed by eye, which absorbed this
silently — so the renderer stays as it is, and the path script converts
true view coordinates to renderer coordinates for the computed stops
only (the main film's departure camera is already in renderer space).

My own first read of the probe sheet was wrong too — I called the
lon −90 frame "full north"; Blender says it's an equatorial view of
Amasia's land-rich western longitude. The model was right, my eyes
weren't. Fitted the closed form against Blender's 5° table (2,664 rows,
mean err 3.9° ≈ UV quantisation), `data_view_model.json`; numeric inverse
`renderer_cam()` asserts its residual. All four stops now reach their
wanted view in the model. Peak lon step 1.83°/frame. **Pending the look:
Amasia's solution has camera_lat 106° — the inverse matched the facing
point, not the image roll, so that frame may be upside-down.**
