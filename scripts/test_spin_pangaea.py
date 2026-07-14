#!/usr/bin/env python3
"""Fast EEVEE draft of the Pangaea spin-reveal window (anim frames 1832-1894).

Adapts the test_rotation.py pattern (EEVEE, 960x540) to render the full
Pangaea hold from camera_path_spin.json so the Earth-axis spin can be judged
in minutes instead of the ~6 hr Cycles pass.

Run headless:
  Blender --background --python scripts/test_spin_pangaea.py

Output: test_spin_pangaea/spin_NNNN.png (one per anim frame in the window).
"""

import bpy
import os
import glob
import json
import math

FRAMES_DIR = os.path.abspath("./frames")
CAMERA_PATH_FILE = os.path.abspath("./camera_path_spin.json")
TEST_DIR = os.path.abspath("./test_spin_pangaea")
os.makedirs(TEST_DIR, exist_ok=True)

WINDOW_START = 1832  # Pangaea hold, per SESSION_LOG.md handoff
WINDOW_END = 1894    # inclusive

RES_X = 960
RES_Y = 540

SPHERE_RADIUS = 2.0
SPHERE_SEGMENTS = 128
SPHERE_RINGS = 64
CAMERA_DISTANCE = 8.0
CAMERA_ELEVATION = 10

with open(CAMERA_PATH_FILE, 'r') as f:
    camera_path = json.load(f)
path_frames = camera_path["frames"]

frame_files = sorted(glob.glob(os.path.join(FRAMES_DIR, "globe_frame_*.png")))

window = list(range(WINDOW_START, WINDOW_END + 1))
print(f"Rendering {len(window)} frames: anim {WINDOW_START}-{WINDOW_END}, "
      f"{path_frames[WINDOW_START]['time_ma']:.0f} Ma, "
      f"lat={path_frames[WINDOW_START]['camera_lat']:.1f}")

# Scene setup (same as test_rotation.py)
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = RES_X
scene.render.resolution_y = RES_Y
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGB'

bpy.ops.mesh.primitive_uv_sphere_add(
    segments=SPHERE_SEGMENTS, ring_count=SPHERE_RINGS,
    radius=SPHERE_RADIUS, location=(0, 0, 0),
)
globe = bpy.context.active_object
globe.name = "TectonicGlobe"
bpy.ops.object.shade_smooth()

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

img = bpy.data.images.load(frame_files[path_frames[WINDOW_START]["geo_frame_idx"]])
tex_image.image = img

links.new(tex_coord.outputs['UV'], tex_image.inputs['Vector'])
links.new(tex_image.outputs['Color'], bsdf.inputs['Base Color'])
links.new(bsdf.outputs['BSDF'], output_node.inputs['Surface'])
globe.data.materials.append(mat)

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

for idx in window:
    pf = path_frames[idx]
    geo_idx = pf["geo_frame_idx"]
    cam_lon = pf["camera_lon"]
    cam_lat = pf["camera_lat"]

    rot_y = -math.radians(cam_lat)
    rot_z = -math.radians(cam_lon)
    globe.rotation_euler = (0, rot_y, rot_z)

    old_img = tex_image.image
    new_img = bpy.data.images.load(frame_files[geo_idx], check_existing=True)
    tex_image.image = new_img
    if old_img and old_img != new_img:
        bpy.data.images.remove(old_img)

    scene.frame_set(1)
    scene.render.filepath = os.path.join(TEST_DIR, f"spin_{idx:04d}")
    bpy.ops.render.render(write_still=True)
    print(f"  Rendered: spin_{idx:04d} (lon={cam_lon:.2f})")

print(f"\n✓ {len(window)} spin draft frames saved to test_spin_pangaea/")
print("Preview video: ffmpeg -framerate 24 -pattern_type glob -i "
      "'test_spin_pangaea/spin_*.png' -pix_fmt yuv420p test_spin_pangaea/preview.mp4")
