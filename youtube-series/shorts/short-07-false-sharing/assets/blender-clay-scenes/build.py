"""Native Short 07 scene builder. Run with Blender --python build.py -- --preview.
Source scene supplied by --source; outputs default beside this script.
No image-generation pixels are used in the render.
"""
import bpy, math, json, ast, argparse, sys, hashlib, re
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
P=argparse.ArgumentParser();P.add_argument('--source',default='/Users/keremkazan/Documents/Projects/Content HQ/youtube-series/shorts/short-06-data-layout/assets/blender-clay-animation/cpp-data-layout-clay-animation.blend');P.add_argument('--preview',action='store_true');P.add_argument('--work',default=None)
a=P.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []);O=Path(__file__).resolve().parent;W=Path(a.work) if a.work else O/'_render/current';assert W.resolve().is_relative_to(O.resolve()), 'Render work must stay inside this Content HQ assets package';W.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=a.source);s=bpy.context.scene;cam=s.camera;s.frame_set(340)
# Retain the approved studio and canonical scalar shell, removing previous content.
arrow_template=s.objects['Clean sculpted ivory arrow'].copy()
master=s.objects['Score 2 assembly'];templates=[o.copy() for o in master.children if o.type=='MESH']
for o in list(s.objects):
 if o.type not in ['LIGHT','CAMERA'] and o.name!='Continuous clay studio ground':bpy.data.objects.remove(o,do_unlink=True)
for o in s.objects:o.animation_data_clear()
MODEL=bpy.data.collections['01 • Clay models'];HUD=bpy.data.collections['02 • Code and results'];STAGE=bpy.data.collections['03 • Studio']
def move(o,c):
 for old in list(o.users_collection):old.objects.unlink(o)
 c.objects.link(o)
def empty(n,parent=None):
 o=bpy.data.objects.new(n,None);MODEL.objects.link(o);o.parent=parent;return o
ROOT=empty('Foreground • common placement');ROOT['additional_top_clearance_px']=100
# Reuse the original native loft functions, without executing its builder/render.
source=Path(a.source).parent.parent/'blender-clay-studio/build.py'
module=ast.parse(source.read_text());exec(compile(ast.Module(body=[n for n in module.body if isinstance(n,ast.FunctionDef) and n.name in ['points','loft','rounded']],type_ignores=[]),str(source),'exec'))
gold=bpy.data.materials['Golden sculpted clay'];blue=bpy.data.materials['Cobalt clay cards'];navy=bpy.data.materials['Plum navy clay cradle'];dark=bpy.data.materials['Recessed history plaque'];brown=bpy.data.materials['Amber recessed clay face'];ivory=bpy.data.materials['Ivory raised clay letters']
def recolor_clay(base,name,h):
 m=base.copy();m.name=name
 rgb=tuple((int(h[i:i+2],16)/255/12.92 if int(h[i:i+2],16)/255<=.04045 else ((int(h[i:i+2],16)/255+.055)/1.055)**2.4) for i in (0,2,4))
 m.diffuse_color=(*rgb,1)
 for n in m.node_tree.nodes:
  if n.type=='VALTORGB':
   n.color_ramp.elements[0].color=tuple(v*.83 for v in rgb)+(1,);n.color_ramp.elements[-1].color=tuple(v*1.06 for v in rgb)+(1,)
  if n.type=='BSDF_PRINCIPLED':n.inputs['Base Color'].default_value=(*rgb,1)
 return m
gold=recolor_clay(blue,'Deep teal worker clay','008F88')
tealface=recolor_clay(dark,'Deep teal recessed face','073738')
font=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Arial.ttf');bold=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Arial Bold.ttf');heavy=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Arial Black.ttf')
def text(n,body,size,mat,parent,loc=(0,0,0),font_=font):
 d=bpy.data.curves.new(n,'FONT');d.body=body;d.font=font_;d.size=size;d.align_x='CENTER';d.resolution_u=12
 d.extrude=.0018 if mat==ivory else 0;d.bevel_depth=.0006 if mat==ivory else 0
 o=bpy.data.objects.new(n,d);MODEL.objects.link(o);o.parent=parent;o.location=loc;d.materials.append(mat);return o

