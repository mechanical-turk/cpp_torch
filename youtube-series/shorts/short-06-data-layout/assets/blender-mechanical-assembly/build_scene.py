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
HUD=collection('03 • Typography and evidence')
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
BLUE=material('Score • anodized blue',(.018,.31,.52),.55,.23)
GRAPHITE=material('History • graphite',(.075,.105,.14),.65,.31)
BASE=material('History • dark spine',(.028,.044,.064),.6,.32)
FLOOR=material('Stage • midnight',(.003,.006,.012),.08,.52)
WHITE=material('Type • ivory',(.84,.91,.97),emission=True)
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
light('Key • large softbox',(-5,-5,12),1300,8,(.77,.88,1))
light('Rim • cool strip',(6,4,8),1400,6,(.30,.70,1))
light('Fill • warm bounce',(-7,3,5),650,5,(1,.72,.4))

scores=[];histories=[]
for i,(x,value) in enumerate(zip([-6.35,-1.75,2.85],[7,2,9])):
    s=empty(f'Player {i} • score motion');scores.append(s)
    cube(f'Score {value}',(0,0,0),(1.04,1.40,.83),BLUE,.065,s)
    n=text(f'Score {value} • numeral',str(value),(0,-.28,.432),.88,WHITE,s,'CENTER',bold,MODEL)
    score_keys=[(1,(x,0,0)),(166,(x,0,0)),(185,(x,-.5,1.05)),(213,((i-1)*1.13,-2.3,1.05)),(230,((i-1)*1.13,-2.3,.08)),(235,((i-1)*1.13,-2.3,.14)),(242,((i-1)*1.13,-2.3,.08)),(456,((i-1)*1.13,-2.3,.08))]
    keys(s,'location',[(f,(v[0],v[1]-1,v[2])) for f,v in score_keys])
    # Selected IDs are 0 and 2 throughout. The center score is never selected.
    if i in (0,2):
        outline=path(f'Selected score {value}',[(-.56,-.75,.47),(.56,-.75,.47),(.56,.75,.47),(-.56,.75,.47),(-.56,-.75,.47)],YELLOW,.024,s)
        visible(outline,61,456)
    h=empty(f'Player {i} • retained history motion');histories.append(h)
    cube(f'History {i} • spine',(0,0,-.10),(3.28,1.4,.53),BASE,.06,h)
    # Fifteen literal identical plates, retained and moved as one history.
    first=None
    for j in range(15):
        plate_x=(j-7)*.214
        if first is None:
            first=cube(f'History {i} • plate {j+1:02}',(plate_x,0,.08),(.191,1.4,.60),GRAPHITE,.025,h)
        else:
            o=first.copy();o.data=first.data;MODEL.objects.link(o);o.name=f'History {i} • plate {j+1:02}';o.location=(plate_x,0,.08)
    cube(f'History {i} • label inset',(0,0,.402),(2.18,.62,.028),BASE,.035,h)
    text(f'History {i} • label','history',(0,-.15,.425),.45,WHITE,h,'CENTER',font,MODEL)
    # First history lifts with the hook, revealing its physical extent.
    hk=[(1,(x+2.19,0,0)),(18,(x+2.19,0,0)),(35,(x+2.19,0,.35 if i==0 else 0)),(57,(x+2.19,0,.35 if i==0 else 0)),(72,(x+2.19,0,0)),(185,(x+2.19,0,0)),(242,((i-1)*3.40,.85,0)),(456,((i-1)*3.40,.85,0))]
    keys(h,'location',[(f,(v[0],v[1]-1,v[2])) for f,v in hk])
    if i in (0,2):
        q=path(f'Selected history {i}',[(-1.69,-.75,.46),(1.69,-.75,.46),(1.69,.75,.46),(-1.69,.75,.46),(-1.69,-.75,.46)],YELLOW,.025,h)
        visible(q,361)

# Camera-facing design system. Copy is deliberately concise; speech stays external.
ht('Eyebrow','C++  /  DATA LAYOUT',.08,.055,.27,MUTED)
ht('Hook • subject','This struct is',.08,.111,.76,YELLOW,1,60,font_=bold)
ht('Hook • stakes','killing performance.',.08,.163,.76,TEAL,1,60,font_=bold)
ht('Score beat','We only need the scores.',.08,.134,.72,WHITE,61,112,font_=bold)
ht('Spacing beat','Look how far apart they are.',.08,.134,.64,WHITE,113,166,font_=bold)
ht('Extraction beat','Put scores together.',.08,.134,.76,WHITE,167,241,font_=bold)
ht('Histories beat','Keep the histories.',.08,.134,.76,WHITE,242,288,font_=bold)
ht('Result heading','12.5x faster.',.08,.134,.88,TEAL,289,360,font_=bold)
ht('Question heading','What if we need both?',.08,.134,.72,WHITE,361,456,font_=bold)

