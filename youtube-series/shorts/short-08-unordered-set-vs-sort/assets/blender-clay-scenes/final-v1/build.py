"""Short 08: native sculpted-clay sequence. Builds editable source; never renders."""
import bpy,math,json,re,hashlib
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
O=Path(__file__).resolve().parent
SRC=O.parents[3]/'short-07-false-sharing/assets/blender-clay-scenes/final-v9/false-sharing-final.blend'
bpy.ops.wm.open_mainfile(filepath=str(SRC));s=bpy.context.scene;s.frame_set(551)
W,H,FPS,END=2160,2300,24,720;cam=s.camera
model=bpy.data.collections['01 • Clay models'];hud=bpy.data.collections['02 • Code and results']
# Preserve actual native templates before removing the previous episode.
templates={k:s.objects[n].copy() for k,n in [('shell','Counter a • shell'),('inset','Counter a • inset'),('tray','Tray • shell'),('floor','Tray • recessed floor'),('dash','Worker 0 dash 0')]}
for o in templates.values():o.data=o.data.copy();o.animation_data_clear();o.parent=None
for o in list(model.all_objects)+list(hud.all_objects):
 if o.name in bpy.data.objects:bpy.data.objects.remove(o,do_unlink=True)
for o in s.objects:o.animation_data_clear()
for m in bpy.data.materials:
 if m.node_tree:m.node_tree.animation_data_clear()
for coll in list(model.children):bpy.data.collections.remove(coll)
s.render.resolution_x=W;s.render.resolution_y=H;s.render.resolution_percentage=100
s.render.fps=FPS;s.frame_start=1;s.frame_end=END;s.render.film_transparent=False
s.render.use_border=False;s.render.use_crop_to_border=False;s.render.use_persistent_data=False
s.render.use_motion_blur=False;cam.data.dof.use_dof=False
s.cycles.samples=96;s.cycles.adaptive_threshold=.007;s.cycles.seed=0;s.cycles.use_animated_seed=False;s.cycles.use_denoising=True
unit=(7*cam.data.sensor_width/cam.data.lens)/W

def linear(h):
 v=[int(h[i:i+2],16)/255 for i in (0,2,4)];return tuple(x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in v)
def clay(name,source,h):
 m=bpy.data.materials[source].copy();m.name=name
 for n in m.node_tree.nodes:
  if n.type=='BSDF_PRINCIPLED':n.inputs['Base Color'].default_value=(*linear(h),1)
  if n.name=='Clay pigment variation':
   rgb=linear(h);n.color_ramp.elements[0].color=tuple(x*.82 for x in rgb)+(1,);n.color_ramp.elements[1].color=tuple(min(1,x*1.13+.001) for x in rgb)+(1,)
 return m
teal=clay('S08 teal sculpted clay','Deep teal worker clay','008F88')
blue=clay('S08 cobalt sculpted clay','Cobalt clay cards','2558BE')
darkteal=clay('S08 deep teal face','Deep teal worker clay','073E3F')
darkblue=clay('S08 deep cobalt face','Cobalt clay cards','132958')
ivory=bpy.data.materials['Ivory raised clay letters']
muted=clay('S08 outside logical end','Deep teal worker clay','244D50')
def emission(name,h):
 m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;n.clear();e=n.new('ShaderNodeEmission');e.inputs['Color'].default_value=(*linear(h),1);out=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(e.outputs[0],out.inputs['Surface']);return m
syntax={k:emission('S08 '+k,h) for k,h in [('plain','FFF8EB'),('keyword','EDC7FF'),('type','B8F2EB'),('number','FFE0A3'),('mint','7AF5C4'),('coral','FF8D6C')]}
menlo=next(f for f in bpy.data.fonts if 'Menlo' in f.name)
heavy=next(f for f in bpy.data.fonts if 'Arial Black' in f.name)
bold=next(f for f in bpy.data.fonts if 'Arial Bold' in f.name)
def empty(name,coll=model,parent=None):
 o=bpy.data.objects.new(name,None);coll.objects.link(o);o.parent=parent;return o
