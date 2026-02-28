#!/usr/bin/env python3
"""
Resume render: picks up from where render_globe.py left off.
Renders only missing frames, then assembles the final MP4.
"""

import bpy
import os
import glob
import json
import math
import subprocess
import time

# ── Configuration (must match render_globe.py) ────────────────
FRAMES_DIR = os.path.abspath("./frames")
CAMERA_PATH_FILE = os.path.abspath("./camera_path.json")
OUTPUT_PATH = os.path.abspath("./tectonic_globe.mp4")
RENDER_DIR = os.path.abspath("./render_frames")

USE_EEVEE = False
RES_X = 1920
RES_Y = 1080
FPS = 24
CYCLES_SAMPLES = 64
CYCLES_DEVICE = 'GPU'

SPHERE_RADIUS = 2.0
SPHERE_SEGMENTS = 128
SPHERE_RINGS = 64
CAMERA_DISTANCE = 8.0
CAMERA_ELEVATION = 10

# ── Load data ─────────────────────────────────────────────────
with open(CAMERA_PATH_FILE, 'r') as f:
    camera_path = json.load(f)

path_frames = camera_path["frames"]
total_anim_frames = len(path_frames)

frame_files = sorted(glob.glob(os.path.join(FRAMES_DIR, "globe_frame_*.png")))
geo_frame_count = len(frame_files)

# Find which frames are already rendered
existing = set()
for fn in os.listdir(RENDER_DIR):
    if fn.startswith("render_") and fn.endswith(".png"):
        try:
            num = int(fn.replace("render_", "").replace(".png", ""))
            existing.add(num)
        except ValueError:
            pass

remaining = [pf for pf in path_frames if (pf["anim_frame"] + 1) not in existing]
print(f"Total frames: {total_anim_frames}, already rendered: {len(existing)}, remaining: {len(remaining)}")

if len(remaining) == 0:
    print("All frames already rendered! Jumping to MP4 assembly.")
else:
    # ── Scene setup (identical to render_globe.py) ────────────
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = total_anim_frames
    scene.render.fps = FPS

    if USE_EEVEE:
        scene.render.engine = 'BLENDER_EEVEE_NEXT'
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

    scene.render.resolution_x = RES_X
    scene.render.resolution_y = RES_Y
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGB'

    # Globe
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=SPHERE_SEGMENTS, ring_count=SPHERE_RINGS,
        radius=SPHERE_RADIUS, location=(0, 0, 0),
    )
    globe = bpy.context.active_object
    globe.name = "TectonicGlobe"
    bpy.ops.object.shade_smooth()

    # Material
    mat = bpy.data.materials.new(name="GlobeMaterial")
    try:
        mat.use_nodes = True
    except AttributeError:
        pass
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)
    tex_image = nodes.new('ShaderNodeTexImage')
    tex_image.location = (-300, 0)
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    bsdf.inputs['Roughness'].default_value = 0.85
    bsdf.inputs['Specular IOR Level'].default_value = 0.05
    output_node = nodes.new('ShaderNodeOutputMaterial')
    output_node.location = (300, 0)

    img = bpy.data.images.load(frame_files[0])
    tex_image.image = img

    links.new(tex_coord.outputs['UV'], tex_image.inputs['Vector'])
    links.new(tex_image.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(bsdf.outputs['BSDF'], output_node.inputs['Surface'])
    globe.data.materials.append(mat)

    # Camera
    cam_elev_rad = math.radians(CAMERA_ELEVATION)
    cam_x = CAMERA_DISTANCE * math.cos(cam_elev_rad)
    cam_z = CAMERA_DISTANCE * math.sin(cam_elev_rad)
    bpy.ops.object.camera_add(location=(cam_x, 0, cam_z))
    camera = bpy.context.active_object
    camera.name = "GlobeCamera"
    camera.data.lens = 35
    constraint = camera.constraints.new(type='TRACK_TO')
    constraint.target = globe
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'
    scene.camera = camera

    # Lighting (parented to camera)
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

    # Background
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

    # ── Render remaining frames ───────────────────────────────
    print(f"\nRendering {len(remaining)} remaining frames...")
    render_start = time.time()
    prev_geo_idx = -1

    for i, pf in enumerate(remaining):
        anim_f = pf["anim_frame"] + 1
        geo_idx = pf["geo_frame_idx"]
        cam_lon = pf["camera_lon"]
        cam_lat = pf["camera_lat"]
        time_ma = pf["time_ma"]

        rot_y = -math.radians(cam_lat)
        rot_z = -math.radians(cam_lon)
        globe.rotation_euler = (0, rot_y, rot_z)

        if geo_idx != prev_geo_idx:
            old_img = tex_image.image
            new_img = bpy.data.images.load(frame_files[geo_idx], check_existing=True)
            tex_image.image = new_img
            if old_img and old_img != new_img:
                bpy.data.images.remove(old_img)
            prev_geo_idx = geo_idx

        scene.frame_set(anim_f)
        scene.render.filepath = os.path.join(RENDER_DIR, f"render_{anim_f:04d}")
        bpy.ops.render.render(write_still=True)

        elapsed = time.time() - render_start
        fps_rate = (i + 1) / elapsed if elapsed > 0 else 0
        eta = (len(remaining) - i - 1) / fps_rate if fps_rate > 0 else 0
        print(f"  [{i+1}/{len(remaining)}] Frame {anim_f}: {time_ma:.0f} Ma (geo #{geo_idx}) "
              f"— {fps_rate:.2f} fps, ETA {eta:.0f}s")

    render_elapsed = time.time() - render_start
    print(f"\n✓ Remaining frames rendered in {render_elapsed:.0f}s")

# ── Assemble MP4 with ffmpeg ─────────────────────────────────
print(f"\nAssembling MP4: {OUTPUT_PATH}")
ffmpeg_cmd = [
    "ffmpeg", "-y",
    "-framerate", str(FPS),
    "-i", os.path.join(RENDER_DIR, "render_%04d.png"),
    "-c:v", "libx264",
    "-crf", "18",
    "-pix_fmt", "yuv420p",
    OUTPUT_PATH
]
result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
if result.returncode == 0:
    duration_sec = total_anim_frames / FPS
    print(f"\n✓ Render complete! Output: {OUTPUT_PATH}")
    print(f"  Duration: {duration_sec:.1f}s ({total_anim_frames} frames at {FPS}fps)")
else:
    print(f"\n✗ ffmpeg failed: {result.stderr}")
    raise SystemExit(1)
