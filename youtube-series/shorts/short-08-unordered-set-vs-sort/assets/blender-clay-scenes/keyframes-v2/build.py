"""Short 08 revision 2: seven review stills only. No video render authorization."""
import bpy,math,json,re,hashlib
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
O=Path(__file__).resolve().parent
SRC=O.parents[3]/'short-07-false-sharing/assets/blender-clay-scenes/final-v9/false-sharing-final.blend'
bpy.ops.wm.open_mainfile(filepath=str(SRC));s=bpy.context.scene;s.frame_set(551)
W,H,FPS,END=2160,2300,24,7;cam=s.camera
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
# Value identity, not algorithm, controls each tile's color.
purple=clay('S08 raspberry clay','Deep teal worker clay','AE3D83')
darkpurple=clay('S08 raspberry recess','Deep teal worker clay','39162E')
neutral=clay('S08 plum tray clay','Cobalt clay cards','342447')
neutralface=clay('S08 plum tray recess','Deep teal worker clay','190F22')
COLORS={1:(teal,darkteal),2:(blue,darkblue),3:(purple,darkpurple)}
input_values=[3,1,3,2,1]
def value_tile(name,v):return tile(name,v,*COLORS[v])
def tray(name):
 g=empty(name);mesh(name+' shell','tray',g,neutral);fl=mesh(name+' floor','floor',g,neutralface);fl.location.z=.265;g.scale=(2.06,.64,.39);return g
inputtray=tray('Hash input tray');arraytray=tray('Single working vector v');flattray=tray('Future flat table')
inputs=[value_tile('Input '+str(i),v) for i,v in enumerate(input_values)]
array=[value_tile('Working '+str(i),v) for i,v in enumerate(input_values)]
nodes=[value_tile('Hash node '+str(i),v) for i,v in enumerate([1,2,3])]
flatvalues=[value_tile('Flat value '+str(i),v) for i,v in enumerate([3,1,2])]
request,request_text=value_tile('Duplicate insertion 1',1)
paths=[];pegs=[]
for i,v in enumerate([1,2,3]):
 g=empty('Bucket '+str(i));mesh('Bucket '+str(i)+' shell','shell',g,neutral);ins=mesh('Bucket '+str(i)+' inset','inset',g,neutralface);ins.location.z=.91;g.scale=(.24,.17,.17);pegs.append(g)
 pg=empty('Bucket path '+str(i));pills=[]
 for j in range(6):pills.append(mesh('Bucket path '+str(i)+' pill '+str(j),'dash',pg,COLORS[v][0]))
 paths.append((pg,pills))
# Native code and results. No titles, Big O badges, values/count labels or captions.
def ui(name,body,x,y,height=46,mat=None,face=bold):
 o=font(name,body,1,mat or syntax['plain'],cam,hud,face);bpy.context.view_layer.update();ys=[v[1] for v in o.bound_box];o.data.size*=height*unit/(max(ys)-min(ys));bpy.context.view_layer.update();xs=[v[0] for v in o.bound_box];ys=[v[1] for v in o.bound_box];o.location=px(x,y)-Vector(((min(xs)+max(xs))/2,(min(ys)+max(ys))/2,0));return o
old=['unordered_set<Number> distinct;','distinct.reserve(v.size());','for (auto value : v)','  distinct.insert(value);','return distinct.size();']
new=['sort(v.begin(), v.end());','auto end = unique(v.begin(), v.end());','return end - v.begin();']
codegroups=[]
for tag,rows in [('hash',old),('sort',new)]:
 objs=[]
 for i,body in enumerate(rows):
  o=font(tag+' code '+str(i),body,96*unit,syntax['plain'],cam,hud,menlo);o.data.offset=.0009
  for k in ['keyword','type','number','mint']:o.data.materials.append(syntax[k])
  for m in re.finditer(r'[A-Za-z_]\w*|\d+',body):
   token=m.group();idx=1 if token in ['auto','for','return'] else 2 if token in ['Number','unordered_set'] else 3 if token.isdigit() else 0
   for j in range(m.start(),m.end()):o.data.body_format[j].material_index=idx
  o.location=px(205,595+i*125);objs.append(o)
 codegroups.append(objs)
