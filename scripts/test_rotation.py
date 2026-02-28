#!/usr/bin/env python3
"""Quick test: render 3 key frames to verify rotation fix."""

import bpy
import os
import glob
import json
import math

FRAMES_DIR = os.path.abspath("./frames")
CAMERA_PATH_FILE = os.path.abspath("./camera_path.json")
TEST_DIR = os.path.abspath("./test_rotation")
os.makedirs(TEST_DIR, exist_ok=True)

USE_EEVEE = True  # Fast draft for testing
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

# Pick 4 test frames: Rodinia, Gondwana, Pangaea, Present
test_indices = [0]  # Rodinia
for target_ma in [480.0, 250.0]:
    for i, pf in enumerate(path_frames):
        if pf["time_ma"] == target_ma:
            test_indices.append(i)
            break
test_indices.append(len(path_frames) - 1)  # Present

print(f"Test frames: {test_indices}")
for idx in test_indices:
    pf = path_frames[idx]
    print(f"  [{idx}] {pf['time_ma']:.0f} Ma, lon={pf['camera_lon']:.1f}, lat={pf['camera_lat']:.1f}, era={pf['era_label']}")

# Scene setup
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
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

# Lighting
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

# Render test frames
for idx in test_indices:
    pf = path_frames[idx]
    geo_idx = pf["geo_frame_idx"]
    cam_lon = pf["camera_lon"]
    cam_lat = pf["camera_lat"]
    time_ma = pf["time_ma"]

    # Y-axis tilt for latitude, Z-axis spin for longitude
    rot_y = -math.radians(cam_lat)
    rot_z = -math.radians(cam_lon)
    globe.rotation_euler = (0, rot_y, rot_z)

    old_img = tex_image.image
    new_img = bpy.data.images.load(frame_files[geo_idx], check_existing=True)
    tex_image.image = new_img
    if old_img and old_img != new_img:
        bpy.data.images.remove(old_img)

    scene.frame_set(1)
    out_name = f"test_{int(time_ma):04d}ma"
    scene.render.filepath = os.path.join(TEST_DIR, out_name)
    bpy.ops.render.render(write_still=True)
    print(f"  Rendered: {out_name} ({time_ma:.0f} Ma, lon={cam_lon:.1f}, lat={cam_lat:.1f})")

print("\n✓ Test rotation frames saved to test_rotation/")
