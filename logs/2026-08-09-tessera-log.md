# Tessera Session Log — 2026-08-09

**Session:** xian returned after a week ("looks great") and approved the full
chain: prequel flat cut locked, previews updated, intermediates cleaned,
globe pass go.

## Work log

- Ritual: pulled a week of briefs (7/30–8/9 skimmed; methodology notes, no
  Globe action items); no new mail.
- **Flat cut LOCKED**: draft5 → `tectonic_prequel_v1.mp4`; drafts 1–4
  removed; previews page updated (prequel section marked LOCKED).
- **Globe pass launched** (the last production step):
  - Hand-framed the Nuna hold camera from ortho candidate renders of the
    real 1452 Ma texture: **lon −120, lat +15** (cluster centered, breathing
    room). Lesson-4 discipline held — no centroids trusted.
  - Terminal camera = v8's opening **exactly** (lon 115.05, lat −12.34);
    verified the registered prequel terminal texture at that view against
    the shipped globe film's actual first frame — same configuration.
  - Camera track: PCHIP over anim frames, keys at 1800/1452/1252/1100/1000;
    the westward antimeridian sweep rides the landmass migration
    (verified against full-span draft frames at 1252 + 1100 Ma); holds
    pinned by duplicate keys; max 0.5°/frame.
  - `render_globe.py` gained FRAMES_DIR/FRAME_PREFIX env; prequel path
    metadata gained the keys render_globe prints (first launch died on
    KeyError — caught in an early-frame check, relaunched).
  - Early-frame verification: render_0011 shows the 1800 Ma cloud world on
    the sphere, correct framing and the main film's look. ~5.8 s/frame,
    ≈3.5 h. Pard memo delivered (>2h courtesy).
- On completion: sweep → assemble (PIL overlay; terminal blend into the
  globe film's render_0001) → deliver pair.

## Evening — GLOBE PREQUEL COMPLETE

Render finished 20:14 (2186/2186, 3 h 35 m, honest accounting reconciled,
png sweep clean). New `scripts/assemble_globe.py` (PIL overlay replaces the
dead ASS path for globe films too; refuses to assemble gappy frame sets;
terminal dissolve into the main globe film's opening render). Nuna hold and
terminal frames spot-verified — the hold sits exactly on the hand-framed
view; the final frame IS the main film's first. `tectonic_prequel_globe_v1.mp4`
(13.1 MB) delivered to xian and the previews page. **Roadmap #2's production
is complete pending xian's verdict.** Task #9 closed; site integration will
be its own task.