def mesh(name,template,parent,mat):
 o=templates[template].copy();o.name=name;model.objects.link(o);o.parent=parent;o.location=(0,0,0);o.rotation_euler=(0,0,0);o.scale=(1,1,1);o.hide_render=False;o.hide_viewport=False
 if len(o.material_slots)==0:o.data.materials.append(mat)
 o.material_slots[0].link='OBJECT';o.material_slots[0].material=mat
 return o
def font(name,body,size,mat,parent=None,coll=model,face=bold,physical=False):
 d=bpy.data.curves.new(name,'FONT');d.body=body;d.font=face;d.size=size;d.resolution_u=16
 if physical:d.extrude=.009;d.bevel_depth=.005;d.bevel_resolution=4
 d.materials.append(mat);o=bpy.data.objects.new(name,d);coll.objects.link(o);o.parent=parent;return o
def px(x,y):return Vector(((x-W/2)*unit,(H/2-y)*unit,-7))
def world(x,y,z=0):
 ray=cam.matrix_world.to_quaternion()@px(x,y);return cam.location+ray*((z-cam.location.z)/ray.z)
def key(o,prop,v,f):setattr(o,prop,v);o.keyframe_insert(data_path=prop,frame=f)
def smooth(t):t=max(0,min(1,t));return t*t*(3-2*t)
def mix(a,b,t):return a+(b-a)*t
def group_objects(g):return [g]+list(g.children_recursive)
def visible(g,on,f):
 for o in group_objects(g):key(o,'hide_render',not on,f)
def pose(g,x,y,f,z=0,scale=None,bank=0):
 key(g,'location',world(x,y,0)+Vector((0,0,z)),f);key(g,'rotation_euler',(0,bank,0),f)
 if scale:key(g,'scale',scale,f)
def tile(name,value,material=teal,face=darkteal):
 g=empty(name);shell=mesh(name+' shell','shell',g,material);inset=mesh(name+' inset','inset',g,face);inset.location.z=.91
 t=font(name+' numeral',str(value),1.25,ivory,g,physical=True);t.data.align_x='CENTER';t.location=(0,-.38,.955)
 g.scale=(.46,.38,.43);g['value']=value;g['family']='value tile';return g,t
source=[];copy=[]
for i,v in enumerate([3,1,3,4,2]):
 source.append(tile(f'Input {i}',v));copy.append(tile(f'Copy {i}',v))
nodes=[]
for i,v in enumerate([3,1,4,2]):nodes.append(tile(f'Hash node {i}',v,blue,darkblue))
def tray(name,mat,face):
 g=empty(name);sh=mesh(name+' shell','tray',g,mat);fl=mesh(name+' floor','floor',g,face);fl.location.z=.265;g.scale=(2.06,.64,.39);g['family']='five slot tray';return g
inputtray=tray('Original input tray',teal,darkteal);copytray=tray('Copied array tray',teal,darkteal)
flat=tray('Flat hash preview tray',blue,darkblue)
# Reuse sculpted counter forms for bucket pegs, with one shared baseline.
pegs=[]
for i in range(4):
 g=empty(f'Bucket {i}');mesh(f'Bucket {i} shell','shell',g,blue);ins=mesh(f'Bucket {i} inset','inset',g,darkblue);ins.location.z=.91;g.scale=(.23,.17,.17);pegs.append(g)
# Real native clay paths: pinched dash master plus overlapping travelling lobes.
paths=[]
for i in range(4):
 g=empty(f'Bucket link {i}');pills=[]
 for j in range(6):pills.append(mesh(f'Link {i} pill {j}','dash',g,blue))
 paths.append((g,pills))
mb=bpy.data.metaballs.new('Substantial travelling clay packet');mb.resolution=.06;mb.render_resolution=.045;mb.threshold=.6;mb.materials.append(blue)
packet=bpy.data.objects.new('Clay pulse',mb);model.objects.link(packet)
for j in range(5):mb.elements.new().stiffness=2
# A second clay value shows the attempted insertion without consuming input.
request,requestnum=tile('Insertion attempt',2,blue,darkblue)
duplicate,dupnum=tile('Duplicate attempt',3,blue,darkblue)
# Compact unlit technical labels use native glyphs and travel with the model view.
def ui(name,body,x,y,height=46,mat=None,face=bold):
 o=font(name,body,1,mat or syntax['plain'],cam,hud,face)
 bpy.context.view_layer.update();ys=[v[1] for v in o.bound_box];o.data.size*=height*unit/(max(ys)-min(ys));bpy.context.view_layer.update()
 xs=[v[0] for v in o.bound_box];ys=[v[1] for v in o.bound_box];o.location=px(x,y)-Vector(((min(xs)+max(xs))/2,(min(ys)+max(ys))/2,0));o['anchor']=[x,y];return o
