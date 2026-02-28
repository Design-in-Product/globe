#!/usr/bin/env python3
"""
Blender script: Renders a 3D animated globe with smart camera path.

The globe rotates so that the geological "action" (continental centroids,
supercontinents) always faces the camera. Camera stays fixed; the globe
rotates per frame based on camera_path.json.

Variable pacing: supercontinents linger, dispersal phases move faster.
The texture frame index is driven by the camera path data, not by
sequential animation frames.

Usage:
    /Applications/Blender.app/Contents/MacOS/Blender --background --python scripts/render_globe.py
"""

import bpy
import os
import glob
import json
import math

# ── Configuration ──────────────────────────────────────────────
FRAMES_DIR = os.path.abspath("./frames")
CAMERA_PATH_FILE = os.path.abspath("./camera_path.json")
OUTPUT_PATH = os.path.abspath("./tectonic_globe_v6.mp4")
CROSSFADE_HALF = 1  # frames from each side of transition = 2-frame crossfade window

# Renderer: set to True for fast drafts, False for final quality
USE_EEVEE = False

# Output resolution
RES_X = 1920
RES_Y = 1080
FPS = 24

# Cycles settings (ignored if USE_EEVEE)
CYCLES_SAMPLES = 64
CYCLES_DEVICE = 'GPU'  # 'GPU' or 'CPU'

# Globe
SPHERE_RADIUS = 2.0
SPHERE_SEGMENTS = 128
SPHERE_RINGS = 64

# Camera (fixed position, looking at globe)
CAMERA_DISTANCE = 8.0
CAMERA_ELEVATION = 10  # degrees above equator

# ── Load camera path data ─────────────────────────────────────
if not os.path.exists(CAMERA_PATH_FILE):
    print(f"ERROR: Camera path file not found: {CAMERA_PATH_FILE}")
    print("Run compute_camera_path.py first.")
    raise SystemExit(1)

with open(CAMERA_PATH_FILE, 'r') as f:
    camera_path = json.load(f)

path_frames = camera_path["frames"]
total_anim_frames = len(path_frames)
meta = camera_path["metadata"]

print(f"Camera path loaded: {total_anim_frames} animation frames")
print(f"  {meta['time_range']}, {meta['pacing']}")

# ── Discover texture frames ───────────────────────────────────
frame_files = sorted(glob.glob(os.path.join(FRAMES_DIR, "globe_frame_*.png")))
geo_frame_count = len(frame_files)

if geo_frame_count == 0:
    print(f"ERROR: No frames found in {FRAMES_DIR}")
    raise SystemExit(1)

print(f"Texture frames: {geo_frame_count} PNGs in {FRAMES_DIR}")

# ── Reset scene ───────────────────────────────────────────────
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = total_anim_frames
scene.render.fps = FPS

# ── Renderer configuration ────────────────────────────────────
if USE_EEVEE:
    scene.render.engine = 'BLENDER_EEVEE'
    print("Renderer: EEVEE Next")
else:
    scene.render.engine = 'CYCLES'
    scene.cycles.device = CYCLES_DEVICE
    scene.cycles.samples = CYCLES_SAMPLES

    try:
        prefs = bpy.context.preferences.addons['cycles'].preferences
        prefs.compute_device_type = 'METAL'
        prefs.get_devices()
        for device in prefs.devices:
            device.use = True
            print(f"  GPU device: {device.name}")
    except Exception as e:
        print(f"  Warning: Could not configure Metal GPU: {e}")
        scene.cycles.device = 'CPU'

    print(f"Renderer: Cycles ({scene.cycles.device}, {CYCLES_SAMPLES} samples)")

# ── Output settings ───────────────────────────────────────────
scene.render.resolution_x = RES_X
scene.render.resolution_y = RES_Y
scene.render.resolution_percentage = 100

# Render individual PNGs, then assemble with ffmpeg
RENDER_DIR = os.path.abspath("./render_frames")
os.makedirs(RENDER_DIR, exist_ok=True)
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGB'

print(f"Output: {RENDER_DIR}/ ({RES_X}x{RES_Y} @ {FPS}fps, {total_anim_frames} frames)")
print(f"Final: {OUTPUT_PATH}")

# ── Create globe (UV Sphere) ─────────────────────────────────
bpy.ops.mesh.primitive_uv_sphere_add(
    segments=SPHERE_SEGMENTS,
    ring_count=SPHERE_RINGS,
    radius=SPHERE_RADIUS,
    location=(0, 0, 0),
)
globe = bpy.context.active_object
globe.name = "TectonicGlobe"
bpy.ops.object.shade_smooth()

print(f"Globe: UV Sphere ({SPHERE_SEGMENTS}x{SPHERE_RINGS})")