def family_copy(g,name):
 h=g.copy();MODEL.objects.link(h);h.name=name
 for c in list(g.children):
  o=c.copy();o.data=c.data;MODEL.objects.link(o);o.parent=h;o.name=name+' • '+c.name.split(' • ')[-1]
 return h

def worker_material(g,mat):
 for o in g.children:
  if o.type=='MESH' and 'shell' in o.name:
   o.material_slots[0].link='OBJECT';o.material_slots[0].material=mat
  elif o.type=='MESH' and 'inset' in o.name and mat==blue:
   o.material_slots[0].link='OBJECT';o.material_slots[0].material=dark

def scalar(name,label):
 g=empty(name,ROOT)
 for t in templates:
  o=t.copy();o.data=t.data;MODEL.objects.link(o);o.parent=g;o.name=name+(' • shell' if 'shell' in t.name else ' • inset');o.animation_data_clear()
  for m in o.modifiers:
   if m.type=='DISPLACE':m.texture_coords='LOCAL'
 text(name+' • label',label,1.55,ivory,g,(0,-.49,.945),bold)
 return g
ca=scalar('Counter a','a');cb=family_copy(ca,'Counter b')
for o in cb.children:
 if o.type=='FONT':o.data=o.data.copy();o.data.body='b'
worker_material(ca,gold)
for o in ca.children:
 if o.type=='MESH' and 'inset' in o.name:o.material_slots[0].link='OBJECT';o.material_slots[0].material=tealface
worker_material(cb,blue)
for g in [ca,cb]:g.scale=(.66,.66,.70)
ca.location=(-3.4,-3.2,.30);cb.location=(-1.6,-3.2,.30)
core0=scalar('Core 0','Core 0')
for o in core0.children:
 if o.type=='FONT':o.data.size=.60;o.data.font=font;o.scale.y=1/.57;o.location=(0,-.30,.945)
core1=family_copy(core0,'Core 1')
for o in core1.children:
 if o.type=='FONT':o.data=o.data.copy();o.data.body='Core 1'
worker_material(core0,gold)
for o in core0.children:
 if o.type=='MESH' and 'inset' in o.name:o.material_slots[0].link='OBJECT';o.material_slots[0].material=tealface
worker_material(core1,blue)
for g,x in [(core0,-2.5),(core1,2.5)]:g.scale=(1.00,.57,.68);g.rotation_euler.x=math.radians(65);g.location=(x,2.05,1.10)
# Identical trays; they represent fixed cache-line address regions, not a physical shared cache.
tray=empty('Cache line 0',ROOT);tray.location=(-2.5,-3.2,0)
body=loft('Tray • shell',[(.02,4.40,2.92,.40),(.09,4.62,3.13,.44),(.26,4.72,3.22,.46),(.52,4.70,3.20,.45),(.68,4.57,3.08,.42),(.72,4.40,2.91,.36),(.67,4.22,2.74,.30),(.55,4.18,2.70,.28),(.16,4.15,2.67,.27)],navy,tray,2)
for v in body.data.vertices:v.co.z*=1.3
floor=rounded('Tray • recessed floor',4.15,2.67,.07,.27,navy,tray);floor.location.z=.265
plaque=rounded('Tray • plaque',3.30,.70,.038,.16,dark,tray);plaque.rotation_euler.x=math.pi/2;plaque.location=(0,-1.608,.47)
t=text('Tray • label','cache line',.58,ivory,tray,(0,-1.635,.27));t.rotation_euler.x=math.pi/2

def path(n,coords,rad,mat,parent=ROOT,closed=False):
 d=bpy.data.curves.new(n,'CURVE');d.dimensions='3D';d.bevel_depth=rad;d.bevel_resolution=4;d.use_fill_caps=True;sp=d.splines.new('POLY');sp.points.add(len(coords)-1)
 for p,c in zip(sp.points,coords):p.co=(*c,1)
 sp.use_cyclic_u=closed;o=bpy.data.objects.new(n,d);MODEL.objects.link(o);o.parent=parent;d.materials.append(mat);return o