inputlabel=ui('Input label','values',985,1218,44,syntax['type'])
hashlabel=ui('Hash label','std::unordered_set',980,2138,46,syntax['type'])
arraylabel=ui('Array label','sort + unique',980,2138,46,syntax['type'])
flatlabel=ui('Next test label','flat hash table',980,1430,46,syntax['type'])
expected=ui('Expected complexity','Expected O(n)',990,1106,51,syntax['type'])
logn=ui('Sort complexity','O(n log n)',990,1106,51,syntax['type'])
count3=ui('Three distinct','3 distinct',1560,2140,40,syntax['plain'],heavy);count4=ui('Four distinct','4 distinct',1560,2140,40,syntax['plain'],heavy)
countlabel=ui('Count label','distinct',1660,2138,31,syntax['type'])
endlabel=ui('Logical end label','end',1412,2080,43,syntax['mint'])
# Narrow clay divider at the logical end, never a deletion of allocated slots.
endmarker=mesh('Logical end divider','dash',None,teal)
# Exact code viewports, short identifiers preserve required meaningful work.
old=['unordered_set<Number> distinct;','distinct.reserve(values.size());','for (auto value : values)','  distinct.insert(value);','return distinct.size();']
new=['auto s = values;','sort(s.begin(), s.end());','auto end = unique(s.begin(), s.end());','return end - s.begin();']
codegroups=[]
for tag,rows in [('hash',old),('sort',new)]:
 objs=[]
 for i,body in enumerate(rows):
  o=font(tag+' code '+str(i),body,96*unit,syntax['plain'],cam,hud,menlo);o.data.offset=.0009
  for k in ['keyword','type','number','mint']:o.data.materials.append(syntax[k])
  for m in re.finditer(r'[A-Za-z_]\w*|\d+',body):
   token=m.group();idx=1 if token in ['auto','for','return'] else 2 if token in ['Number','unordered_set'] else 3 if token.isdigit() else 0
   for j in range(m.start(),m.end()):o.data.body_format[j].material_index=idx
  o.location=px(205,575+i*115);o['base_y']=575+i*115;objs.append(o)
 codegroups.append(objs)
def line(name,width,mat):
 d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.bevel_depth=2.5*unit;d.bevel_resolution=3;sp=d.splines.new('POLY');sp.points.add(1);sp.points[0].co=(0,0,0,1);sp.points[1].co=(width*unit,0,0,1);d.materials.append(mat);o=bpy.data.objects.new(name,d);hud.objects.link(o);o.parent=cam;return o