def line(name,width,mat):
 d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.bevel_depth=2.5*unit;d.bevel_resolution=3;sp=d.splines.new('POLY');sp.points.add(1);sp.points[0].co=(0,0,0,1);sp.points[1].co=(width*unit,0,0,1);d.materials.append(mat);o=bpy.data.objects.new(name,d);hud.objects.link(o);o.parent=cam;return o
insertline=line('Insert emphasis',1050,syntax['mint']);insertline.location=px(310,995)
sortline=line('Sort emphasis',610,syntax['mint']);sortline.location=px(205,620)
tease=ui('Early speedup','9.68× faster',990,740,133,syntax['mint'],heavy)
left=ui('Hash time','25.25',530,662,120,syntax['coral'],heavy);lu=ui('Hash unit','s',800,690,48,syntax['coral'])
right=ui('Sort time','2.61',1405,662,120,syntax['mint'],heavy);ru=ui('Sort unit','s',1625,690,48,syntax['mint'])
lt=ui('Measured hash method','unordered_set',600,800,43,syntax['plain']);rt=ui('Measured sort method','sort + unique',1450,800,43,syntax['plain']);ratio=ui('Measured ratio','9.68× faster',990,990,120,syntax['mint'],heavy)
d=bpy.data.curves.new('Clean benchmark arrow','CURVE');d.dimensions='2D';d.fill_mode='BOTH';d.extrude=2*unit;d.bevel_depth=6*unit;d.bevel_resolution=5;sp=d.splines.new('POLY');pts=[(-92,-12),(40,-12),(40,-39),(96,0),(40,39),(40,12),(-92,12)];sp.points.add(len(pts)-1)
for p,(x,y) in zip(sp.points,pts):p.co=(x*unit,y*unit,0,1)
sp.use_cyclic_u=True;d.materials.append(syntax['plain']);arrow=bpy.data.objects.new('Benchmark arrow',d);hud.objects.link(arrow);arrow.parent=cam;arrow.location=px(1030,662)
futurelabel=ui('Future table identity','flat hash table',980,1660,45,syntax['plain'])
# Visible empty tail recesses keep allocation distinct from the retained prefix.
tail=[]
for i in range(2):
 g=empty('Inactive tail slot '+str(i));o=mesh('Inactive tail slot '+str(i)+' inset','inset',g,neutralface);g.scale=(.46,.38,.43);o.location.z=.22;tail.append(g)