rim=path('Tray • ownership rim',[(x,y,.935) for x,y in points(4.40,2.91,.36)],.035,gold,tray,True)
tray2=family_copy(tray,'Cache line 1');tray2.location=(2.5,-3.2,0)
rim2=next(o for o in tray2.children if o.type=='CURVE');rim2.material_slots[0].link='OBJECT';rim2.material_slots[0].material=blue
# Ownership is keyed as object material color, retaining matte clay texture.
rim_mat=gold.copy();rim_mat.name='Whole line • ownership tint';rim.data.materials.clear();rim.data.materials.append(rim_mat)
rim2.material_slots[0].link='OBJECT';rim2.material_slots[0].material=blue
pb=next(n for n in rim_mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
for link in list(pb.inputs['Base Color'].links):rim_mat.node_tree.links.remove(link)

def lin(h):
 c=[int(h[i:i+2],16)/255 for i in (0,2,4)];return tuple(v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in c)
colors=[(*lin('008F88'),1),(*lin('2558BE'),1)]
# Whole-region ownership is visible on the body and recessed floor, not only a rim.
owned_nodes=[];ownership_trees=[]
for part,base in [('shell',navy),('recessed floor',navy)]:
 m=base.copy();m.name='Owned cache line • '+part
 node=m.node_tree.nodes.get('Principled BSDF')
 for link in list(node.inputs['Base Color'].links):m.node_tree.links.remove(link)
 owned_nodes.append((node,part));ownership_trees.append(m.node_tree)
 obj=next(o for o in tray.children if o.name.endswith(' • '+part));obj.material_slots[0].link='OBJECT';obj.material_slots[0].material=m
 obj2=next(o for o in tray2.children if o.name.endswith(' • '+part));m2=m.copy();m2.name='Independent cobalt line • '+part
 n2=m2.node_tree.nodes.get('Principled BSDF');n2.inputs['Base Color'].default_value=(*lin('2558BE' if part=='shell' else '132958'),1)
 obj2.material_slots[0].link='OBJECT';obj2.material_slots[0].material=m2

# Dashed paths terminate at the rear edge of the actual corresponding counter.
# Points clear the tray rim at z=.86; no cable between counters is implied.
paths=[];beads=[];increments=[];counter_digits=[]
for i,mat in enumerate([gold,blue]):
 segs=[path(f'Worker {i} • clay dash {j}',[(0,0,0),(0,.24,0)],.10,mat) for j in range(7)];paths.append(segs)
 bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=12,radius=.16);o=bpy.context.object;o.name=f'Worker {i} • update pulse';move(o,MODEL);o.parent=ROOT;o.data.materials.append(mat)
 for p in o.data.polygons:p.use_smooth=True
 beads.append(o)
 bubble=empty(f'Counter {i} • increment bubble',ROOT)
 bubble.rotation_euler.x=math.radians(45)
 pill=rounded(f'Counter {i} • bubble clay',1.35,.78,.14,.34,tealface if i==0 else dark,bubble);move(pill,MODEL)
 if i==1:
  pill.data=bpy.data.objects['Counter 0 • bubble clay'].data;pill.material_slots[0].link='OBJECT';pill.material_slots[0].material=dark
 inc=text(f'Counter {i} • increment','+1',.64,ivory,bubble,(0,-.21,.15),bold);increments.append(bubble)
for g in [ca,cb]:
 label=next(o for o in g.children if o.type=='FONT' and o.data.body in ['a','b']);label.data=label.data.copy();label.data.size=.72;label.location.y=.42
 digits=[]
 for value in range(20):digits.append(text(g.name+' • value '+str(value),str(value),1.25,ivory,g,(0,-.61,.945),bold))
 counter_digits.append(digits)