underline=line('Focused code underline',760,syntax['mint'])
tease=ui('Early numerical tease','9.68× faster',990,760,133,syntax['mint'],heavy)
left=ui('Hash measured seconds','25.25',530,662,120,syntax['coral'],heavy);lu=ui('Hash unit','s',800,690,48,syntax['coral'])
right=ui('Sort measured seconds','2.61',1405,662,120,syntax['mint'],heavy);ru=ui('Sort unit','s',1625,690,48,syntax['mint'])
lt=ui('Result original method','unordered_set',600,800,43,syntax['plain']);rt=ui('Result new method','sort + unique',1450,800,43,syntax['plain'])
ratio=ui('Measured speedup','9.68× faster',990,990,120,syntax['mint'],heavy)
d=bpy.data.curves.new('Continuous rounded result arrow','CURVE');d.dimensions='2D';d.fill_mode='BOTH';d.extrude=2*unit;d.bevel_depth=6*unit;d.bevel_resolution=5;sp=d.splines.new('POLY');pts=[(-92,-12),(40,-12),(40,-39),(96,0),(40,39),(40,12),(-92,12)];sp.points.add(len(pts)-1)
for p,(x,y) in zip(sp.points,pts):p.co=(x*unit,y*unit,0,1)
sp.use_cyclic_u=True;d.materials.append(syntax['plain']);arrow=bpy.data.objects.new('Benchmark arrow',d);hud.objects.link(arrow);arrow.parent=cam;arrow.location=px(1030,662)
# Local coordinate reveal, same robust construction as the approved reference.
mat=syntax['plain'].copy();mat.name='S08 arrow draw';d.materials[0]=mat;n=mat.node_tree.nodes;l=mat.node_tree.links;out=next(x for x in n if x.type=='OUTPUT_MATERIAL');base=out.inputs['Surface'].links[0].from_socket;tc=n.new('ShaderNodeTexCoord');sep=n.new('ShaderNodeSeparateXYZ');l.new(tc.outputs['Object'],sep.inputs[0]);progress=n.new('ShaderNodeValue');progress.name='Draw progress';cmp=n.new('ShaderNodeMath');cmp.operation='GREATER_THAN';l.new(sep.outputs['X'],cmp.inputs[0]);l.new(progress.outputs[0],cmp.inputs[1]);tr=n.new('ShaderNodeBsdfTransparent');ms=n.new('ShaderNodeMixShader');l.new(cmp.outputs[0],ms.inputs[0]);l.new(base,ms.inputs[1]);l.new(tr.outputs[0],ms.inputs[2]);l.new(ms.outputs[0],out.inputs['Surface'])
clips=[('01-big-o-opening',1,72),('02-speedup-tease',73,120),('03-hash-insertions',121,288),('04-sort-and-compact',289,408),('05-benchmark-result',409,480),('06-memory-layout',481,648),('07-flat-table-tease',649,720)]
for marker in list(s.timeline_markers):s.timeline_markers.remove(marker)
for name,a,b in clips:s.timeline_markers.new(name,frame=a)
xs=[450,710,970,1230,1490];node_x=[440,755,1070,1385]
base_scale=Vector((.46,.38,.43))
# Sorting: values [3,1,3,4,2] -> [1,2,3,3,4], followed by unique -> [1,2,3,4,_].
# Deliberately illustrative placement, never claimed as the libc++ sort trace.
sort_target=[2,0,3,4,1]
def hudplace(o,x,y,f):
 anchor=o['anchor'];delta=px(x,y)-px(anchor[0],anchor[1]);base=o.get('base_location')
 if base is None:o['base_location']=list(o.location);base=o['base_location']
 key(o,'location',Vector(base)+delta,f)