panel('Code panel',.475,.315,.79,.26,start=1,end=288)
ht('Code • original','struct Player {\n  int score;\n  array<int, 15> history;\n};',.105,.229,.55,WHITE,1,166,font_=mono)
ht('Code • lookup before','  total += players[id].score;',.105,.419,.55,YELLOW,1,166,font_=mono)
ht('Code • split','vector<int> scores;\nvector<array<int, 15>> histories;',.105,.249,.55,WHITE,167,288,font_=mono)
ht('Code • lookup after','  total += scores[id];',.105,.419,.55,YELLOW,167,288,font_=mono)
# A concise loop context prevents these snippets being read as a sequential scan.
ht('Lookup context','for (int id : ids)',.105,.385,.55,WHITE,1,288,font_=mono)
ht('Before layout label','BY PLAYER',.08,.482,.30,MUTED,1,166)
ht('After layout label','BY FIELD',.08,.482,.30,MUTED,242,456)
ht('Score-only scope','Score-only lookups',.08,.780,.40,MUTED,1,288)
ht('History count note','Each history retains 15 values',.08,.817,.34,MUTED,1,288)

# First-frame red mark tied to the actual history declaration.
oval=[]
for j in range(49):
    t=j*2*math.pi/48;oval.append((.393+.064*math.cos(t),.289+.019*math.sin(t)))
hline('History • red ellipse',oval,RED,.019,1,60)

# Spacing marker uses actual endpoints of selected score objects, projected from world.
from bpy_extras.object_utils import world_to_camera_view
scene.frame_set(120)
left=world_to_camera_view(scene,cam,Vector((-6.35+.56,-1.9,.4)))
right=world_to_camera_view(scene,cam,Vector((2.85-.56,-1.9,.4)))
yy=1-left.y+.025
bracket=hline('Separation • bracket',[(left.x,yy-.012),(left.x,yy),(right.x,yy),(right.x,yy-.012)],RED,.025,113,166)
keys(bracket,'scale',[(113,(.001,1,1)),(126,(1,1,1)),(166,(1,1,1))])

# Labels attach to the final physical lanes without inventing extra history arrays.
ht('History lane','histories',.5,.577,.35,MUTED,242,288,align='CENTER')
ht('Score lane','scores',.5,.721,.35,YELLOW,242,288,align='CENTER')

# Evidence is a static measured result, not a simulated read speed or timer.
panel('Result • card',.475,.315,.79,.26,start=289,end=360)
ht('Result • unit','Same score lookups / Median batch time',.105,.230,.37,MUTED,289,360)
ht('Result • before label','Player records',.105,.290,.55,WHITE,289,360)
ht('Result • before time','4.36 ms',.82,.290,.64,WHITE,289,360,align='RIGHT',font_=bold)
ht('Result • after label','Separate scores',.105,.345,.55,TEAL,289,360)
ht('Result • after time','0.35 ms',.82,.345,.64,TEAL,289,360,align='RIGHT',font_=bold)
ht('Result • workload','1.05M ordered IDs / 4.19M players',.105,.390,.39,MUTED,289,360)
ht('Result • compiler','Normal -O3 / Both scalar',.105,.422,.39,MUTED,289,360)
ht('Question • next test','NEXT TEST',.08,.741,.27,YELLOW,361,456)
ht('Question • scope','Read scores + histories',.08,.790,.55,WHITE,361,456,font_=bold)
for side in [-1,1]:
    link=path(f'Next test • selected player connection {side}',[(side*1.13,-2.55,.50),(side*1.13,-2.22,.50),(side*3.4,-1.24,.50),(side*3.4,-.92,.50)],YELLOW,.017)
    visible(link,361)

for f,n in [(1,'01 HOOK • point at history'),(61,'02 SCORES • selected IDs 0 and 2'),(113,'03 SPACING • spread hands'),(167,'04 EXTRACT • bring hands together'),(230,'05 SNAP • tactile click'),(242,'06 HISTORIES • point behind'),(289,'07 RESULT • measured medians'),(361,'08 NEXT TEST • read both'),(456,'CUT • 19 seconds')]:
    scene.timeline_markers.new(n,frame=f)
scene['README']='19-second lower-screen animation. 2160x2352, 24 fps. Three symbolic players: IDs 0 and 2 selected, scores 7 and 9; center score 2 retained. Each history has 15 plates. Movement illustrates layout, not memory traffic. Existing ordered-workload medians only; no measured cache misses. Narration/presenter are external.'
scene['SOURCE_EVIDENCE']='/Users/keremkazan/code/data-layout/LOOKUP-RESULTS.md'
scene['MEASURED_BEFORE_MS']=4.355233
scene['MEASURED_AFTER_MS']=0.347342
scene['MASTER_COMPOSITE']='Place this opaque 2160x2352 region at x=0, y=1488 in a 2160x3840 vertical timeline. Webcam region: 2160x1488.'

# EEVEE is fast and deterministic for this motion-graphics geometry.
scene.render.engine='BLENDER_EEVEE'
scene.eevee.taa_render_samples=32
scene.render.image_settings.compression=15
scene.render.filepath=os.path.join(OUT,'frames','frame_')
scene.frame_set(1)
for area in bpy.context.screen.areas:
    if area.type=='VIEW_3D':
        area.spaces.active.region_3d.view_perspective='CAMERA'
        area.spaces.active.overlay.show_overlays=False
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'cpp-data-layout-mechanical-assembly.blend'))
if a.test_frame:
    scene.frame_set(a.test_frame)
    scene.render.filepath=os.path.join(OUT,f'frame-{a.test_frame:04}.png')
    bpy.ops.render.render(write_still=True)
print('BUILD_OK',json.dumps({'width':scene.render.resolution_x,'height':scene.render.resolution_y,'frames':scene.frame_end,'fps':scene.render.fps,'objects':len(scene.objects),'device':scene.cycles.device,'camera_width':W,'camera_height':H}))