# One baseline curve for all worker dashes; object-level materials keep identities.
for i in range(2):
 for o in paths[i]:
  o.data=paths[0][0].data;o.material_slots[0].link='OBJECT';o.material_slots[0].material=gold if i==0 else blue
face_nodes=[];face_trees=[]
for g in [ca,cb]:
 inset=next(o for o in g.children if o.type=='MESH' and 'inset' in o.name);m=inset.material_slots[0].material.copy();m.name=g.name+' update face';inset.material_slots[0].link='OBJECT';inset.material_slots[0].material=m
 node=m.node_tree.nodes.get('Principled BSDF');face_nodes.append(node);face_trees.append(m.node_tree)
# All objects created by loft go into the model collection.
for o in list(s.objects):
 if o.parent in [tray,tray2]:move(o,MODEL)
# Place the whole native arrangement, once, preserving all peer dimensions.
def bounds(objects):
 vs=[world_to_camera_view(s,cam,o.matrix_world@Vector(v)) for o in objects if o.type in ['FONT','MESH','CURVE'] for v in o.bound_box]
 return [min(v.x for v in vs)*2360,min(1-v.y for v in vs)*2352,max(v.x for v in vs)*2360,max(1-v.y for v in vs)*2352]
cb.location.x=1.6
# Ignore not-yet-positioned pulse graphics while solving physical composition.
geometry=[o for g in [ca,cb,core0,core1,tray,tray2] for o in g.children]
for _ in range(7):
 bpy.context.view_layer.update();b=bounds(geometry);ROOT.scale*=1940/(b[2]-b[0]);bpy.context.view_layer.update();b=bounds(geometry)
 ROOT.location.y+=.1;bpy.context.view_layer.update();q=bounds(geometry);ROOT.location.y-=.1
 ROOT.location.y+=(2175-b[3])/((q[3]-b[3])/.1)
bpy.context.view_layer.update();print('MODEL_COMPOSITION',bounds(geometry),tuple(ROOT.location),tuple(ROOT.scale),flush=True)
# Dedicated HUD is anchored at the corrected y=590, 100 pixels below old result.
unit=(7*36/80)/2360
def px(x,y,z=-7):return Vector(((x-1180)*unit,(1176-y)*unit,z))
def height(o,h):
 bpy.context.view_layer.update();v=[p[1] for p in o.bound_box];o.data.size*=h*unit/(max(v)-min(v));bpy.context.view_layer.update()
def timing(value,x,mat):
 g=empty('Timing '+value);move(g,HUD);g.parent=cam;g.location=px(x,590)
 n=text('Timing digits '+value,value,1,mat,g,font_=heavy);u=text('Timing unit '+value,'ms',1,mat,g);move(n,HUD);move(u,HUD);height(n,138);height(u,55)
 nw=max(p[0] for p in n.bound_box)-min(p[0] for p in n.bound_box);uw=max(p[0] for p in u.bound_box)-min(p[0] for p in u.bound_box);gap=14*unit
 n.location.x=-(nw+uw+gap)/2+nw/2;u.location.x=(nw+uw+gap)/2-uw/2
 for o in [n,u]:
  yy=[p[1] for p in o.bound_box];o.location.y=-(min(yy)+max(yy))/2
 return g
left=timing('244.52',570,bpy.data.materials['Coral timing']);right=timing('44.19',1760,bpy.data.materials['Mint timing'])
# Load the exact approved clean arrow curve directly from the source library.
cream=ivory.copy();cream.name='Ivory clay arrow';cream.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=.44;cream.node_tree.nodes.get('Principled BSDF').inputs['Emission Strength'].default_value=0
arrow=arrow_template;HUD.objects.link(arrow);arrow.parent=cam;arrow.animation_data_clear();arrow.hide_render=False;arrow.hide_viewport=False;arrow.location=px(1180,590);arrow.scale=(.70,1,1)
arrow.data=arrow.data.copy();arrow.data.materials.clear();arrow.data.materials.append(bpy.data.materials['Ivory clay arrow'])
# Native syntax-colored excerpts from counters.hpp (using declarations omitted).
# Four reflowed rows retain the approved 105-unit Menlo font without tiny code.
menlo=bpy.data.fonts.load('/System/Library/Fonts/Menlo.ttc')
def emission(name,h):
 m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;n.clear();e=n.new('ShaderNodeEmission');e.inputs['Color'].default_value=(*lin(h),1);o=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(e.outputs[0],o.inputs[0]);return m