def press(age,duration=10):return .08*math.sin(math.pi*age/duration) if 0<=age<=duration else 0
for f in range(1,END+1,2):
 hashview=f<289;sorting=289<=f<409;result=f>=409;compare=f>=481;flatphase=f>=649
 # Input remains unchanged until memory comparison replaces the complete view.
 visible(inputtray,f<481,f);pose(inputtray,970,1400,f)
 visible(inputlabel,f<481,f)
 for i,(g,t) in enumerate(source):visible(g,f<481,f);pose(g,xs[i],1365,f,z=.13,scale=base_scale)
 visible(copytray,f>=305,f);pose(copytray,970,1960 if not compare else 1920,f)
 # Native copied values emerge above their originals, travel, then reorder.
 for i,(g,t) in enumerate(copy):
  on=f>=313;visible(g,on,f);x=xs[i];y=1365;z=.13;bank=0
  if f>=305:
   u=smooth((f-313)/16);y=mix(1670,1915,u);z=.13+.18*(1-u)+.30*math.sin(math.pi*u)
  if f>=329:
   u1=smooth((f-333)/8);u2=smooth((f-351)/12);y=1915
   x=[mix(mix(xs[0],xs[1],u1),xs[2],u2),mix(xs[1],xs[0],u1),mix(xs[2],xs[3],u2),mix(xs[3],xs[4],u2),mix(xs[4],xs[1],u2)][i]
   lift=(smooth((f-329)/4)*(1-smooth((f-341)/4))) if i==1 else (smooth((f-347)/4)*(1-smooth((f-363)/6))) if i==4 else 0
   z=.13+.90*lift;bank=.025*math.sin(2*math.pi*(u1 if i==1 else u2)) if i in [1,4] else 0
  if f>=371:
   x=xs[sort_target[i]];y=1915;z=.13
   if i==3:x=mix(xs[4],xs[3],smooth((f-387)/18))
   if i==2:
    # The overwritten duplicate is no longer a live tile in the valid prefix.
    visible(g,f<387,f)
  if compare:y=1875
  age=f-369;compress=press(age)
  if i==2 and 373<=f<387:compress=.97*smooth((f-373)/12)
  pose(g,x,y,f,z,tuple(base_scale*Vector((1+compress/2,1+compress/2,1-compress))),bank)
 # Tail slot stays allocated but loses its value; no guaranteed tail contents.
 visible(endmarker,f>=407,f);pose(endmarker,1410,1915 if not compare else 1875,f,z=.25,scale=(.035,.55,.09))
 visible(endlabel,f>=407,f);hudplace(endlabel,1410,2070 if not compare else 2030,f)
 # Hash model: separate nodes, compact layout in the explanatory comparison.
 nodesy=1850 if not compare else 1560;bucket_y=1610 if not compare else 1345
 retract=smooth((f-659)/34) if flatphase else 0
 for i,g in enumerate(pegs):visible(g,hashview or compare and retract<1,f);pose(g,node_x[i],bucket_y,f,z=.03,scale=(.23*(1-retract),.17*(1-retract),.17*(1-retract)))
 for i,(g,t) in enumerate(nodes):
  on=(hashview and (i<3 or f>=163)) or compare;visible(g,on,f)
  y=nodesy;x=node_x[i];z=.04
  if flatphase:x=mix(x,[530,820,1110,1400][i],retract);y=mix(y,1530,retract);z+=.45*math.sin(math.pi*retract)
  age=f-163 if i==3 else f-231 if i==0 else -100
  pr=press(age);pose(g,x,y,f,z,tuple(base_scale*Vector((1+pr/2,1+pr/2,1-pr))))
 visible(flat,flatphase,f);pose(flat,970,1580,f,scale=(2.06*retract,.64*retract,.39*retract))
 # Packet routes are short, high contrast, with local pills merging into its body.
 pulse_on=False;which=3;t=0
 if f<=120:pulse_on=True;which=3;t=.4*smooth((f-1)/72)
 elif 121<=f<=163:pulse_on=True;which=3;t=.4+.6*smooth((f-121)/42)
 elif 189<=f<=231:pulse_on=True;which=0;t=smooth((f-189)/42)
 elif 501<=f<=557:pulse_on=True;which=1;t=smooth((f-501)/56)
 for i,(g,pills) in enumerate(paths):
  visible(g,hashview or compare and not flatphase,f)
  a=world(node_x[i],bucket_y+26,.16);b=world(node_x[i],nodesy-65,.16);vec=b-a
  for j,o in enumerate(pills):
   u=(j+.5)/6;v=a+vec*u;dist=abs(u-t) if pulse_on and i==which else 9
   swell=1+.55*max(0,1-dist/.28);consume=max(.05,min(1,(dist-.07)/.10)) if dist<.17 else 1
   key(o,'location',v,f);key(o,'scale',(.07*swell*consume,.16*swell*consume,.085*swell*consume),f)
 visible(packet,pulse_on,f)
 if pulse_on:
  a=world(node_x[which],bucket_y+26,.16);b=world(node_x[which],nodesy-65,.16);v=a+(b-a)*t
  for j,e in enumerate(mb.elements):
   e.co=v+Vector((0,(j-2)*.12,0));e.radius=.20*(1-.12*abs(j-2));e.keyframe_insert(data_path='co',frame=f);e.keyframe_insert(data_path='radius',frame=f)
 visible(request,f<163,f);pose(request,node_x[3],mix(bucket_y,nodesy,t if which==3 else 1),f,z=.52,scale=base_scale*.8)
 visible(duplicate,189<=f<243,f);pose(duplicate,node_x[0]+80*(1-smooth((f-223)/20)),mix(bucket_y,nodesy,smooth((f-189)/42)),f,z=.55,scale=base_scale*.8)
 # A short contact sequence traces adjacent array cells; it is not another sort.
 if 573<=f<=633:
  for i in [1,4,0,3]:
   slot={1:0,4:1,0:2,3:3}[i];pr=press(f-(573+slot*14),12);g=copy[i][0];key(g,'scale',tuple(base_scale*Vector((1+pr/2,1+pr/2,1-pr))),f)
 # Code choreography: no semantic edit can occur invisibly.
 for kind,rows in enumerate(codegroups):
  for i,o in enumerate(rows):
   on=(f<73 or 121<=f<289) if kind==0 else 289<=f<409
   scale=1;dx=0
   if kind==0 and 289<=f<299+i*2:on=True;u=smooth((f-289-i*2)/10);scale=max(.001,1-u);dx=-15*u
   if kind==1:u=smooth((f-291-i*4)/14);scale=max(.001,u);dx=12*(1-u)
   key(o,'hide_render',not on,f);key(o,'location',px(205+dx,o['base_y']),f);key(o,'scale',(1,scale,1),f)
 visible(expected,hashview and not 73<=f<121,f);visible(logn,309<=f<409,f)
 visible(tease,73<=f<121,f)
 if 73<=f<121:
  u=smooth((f-73)/10);hudplace(tease,990,760-22*(1-u),f)
 visible(underline,121<=f<271 or 303<=f<407,f)
 row=3 if f<289 else 0 if f<329 else 1 if f<371 else 2
 key(underline,'location',px(205+(120 if row==3 and f<289 else 0),599+row*115),f)
 key(underline,'scale',(.73 if row==0 else .86 if row==1 else 1,1,1),f)
 visible(inputlabel,f<481,f);visible(hashlabel,hashview or compare and not flatphase,f);hudplace(hashlabel,930,2140 if not compare else 1715,f)
 visible(arraylabel,f>=305,f);hudplace(arraylabel,920,2160 if not compare else 2130,f)
 visible(flatlabel,flatphase,f);hudplace(flatlabel,930,1715,f)
 visible(count3,hashview and f<163,f);visible(count4,hashview and f>=163 or f>=407,f);visible(countlabel,False,f)
 hudplace(count4,1560,2160 if not compare else 2160,f);hudplace(countlabel,1650,2140 if not compare else 2180,f)
 for o in [left,lu,right,ru,lt,rt]:visible(o,result,f)
 visible(arrow,f>=415,f);progress.outputs[0].default_value=mix(-105,108,smooth((f-415)/12))*unit;progress.outputs[0].keyframe_insert(data_path='default_value',frame=f)
 visible(ratio,f>=433,f)
