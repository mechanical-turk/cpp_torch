"""Build Short 06's editable, deterministic Blender motion-design scene.
Run: blender -b --python build_scene.py -- --out /absolute/output/directory
"""
import bpy, math, os, sys, argparse, json
from mathutils import Vector

p = argparse.ArgumentParser()
p.add_argument('--out', required=True)
p.add_argument('--test-frame', type=int, default=0)
a = p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
OUT = os.path.abspath(a.out)
os.makedirs(OUT, exist_ok=True)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for c in list(bpy.data.collections):
    if c.name != 'Collection' and not c.objects: bpy.data.collections.remove(c)
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 16
scene.cycles.use_denoising = True
scene.render.resolution_x, scene.render.resolution_y = 2160, 2352
scene.render.resolution_percentage = 100
scene.render.fps = 24
scene.frame_start, scene.frame_end = 1, 456
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGB'
scene.render.film_transparent = False
scene.view_settings.view_transform = 'Standard'
scene.render.fps_base = 1
scene.world.color = (0.08, 0.08, 0.08)
scene.world.use_nodes = True
scene.world.node_tree.nodes['Background'].inputs['Color'].default_value = (.10,.14,.20,1)
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value = .35

def collection(name):
    c=bpy.data.collections.new(name); scene.collection.children.link(c); return c
MODEL=collection('01 • Player assemblies')
STAGE=collection('02 • Studio and camera')
HUD=collection('03 • Code and timings')
MARK=collection('04 • Selection and spacing')
def move_collection(o,c):
    for old in list(o.users_collection): old.objects.unlink(o)
    c.objects.link(o)
def material(name, rgb, metal=0, rough=.35, emission=False):
    m=bpy.data.materials.new(name); m.diffuse_color=(*rgb,1);m.use_nodes=True
    nt=m.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial')
    if emission:
        s=nt.nodes.new('ShaderNodeEmission');s.inputs['Color'].default_value=(*rgb,1);s.inputs['Strength'].default_value=1
    else:
        s=nt.nodes.new('ShaderNodeBsdfPrincipled');s.inputs['Base Color'].default_value=(*rgb,1)
        s.inputs['Metallic'].default_value=metal;s.inputs['Roughness'].default_value=rough
    nt.links.new(s.outputs[0],out.inputs['Surface']);return m
BLUE=material('Score • blue body',(.012,.09,.24),.18,.48)
FACE=material('Score • glare-free navy face',(.012,.045,.105),emission=True)
KEYWORD=material('Syntax • keyword',(.67,.40,.90),emission=True)
TYPE=material('Syntax • type',(.16,.72,.69),emission=True)
GRAPHITE=material('History • graphite',(.055,.08,.12),.30,.45)
BASE=material('History • dark spine',(.028,.044,.064),.6,.32)
FLOOR=material('Stage • midnight',(.003,.006,.012),.08,.52)
WHITE=material('Type • ivory',(.92,.95,.98),emission=True)
MUTED=material('Type • cool grey',(.36,.46,.56),emission=True)
YELLOW=material('Caption • yellow',(.98,.73,.18),emission=True)
TEAL=material('Result • teal',(.12,.86,.69),emission=True)
RED=material('Annotation • coral',(.98,.16,.15),emission=True)
CODE_BG=material('Panel • ink',(.016,.026,.041),emission=True)
RULE=material('Panel • line',(.065,.108,.15),emission=True)

def cube(name, loc, dims, mat, bevel=.04, parent=None, coll=MODEL):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o=bpy.context.object;o.name=name;o.dimensions=dims
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    o.data.materials.append(mat)
    if bevel:
        m=o.modifiers.new('Precision edge radius','BEVEL');m.width=bevel;m.segments=3
        m=o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
    if parent:o.parent=parent
    move_collection(o,coll);return o
def empty(name, coll=MODEL):
    o=bpy.data.objects.new(name,None);coll.objects.link(o);return o
def path(name,pts,mat,r=.022,parent=None,coll=MARK):
    d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.bevel_depth=r;d.bevel_resolution=3
    s=d.splines.new('POLY');s.points.add(len(pts)-1)
    for q,co in zip(s.points,pts):q.co=(*co,1)
    o=bpy.data.objects.new(name,d);coll.objects.link(o);d.materials.append(mat)
    if parent:o.parent=parent
    return o
