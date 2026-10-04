"""Bucket-well redesign. Preserve approved sorting/code; build only, never render."""
import bpy, math, json
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
O=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(O.parent/'final-v2/short-08-clay.blend'))
s=bpy.context.scene; cam=s.camera; W,H=2160,2300
model=bpy.data.collections['01 • Clay models']; hud=bpy.data.collections['02 • Code and results']
unit=(7*cam.data.sensor_width/cam.data.lens)/W
base=Vector((.46,.38,.43)); bx=[480,970,1460]; xs=[450,710,970,1230,1490]
inputs=[s.objects[f'Input {i}'] for i in range(5)]
nodes=[s.objects[f'Hash node {i}'] for i in range(3)]
array=[s.objects[f'Working {i}'] for i in range(5)]
queries={1:s.objects['Duplicate insertion 1'],2:s.objects['Insertion query 2'],3:s.objects['Insertion query 3']}
manifest=json.loads((O.parent/'final-v2/scene-manifest.json').read_text())
manifest.update(preview_width=216,preview_height=230,preview_percentage=10,
                status='tiny_motion_review_only',full_render_authorized=False,
                hash_model='Three separate schematic bucket wells; deterministic destination by key identity, no ropes.')
manifest['clips'][0]['purpose']='Active input outlined; duplicate compares above its occupied bucket and squashes away.'
manifest['clips'][2]['purpose']='Five attempts in source order: select input, select bucket, land new key or reject equal duplicate.'
manifest['clips'][5]['purpose']='Separate bucket-owned node allocations versus a sequential adjacent array scan.'
manifest['clips'][6]['purpose']='Old buckets disappear before a compact, unmeasured flat-table layout appears.'

# Delete rejected visual grammar, including the purposeless cyan end edge.
for o in list(model.all_objects):
 if o.name.startswith(('Bucket ', 'Contiguous bucket pointer rail')) or o.name=='Retained range divider':
  bpy.data.objects.remove(o,do_unlink=True)

def clone_assembly(src,name):
 root=src.copy();root.name=name;root.animation_data_clear();model.objects.link(root)
 for c in src.children:
  n=c.copy();n.name=name+' '+c.name.split()[-1];n.animation_data_clear();n.parent=root;model.objects.link(n)
 return root
wells=[clone_assembly(s.objects['Hash input tray'],f'Bucket well {i}') for i in range(3)]

def outline(name):
 d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.bevel_depth=8*unit;d.bevel_resolution=3
 # 200px canonical rounded rectangle. Transform follows projected object bounds.
 sp=d.splines.new('POLY');pts=[]
 for x,y,a in [(82,82,0),(-82,82,90),(-82,-82,180),(82,-82,270)]:
  for j in range(9):
   t=math.radians(a+j*90/8);pts.append(((x+18*math.cos(t))*unit,(y+18*math.sin(t))*unit,0,1))
 sp.points.add(len(pts)-1)
 for p,v in zip(sp.points,pts):p.co=v
 sp.use_cyclic_u=True;d.materials.append(bpy.data.materials['S08 plain'])
 o=bpy.data.objects.new(name,d);hud.objects.link(o);o.parent=cam;return o
active=outline('Active input white outline');target=outline('Selected bucket white outline')
changed=[*wells,*nodes,*queries.values(),*inputs,active,target]
changed += [s.objects['Future flat table']]+[s.objects[f'Flat value {i}'] for i in range(3)]
# Capture inherited poses before replacing their keys, preserving the approved array.
saved={}
for f in range(1,s.frame_end+1,2):
 s.frame_set(f)
 saved[f]={o.name:(o.location.copy(),o.rotation_euler.copy(),o.scale.copy(),o.hide_render) for r in changed for o in [r]+list(r.children_recursive)}
for r in changed:
 for o in [r]+list(r.children_recursive):o.animation_data_clear()

def ease(t):t=max(0,min(1,t));return t*t*(3-2*t)
def u(q,a,b):return ease((q-a)/(b-a))
def pulse(q,a,b):return math.sin(math.pi*max(0,min(1,(q-a)/(b-a))))**2 if a<=q<=b else 0
def world(x,y,z=0):
 ray=cam.matrix_world.to_quaternion()@Vector(((x-W/2)*unit,(H/2-y)*unit,-7))
 return cam.location+ray*(-cam.location.z/ray.z)+Vector((0,0,z))
def show(r,on=True):
 for o in [r]+list(r.children_recursive):o.hide_render=not on
def place(r,x,y,z=0,scale=base):
 r.location=world(x,y,z);r.rotation_euler=(0,0,0);r.scale=scale
def press(r,p):r.scale=Vector((r.scale.x*(1+.045*p),r.scale.y*(1+.025*p),r.scale.z*(1-.12*p)))
def frame_outline(o,root,pad=13):
 bpy.context.view_layer.update()
 shell=next(c for c in root.children if c.name.endswith('shell'))
 vv=[world_to_camera_view(s,cam,shell.matrix_world@Vector(v)) for v in shell.bound_box]
 x0=min(v.x for v in vv)*W-pad;x1=max(v.x for v in vv)*W+pad
 y0=min(1-v.y for v in vv)*H-pad;y1=max(1-v.y for v in vv)*H+pad
 o.location=Vector((((x0+x1)/2-W/2)*unit,(H/2-(y0+y1)/2)*unit,-7))
 o.scale=((x1-x0)/200,(y1-y0)/200,1);show(o)