syntax={k:emission('Code '+k,h) for k,h in [('plain','FFF0D5'),('keyword','DCAEF1'),('type','84E3D4'),('number','F3C56B'),('change','7AF5C4')]}
def code_row(name,body,y):
 g=empty(name);move(g,HUD);g.parent=cam;g.location=px(225,y)
 o=text(name+' text',body,105*unit,syntax['plain'],g,font_=menlo);move(o,HUD);o.data.align_x='LEFT'
 roles=list(syntax)
 for role in roles[1:]:o.data.materials.append(syntax[role])
 for match in re.finditer(r'[A-Za-z_][A-Za-z_0-9]*|[0-9]+',body):
  token=match.group();role='keyword' if token in ['alignas','struct'] else 'type' if token in ['atomic','uint64_t','Counters'] else 'number' if token.isdigit() else 'plain'
  for index in range(match.start(),match.end()):o.data.body_format[index].material_index=roles.index(role)
 return g
code_header=code_row('Code struct header','struct Counters {',515)
code_a=code_row('Code counter a','  atomic<uint64_t> a{0};',622)
code_b=code_row('Code counter b','  atomic<uint64_t> b{0};',729)
code_footer=code_row('Code struct footer','};',836)
new_a=code_row('Code aligned a','  alignas(128) atomic<uint64_t> a{0};',622)
new_b=code_row('Code aligned b','  alignas(128) atomic<uint64_t> b{0};',729)
underlines=[]
for y in [639,746]:
 g=empty('Changed alignment underline');move(g,HUD);g.parent=cam;g.location=px(225+2*105*.46,y)
 o=path('Mint alignment underline',[(0,0,0),(12*105*.46*unit,0,0)],3*unit,syntax['change'],g);move(o,HUD);underlines.append(g)
ratio=text('Measured speedup','5.5× faster',1,bpy.data.materials['Mint timing'],cam,font_=heavy);move(ratio,HUD);height(ratio,100);ratio.location=px(1180,855)
yy=[v[1] for v in ratio.bound_box];ratio.location.y-=(min(yy)+max(yy))/2

PAD=577;LIFT=601;CROSS_START=621;CROSS_END=661;LAND=685;RESULT=721;END=1008
# Animation keys are authored on twos for tactile stop-motion timing, rendered at 24 fps.
def key(o,prop,value,f):setattr(o,prop,value);o.keyframe_insert(data_path=prop,frame=f)
def vis(o,on,f):key(o,'hide_render',not on,f);key(o,'hide_viewport',not on,f)
def smooth(t):t=max(0,min(1,t));return t*t*(3-2*t)
# One ordered request/ownership/transfer cycle per four seconds.
# Bubble lifetimes are independent of the current owner and scene boundaries.
writes=[[],[]];events=[]
for cycle in range(6):
 start=1+cycle*96;requester=1-cycle%2
 writes[requester].append(start+74)
 events.append({'requester':requester,'pulse_start':start,'pulse_arrival':start+24,'ownership_change':start+28,'transfer_start':start+36,'transfer_end':start+72,'write':start+74,'bubble_end':start+108})
for i in range(2):
 base=LAND+8*i
 for t in range(base+26,END+1,72):writes[i].append(t)