# Discrete hand-authored poses on twos. No accidental Bezier interpolation.
for action in bpy.data.actions:
 for layer in action.layers:
  for strip in layer.strips:
   for slot in action.slots:
    bag=strip.channelbag(slot)
    if bag:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:k.interpolation='CONSTANT'
# Remove detached templates; shared mesh data remains on the canonical copies.
for o in templates.values():bpy.data.objects.remove(o)
s.frame_set(1);bpy.context.view_layer.update()
# Record exact project benchmark and episode-specific semantic invariants.
manifest={'resolution':[W,H],'fps':FPS,'frames':END,'native_reference':str(SRC),'aesthetic':'Approved hand-sculpted Retro Sunset clay, Short 07 final-v9','input':[3,1,3,4,2],'sorted':[1,2,3,3,4],'unique_prefix':[1,2,3,4],'original_unchanged':True,'benchmark':{'hash_ms':25248.86446,'sort_ms':2608.428625,'ratio':9.679722196,'n':100000000,'duplicate_percent':1},'clips':[{'file':n+'.mp4','start':a,'end':b,'frames':b-a+1,'seconds':(b-a+1)/FPS} for n,a,b in clips]}
(O/'scene-manifest.json').write_text(json.dumps(manifest,indent=2))
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(O/'short-08-clay.blend'))
print('BUILD_COMPLETE',flush=True)