# ── Material: Dual-texture crossfade shader ──────────────────
# Two image texture nodes + Mix node for smooth transitions between
# consecutive geological frames during the render loop.
mat = bpy.data.materials.new(name="GlobeMaterial")
try:
    mat.use_nodes = True
except AttributeError:
    pass
nodes = mat.node_tree.nodes
links = mat.node_tree.links
nodes.clear()

tex_coord = nodes.new('ShaderNodeTexCoord')
tex_coord.location = (-700, 0)

# Texture A (outgoing / primary)
tex_image_a = nodes.new('ShaderNodeTexImage')
tex_image_a.name = 'TexA'
tex_image_a.location = (-400, 150)

# Texture B (incoming / crossfade target)
tex_image_b = nodes.new('ShaderNodeTexImage')
tex_image_b.name = 'TexB'
tex_image_b.location = (-400, -150)

# Mix node for crossfade (RGBA mode)
mix_node = nodes.new('ShaderNodeMix')
mix_node.name = 'CrossfadeMix'
mix_node.data_type = 'RGBA'
mix_node.location = (-100, 0)
mix_node.inputs[0].default_value = 0.0  # Factor: 0 = pure A, 1 = pure B

bsdf = nodes.new('ShaderNodeBsdfPrincipled')
bsdf.location = (200, 0)
bsdf.inputs['Roughness'].default_value = 0.85
bsdf.inputs['Specular IOR Level'].default_value = 0.05

output_node = nodes.new('ShaderNodeOutputMaterial')
output_node.location = (500, 0)

# Load initial texture into both slots
img = bpy.data.images.load(frame_files[0])
tex_image_a.image = img
tex_image_b.image = img

# Wire up: TexCoord → both textures → Mix → BSDF → Output
links.new(tex_coord.outputs['UV'], tex_image_a.inputs['Vector'])
links.new(tex_coord.outputs['UV'], tex_image_b.inputs['Vector'])
links.new(tex_image_a.outputs['Color'], mix_node.inputs[6])   # A input
links.new(tex_image_b.outputs['Color'], mix_node.inputs[7])   # B input
links.new(mix_node.outputs[2], bsdf.inputs['Base Color'])     # Result output
links.new(bsdf.outputs['BSDF'], output_node.inputs['Surface'])

globe.data.materials.append(mat)
print("Material: Dual-texture crossfade shader (Mix node for smooth transitions)")

# Debug: print Mix node input/output indices for verification
print(f"  Mix node inputs: {[(i, inp.name) for i, inp in enumerate(mix_node.inputs)]}")
print(f"  Mix node outputs: {[(i, out.name) for i, out in enumerate(mix_node.outputs)]}")

# Globe rotation will be set directly per-frame during render loop
print("Globe rotation: will be set per-frame during render")

# ── Camera (fixed position) ──────────────────────────────────
# Camera sits at a fixed position, slightly above the equator, looking at origin
cam_elev_rad = math.radians(CAMERA_ELEVATION)
cam_x = CAMERA_DISTANCE * math.cos(cam_elev_rad)
cam_z = CAMERA_DISTANCE * math.sin(cam_elev_rad)

bpy.ops.object.camera_add(location=(cam_x, 0, cam_z))
camera = bpy.context.active_object
camera.name = "GlobeCamera"
camera.data.lens = 35

# Track-To constraint: camera always points at globe center
constraint = camera.constraints.new(type='TRACK_TO')
constraint.target = globe
constraint.track_axis = 'TRACK_NEGATIVE_Z'
constraint.up_axis = 'UP_Y'

scene.camera = camera
print(f"Camera: fixed at distance {CAMERA_DISTANCE}, elevation {CAMERA_ELEVATION}°")

# ── Lighting ──────────────────────────────────────────────────
# Parent lights to camera so they always illuminate the visible hemisphere
bpy.ops.object.light_add(type='SUN', location=(10, 5, 10))
key_light = bpy.context.active_object
key_light.name = "KeyLight"
key_light.data.energy = 3.0
key_light.data.angle = 0.05
key_light.parent = camera

bpy.ops.object.light_add(type='SUN', location=(-5, -10, -5))
fill_light = bpy.context.active_object
fill_light.name = "FillLight"
fill_light.data.energy = 1.0
fill_light.parent = camera

print("Lighting: Key + Fill sun lights (parented to camera)")

# ── World background (dark space) ─────────────────────────────
world = bpy.data.worlds.new(name="SpaceBackground")
scene.world = world
try:
    world.use_nodes = True
except AttributeError:
    pass
world_nodes = world.node_tree.nodes
bg_node = world_nodes.get("Background")
if bg_node:
    bg_node.inputs['Color'].default_value = (0.005, 0.005, 0.02, 1.0)
    bg_node.inputs['Strength'].default_value = 1.0

print("Background: Dark space")