def attempt(q,value,index,duplicate,well_y=1960):
 """Source remains intact. One airborne query lands OR compares above a key.
 New node becomes visible only after query disappears: no coincident shells.
 """
 k=value-1;r=queries[value];frame_outline(active,inputs[index]);press(inputs[index],pulse(q,0,8))
 if q>=8:frame_outline(target,wells[k],8)
 press(wells[k],pulse(q,8,16))
 show(r,4<=q<44)
 # Clear source row, then travel horizontally above the destination.
 t=u(q,8,22);y=1620+100*t;x=xs[index]+(bx[k]-xs[index])*t
 size=max(.001,u(q,2,8));z=.12
 if not duplicate:
  land=u(q,24,36);y+=(well_y-45-y)*land
  size*=1+.055*pulse(q,34,40);show(r,4<=q<38)
  show(nodes[k],q>=38)
  if q>=38:press(nodes[k],pulse(q,36,44))
 else:
  # Keep the two boxes vertically separate through comparison and squash-out.
  size*=max(.001,1-u(q,34,44));press(nodes[k],pulse(q,24,34))
 place(r,x,y,z,base*size);press(r,pulse(q,24 if duplicate else 34,34 if duplicate else 40))
 r.rotation_euler.y=.06*math.sin(math.pi*t)

events=[]
for ci,c in enumerate(manifest['clips'],1):
 for f in range(c['start'],c['end']+1,2):
  s.frame_set(f);q=f-c['start']
  for r in changed:
   for o in [r]+list(r.children_recursive):
    loc,rot,sc,h=saved[f][o.name];o.location=loc;o.rotation_euler=rot;o.scale=sc;o.hide_render=h
  show(active,False);show(target,False)
  for r in queries.values():show(r,False)
  for i,(well,node) in enumerate(zip(wells,nodes)):
   show(well,ci in [1,2,3,6,7]);show(node,ci in [1,2,6,7])
   wy=1960 if ci<=3 else 1450
   place(well,bx[i],wy,scale=Vector((.63,.63,.37)))
   place(node,bx[i],wy-45,.13)
  if ci==1:
   # A clear, slower duplicate beat instead of a travelling rope/pointer.
   attempt(q*.65,1,4,True)
  elif ci==2:
   pass
  elif ci==3:
   values=[3,1,3,2,1];ev=min(4,q//48);local=q%48;value=values[ev];prior=values[:ev]
   for i,node in enumerate(nodes):show(node,i+1 in prior)
   attempt(local,value,ev,value in prior)
   events.append({'frame':f,'source_index':ev,'value':value,'duplicate':value in prior})
  elif ci==4:
   # Follow the actual moving/compared input, not an arbitrary bounce cue.
   selection=None
   for index,a,b in [(1,32,58),(4,68,104),(3,114,146)]:
    if a-8<=q<=b+4:selection=array[index]
   if 150<=q<168:selection=array[4]
   elif 170<=q<186:selection=array[3]
   elif 186<=q<204:selection=array[0]
   elif 204<=q<218:selection=array[2]
   if selection is not None and not selection.hide_render:frame_outline(active,selection)
  elif ci==6:
   t=u(q,12,30)
   for well,node in zip(wells,nodes):
    well.scale*=max(.001,t);node.scale*=max(.001,t);show(well,t>0);show(node,t>0)
   if 34<=q<60:frame_outline(target,wells[0],8)
   if 60<=q<86:frame_outline(active,nodes[0]);press(nodes[0],pulse(q,62,80))
   for i,index in enumerate([1,3,0]):
    if 94+i*14<=q<108+i*14:frame_outline(active,array[index])
  elif ci==7:
   t=1-u(q,8,26)
   for well,node in zip(wells,nodes):
    well.scale*=max(.001,t);node.scale*=max(.001,t);show(well,q<26);show(node,q<26)
   tray=s.objects['Future flat table'];show(tray,q>=32);tray.scale=Vector((2.06,.64,.39))*max(.001,u(q,32,42))
   for i in range(3):
    r=s.objects[f'Flat value {i}'];show(r,q>=42+i*6);r.scale=base*max(.001,u(q,42+i*6,52+i*6))
  for r in changed:
   for o in [r]+list(r.children_recursive):
    for prop in ['location','rotation_euler','scale','hide_render']:o.keyframe_insert(data_path=prop,frame=f)
for action in bpy.data.actions:
 for layer in action.layers:
  for strip in layer.strips:
   for slot in action.slots:
    bag=strip.channelbag(slot)
    if bag:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:k.interpolation='CONSTANT'
s.render.resolution_percentage=10;s.frame_set(1)
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(O/'short-08-clay.blend'))
(O/'scene-manifest.json').write_text(json.dumps(manifest,indent=2))
(O/'hash-events.json').write_text(json.dumps(events,indent=2))
print('TINY_PREVIEW_SCENE_BUILT',flush=True)