endbar=mesh('Retained range divider','dash',None,teal)
xs=[450,710,970,1230,1490];base=Vector((.46,.38,.43));node_x=[550,980,1410]
# Review poses, not an animation timeline. Exactly one pose for each intended scene.
for f in range(1,8):
 hashview=f<=3;sortview=f==4;result=f>=5;compare=f==6;future=f==7
 for g in [inputtray,arraytray,flattray]:visible(g,False,f)
 visible(inputtray,hashview,f);pose(inputtray,970,1420,f)
 for i,(g,t) in enumerate(inputs):visible(g,hashview,f);pose(g,xs[i],1380,f,z=.13,scale=base)
 for i,(g,t) in enumerate(nodes):visible(g,hashview or compare,f);pose(g,node_x[i],1870 if hashview else 1530,f,z=.04,scale=base)
 for i,g in enumerate(pegs):visible(g,hashview or compare,f);pose(g,node_x[i],1620 if hashview else 1320,f,z=.03,scale=(.24,.17,.17))
 for i,(g,pills) in enumerate(paths):
  visible(g,hashview or compare,f);a=world(node_x[i],1646 if hashview else 1346,.16);b=world(node_x[i],1805 if hashview else 1465,.16)
  for j,o in enumerate(pills):key(o,'location',a+(b-a)*((j+.5)/6),f);key(o,'scale',(.075,.16,.085),f)
 # Duplicate 1 has the same teal pigment and raised numeral as the stored 1.
 visible(request,f in [1,3],f);pose(request,node_x[0]+(60 if f==1 else 35),1670 if f==1 else 1810,f,z=.60,scale=base*.86)
 visible(arraytray,f>=4,f);ay=1720 if f in [4,5] else 1960;pose(arraytray,970,ay,f)
 sorted_slots={1:0,4:1,3:2,0:3,2:4};prefix_slots={1:0,3:1,0:2}
 for i,(g,t) in enumerate(array):
  on=f==4 or f>=5 and i in prefix_slots;visible(g,on,f)
  slot=sorted_slots[i] if f==4 else prefix_slots.get(i,4)
  pose(g,xs[slot],ay-45,f,z=.13,scale=base)
 for i,g in enumerate(tail):visible(g,f>=5,f);pose(g,xs[3+i],ay-45,f,z=.13,scale=base)
 visible(endbar,f>=5,f);pose(endbar,1100,ay-45,f,z=.25,scale=(.035,.55,.09))
 visible(flattray,future,f);pose(flattray,970,1530,f)
 for i,(g,t) in enumerate(flatvalues):visible(g,future,f);pose(g,[620,970,1320][i],1485,f,z=.13,scale=base)
 for o in codegroups[0]:visible(o,f in [1,3],f)
 for o in codegroups[1]:visible(o,sortview,f)
 visible(insertline,f==3,f);visible(sortline,sortview,f);visible(tease,f==2,f)
 for o in [left,lu,right,ru,lt,rt,ratio,arrow]:visible(o,result,f)
 visible(futurelabel,future,f)
# Every frame is a standalone review pose, no interpolation or video scheduling.
for action in bpy.data.actions:
 for layer in action.layers:
  for strip in layer.strips:
   for slot in action.slots:
    bag=strip.channelbag(slot)
    if bag:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:k.interpolation='CONSTANT'
for o in templates.values():bpy.data.objects.remove(o)
# Check actual glyph bounds in every delivered pose.
violations=[];bounds={}
for f in range(1,8):
 s.frame_set(f);bpy.context.view_layer.update()
 for o in s.objects:
  if o.type!='FONT' or o.hide_render:continue
  vv=[world_to_camera_view(s,cam,o.matrix_world@Vector(v)) for v in o.bound_box];b=[min(v.x for v in vv)*W,min(1-v.y for v in vv)*H,max(v.x for v in vv)*W,max(1-v.y for v in vv)*H]
  guard=(180,480,1812,1180) if 'code ' in o.name or o in [tease,left,lu,right,ru,lt,rt,ratio] else (120,440,1872,2260)
  bounds[f'{f}:{o.name}']=b
  if b[0]<guard[0] or b[1]<guard[1] or b[2]>guard[2] or b[3]>guard[3]:violations.append({'frame':f,'object':o.name,'bounds':b,'guard':guard})
manifest={'status':'stills_only_awaiting_creator_review','input':input_values,'sorted':[1,1,2,3,3],'retained':[1,2,3],'duplicates_removed':2,'palette':{'1':'teal','2':'cobalt','3':'raspberry'},'dimensions':[W,H],'frames':[{'frame':i,'file':name+'.png'} for i,name in enumerate(['01-opening','02-speedup-tease','03-duplicate-insertion','04-sort-before-unique','05-deduplicated-result','06-memory-layout','07-flat-table-next'],1)],'no_video_authorized':True,'benchmark_copy':'Prepared working vector v before this viewport; actual benchmark timing scope unchanged.'}
(O/'keyframes-manifest.json').write_text(json.dumps(manifest,indent=2));(O/'scene-verification.json').write_text(json.dumps({'violations':violations,'bounds':bounds},indent=2));assert not violations,violations
s.frame_set(1);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(O/'short-08-keyframes.blend'));print('SEVEN_REVIEW_POSES_READY',flush=True)
