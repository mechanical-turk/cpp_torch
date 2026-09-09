"""Approved Short 07 clay scene, six independent final animation segments.

Run with Blender. Native approved geometry/materials, no generated in-betweens.
This script builds and audits; render.py handles native frames separately.
"""
import bpy, math, json, hashlib, re
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

O=Path(__file__).resolve().parent
SOURCE=O.parent/'still-v8/short-07-clay-study-safe-code.blend'
bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
s=bpy.context.scene; cam=s.camera
MODEL=bpy.data.collections['01 • Clay models']; HUD=bpy.data.collections['02 • Code and results']
ROOT=s.objects['Foreground • common placement']; ROOT_BASE=ROOT.location.copy()
WIDTH,HEIGHT,FPS=2160,2300,24
s.render.resolution_x=WIDTH; s.render.resolution_y=HEIGHT
s.render.resolution_percentage=100; s.render.pixel_aspect_x=s.render.pixel_aspect_y=1
cam.data.sensor_fit='HORIZONTAL';cam.data.dof.use_dof=False
s.render.use_motion_blur=False
for o in s.objects:
    o.animation_data_clear();o.hide_viewport=False
for m in bpy.data.materials:
    if m.node_tree:m.node_tree.animation_data_clear()
for o in list(HUD.objects):bpy.data.objects.remove(o,do_unlink=True)
for o in list(MODEL.objects):
    if o.name.startswith('V8 ') or 'increment bubble' in o.name or ' • increment' in o.name or 'bubble clay' in o.name:
        bpy.data.objects.remove(o,do_unlink=True)
