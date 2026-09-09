"""Native Cycles look-development still. Does not modify the existing animation."""
import bpy, math, re, json
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

OUT = Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(OUT.parent / 'false-sharing-clay.blend'))
s = bpy.context.scene
s.frame_set(13)
for obj in s.objects:
    obj.animation_data_clear()
for mat in bpy.data.materials:
    if mat.node_tree:
        mat.node_tree.animation_data_clear()
W, H = 2160, 2420
s.render.resolution_x = W
s.render.resolution_y = H
s.render.resolution_percentage = 100
s.render.pixel_aspect_x = s.render.pixel_aspect_y = 1
s.render.use_border = False
s.render.film_transparent = False
s.render.image_settings.file_format = 'PNG'
s.render.image_settings.color_mode = 'RGB'
s.render.image_settings.color_depth = '8'
cam = s.camera
cam.data.sensor_fit = 'HORIZONTAL'
cam.data.dof.use_dof = False
s.render.use_motion_blur = False
root = s.objects['Foreground • common placement']
model = bpy.data.collections['01 • Clay models']
hud = bpy.data.collections['02 • Code and results']

# Keep the approved canonical geometry and worker identities. Remove old HUD
# rather than fitting the original small code into the newly sized rectangle.
for obj in list(hud.objects):
    bpy.data.objects.remove(obj, do_unlink=True)

def linear(h):
    c = [int(h[i:i+2], 16)/255 for i in (0,2,4)]
    return tuple(v/12.92 if v <= .04045 else ((v+.055)/1.055)**2.4 for v in c)

def emission(name, color):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    n, l = m.node_tree.nodes, m.node_tree.links
    n.clear()
    e = n.new('ShaderNodeEmission')
    e.inputs['Color'].default_value = (*linear(color), 1)
    o = n.new('ShaderNodeOutputMaterial')
    l.new(e.outputs[0], o.inputs['Surface'])
    return m

# Object-space grain, shallow tool marks and broad clay variation. Normal maps
# remain stable on the surface; none is driven by time or world coordinates.
used = {slot.material for o in model.objects for slot in o.material_slots if slot.material}
for m in used:
    if not m.node_tree:
        continue
    n, l = m.node_tree.nodes, m.node_tree.links
    p = next((v for v in n if v.type == 'BSDF_PRINCIPLED'), None)
    if p is None or m.name == 'Ivory raised clay letters':
        continue
    p.inputs['Metallic'].default_value = 0
    p.inputs['Specular IOR Level'].default_value = .20
    p.inputs['Roughness'].default_value = .79
    p.inputs['Coat Weight'].default_value = 0
    p.inputs['Subsurface Weight'].default_value = .015
    for link in list(p.inputs['Normal'].links):
        l.remove(link)
    tc = n.new('ShaderNodeTexCoord')
    tc.label = 'Clay texture fixed to object'
    broad = n.new('ShaderNodeTexNoise')
    broad.inputs['Scale'].default_value = 13
    broad.inputs['Detail'].default_value = 3
    broad.inputs['Roughness'].default_value = .7
    l.new(tc.outputs['Object'], broad.inputs['Vector'])
    press = n.new('ShaderNodeBump')
    press.inputs['Strength'].default_value = .38
    press.inputs['Distance'].default_value = .038
    l.new(broad.outputs['Fac'], press.inputs['Height'])
    fine = n.new('ShaderNodeTexNoise')
    fine.inputs['Scale'].default_value = 72
    fine.inputs['Detail'].default_value = 2
    l.new(tc.outputs['Object'], fine.inputs['Vector'])
    grain = n.new('ShaderNodeBump')
    grain.inputs['Strength'].default_value = .30
    grain.inputs['Distance'].default_value = .012
    l.new(fine.outputs['Fac'], grain.inputs['Height'])
    l.new(press.outputs['Normal'], grain.inputs['Normal'])
    l.new(grain.outputs['Normal'], p.inputs['Normal'])
    rough = n.new('ShaderNodeMapRange')
    rough.inputs['To Min'].default_value = .70
    rough.inputs['To Max'].default_value = .87
    l.new(broad.outputs['Fac'], rough.inputs['Value'])
    l.new(rough.outputs['Result'], p.inputs['Roughness'])