for f in range(1,END+1,2):
 moving=LIFT<=f<LAND;settled=f>=LAND
 if f<LIFT:bx=-1.6;bz=.30
 elif f<CROSS_START:bx=-1.6;bz=.30+1.20*smooth((f-LIFT)/20)
 elif f<CROSS_END:bx=-1.6+3.2*smooth((f-CROSS_START)/40);bz=1.50+.13*math.sin(math.pi*(f-CROSS_START)/40)
 elif f<LAND:bx=1.6;bz=.30+1.20*(1-smooth((f-CROSS_END)/24))
 else:bx=1.6;bz=.30
 dx=0;owner=0;requester=None;travel=[False,False];packet=[0,0]
 if f<PAD:
  cycle=(f-1)//96;phase=(f-1)%96;requester=1-cycle%2
  owner=requester if phase>=28 else 1-requester
  old_dx=0 if requester==1 else 5;new_dx=5-old_dx
  dx=old_dx+(new_dx-old_dx)*smooth((phase-36)/36)
  travel[requester]=phase<=24;packet[requester]=smooth(phase/24)
 elif settled:
  for i in range(2):
   base=LAND+8*i;phase=(f-base)%72
   travel[i]=f>=base and phase<=24;packet[i]=smooth(phase/24)
 counts=[sum(t<=f for t in times) for times in writes]
 ages=[f-max([t for t in times if t<=f],default=-1000) for times in writes]
 active=[0<=age<34 for age in ages]
 key(tray,'location',(-2.5+dx,-3.2,0),f)
 key(ca,'location',(-3.4+dx,-3.2,.30),f);key(cb,'location',(bx+dx,-3.2,bz),f)
 for i,g in enumerate([ca,cb]):
  press=1-.02*(1-smooth(ages[i]/8)) if 0<=ages[i]<8 else 1
  key(g,'scale',(.66,.66,.70*press),f)
 for o in [tray2]+list(tray2.children):vis(o,f>=PAD,f)
 pb.inputs['Base Color'].default_value=colors[owner];pb.inputs['Base Color'].keyframe_insert(data_path='default_value',frame=f)
 for node,part in owned_nodes:
  palette=['008F88','2558BE'] if part=='shell' else ['073E3F','132958'];node.inputs['Base Color'].default_value=(*lin(palette[owner]),1);node.inputs['Base Color'].keyframe_insert(data_path='default_value',frame=f)
 for i in range(2):
  start=Vector((-2.5 if i==0 else 2.5,.75,.84));end=Vector(((-3.4 if i==0 else bx)+dx,-2.27,1.06 if i==0 else bz+.76))
  for j,o in enumerate(paths[i]):
   key(o,'location',start.lerp(end,j/7),f);key(o,'rotation_euler',Vector((0,1,0)).rotation_difference((end-start).normalized()).to_euler(),f);vis(o,not moving,f)
  key(beads[i],'location',start.lerp(end,packet[i])+Vector((0,-.04,.04)),f);vis(beads[i],travel[i],f)
  u=max(0,min(1,ages[i]/34));bubble=increments[i]
  strength=.04+.12*(1-smooth(ages[i]/8)) if 0<=ages[i]<8 else .04
  face_nodes[i].inputs['Emission Strength'].default_value=strength;face_nodes[i].inputs['Emission Strength'].keyframe_insert(data_path='default_value',frame=f)
  key(bubble,'location',((-3.4 if i==0 else bx)+dx,-3.25,2.60+1.50*smooth(u)),f)
  envelope=min(1,.75+u*3)*(1-.15*smooth((u-.8)/.2));key(bubble,'scale',(envelope,)*3,f)
  for o in bubble.children:vis(o,active[i],f)
  for value,digit in enumerate(counter_digits[i]):
   vis(digit,value==counts[i],f);bump=1+.12*(1-smooth(ages[i]/8)) if 0<=ages[i]<8 else 1;key(digit,'scale',(bump,)*3,f)
 for row in [code_header,code_footer]:
  for o in row.children:vis(o,f<721,f)
 for old,new,y,start in [(code_a,new_a,622,601),(code_b,new_b,729,609)]:
  out=smooth((f-start)/8);incoming=smooth((f-start-9)/20)
  key(old,'location',px(225-38*out,y),f);key(old,'scale',(1,max(.01,1-out),1),f)
  key(new,'location',px(225+65*(1-incoming),y),f);key(new,'scale',(1,max(.01,incoming),1),f)
  for o in old.children:vis(o,f<start+9,f)
  for o in new.children:vis(o,start+9<=f<721,f)
 for g,start in zip(underlines,[615,623]):
  t=smooth((f-start)/12)*(1-smooth((f-677)/16));key(g,'scale',(max(.001,t),1,1),f)
  for o in g.children:vis(o,start<=f<695,f)
 vis(ratio,f>=745,f);t=smooth((f-745)/16);key(ratio,'scale',(.9+.1*t,)*3,f)
 for g in [left,right]:
  t=smooth((f-721)/20);key(g,'scale',(1,1,1) if f>=743 else (.92+.08*t,)*3,f)
  for o in g.children:vis(o,f>=721,f)
 vis(arrow,f>=721,f);key(arrow,'scale',(.70*smooth((f-721)/20),1,1),f)