# ── Crossfade schedule computation ────────────────────────────
def compute_crossfade_schedule(path_frames, crossfade_half=2):
    """
    Compute which animation frames need crossfading between geological textures.

    Returns dict: anim_frame_index -> (geo_idx_a, geo_idx_b, alpha)
    where alpha=0.0 means pure A and alpha=1.0 means pure B.
    """
    runs = []
    prev_geo = path_frames[0]["geo_frame_idx"]
    run_start = 0
    for i, pf in enumerate(path_frames):
        if pf["geo_frame_idx"] != prev_geo:
            runs.append((prev_geo, run_start, i, i - run_start))
            run_start = i
            prev_geo = pf["geo_frame_idx"]
    runs.append((prev_geo, run_start, len(path_frames), len(path_frames) - run_start))

    crossfade_map = {}
    for ri in range(len(runs) - 1):
        out_run = runs[ri]
        in_run = runs[ri + 1]
        half = min(out_run[3] // 2, in_run[3] // 2, crossfade_half)
        if half < 1:
            continue
        window = 2 * half
        transition = in_run[1]
        for k in range(window):
            anim_idx = transition - half + k
            alpha = (k + 1) / (window + 1)
            crossfade_map[anim_idx] = (out_run[0], in_run[0], alpha)

    return crossfade_map

crossfade_map = compute_crossfade_schedule(path_frames, CROSSFADE_HALF)

# ── Per-frame render loop ─────────────────────────────────────
# Blender's image sequence frame_offset keyframing is broken in 5.0.
# Instead, we explicitly load the correct texture and set globe rotation
# for each frame, then render individually.
# Crossfade: at transition boundaries, both texture slots are loaded
# and the Mix node blends between them.
duration_sec = total_anim_frames / FPS
print(f"\n{'='*60}")
print(f"Starting per-frame render: {total_anim_frames} frames at {RES_X}x{RES_Y}")
print(f"Duration: {duration_sec:.1f}s at {FPS}fps")
print(f"Crossfade frames: {len(crossfade_map)} (across {geo_frame_count - 1} transitions)")
print(f"Render dir: {RENDER_DIR}")
print(f"{'='*60}\n")

import subprocess
import time

render_start = time.time()
prev_geo_a = -1
prev_geo_b = -1

for i, pf in enumerate(path_frames):
    anim_f = pf["anim_frame"] + 1  # Blender 1-indexed
    geo_idx = pf["geo_frame_idx"]
    cam_lon = pf["camera_lon"]
    cam_lat = pf["camera_lat"]
    time_ma = pf["time_ma"]

    # Set globe rotation so cam_lon/cam_lat faces the camera
    # Y-axis tilt for latitude, Z-axis spin for longitude
    rot_y = -math.radians(cam_lat)
    rot_z = -math.radians(cam_lon)
    globe.rotation_euler = (0, rot_y, rot_z)

    if i in crossfade_map:
        # ── Crossfade frame: blend two textures ──
        geo_a, geo_b, alpha = crossfade_map[i]

        # Load texture A (outgoing) if changed
        if geo_a != prev_geo_a:
            old_a = tex_image_a.image
            new_a = bpy.data.images.load(frame_files[geo_a], check_existing=True)
            tex_image_a.image = new_a
            if old_a and old_a != new_a and old_a != tex_image_b.image:
                bpy.data.images.remove(old_a)
            prev_geo_a = geo_a

        # Load texture B (incoming) if changed
        if geo_b != prev_geo_b:
            old_b = tex_image_b.image
            new_b = bpy.data.images.load(frame_files[geo_b], check_existing=True)
            tex_image_b.image = new_b
            if old_b and old_b != new_b and old_b != tex_image_a.image:
                bpy.data.images.remove(old_b)
            prev_geo_b = geo_b

        # Set crossfade factor
        mix_node.inputs[0].default_value = alpha
    else:
        # ── Normal frame: single texture, no crossfade ──
        if geo_idx != prev_geo_a:
            old_a = tex_image_a.image
            new_a = bpy.data.images.load(frame_files[geo_idx], check_existing=True)
            tex_image_a.image = new_a
            if old_a and old_a != new_a and old_a != tex_image_b.image:
                bpy.data.images.remove(old_a)
            prev_geo_a = geo_idx

        # Pure texture A (no crossfade)
        mix_node.inputs[0].default_value = 0.0

    # Render this frame
    scene.frame_set(anim_f)
    scene.render.filepath = os.path.join(RENDER_DIR, f"render_{anim_f:04d}")
    bpy.ops.render.render(write_still=True)

    # Progress reporting
    elapsed = time.time() - render_start
    fps_rate = (i + 1) / elapsed if elapsed > 0 else 0
    eta = (total_anim_frames - i - 1) / fps_rate if fps_rate > 0 else 0
    blend_str = f" [blend {alpha:.1f}]" if i in crossfade_map else ""
    print(f"  [{i+1}/{total_anim_frames}] Frame {anim_f}: {time_ma:.0f} Ma (geo #{geo_idx}){blend_str} "
          f"— {fps_rate:.2f} fps, ETA {eta:.0f}s")

render_elapsed = time.time() - render_start
print(f"\n✓ Frames rendered in {render_elapsed:.0f}s ({total_anim_frames / render_elapsed:.2f} fps)")

# ── Assemble MP4 with ffmpeg + text overlay ──────────────────
# Step 1: Build per-frame text overlay using ffmpeg drawtext with textfile
# Generate a subtitle file (ASS format) for precise per-frame text
print(f"\nGenerating text overlay data...")

OVERLAY_SCRIPT = os.path.abspath("./overlay_text.ass")

# Build ASS subtitle file for time + era overlay
ass_header = """[Script Info]
Title: Tectonic Globe Overlay
ScriptType: v4.00+
WrapStyle: 0
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: TimeLabel,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,0,1,40,40,35,1
Style: EraLabel,Arial,32,&H00CCCCCC,&H000000FF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,2,0,1,40,40,95,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def frame_to_ass_time(frame_num, fps):
    """Convert frame number to ASS timestamp (H:MM:SS.CC)."""
    total_seconds = frame_num / fps
    h = int(total_seconds // 3600)
    m = int((total_seconds % 3600) // 60)
    s = total_seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"

ass_events = []
prev_time_ma = None
prev_era = None
block_start_frame = 0

# Group consecutive frames with the same time_ma and era
for pf in path_frames:
    anim_f = pf["anim_frame"]
    time_ma = pf["time_ma"]
    era = pf.get("era_label", "")

    if time_ma != prev_time_ma or era != prev_era:
        # Close previous block
        if prev_time_ma is not None:
            start_ts = frame_to_ass_time(block_start_frame, FPS)
            end_ts = frame_to_ass_time(anim_f, FPS)
            time_str = f"{int(prev_time_ma)} Ma" if prev_time_ma == int(prev_time_ma) else f"{prev_time_ma:.1f} Ma"
            ass_events.append(
                f"Dialogue: 0,{start_ts},{end_ts},TimeLabel,,0,0,0,,{time_str}"
            )
            if prev_era:
                ass_events.append(
                    f"Dialogue: 0,{start_ts},{end_ts},EraLabel,,0,0,0,,{prev_era}"
                )
        block_start_frame = anim_f
        prev_time_ma = time_ma
        prev_era = era

# Close final block
if prev_time_ma is not None:
    start_ts = frame_to_ass_time(block_start_frame, FPS)
    end_ts = frame_to_ass_time(total_anim_frames, FPS)
    time_str = f"{int(prev_time_ma)} Ma"
    ass_events.append(
        f"Dialogue: 0,{start_ts},{end_ts},TimeLabel,,0,0,0,,{time_str}"
    )
    if prev_era:
        ass_events.append(
            f"Dialogue: 0,{start_ts},{end_ts},EraLabel,,0,0,0,,{prev_era}"
        )

with open(OVERLAY_SCRIPT, 'w') as f:
    f.write(ass_header)
    f.write("\n".join(ass_events))
    f.write("\n")

print(f"  Subtitle file: {OVERLAY_SCRIPT} ({len(ass_events)} events)")

# Step 2: Assemble frames into MP4 with subtitle overlay
print(f"\nAssembling MP4 with overlay: {OUTPUT_PATH}")
ffmpeg_cmd = [
    "ffmpeg", "-y",
    "-framerate", str(FPS),
    "-i", os.path.join(RENDER_DIR, "render_%04d.png"),
    "-vf", f"ass={OVERLAY_SCRIPT}",
    "-c:v", "libx264",
    "-crf", "18",
    "-pix_fmt", "yuv420p",
    OUTPUT_PATH
]
result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
if result.returncode == 0:
    print(f"\n✓ Render complete! Output: {OUTPUT_PATH}")
    print(f"  Duration: {duration_sec:.1f}s ({total_anim_frames} frames at {FPS}fps)")
else:
    print(f"\n✗ ffmpeg with subtitles failed: {result.stderr}")
    print("  Falling back to plain assembly...")
    ffmpeg_cmd_plain = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", os.path.join(RENDER_DIR, "render_%04d.png"),
        "-c:v", "libx264",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        OUTPUT_PATH
    ]
    result2 = subprocess.run(ffmpeg_cmd_plain, capture_output=True, text=True)
    if result2.returncode == 0:
        print(f"\n✓ Render complete (no overlay): {OUTPUT_PATH}")
    else:
        print(f"\n✗ ffmpeg failed: {result2.stderr}")
        raise SystemExit(1)