# Retain real directional studio illumination; avoid broad plastic reflections.
s.objects['Studio warm key'].data.energy = 1450
s.objects['Cool edge strip'].data.energy = 610
s.objects['Restrained neutral front fill'].data.energy = 115
s.objects['Arrow studio softbox'].data.energy = 0
clay = bpy.data.textures.new('V8 hand pressed surface contour', type='CLOUDS')
clay.noise_scale = .24
clay.noise_depth = 2
for obj in model.objects:
    if obj.type == 'MESH' and 'shell' in obj.name:
        existing = [m for m in obj.modifiers if m.type == 'DISPLACE']
        deform = existing[0] if existing else obj.modifiers.new('Hand pressed clay contour', 'DISPLACE')
        deform.texture = clay
        deform.texture_coords = 'LOCAL'
        deform.strength = .027
        deform.mid_level = .5

# A schematic handoff request in flight. Three neighboring dashes coalesce
# with a much larger packet into one continuous, rounded clay mesh.
for obj in list(model.objects):
    if 'clay dash' in obj.name or 'update pulse' in obj.name:
        bpy.data.objects.remove(obj, do_unlink=True)

teal = bpy.data.materials['Deep teal worker clay']
blue = bpy.data.materials['Cobalt clay cards']
def pill(name, a, b, radius, mat):
    d = b-a
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=16, radius=1)
    o = bpy.context.object
    o.name = name
    for c in list(o.users_collection): c.objects.unlink(o)
    model.objects.link(o)
    o.parent = root
    o.location = (a+b)/2
    o.rotation_euler = Vector((0,1,0)).rotation_difference(d.normalized()).to_euler()
    o.scale = (radius, d.length/2 + radius, radius)
    o.data.materials.append(mat)
    for p in o.data.polygons: p.use_smooth = True
    return o

for i,mat in enumerate([teal, blue]):
    start = Vector((-2.5 if i == 0 else 2.5, .75, .84))
    end = Vector((-3.4 if i == 0 else -1.6, -2.27, 1.06))
    direction = (end-start).normalized()
    for j in range(7):
        if i == 1 and j in (2,3,4): continue
        a = start.lerp(end, j/7)
        pill(f'V8 worker {i} dash {j}', a, a+direction*.22, .135, mat)
    if i == 1:
        mb = bpy.data.metaballs.new('Traveling clay deformation')
        mb.resolution = .045
        mb.render_resolution = .035
        mb.threshold = .6
        obj = bpy.data.objects.new('V8 pulse merged into three dashes', mb)
        model.objects.link(obj)
        obj.parent = root
        mb.materials.append(mat)
        for j in range(27):
            t = .29+j/26*.36
            e = mb.elements.new()
            e.co = start.lerp(end, t)
            e.radius = .19 + .34*math.exp(-((t-.48)/.095)**2)
            e.stiffness = 2
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.convert(target='MESH')
        obj = bpy.context.object
        for p in obj.data.polygons: p.use_smooth = True

def bounds(objects):
    bpy.context.view_layer.update()
    vs = [world_to_camera_view(s,cam,o.matrix_world@Vector(v))
          for o in objects if o.type in {'FONT','MESH','CURVE'} and not o.hide_render
          for v in o.bound_box]
    return [min(v.x for v in vs)*W, min(1-v.y for v in vs)*H,
            max(v.x for v in vs)*W, max(1-v.y for v in vs)*H]

