#!/usr/bin/env python3
"""Test Y-axis rotation for present day and Pangaea to make sure they still look right."""

import bpy
import os
import glob
import math

FRAMES_DIR = os.path.abspath("./frames")
TEST_DIR = os.path.abspath("./test_rotation")
os.makedirs(TEST_DIR, exist_ok=True)

frame_files = sorted(glob.glob(os.path.join(FRAMES_DIR, "globe_frame_*.png")))

# Test cases: (name, geo_idx, cam_lon, cam_lat)
tests = [
    ("yaxis_0ma",    200, 25.6, 29.4),    # Present day
    ("yaxis_250ma",  150, 11.6, -2.2),     # Pangaea assembled
    ("yaxis_480ma",  104, 120, -50),        # Gondwana (best view from earlier test)
    ("yaxis_900ma",   20, 109.6, -23.3),   # Rodinia
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

img = bpy.data.images.load(frame_files[0])
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

for name, geo_idx, cam_lon, cam_lat in tests:
    # Swap texture
    old_img = tex_image.image
    new_img = bpy.data.images.load(frame_files[geo_idx], check_existing=True)
    tex_image.image = new_img
    if old_img and old_img != new_img:
        bpy.data.images.remove(old_img)

    # Y-axis rotation: (0, -radians(lat), -radians(lon))
    rot_y = -math.radians(cam_lat)
    rot_z = -math.radians(cam_lon)
    globe.rotation_euler = (0, rot_y, rot_z)

    scene.frame_set(1)
    scene.render.filepath = os.path.join(TEST_DIR, name)
    bpy.ops.render.render(write_still=True)
    print(f"  {name}: lon={cam_lon}, lat={cam_lat}, euler=(0, {math.degrees(rot_y):.1f}°, {math.degrees(rot_z):.1f}°)")

print("\n✓ Y-axis rotation test complete")