font=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Arial.ttf')
bold=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Arial Bold.ttf')
mono=bpy.data.fonts.load('/System/Library/Fonts/Menlo.ttc')
def text(name,body,loc,size,mat=WHITE,parent=None,align='LEFT',font_=None,coll=HUD):
    d=bpy.data.curves.new(name,'FONT');d.body=body;d.size=size;d.align_x=align;d.font=font_ or font
    d.space_line=1.18;d.resolution_u=8
    o=bpy.data.objects.new(name,d);coll.objects.link(o);o.location=loc;d.materials.append(mat)
    if parent:o.parent=parent
    return o
def keys(o,attr,values,interp='BEZIER'):
    for f,v in values:setattr(o,attr,v);o.keyframe_insert(data_path=attr,frame=f)
    if o.animation_data and o.animation_data.action:
        for slot in o.animation_data.action.slots:
            for layer in o.animation_data.action.layers:
                for strip in layer.strips:
                    bag=strip.channelbag(slot)
                    if bag:
                        for fc in bag.fcurves:
                            for k in fc.keyframe_points:
                                k.interpolation=interp
                                if interp=='BEZIER':k.handle_left_type=k.handle_right_type='AUTO_CLAMPED'
def visible(o,start,end=456):
    for f,v in [(0,False),(start,True),(end+1,False)]:
        o.hide_render=not v;o.keyframe_insert(data_path='hide_render',frame=f)
        o.hide_viewport=not v;o.keyframe_insert(data_path='hide_viewport',frame=f)

camdata=bpy.data.cameras.new('Camera • shallow overhead');cam=bpy.data.objects.new('Camera',camdata)
STAGE.objects.link(cam);cam.location=(0,-18,24)
cam.rotation_euler=(Vector((0,0,0))-cam.location).to_track_quat('-Z','Y').to_euler()
camdata.type='ORTHO';camdata.ortho_scale=18.6;camdata.lens=50
scene.camera=cam
vf=camdata.view_frame(scene=scene);W=max(v.x for v in vf)*2;H=max(v.y for v in vf)*2
def uv(u,v,z=-8):return ((u-.5)*W,(.5-v)*H,z)
def ht(name,body,u,v,size,mat=WHITE,start=1,end=456,align='LEFT',font_=None):
    o=text(name,body,uv(u,v),size,mat,cam,align,font_);visible(o,start,end);return o
def panel(name,u,v,w,h,mat=CODE_BG,start=1,end=456):
    o=cube(name,uv(u,v,-8.05),(W*w,H*h,.015),mat,0,cam,HUD);visible(o,start,end);return o
def hline(name,pts,mat=RED,r=.021,start=1,end=456):
    o=path(name,[uv(u,v,-7.95) for u,v in pts],mat,r,cam);visible(o,start,end);return o

# Opaque stage with soft studio lighting.
cube('Endless matte stage',(0,0,-.64),(200,200,.35),FLOOR,.0,coll=STAGE)
def light(name,loc,power,size,color):
    d=bpy.data.lights.new(name,'AREA');o=bpy.data.objects.new(name,d);STAGE.objects.link(o)
    o.location=loc;o.rotation_euler=(Vector((0,0,0))-o.location).to_track_quat('-Z','Y').to_euler()
    d.energy=power;d.shape='DISK';d.size=size;d.color=color
light('Key • large softbox',(0,-4,13),1200,10,(.85,.92,1))
light('Rim • cool strip',(5,5,8),850,7,(.50,.72,1))
light('Fill • soft neutral',(-6,3,7),550,8,(.85,.90,1))

# Rebuilt composition: code above a substantially larger, deeper physical assembly.
scores=[];histories=[]
for i,(x,value) in enumerate(zip([-6.4,-1.65,3.1],[7,2,9])):
    s=empty(f'Player {i} • score motion');scores.append(s)
    cube(f'Score {value} • body',(0,0,0),(1.60,2.80,1.04),BLUE,.09,s)
    cube(f'Score {value} • matte face',(0,0,.533),(1.46,2.65,.035),FACE,.05,s)
    text(f'Score {value} • field label','score',(0,.55,.560),.44,WHITE,s,'CENTER',font,MODEL)
    text(f'Score {value} • numeral',str(value),(0,-.78,.562),1.20,WHITE,s,'CENTER',bold,MODEL)
    sk=[(1,(x,-1.5,0)),(166,(x,-1.5,0)),(185,(x,-2,1.35)),(213,((i-1)*1.76,-5.45,1.35)),(230,((i-1)*1.76,-5.45,.08)),(235,((i-1)*1.76,-5.45,.14)),(242,((i-1)*1.76,-5.45,.08)),(456,((i-1)*1.76,-5.45,.08))]
    keys(s,'location',sk)
    h=empty(f'Player {i} • history motion');histories.append(h)
    cube(f'History {i} • spine',(0,0,-.08),(3.02,2.80,.66),BASE,.08,h)
    first=None
    for j in range(15):
        px=(j-7)*.197
        if first is None:
            first=cube(f'History {i} • plate {j+1:02}',(px,0,.15),(.176,2.80,.77),GRAPHITE,.025,h)
        else:
            o=first.copy();o.data=first.data;MODEL.objects.link(o);o.name=f'History {i} • plate {j+1:02}';o.location=(px,0,.15)
    cube(f'History {i} • field inset',(0,0,.551),(2.40,.73,.045),BASE,.04,h)
    text(f'History {i} • field label','history',(0,-.17,.582),.49,WHITE,h,'CENTER',font,MODEL)
    # All records receive the same treatment. No query-subset highlighting.
    hk=[(1,(x+2.38,-1.5,0)),(18,(x+2.38,-1.5,0)),(35,(x+2.38,-1.5,.25)),(57,(x+2.38,-1.5,.25)),(72,(x+2.38,-1.5,0)),(185,(x+2.38,-1.5,0)),(242,((i-1)*3.17,.05,0)),(456,((i-1)*3.17,.05,0))]
    keys(h,'location',hk)