ca=s.objects['Counter a'];cb=s.objects['Counter b']
cores=[s.objects['Core 0'],s.objects['Core 1']]
tray=s.objects['Cache line 0']
old=s.objects['Cache line 1']
for o in list(old.children):bpy.data.objects.remove(o,do_unlink=True)
bpy.data.objects.remove(old,do_unlink=True)
tray2=tray.copy();MODEL.objects.link(tray2);tray2.name='Cache line 1';tray2.location=(2.5,-3.2,0)
for c in list(tray.children):
    o=c.copy();o.data=c.data;MODEL.objects.link(o);o.parent=tray2;o.name='Independent line • '+c.name
    if o.material_slots:
        mat=o.material_slots[0].material
        if 'shell' in o.name or 'floor' in o.name or 'ownership rim' in o.name:
            mat=mat.copy();mat.name='V8 independent blue '+o.name
            p=next((n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
            h='132958' if 'floor' in o.name else '2558BE'
            rgb=[int(h[i:i+2],16)/255 for i in (0,2,4)]
            if p:p.inputs['Base Color'].default_value=tuple(v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in rgb)+(1,)
            o.material_slots[0].link='OBJECT';o.material_slots[0].material=mat

def lin(h):
    return tuple(v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in [int(h[i:i+2],16)/255 for i in (0,2,4)])
ivory=bpy.data.materials['Ivory raised clay letters']
teal=bpy.data.materials['Deep teal worker clay'];blue=bpy.data.materials['Cobalt clay cards']
dark=bpy.data.materials['Recessed history plaque'];tealface=bpy.data.materials['Deep teal recessed face']
unit=(7*cam.data.sensor_width/cam.data.lens)/WIDTH
def px(x,y):return Vector(((x-WIDTH/2)*unit,(HEIGHT/2-y)*unit,-7))
def empty(name,coll=MODEL,parent=ROOT):
    o=bpy.data.objects.new(name,None);coll.objects.link(o);o.parent=parent;return o
def key(o,prop,v,f):setattr(o,prop,v);o.keyframe_insert(data_path=prop,frame=f)
def show(o,on,f):key(o,'hide_render',not on,f)
def smooth(t):t=max(0,min(1,t));return t*t*(3-2*t)
def lerp(a,b,t):return a+(b-a)*t
def emission(name,h):
    m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;n.clear()
    e=n.new('ShaderNodeEmission');e.inputs['Color'].default_value=(*lin(h),1)
    out=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(e.outputs[0],out.inputs['Surface']);return m
syntax={k:emission('V8 '+k,h) for k,h in [('plain','FFF8EB'),('keyword','EDC7FF'),('type','B8F2EB'),('number','FFE0A3'),('change','7AF5C4')]}
menlo=bpy.data.fonts.load('/System/Library/Fonts/Menlo.ttc')
bold=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Arial Bold.ttf')
heavy=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Arial Black.ttf')
def text(name,body,size,mat,parent,coll=MODEL,font=bold):
    d=bpy.data.curves.new(name,'FONT');d.body=body;d.font=font;d.size=size;d.resolution_u=24
    o=bpy.data.objects.new(name,d);coll.objects.link(o);o.parent=parent;d.materials.append(mat);return o
def code(name,body):
    o=text(name,body,100*unit,syntax['plain'],cam,HUD,menlo);o.data.offset=.0009
    roles=list(syntax)
    for role in roles[1:]:o.data.materials.append(syntax[role])
    for match in re.finditer(r'[A-Za-z_][A-Za-z_0-9]*|[0-9]+',body):
        token=match.group();role='keyword' if token in ['struct','alignas'] else 'type' if token in ['Counters','atomic','uint64_t'] else 'number' if token.isdigit() else 'plain'
        for j in range(match.start(),match.end()):o.data.body_format[j].material_index=roles.index(role)
    return o
header=code('Code header','struct Counters {')
rowa=code('Code a','  atomic<uint64_t> a{0};');rowb=code('Code b','  atomic<uint64_t> b{0};')
footer=code('Code footer','};')
aligns=[code('Alignment a','  alignas(128) atomic<uint64_t> a{0};'),code('Alignment b','  alignas(128) atomic<uint64_t> b{0};')]
underlines=[]
for i in range(2):
    d=bpy.data.curves.new('Alignment underline','CURVE');d.dimensions='3D';d.bevel_depth=2.8*unit;d.bevel_resolution=4
    sp=d.splines.new('POLY');sp.points.add(1);sp.points[0].co=(0,0,0,1);sp.points[1].co=(530*unit,0,0,1)
    o=bpy.data.objects.new('Alignment underline '+str(i),d);HUD.objects.link(o);o.parent=cam;d.materials.append(syntax['change']);underlines.append(o)

# Pure emission result typography and one continuous filled arrow, optically aligned.
coral=emission('V8 benchmark coral','FF8D6C');mint=emission('V8 benchmark mint','7AF5C4')
def visible_bounds(obs):
    bpy.context.view_layer.update()
    vs=[world_to_camera_view(s,cam,o.matrix_world@Vector(v)) for o in obs if o.type in {'MESH','FONT','CURVE','META'} and not o.hide_render for v in o.bound_box]
    if not vs:return None
    return [min(v.x for v in vs)*WIDTH,min(1-v.y for v in vs)*HEIGHT,max(v.x for v in vs)*WIDTH,max(1-v.y for v in vs)*HEIGHT]
def set_glyph_height(o,h):
    bpy.context.view_layer.update();ys=[v[1] for v in o.bound_box];o.data.size*=h*unit/(max(ys)-min(ys));bpy.context.view_layer.update()
def timing(value,x,mat):
    g=empty('Timing '+value,HUD,cam);g.location=px(x,640)
    n=text(value,value,1,mat,g,HUD,heavy);u=text(value+' ms','ms',1,mat,g,HUD,bold)
    set_glyph_height(n,120);set_glyph_height(u,46)
    nw=max(v[0] for v in n.bound_box)-min(v[0] for v in n.bound_box);uw=max(v[0] for v in u.bound_box)-min(v[0] for v in u.bound_box)
    for o,start in [(n,-(nw+uw+14*unit)/2),(u,(nw+uw+14*unit)/2-uw)]:
        xs=[v[0] for v in o.bound_box];ys=[v[1] for v in o.bound_box]
        o.location=(start-min(xs),-(min(ys)+max(ys))/2,0)
    return g
left=timing('244.52',560,coral);right=timing('44.19',1500,mint)
ratio=text('Measured speedup','5.5× faster',1,mint,cam,HUD,heavy);set_glyph_height(ratio,126)
def center_text(o,x,y):
    bpy.context.view_layer.update();xs=[v[0] for v in o.bound_box];ys=[v[1] for v in o.bound_box]
    o.location=px(x,y)-Vector(((min(xs)+max(xs))/2,(min(ys)+max(ys))/2,0))
center_text(ratio,1000,880)
d=bpy.data.curves.new('Single continuous benchmark arrow','CURVE');d.dimensions='2D';d.fill_mode='BOTH';d.extrude=2*unit;d.bevel_depth=6*unit;d.bevel_resolution=5
sp=d.splines.new('POLY');points=[(-92,-12),(40,-12),(40,-39),(96,0),(40,39),(40,12),(-92,12)];sp.points.add(len(points)-1)
for p,(x,y) in zip(sp.points,points):p.co=(x*unit,y*unit,0,1)
sp.use_cyclic_u=True
arrow=bpy.data.objects.new('Clean benchmark arrow',d);HUD.objects.link(arrow);arrow.parent=cam;arrow.location=px(1070,640);d.materials.append(syntax['plain'])
# Reveal using a local-coordinate shader mask, preserving the arrow silhouette.
m=syntax['plain'].copy();m.name='V8 arrow reveal';d.materials[0]=m;n=m.node_tree.nodes;l=m.node_tree.links
out=next(x for x in n if x.type=='OUTPUT_MATERIAL');base=out.inputs['Surface'].links[0].from_socket
tc=n.new('ShaderNodeTexCoord');sep=n.new('ShaderNodeSeparateXYZ');l.new(tc.outputs['Object'],sep.inputs[0])
val=n.new('ShaderNodeValue');val.name='Draw progress';cmp=n.new('ShaderNodeMath');cmp.operation='GREATER_THAN';l.new(sep.outputs['X'],cmp.inputs[0]);l.new(val.outputs[0],cmp.inputs[1])
tr=n.new('ShaderNodeBsdfTransparent');mix=n.new('ShaderNodeMixShader');l.new(cmp.outputs[0],mix.inputs[0]);l.new(base,mix.inputs[1]);l.new(tr.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],out.inputs['Surface'])

# Seven canonical clay pills and a continuous metaball packet that consumes and
# releases neighboring pills. Element positions/radii are native animated data.
paths=[];packets=[]
for i,mat in enumerate([teal,blue]):
    pills=[]
    for j in range(7):
        if i==0 and j==0:
            bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=16,radius=1);o=bpy.context.object
            for c in list(o.users_collection):c.objects.unlink(o)
            MODEL.objects.link(o)
            for p in o.data.polygons:p.use_smooth=True
            canonical=o.data
        else:o=bpy.data.objects.new('dash',canonical);MODEL.objects.link(o)
        o.name=f'Worker {i} dash {j}';o.parent=ROOT
        if not o.material_slots:o.data.materials.append(mat)
        o.material_slots[0].link='OBJECT';o.material_slots[0].material=mat;pills.append(o)
    paths.append(pills)
    mb=bpy.data.metaballs.new(f'Worker {i} flowing clay');mb.resolution=.045;mb.render_resolution=.035;mb.threshold=.6
    o=bpy.data.objects.new(f'Worker {i} merged packet',mb);MODEL.objects.link(o);o.parent=ROOT;mb.materials.append(mat)
    for j in range(27):mb.elements.new().stiffness=2
    packets.append(o)

