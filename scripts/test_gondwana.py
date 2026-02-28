#!/usr/bin/env python3
"""Test different views of Gondwana at 480 Ma."""

import bpy
import os
import glob
import math

FRAMES_DIR = os.path.abspath("./frames")
TEST_DIR = os.path.abspath("./test_rotation")
os.makedirs(TEST_DIR, exist_ok=True)

frame_files = sorted(glob.glob(os.path.join(FRAMES_DIR, "globe_frame_*.png")))
GEO_IDX = 104  # 480 Ma

# Different camera targets to try
tests = [
    # Using (0, -radians(lat), -radians(lon)) — Y-axis for latitude
    ("gond_y_lon0_lat-50",   (0, math.radians(50), 0),                          "Y-axis: lon=0, lat=-50"),
    ("gond_y_lon90_lat-50",  (0, math.radians(50), -math.radians(90)),           "Y-axis: lon=90, lat=-50"),
    ("gond_y_lon120_lat-50", (0, math.radians(50), -math.radians(120)),          "Y-axis: lon=120, lat=-50"),
    ("gond_y_lon60_lat-60",  (0, math.radians(60), -math.radians(60)),           "Y-axis: lon=60, lat=-60"),
    # Using X-axis (current approach)
    ("gond_x_lon0_lat-50",   (math.radians(-50), 0, 0),                          "X-axis: lon=0, lat=-50"),
    ("gond_x_lon90_lat-50",  (math.radians(-50), 0, -math.radians(90)),           "X-axis: lon=90, lat=-50"),
]

SPHERE_RADIUS = 2.0
SPHERE_SEGMENTS = 128
SPHERE_RINGS = 64
CAMERA_DISTANCE = 8.0
CAMERA_ELEVATION = 10

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGB'

bpy.ops.mesh.primitive_uv_sphere_add(
    segments=SPHERE_SEGMENTS, ring_count=SPHERE_RINGS,
    radius=SPHERE_RADIUS, location=(0, 0, 0),
)
globe = bpy.context.active_object
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
tex_image = nodes.new('ShaderNodeTexImage')
bsdf = nodes.new('ShaderNodeBsdfPrincipled')
bsdf.inputs['Roughness'].default_value = 0.85
bsdf.inputs['Specular IOR Level'].default_value = 0.05
output_node = nodes.new('ShaderNodeOutputMaterial')

img = bpy.data.images.load(frame_files[GEO_IDX])
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
camera.data.lens = 35
constraint = camera.constraints.new(type='TRACK_TO')
constraint.target = globe
constraint.track_axis = 'TRACK_NEGATIVE_Z'
constraint.up_axis = 'UP_Y'
scene.camera = camera

bpy.ops.object.light_add(type='SUN', location=(10, 5, 10))
key_light = bpy.context.active_object
key_light.data.energy = 3.0
key_light.parent = camera

bpy.ops.object.light_add(type='SUN', location=(-5, -10, -5))
fill_light = bpy.context.active_object
fill_light.data.energy = 1.0
fill_light.parent = camera

world = bpy.data.worlds.new(name="SpaceBackground")
scene.world = world
try:
    world.use_nodes = True
except AttributeError:
    pass
bg_node = world.node_tree.nodes.get("Background")
if bg_node:
    bg_node.inputs['Color'].default_value = (0.005, 0.005, 0.02, 1.0)

for name, euler, desc in tests:
    globe.rotation_euler = euler
    scene.frame_set(1)
    scene.render.filepath = os.path.join(TEST_DIR, name)
    bpy.ops.render.render(write_still=True)
    print(f"  Rendered: {name} — {desc}")

print("\n✓ Gondwana rotation tests complete")