# Syntax highlighting uses material slots in a single monospaced text object.
import re
def code(name,body,start,end):
    o=ht(name,body,.085,.103,.64,WHITE,start,end,font_=mono)
    for m in (KEYWORD,TYPE,YELLOW):o.data.materials.append(m)
    for match in re.finditer(r'\b(struct|for|int|Player|SplitPlayers|array|vector|\d+)\b',body):
        word=match.group(0)
        index=1 if word in {'struct','for'} else 3 if word.isdigit() else 2
        for j in range(match.start(),match.end()):o.data.body_format[j].material_index=index
    return o
before='struct Player {\n  int score;\n  array<int, 15> history;\n};\n\nfor (int id : ids)\n  total += players[id].score;'
after='struct SplitPlayers {\n  vector<int> scores;\n  vector<array<int, 15>> histories;\n};\n\nfor (int id : ids)\n  total += scores[id];'
code('Code • before',before,1,166)
code('Code • after',after,167,288)
code('Code • final hold',after,361,456)

# Minimal result: the measured transition and its ratio, with no panel or headline.
ht('Timing • before','4.36 ms',.29,.150,1.02,WHITE,289,360,align='CENTER',font_=bold)
ht('Timing • after','0.35 ms',.72,.150,1.02,TEAL,289,360,align='CENTER',font_=bold)
hline('Timing • arrow',[(.445,.126),(.555,.126)],MUTED,.027,289,360)
hline('Timing • arrowhead',[(.535,.113),(.555,.126),(.535,.139)],MUTED,.027,289,360)
ht('Timing • ratio','12.5x faster',.50,.275,1.25,TEAL,289,360,align='CENTER',font_=bold)

for f,n in [(1,'01 • Assembly'),(61,'02 • Score-only lookup'),(167,'03 • Lift and gather'),(230,'04 • Contact'),(242,'05 • Separate arrays'),(289,'06 • Measured result'),(361,'07 • Final hold'),(456,'End • 19 seconds')]:
    scene.timeline_markers.new(n,frame=f)
scene['README']='Simplified v2. Code, field labels, values, and minimal timings only. No titles, captions, banners, voice, or selective highlights. 2160x2352, 24 fps, 19 seconds. All three scores and all 45 history plates are retained. The matte score faces use an unlit navy material to preserve white label contrast under every light.'
scene['SOURCE_EVIDENCE']='/Users/keremkazan/code/data-layout/LOOKUP-RESULTS.md'
scene['MEASURED_BEFORE_MS']=4.355233
scene['MEASURED_AFTER_MS']=0.347342
scene['MASTER_COMPOSITE']='Place at x=0, y=1488 in a 2160x3840 composition.'
scene.render.engine='BLENDER_EEVEE';scene.eevee.taa_render_samples=32
scene.render.image_settings.compression=15
scene.render.filepath=os.path.join(OUT,'frames','frame_')
scene.frame_set(1)
for area in bpy.context.screen.areas:
    if area.type=='VIEW_3D':
        area.spaces.active.region_3d.view_perspective='CAMERA'
        area.spaces.active.overlay.show_overlays=False
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'cpp-data-layout-clean.blend'))
if a.test_frame:
    scene.frame_set(a.test_frame);scene.render.filepath=os.path.join(OUT,f'frame-{a.test_frame:04}.png');bpy.ops.render.render(write_still=True)
print('BUILD_OK',flush=True)