# Set constant interpolation for authored clay holds, including material ownership.
for obj in list(s.objects)+[rim_mat.node_tree]+ownership_trees+face_trees:
 if obj.animation_data and obj.animation_data.action:
  action=obj.animation_data.action
  for layer in action.layers:
   for strip in layer.strips:
    for slot in action.slots:
     bag=strip.channelbag(slot)
     if bag:
      for fc in bag.fcurves:
       for k in fc.keyframe_points:k.interpolation='CONSTANT'
# Result arrow preserves topology; its small horizontal reveal is replaced by a local mask below.
arrow.animation_data_clear();arrow.scale=(.70,1,1)
for f in [1,721,1009]:vis(arrow,721<=f<1009,f)
m=arrow.data.materials[0].copy();m.name='Clean arrow • object-space reveal';arrow.data.materials[0]=m;n=m.node_tree.nodes;l=m.node_tree.links;out=next(v for v in n if v.type=='OUTPUT_MATERIAL');shader=out.inputs['Surface'].links[0].from_socket
coord=n.new('ShaderNodeTexCoord');sep=n.new('ShaderNodeSeparateXYZ');l.new(coord.outputs['Object'],sep.inputs[0]);mp=n.new('ShaderNodeMapRange');mp.inputs['From Min'].default_value=-209*unit;mp.inputs['From Max'].default_value=211*unit;l.new(sep.outputs['X'],mp.inputs[0]);val=n.new('ShaderNodeValue');val.name='Draw progress';mask=n.new('ShaderNodeMath');mask.operation='GREATER_THAN';l.new(mp.outputs['Result'],mask.inputs[0]);l.new(val.outputs[0],mask.inputs[1]);tr=n.new('ShaderNodeBsdfTransparent');mix=n.new('ShaderNodeMixShader');l.new(mask.outputs[0],mix.inputs[0]);l.new(shader,mix.inputs[1]);l.new(tr.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],out.inputs[0])
for f in range(1,1009):val.outputs[0].default_value=-.02+1.04*smooth((f-721)/20);val.outputs[0].keyframe_insert(data_path='default_value',frame=f)
s.render.engine='CYCLES';s.render.resolution_x=2360;s.render.resolution_y=2352;s.render.resolution_percentage=100;s.render.fps=24;s.render.fps_base=1;s.frame_start=1;s.frame_end=END;s.render.use_border=False;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.film_transparent=False;s.render.use_persistent_data=True
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.kernel_optimization_level='OFF';prefs.metalrt='OFF';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='METAL'
s.cycles.device='GPU';s.cycles.samples=96;s.cycles.adaptive_threshold=.012;s.cycles.filter_width=1;s.cycles.use_denoising=True
clips=[('01-crowded-opening',1,192),('02-shared-cache-line',193,384),('03-write-ownership',385,576),('04-add-padding',577,720),('05-benchmark-result',721,816),('06-discussion-hold',817,1008)]
for x in list(s.timeline_markers):s.timeline_markers.remove(x)
for name,start,end in clips:s.timeline_markers.new(name,frame=start)
manifest={'resolution':[2360,2352],'fps':24,'benchmark':{'packed_ms':'244.52','separated_ms':'44.19','spoken_ratio':'5.5','displayed_ratio':'5.5× faster','source':'benchmark-results.md, run 04'},'clips':[{'file':n+'.mp4','start':st,'end':en,'frames':en-st+1,'seconds':(en-st+1)/24} for n,st,en in clips],'source_script_sha256':hashlib.sha256((Path(a.source).parents[3]/'short-07-false-sharing/script.md').read_bytes()).hexdigest()}
(O/'scene-manifest.json').write_text(json.dumps(manifest,indent=2))
# State hashes include every visible transform, ownership color and arrow reveal.
seen={'model':{},'hud':{}};maps={'model':{},'hud':{}};bb={'model':[2360,2352,0,0],'hud':[2360,2352,0,0]}
for f in range(1,END+1):
 s.frame_set(f)
 for tag,coll in [('model',MODEL),('hud',HUD)]:
  state=[]
  for o in coll.objects:
   if o.type not in ['MESH','FONT','CURVE'] or o.hide_render:continue
   state.append((o.name,tuple(round(v,6) for row in o.matrix_world for v in row)))
   ob=bounds([o]);bb[tag]=[min(bb[tag][0],ob[0]),min(bb[tag][1],ob[1]),max(bb[tag][2],ob[2]),max(bb[tag][3],ob[3])]
  state.append(tuple(round(v,5) for v in pb.inputs['Base Color'].default_value) if tag=='model' else round(val.outputs[0].default_value,5))
  if tag=='model':state.append(tuple(round(n.inputs['Emission Strength'].default_value,5) for n in face_nodes))
  digest=hashlib.sha256(repr(state).encode()).hexdigest();maps[tag][f]=seen[tag].setdefault(digest,f)