# Canonical bubble geometry; each write owns its complete 40-frame lifetime.
template=next(o for o in ca.children if 'inset' in o.name)
bubbles=[]
for i in range(2):
    pool=[]
    for j in range(2):
        g=empty(f'Counter {i} bubble {j}');g.rotation_euler.x=math.radians(45)
        # A rounded dark clay capsule gives the raised +1 consistent contrast.
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=16,radius=1);o=bpy.context.object
        for c in list(o.users_collection):c.objects.unlink(o)
        MODEL.objects.link(o);o.name=f'Counter {i} bubble {j} capsule';o.parent=g;o.scale=(.69,.39,.105);o.data.materials.append(tealface if i==0 else dark)
        for p in o.data.polygons:p.use_smooth=True
        t=text(f'Counter {i} bubble {j} plus one','+1',.64,ivory,g);t.data.align_x='CENTER';t.data.extrude=.0018;t.data.bevel_depth=.0006;t.location=(0,-.21,.11)
        pool.append(g)
    bubbles.append(pool)
digits=[]
for counter in [ca,cb]:digits.append(sorted([o for o in counter.children if ' • value ' in o.name],key=lambda o:int(o.name.split(' • value ')[-1])))
owned=[]
for o in tray.children:
    if o.material_slots and any(k in o.name for k in ['shell','floor','ownership rim']):
        mat=o.material_slots[0].material;p=next((n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
        if p:owned.append((p,'floor' in o.name))

PAD,LIFT,CROSS,LANDED,RESULT,END=433,467,485,529,577,864
clips=[('01-crowded-opening',1,144),('02-shared-cache-line',145,288),('03-write-ownership',289,432),('04-add-padding',433,576),('05-benchmark-result',577,672),('06-discussion-hold',673,864)]
events=[];writes=[[],[]]
for cycle in range(6):
    st=1+cycle*72;i=1-cycle%2
    events.append(dict(requester=i,pulse_start=st,pulse_arrival=st+20,ownership=st+24,transfer_start=st+30,transfer_end=st+48,writes=[st+50,st+66]))
    writes[i]+=[st+50,st+66]
for i in range(2):writes[i]+=list(range(LANDED+24+8*i,END+1,72))
def transfer(t):
    # Resisted launch, quick travel, overshoot, and damped landing.
    if t<0:return 0
    if t<2:return -.025*smooth(t/2)
    if t<14:return -.025+1.075*smooth((t-2)/12)
    if t<18:return 1.05-.05*smooth((t-14)/4)
    return 1
def motion(f):
    owner=0;dx=0;travel=[False,False];progress=[0,0]
    if f<PAD:
        cycle=(f-1)//72;phase=(f-1)%72;i=1-cycle%2
        owner=i if phase>=24 else 1-i
        old=0 if i==1 else 3.35;new=3.35-old;dx=lerp(old,new,transfer(phase-30))
        travel[i]=phase<=20;progress[i]=smooth(phase/20)
    elif f>=LANDED:
        for i in range(2):
            phase=(f-LANDED-8*i)%72;travel[i]=f>=LANDED+8*i and phase<=20;progress[i]=smooth(phase/20)
    return owner,dx,travel,progress
def b_pose(f):
    if f<LIFT:return -1.6,.30
    if f<CROSS:return -1.6,.30+1.35*smooth((f-LIFT)/(CROSS-LIFT))
    if f<513:
        t=(f-CROSS)/28;return lerp(-1.6,1.6,smooth(t)),1.65+.16*math.sin(math.pi*t)
    if f<LANDED:
        t=(f-513)/(LANDED-513);return 1.6,.30+1.35*(1-smooth(t))
    return 1.6,.30

for f in range(1,END+1,2):
    owner,dx,travel,progress=motion(f);bx,bz=b_pose(f)
    # Reframe horizontally as the second address region becomes visible. All
    # native object scales remain the approved scales; a stays fixed in its tray.
    pan=smooth((f-PAD)/24);ROOT.location=ROOT_BASE+Vector((-.99*pan,0,0));ROOT.keyframe_insert(data_path='location',frame=f)
    core_shift=0
    for o,x in zip(cores,[-2.5,2.5]):key(o,'location',(x,2.05-core_shift,1.10),f)
    key(tray,'location',(-2.5+dx,-3.2,0),f);key(tray2,'location',(2.5,-3.2,0),f)
    for o in [tray2]+list(tray2.children):show(o,f>=PAD+24,f)
    # Small common assembly bank conveys inertia without independently deforming peers.
    phase=(f-1)%72;bank=0
    if f<PAD and 30<=phase<48:bank=math.radians(1.8)*math.sin(math.pi*(phase-30)/18)*(1 if owner else -1)
    key(tray,'rotation_euler',(0,bank,0),f)
    key(ca,'location',(-3.4+dx,-3.2,.30+.9*math.sin(bank)),f)
    key(cb,'location',(bx+dx,-3.2,bz-.9*math.sin(bank)),f)
    for o in [ca,cb]:key(o,'rotation_euler',(0,bank,0),f)
    counts=[sum(t<=f for t in ts) for ts in writes]
    ages=[f-max([t for t in ts if t<=f],default=-1000) for ts in writes]
    for i,o in enumerate([ca,cb]):
        press=1-.045*(1-smooth(ages[i]/8)) if 0<=ages[i]<8 else 1
        key(o,'scale',(.66,.66,.70*press),f)
        for value,digit in enumerate(digits[i]):
            show(digit,value==counts[i],f);p=1+.10*(1-smooth(ages[i]/8)) if 0<=ages[i]<8 else 1;key(digit,'scale',(p,p,p),f)
    for node,floor in owned:
        node.inputs['Base Color'].default_value=(*lin((['073E3F','132958'] if floor else ['008F88','2558BE'])[owner]),1)
        node.inputs['Base Color'].keyframe_insert(data_path='default_value',frame=f)
    for i in range(2):
        start=Vector((-2.5 if i==0 else 2.5,.75-core_shift,.84))
        end=Vector(((-3.4 if i==0 else bx)+dx,-2.27,1.06 if i==0 else bz+.76))
        direction=(end-start).normalized();p=progress[i];is_on=travel[i] and not LIFT<=f<LANDED
        for j,o in enumerate(paths[i]):
            t=j/7;point=start.lerp(end,t);dist=abs(t-p)
            swell=1+.55*math.exp(-((dist-.21)/.055)**2) if is_on else 1
            key(o,'location',point+direction*.11,f);key(o,'rotation_euler',Vector((0,1,0)).rotation_difference(direction).to_euler(),f)
            key(o,'scale',(.135*swell,.245*swell,.135*swell),f)
            show(o,not LIFT<=f<LANDED and not (is_on and dist<.18),f)
        packet=packets[i];show(packet,is_on,f)
        for j,e in enumerate(packet.data.elements):
            offset=-.18+j/26*.36;t=max(0,min(1,p+offset))
            e.co=start.lerp(end,t);e.radius=.19+.34*math.exp(-(offset/.095)**2)
            e.keyframe_insert(data_path='co',frame=f);e.keyframe_insert(data_path='radius',frame=f)
        for j,g in enumerate(bubbles[i]):
            eligible=[t for ix,t in enumerate(writes[i]) if ix%2==j and 0<=f-t<40]
            for o in g.children:show(o,bool(eligible),f)
            if eligible:
                t=eligible[-1];age=f-t;u=age/40;_,wdx,_,_=motion(t);wbx,_=b_pose(t)
                key(g,'location',((-3.4 if i==0 else wbx)+wdx,-3.25,2.55+1.65*smooth(u)),f)
                envelope=min(1,.82+u*2)*(1-.10*smooth((u-.8)/.2));key(g,'scale',(envelope,)*3,f)

    # Both layouts retain four rows. Inline alignas is explicit creator direction;
    # one smaller font fits the longest complete declaration in the safe zone.
    ys=[590,715,840,965]
    for o,y in zip([header,rowa,rowb,footer],ys):key(o,'location',px(200,y),f);show(o,f<RESULT,f)
    for i,o in enumerate(aligns):
        start=PAD+6+i*8;y=715+i*125
        out=smooth((f-start)/8);reveal=smooth((f-start-9)/18)
        old=[rowa,rowb][i];key(old,'location',px(200-20*out,y),f);key(old,'scale',(1,max(.02,1-out),1),f);show(old,f<start+9,f)
        key(o,'location',px(200+28*(1-reveal),y),f);key(o,'scale',(1,max(.02,reveal),1),f);show(o,start+9<=f<RESULT,f)
        g=underlines[i];key(g,'location',px(295,y+24),f)
        show(g,start+20<=f<RESULT-12,f)
        key(g,'scale',(max(.001,smooth((f-start-20)/14)*(1-smooth((f-RESULT+30)/18))),1,1),f)
    for g,delay in [(left,0),(right,8)]:
        t=smooth((f-RESULT-delay)/16);key(g,'scale',(.96+.04*t,)*3,f)
        for o in g.children:show(o,f>=RESULT+delay,f)
    show(arrow,f>=RESULT+4,f);val.outputs[0].default_value=lerp(-105,110,smooth((f-RESULT-4)/16))*unit;val.outputs[0].keyframe_insert(data_path='default_value',frame=f)
    show(ratio,f>=RESULT+24,f);t=smooth((f-RESULT-24)/16);key(ratio,'scale',(.94+.06*t,)*3,f)

# Exact held poses on twos. No optical-flow or invented intermediate frames.
animated=list(s.objects)+[m.node_tree for m in bpy.data.materials if m.node_tree]+[p.data for p in packets]
for obj in animated:
    if obj.animation_data and obj.animation_data.action:
        a=obj.animation_data.action
        for layer in a.layers:
            for strip in layer.strips:
                for slot in a.slots:
                    bag=strip.channelbag(slot)
                    if bag:
                        for fc in bag.fcurves:
                            for k in fc.keyframe_points:k.interpolation='CONSTANT'

s.render.engine='CYCLES';s.render.fps=FPS;s.render.fps_base=1;s.frame_start=1;s.frame_end=END
s.render.use_border=False;s.render.film_transparent=False;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB'
s.render.use_persistent_data=True;s.cycles.samples=96;s.cycles.adaptive_threshold=.008;s.cycles.filter_width=.8;s.cycles.use_denoising=True;s.cycles.use_animated_seed=False;s.cycles.seed=0
s.render.use_compositing=False;s.render.use_sequencer=False
for marker in list(s.timeline_markers):s.timeline_markers.remove(marker)
for name,st,en in clips:s.timeline_markers.new(name,frame=st)
script=O.parents[2]/'script.md'
manifest={'revision':8,'resolution':[WIDTH,HEIGHT],'fps':FPS,'master_resolution':[2160,3840],'master_placement':[0,0],
          'clips':[dict(file=n+'.mp4',start=st,end=en,frames=en-st+1,seconds=(en-st+1)/FPS) for n,st,en in clips],
          'benchmark':{'packed_ms':'244.52','separated_ms':'44.19','speedup':'5.5× faster'},'source_script_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),
          'template':'youtube-series/assets/all-platforms-safe-zone-template-1080x1920.png','font_units':100,'alignment_layout':'inline with each atomic declaration; four rows in both layouts',
          'approved_reference':str(SOURCE),'motion':'72-frame handoffs: 20 travel, color at 24, resisted transfer at 30 through 48, writes at 50 and 66; rising bubbles last 40 frames'}
(O/'scene-manifest.json').write_text(json.dumps(manifest,indent=2))
# Audit every authored pose before expensive rendering. Model geometry may use
# the nonessential margins; all code and physical labels must fit the template.
overall={'hud':[WIDTH,HEIGHT,0,0],'labels':[WIDTH,HEIGHT,0,0],'model':[WIDTH,HEIGHT,0,0]};violations=[]
maps={'model':{},'hud':{}};seen={'model':{},'hud':{}}
for f in range(1,END+1):
    s.frame_set(f);bpy.context.view_layer.update()
    groups={'hud':[o for o in HUD.objects if o.type in {'FONT','CURVE'}],
            'labels':[o for o in MODEL.objects if o.type=='FONT'],
            'model':[o for o in MODEL.objects if o.type in {'FONT','MESH','CURVE'}]}
    for name,obs in groups.items():
        b=visible_bounds(obs)
        if not b:continue
        overall[name]=[min(overall[name][0],b[0]),min(overall[name][1],b[1]),max(overall[name][2],b[2]),max(overall[name][3],b[3])]
        safe=(180,480,1812,1180) if name=='hud' else (120,440,1872,2260) if name=='labels' else (0,990,2160,2300)
        if b[0]<safe[0] or b[1]<safe[1] or b[2]>safe[2] or b[3]>safe[3]:violations.append((f,name,b))
    for tag,coll in [('model',MODEL),('hud',HUD)]:
        state=[]
        for o in coll.objects:
            if o.hide_render or o.type not in {'FONT','MESH','CURVE','META'}:continue
            state.append((o.name,tuple(round(v,6) for row in o.matrix_world for v in row)))
            if o.type=='META':state.append(tuple(tuple(round(v,5) for v in e.co)+(round(e.radius,5),) for e in o.data.elements))
        if tag=='model':state.append(tuple(tuple(p.inputs['Base Color'].default_value) for p,_ in owned))
        else:state.append(round(val.outputs[0].default_value,6))
        digest=hashlib.sha256(repr(state).encode()).hexdigest();maps[tag][str(f)]=seen[tag].setdefault(digest,f)
report={'bounds':overall,'frame_maps':maps,'unique_states':{k:len(v) for k,v in seen.items()},'split_y':990,
        'violations':violations[:30],'violation_count':len(violations),'events':events,'writes':writes,
        'same_canonical_trays':all(a.data==b.data for a,b in zip(tray.children,tray2.children)),
        'native_resolution':[WIDTH,HEIGHT],'no_post_render_scaling':True,'template_scale':2}
(O/'scene-verification.json').write_text(json.dumps(report,indent=2));print('AUDIT',json.dumps({k:v for k,v in report.items() if k!='frame_maps'}),flush=True)
s.frame_set(1);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(O/'false-sharing-final.blend'))
assert not violations, 'Safe-zone/layout audit failed; inspect scene-verification.json before rendering.'
