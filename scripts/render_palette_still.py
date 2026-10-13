#!/usr/bin/env python3
"""
Render ONE Cycles still of the globe from a given texture at a given camera
pose — the same sphere, camera, lights and world as render_globe.py — so a
candidate palette can be judged on the real render before any film is
re-rendered (roadmap item 4).

  Blender --background --python scripts/render_palette_still.py -- \
      --texture tex.png --out still.png --lat -2.2 --lon 11.7 \
      [--bg 0.005,0.005,0.02] [--key 1,1,1] [--fill 1,1,1] [--samples 64]

lat/lon are RENDERER-space camera values (copy them from a camera path; see
the renderer-camera-mapping note — do not hand-aim).
"""
import bpy, sys, os, math, argparse

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--texture", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--lat", type=float, required=True)
ap.add_argument("--lon", type=float, required=True)
ap.add_argument("--bg", default="0.005,0.005,0.02")
ap.add_argument("--key", default="1,1,1")
ap.add_argument("--fill", default="1,1,1")
ap.add_argument("--samples", type=int, default=64)
ap.add_argument("--width", type=int, default=1920)
ap.add_argument("--height", type=int, default=1080)
args = ap.parse_args(argv)
rgb = lambda s: tuple(float(x) for x in s.split(","))

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = args.samples
try:
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = 'METAL'
    prefs.get_devices()
    for d in prefs.devices:
        d.use = True
    scene.cycles.device = 'GPU'
except Exception as e:
    print(f"Metal unavailable ({e}); CPU")
    scene.cycles.device = 'CPU'
scene.render.resolution_x = args.width
scene.render.resolution_y = args.height
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGB'

bpy.ops.mesh.primitive_uv_sphere_add(segments=128, ring_count=64, radius=2.0, location=(0, 0, 0))
globe = bpy.context.active_object
bpy.ops.object.shade_smooth()
mat = bpy.data.materials.new(name="GlobeMaterial")
mat.use_nodes = True
nodes, links = mat.node_tree.nodes, mat.node_tree.links
nodes.clear()
tc = nodes.new('ShaderNodeTexCoord')
ti = nodes.new('ShaderNodeTexImage')
ti.image = bpy.data.images.load(os.path.abspath(args.texture))
bsdf = nodes.new('ShaderNodeBsdfPrincipled')
outn = nodes.new('ShaderNodeOutputMaterial')
links.new(tc.outputs['UV'], ti.inputs['Vector'])
links.new(ti.outputs['Color'], bsdf.inputs['Base Color'])
links.new(bsdf.outputs['BSDF'], outn.inputs['Surface'])
globe.data.materials.append(mat)
globe.rotation_euler = (0, -math.radians(args.lat), -math.radians(args.lon))

elev = math.radians(10)
bpy.ops.object.camera_add(location=(8.0 * math.cos(elev), 0, 8.0 * math.sin(elev)))
cam = bpy.context.active_object
cam.data.lens = 35
c = cam.constraints.new(type='TRACK_TO'); c.target = globe
c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'
scene.camera = cam

bpy.ops.object.light_add(type='SUN', location=(10, 5, 10))
key = bpy.context.active_object; key.data.energy = 3.0; key.data.angle = 0.05
key.data.color = rgb(args.key); key.parent = cam
bpy.ops.object.light_add(type='SUN', location=(-5, -10, -5))
fill = bpy.context.active_object; fill.data.energy = 1.0
fill.data.color = rgb(args.fill); fill.parent = cam

world = bpy.data.worlds.new(name="SpaceBackground"); scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
bg.inputs['Color'].default_value = rgb(args.bg) + (1.0,)
bg.inputs['Strength'].default_value = 1.0

scene.render.filepath = os.path.abspath(args.out)
bpy.ops.render.render(write_still=True)
print(f"still: {scene.render.filepath}")