assert bb['hud'][1]>440 and bb['model'][3]<2230,(bb)
assert bb['model'][0]>120 and bb['model'][2]<2240,bb
assert bb['hud'][3]<930 and bb['model'][1]>930,bb
report={'bounds':bb,'frame_maps':maps,'unique_states':{k:len(v) for k,v in seen.items()},'split_y':930,'native_geometry':True,'same_peer_meshes':True,'counter_a_address_fixed_relative_to_line':True,'schematic_pulses_not_measurements':True,'extra_foreground_clearance':100,'platform_composite_clearance':'not verified','motion_cadence':'authored on twos; no synthesized/interpolated render frames','revision':7,'pulse_travel_seconds':1.0,'increment_hold_seconds':34/24,'handoff_seconds':4.0,'contention_events':events,'write_events':writes,'activity_continues_through_result':True,'path_radius':.10,'worker_0_color':'#008F88','toon_outlines':False,'increment_font_size':.64,'increment_style':'rising clay bubble','visible_counter_values':'illustrative updates, not benchmark totals','whole_tray_ownership_color':True,'opening_handoff_motion':True,'code_font_size':105,'code_alignment_insertion':True,'code_struct_preserved':'Counters','displayed_speedup':'5.5× faster'}
(O/'scene-verification.json').write_text(json.dumps(report,indent=2));print('AUDIT',json.dumps({k:v for k,v in report.items() if k!='frame_maps'}),flush=True)
s['README']='Short 07 false sharing: six numbered independent clips. Native Retro Sunset studio clay. Timings 244.52 ms to 44.19 ms from matched run 04. Tray regions and counter sizes fixed; b crosses a boundary; schematic writes. No captions or narration. Scene manifest defines clip frame ranges.'
s.frame_set(1);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(O/'false-sharing-clay.blend'))
if a.preview:
 s.render.resolution_percentage=50;s.cycles.samples=32
 for f in [25,29,55,91,649,799]:
  s.frame_set(f);s.render.filepath=str(W/f'preview-{f}.png');bpy.ops.render.render(write_still=True);print('PREVIEW_DONE',f,flush=True)
