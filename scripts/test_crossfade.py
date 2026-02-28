#!/usr/bin/env python3
"""
Quick EEVEE test of the crossfade shader.

Renders 6 frames around a transition point to verify the Mix node
blending works correctly. Uses EEVEE for speed (~1s per frame).

Usage:
    /Applications/Blender.app/Contents/MacOS/Blender --background --python scripts/test_crossfade.py
"""

import bpy
import os
import glob
import json
import math

# ── Configuration ──────────────────────────────────────────────
FRAMES_DIR = os.path.abspath("./frames")
CAMERA_PATH_FILE = os.path.abspath("./camera_path.json")
TEST_DIR = os.path.abspath("./test_crossfade")
os.makedirs(TEST_DIR, exist_ok=True)

RES_X = 960
RES_Y = 540
CROSSFADE_HALF = 2

# ── Load data ──────────────────────────────────────────────────
with open(CAMERA_PATH_FILE, 'r') as f:
    camera_path = json.load(f)

path_frames = camera_path["frames"]
frame_files = sorted(glob.glob(os.path.join(FRAMES_DIR, "globe_frame_*.png")))

# ── Compute crossfade schedule ─────────────────────────────────
def compute_crossfade_schedule(path_frames, crossfade_half=2):
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

# ── Find test frames: 6 frames around the transition at ~500 Ma ──
# Transition 99 is at anim_frame ~672, geo 99->100
test_center = None
for i in range(1, len(path_frames)):
    if path_frames[i]["geo_frame_idx"] != path_frames[i-1]["geo_frame_idx"]:
        if path_frames[i]["time_ma"] <= 500:
            test_center = i
            break

if test_center is None:
    test_center = 672  # fallback

# Test 6 frames: 3 before transition, 3 after
test_indices = list(range(test_center - 3, test_center + 3))
print(f"Test frames around transition at anim_frame {test_center}:")
for idx in test_indices:
    pf = path_frames[idx]
    cf = crossfade_map.get(idx)
    cf_str = f" CROSSFADE alpha={cf[2]:.2f} (geo {cf[0]}->{cf[1]})" if cf else " (pure)"
    print(f"  anim[{idx}] geo={pf['geo_frame_idx']} {pf['time_ma']:.0f}Ma{cf_str}")

# ── Reset scene ───────────────────────────────────────────────
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = RES_X
scene.render.resolution_y = RES_Y
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGB'

# ── Create globe ──────────────────────────────────────────────
bpy.ops.mesh.primitive_uv_sphere_add(segments=128, ring_count=64, radius=2.0, location=(0, 0, 0))
globe = bpy.context.active_object
globe.name = "TectonicGlobe"
bpy.ops.object.shade_smooth()

# ── Dual-texture crossfade material ──────────────────────────
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

tex_image_a = nodes.new('ShaderNodeTexImage')
tex_image_a.name = 'TexA'
tex_image_a.location = (-400, 150)

tex_image_b = nodes.new('ShaderNodeTexImage')
tex_image_b.name = 'TexB'
tex_image_b.location = (-400, -150)

mix_node = nodes.new('ShaderNodeMix')
mix_node.name = 'CrossfadeMix'
mix_node.data_type = 'RGBA'
mix_node.location = (-100, 0)
mix_node.inputs[0].default_value = 0.0

bsdf = nodes.new('ShaderNodeBsdfPrincipled')
bsdf.location = (200, 0)
bsdf.inputs['Roughness'].default_value = 0.85
bsdf.inputs['Specular IOR Level'].default_value = 0.05

output_node = nodes.new('ShaderNodeOutputMaterial')
output_node.location = (500, 0)

img = bpy.data.images.load(frame_files[0])
tex_image_a.image = img
tex_image_b.image = img

links.new(tex_coord.outputs['UV'], tex_image_a.inputs['Vector'])
links.new(tex_coord.outputs['UV'], tex_image_b.inputs['Vector'])
links.new(tex_image_a.outputs['Color'], mix_node.inputs[6])
links.new(tex_image_b.outputs['Color'], mix_node.inputs[7])
links.new(mix_node.outputs[2], bsdf.inputs['Base Color'])
links.new(bsdf.outputs['BSDF'], output_node.inputs['Surface'])

globe.data.materials.append(mat)

# Debug: verify Mix node connections
print(f"\nMix node inputs: {[(i, inp.name, inp.type) for i, inp in enumerate(mix_node.inputs)]}")
print(f"Mix node outputs: {[(i, out.name, out.type) for i, out in enumerate(mix_node.outputs)]}")

# ── Camera ────────────────────────────────────────────────────
cam_elev_rad = math.radians(10)
cam_x = 8.0 * math.cos(cam_elev_rad)
cam_z = 8.0 * math.sin(cam_elev_rad)
bpy.ops.object.camera_add(location=(cam_x, 0, cam_z))
camera = bpy.context.active_object
camera.data.lens = 35
constraint = camera.constraints.new(type='TRACK_TO')
constraint.target = globe
constraint.track_axis = 'TRACK_NEGATIVE_Z'
constraint.up_axis = 'UP_Y'
scene.camera = camera

# ── Lighting ──────────────────────────────────────────────────
bpy.ops.object.light_add(type='SUN', location=(10, 5, 10))
key_light = bpy.context.active_object
key_light.data.energy = 3.0
key_light.parent = camera

bpy.ops.object.light_add(type='SUN', location=(-5, -10, -5))
fill_light = bpy.context.active_object
fill_light.data.energy = 1.0
fill_light.parent = camera

# ── World ─────────────────────────────────────────────────────
world = bpy.data.worlds.new(name="SpaceBackground")
scene.world = world
try:
    world.use_nodes = True
except AttributeError:
    pass
bg_node = world.node_tree.nodes.get("Background")
if bg_node:
    bg_node.inputs['Color'].default_value = (0.005, 0.005, 0.02, 1.0)

# ── Render test frames ────────────────────────────────────────
print(f"\nRendering {len(test_indices)} test frames with EEVEE...")
prev_geo_a = -1
prev_geo_b = -1

for idx in test_indices:
    pf = path_frames[idx]
    cam_lon = pf["camera_lon"]
    cam_lat = pf["camera_lat"]
    geo_idx = pf["geo_frame_idx"]

    rot_y = -math.radians(cam_lat)
    rot_z = -math.radians(cam_lon)
    globe.rotation_euler = (0, rot_y, rot_z)

    if idx in crossfade_map:
        geo_a, geo_b, alpha = crossfade_map[idx]
        if geo_a != prev_geo_a:
            tex_image_a.image = bpy.data.images.load(frame_files[geo_a], check_existing=True)
            prev_geo_a = geo_a
        if geo_b != prev_geo_b:
            tex_image_b.image = bpy.data.images.load(frame_files[geo_b], check_existing=True)
            prev_geo_b = geo_b
        mix_node.inputs[0].default_value = alpha
        label = f"blend_{alpha:.2f}"
    else:
        if geo_idx != prev_geo_a:
            tex_image_a.image = bpy.data.images.load(frame_files[geo_idx], check_existing=True)
            prev_geo_a = geo_idx
        mix_node.inputs[0].default_value = 0.0
        label = "pure"

    outpath = os.path.join(TEST_DIR, f"test_anim{idx:04d}_{label}")
    scene.render.filepath = outpath
    bpy.ops.render.render(write_still=True)
    print(f"  ✓ anim[{idx}] geo={geo_idx} {pf['time_ma']:.0f}Ma ({label})")

print(f"\n✓ Test frames saved to {TEST_DIR}/")