# Fit the complete visible assembly for this look-development still.
# The extra height is available composition space, never a post-render stretch.
geo = [o for o in model.objects if not o.hide_render and o.type in {'FONT','MESH','CURVE'}]
for _ in range(7):
    b = bounds(geo)
    root.scale *= min(1840/(b[2]-b[0]), 1150/(b[3]-b[1]))
    b = bounds(geo)
    root.location.y += .1
    q = bounds(geo)
    root.location.y -= .1
    root.location.y += (2260-b[3])/((q[3]-b[3])/.1)
    b = bounds(geo)
    root.location.x += .1
    q = bounds(geo)
    root.location.x -= .1
    root.location.x += (W/2-(b[0]+b[2])/2)/((q[0]+q[2]-b[0]-b[2])/.2)

# Camera-facing vector outlines, unlit ivory/lilac/aqua syntax. Independently
# configurable HUD, with no extrusion, DOF, bloom, motion blur or texture.
unit = (7*cam.data.sensor_width/cam.data.lens)/W
def px(x,y): return ((x-W/2)*unit,(H/2-y)*unit,-7)
font = bpy.data.fonts.load('/System/Library/Fonts/Menlo.ttc')
colors = [('plain','FFF8EB'),('keyword','EDC7FF'),('type','B8F2EB'),('number','FFE0A3')]
mats = [emission('V8 readable code '+role,h) for role,h in colors]
rows = ['struct Counters {','  atomic<uint64_t> a{0};','  atomic<uint64_t> b{0};','};']
texts = []
for i,body in enumerate(rows):
    d = bpy.data.curves.new('V8 code row '+str(i),'FONT')
    d.body = body
    d.font = font
    d.align_x = 'LEFT'
    d.size = 180*unit
    d.offset = .0009
    d.resolution_u = 24
    for m in mats: d.materials.append(m)
    for match in re.finditer(r'[A-Za-z_][A-Za-z_0-9]*|[0-9]+',body):
        token = match.group()
        role = 1 if token == 'struct' else 2 if token in ['Counters','atomic','uint64_t'] else 3 if token.isdigit() else 0
        for j in range(match.start(),match.end()): d.body_format[j].material_index = role
    o = bpy.data.objects.new('V8 readable code row '+str(i),d)
    hud.objects.link(o)
    o.parent = cam
    o.location = px(155,520+i*160)
    texts.append(o)
b = bounds(texts)
factor = min(1,1850/(b[2]-b[0]))
for o in texts: o.data.size *= factor
b = bounds(texts)
model_bounds = bounds(geo)
assert b[0] >= 120 and b[2] <= W-120, b
assert b[1] >= 350, b
assert b[3]+60 < model_bounds[1], (b,model_bounds)
assert model_bounds[3] < H-100,model_bounds

s.render.engine = 'CYCLES'
prefs = bpy.context.preferences.addons['cycles'].preferences
prefs.compute_device_type = 'METAL'
prefs.kernel_optimization_level = 'OFF'
prefs.metalrt = 'OFF'
prefs.get_devices()
for d in prefs.devices: d.use = d.type == 'METAL'
s.cycles.device = 'GPU'
s.cycles.samples = 160
s.cycles.adaptive_threshold = .008
s.cycles.use_denoising = True
s.cycles.filter_width = .8
s.render.use_compositing = False
s.render.use_sequencer = False
s.frame_start = s.frame_end = 13
s.render.filepath = str(OUT/'short-07-clay-study-2160x2420.png')
s['still_revision'] = 'v8 native clay still; 2160x2420; animation not revised yet'
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'short-07-clay-study.blend'))
report = {'resolution':[W,H], 'code_bounds_px':b, 'model_bounds_px':model_bounds,
          'code_font_size':texts[0].data.size/unit, 'native_render':True,
          'post_render_resize':False, 'single_still_only':True}
(OUT/'still-verification.json').write_text(json.dumps(report,indent=2))
print('STILL_CONFIGURATION',json.dumps(report),flush=True)
bpy.ops.render.render(write_still=True)
