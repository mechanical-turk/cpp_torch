"""Animate the creator-approved v3 native poses. Build/audit only; never render."""
import bpy,math,json,hashlib
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
O=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(O.parent/'keyframes-v3/short-08-keyframes.blend'))
s=bpy.context.scene;cam=s.camera;W,H,FPS=2160,2300,24
model=bpy.data.collections['01 • Clay models'];hud=bpy.data.collections['02 • Code and results']
objects=list(model.all_objects)+list(hud.all_objects)
poses={}
for p in range(1,8):
 s.frame_set(p);bpy.context.view_layer.update()
 poses[p]={o.name:(o.location.copy(),o.rotation_euler.copy(),o.scale.copy(),o.hide_render) for o in objects}
for o in objects:o.animation_data_clear()
for m in bpy.data.materials:
 if m.node_tree:m.node_tree.animation_data_clear()
unit=(7*cam.data.sensor_width/cam.data.lens)/W
base=Vector((.46,.38,.43));xs=[450,710,970,1230,1490]
node_x=[430,1010,1510];bucket_x=[610,970,1330]
inputs=[s.objects[f'Input {i}'] for i in range(5)]
nodes=[s.objects[f'Hash node {i}'] for i in range(3)]
array=[s.objects[f'Working {i}'] for i in range(5)]
pegs=[s.objects[f'Bucket {i}'] for i in range(3)]
paths=[[s.objects[f'Bucket path {i} pill {j}'] for j in range(10)] for i in range(3)]
request=s.objects['Duplicate insertion 1']
requests={1:request}
# Each query has the same linked shell/inset and value pigment as its stored key.
for value,index in [(2,1),(3,2)]:
 root=nodes[index].copy();root.name=f'Insertion query {value}';root.animation_data_clear();model.objects.link(root)
 for child in nodes[index].children:
  c=child.copy();c.name=f'Insertion query {value} {child.name.split()[-1]}';c.animation_data_clear();c.parent=root;model.objects.link(c)
 requests[value]=root
objects=list(model.all_objects)+list(hud.all_objects)
code_old=[s.objects[f'hash code {i}'] for i in range(5)]
code_new=[s.objects[f'sort code {i}'] for i in range(3)]
result_names=['Hash time','Hash unit','Sort time','Sort unit','Measured ratio','Benchmark arrow']
results=[s.objects[n] for n in result_names]
manifest={'width':W,'height':H,'fps':FPS,'poses_on_twos':True,'approved_reference':'../keyframes-v3','clips':[]}
start=1
for name,duration,purpose in [
 ('01-big-o-opening',3,'An existing duplicate follows a bucket pointer and checks a stored key.'),
 ('02-speedup-tease',3,'Hold the early measured speedup without revealing the replacement.'),
 ('03-hash-insertions',10,'Replay all five input requests: bucket selection, pointer following, new node or equality check.'),
 ('04-sort-and-compact',10,'Reveal direct v code, reorder in three weighted moves, then exclude two duplicates.'),
 ('05-benchmark-result',3,'Reveal 25.25 s -> 2.61 s and 9.68x, keeping the retained prefix.'),
 ('06-memory-layout',6,'Contrast one dependent node lookup with a sequential pass across adjacent values.'),
 ('07-flat-table-tease',3,'Clear old timings, retract pointers and seat keys in compact next-test storage.')]:
 n=duration*FPS;manifest['clips'].append({'file':name+'.mp4','start':start,'end':start+n-1,'frames':n,'seconds':duration,'purpose':purpose});start+=n
END=start-1;s.frame_start=1;s.frame_end=END;s.render.fps=FPS

def ease(t):t=max(0,min(1,t));return t*t*(3-2*t)
def progress(q,a,b):return ease((q-a)/(b-a))
def pulse(q,a,b):return math.sin(math.pi*max(0,min(1,(q-a)/(b-a))))**2 if a<=q<=b else 0

def world(x,y,z=0):
 ray=cam.matrix_world.to_quaternion()@Vector(((x-W/2)*unit,(H/2-y)*unit,-7))
 return cam.location+ray*((-cam.location.z)/ray.z)+Vector((0,0,z))
def show(o,on=True):
 for ob in [o]+list(o.children_recursive):ob.hide_render=not on

def place(o,x,y,z=0,scale=None,bank=0):
 o.location=world(x,y,z);o.rotation_euler=(0,bank,0)
 if scale is not None:o.scale=scale

def restore(p):
 for o in objects:
  if o.name in poses[p]:
   loc,rot,sc,hidden=poses[p][o.name];o.location=loc;o.rotation_euler=rot;o.scale=sc;o.hide_render=hidden
  else:o.hide_render=True
 for r in requests.values():show(r,False)

def press(o,amount):o.scale=(o.scale.x*(1+.055*amount),o.scale.y*(1+.025*amount),o.scale.z*(1-.13*amount))
def text_enter(o,t,dx=0):
 show(o,t>0);o.scale.y*=max(.001,t);o.location.x+=dx*(1-t)*unit

def path_pulse(i,t,on=True):
 # Thickened neighboring pills merge into a travelling clay bulge.
 for j,o in enumerate(paths[i]):
  u=(j+.5)/10;w=math.exp(-((u-t)/.15)**2) if on else 0
  o.scale=(.085+.075*w,.17+.115*w,.08+.065*w)

def query_motion(value,q,phase=0,duplicate=True):
 """Input press -> bucket press -> pointer pulse -> node allocation/equality check.
 Only a duplicate needs a second box; it grows in a vacant comparison position,
 never materializes on the stored key or inside the source/bucket geometry.
 """
 idx=value-1;r=requests[value];nx=node_x[idx];ny=[1950,2100,1930][idx]
 press(inputs[phase],pulse(q,0,8));press(pegs[idx],pulse(q,8,16))
 path_pulse(idx,progress(q,14,30),14<=q<=32)
 show(r,False)
 if duplicate:
  show(r,30<q<46)
  dx=255 if value==1 else -255
  size=progress(q,30,34)*(1-progress(q,42,46))
  place(r,nx+dx,ny,.04,base*max(.001,size))
  press(r,pulse(q,34,42));press(nodes[idx],pulse(q,34,42))
 else:
  show(nodes[idx],q>=30)
  if q>=30:
   nodes[idx].scale=base*max(.001,progress(q,30,38));press(nodes[idx],pulse(q,36,44))

def move_tile(o,a,b,q,start,end):
 t=max(0,min(1,(q-start)/(end-start)));h=progress(t,0,.25)*(1-progress(t,.75,1));u=progress(t,.25,.75)
 place(o,a+(b-a)*u,1675,.13+1.20*h,base,bank=.045*math.sin(math.pi*u))
 if t>=.85:press(o,pulse(t,.85,1))

semantic=[]
for clip_index,clip in enumerate(manifest['clips'],1):
 for f in range(clip['start'],clip['end']+1,2):
  q=f-clip['start'];restore(clip_index)
  if clip_index==1:
   # Opening starts in flight, matching the approved composition.
   r=requests[1];show(r,q<56);t=progress(q,0,30)
   place(r,565+120*t,1800+150*t,.90-.86*progress(q,22,32),base,bank=-.035*math.sin(math.pi*t))
   path_pulse(0,.45+.55*t,q<32);press(nodes[0],pulse(q,30,44));press(r,pulse(q,30,44))
   if q>=46:r.scale*=max(.02,1-progress(q,46,56))
  elif clip_index==2:
   o=s.objects['Early speedup'];text_enter(o,progress(q,0,14));o.scale*=1+.025*pulse(q,10,22)
   for i in range(3):path_pulse(i,0,False)
  elif clip_index==3:
   values=[3,1,3,2,1];event=min(4,q//48);local=q%48;done=values[:event];value=values[event]
   # The full illustrative multiset is preserved in the source tray.
   for i,node in enumerate(nodes):
    exists=(i+1) in done;show(node,exists)
    for p in paths[i]:p.hide_render=not (exists or value==i+1 and local>=12)
    path_pulse(i,0,False)
   query_motion(value,local,event,value in done)
   show(s.objects['Insert emphasis'],True)
  elif clip_index==4:
   # First expose the new code at the same origin, with a readable stagger.
   for i,o in enumerate(code_old):
    loc,rot,sc,_=poses[1][o.name];o.location=loc;o.rotation_euler=rot;o.scale=sc
    text_enter(o,1-progress(q,0,10),-10)
   for i,o in enumerate(code_new):text_enter(o,progress(q,10+i*4,24+i*4),12)
   # One working vector only, initially unsorted.
   show(s.objects['Single working vector v'],q>=12)
   for o in array:show(o,q>=12)
   slots={i:i for i in range(5)}
   moves=[(1,0,32,58),(4,1,68,104),(3,2,114,146)]
   order=[0,1,2,3,4]
   for index,target,a,b in moves:
    before=order.copy();src=before.index(index);after=before.copy();after.remove(index);after.insert(target,index)
    if q>=b:order=after;continue
    if q>=a:
     u=progress((q-a)/(b-a),.25,.75)
     for i,o in enumerate(array):
      if i==index:move_tile(o,xs[src],xs[target],q,a,b)
      else:place(o,xs[before.index(i)]+(xs[after.index(i)]-xs[before.index(i)])*u,1675,.13,base)
     break
    for i,o in enumerate(array):place(o,xs[order.index(i)],1675,.13,base)
    break
   else:
    for i,o in enumerate(array):place(o,xs[order.index(i)],1675,.13,base)
   # Separate unique phase; storage and identities remain explicit.
   show(s.objects['Sort emphasis'],24<=q<150)
   underline=s.objects['Insert emphasis'];show(underline,150<=q<228)
   underline.location=s.objects['sort code 1'].location+Vector((0,-25*unit,0));underline.scale.x=1.42
   for o in [array[1],array[4]]:press(o,pulse(q,150,160))
   if q>=158:
    array[4].scale*=max(.015,1-progress(q,158,170));show(array[4],q<168)
   if q>=170:move_tile(array[3],xs[2],xs[1],q,170,186)
   if q>=186:move_tile(array[0],xs[3],xs[2],q,186,202)
   if q>=202:
    press(array[0],pulse(q,202,212));press(array[2],pulse(q,202,212))
    array[2].scale*=max(.015,1-progress(q,210,220));show(array[2],q<218)
   for j in range(2):
    o=s.objects[f'Inactive tail slot {j}'];show(o,q>=202+18*j);place(o,xs[3+j],1675,.13,base)
   bar=s.objects['Retained range divider'];show(bar,q>=220);place(bar,1100,1675,.25,Vector((.035,.55,.09))*max(.02,progress(q,220,230)))
   semantic.append({'frame':f,'stage':'unique' if q>=150 else 'sort','values':[o['value'] for o in sorted([a for a in array if not a.hide_render],key=lambda a:a.location.x)]})
  elif clip_index==5:
   for i,o in enumerate(code_new):
    loc,rot,sc,_=poses[4][o.name];o.location=loc;o.rotation_euler=rot;o.scale=sc;text_enter(o,1-progress(q,0,12),-10)
   for name in ['Hash time','Hash unit','Sort time','Sort unit']:
    o=s.objects[name];text_enter(o,progress(q,12,26));o.scale*=1+.018*pulse(q,22,34)
   arrow=s.objects['Benchmark arrow'];t=progress(q,26,40);show(arrow,t>0);arrow.scale.x*=max(.001,t);arrow.location.x-=(1-t)*92*unit
   text_enter(s.objects['Measured ratio'],progress(q,40,54))
  elif clip_index==6:
   # Completed result holds while the comparison is assembled below it.
   t=progress(q,0,24);ay=1720+240*t
   place(s.objects['Single working vector v'],970,ay,scale=Vector((2.06,.64,.39)))
   for i,slot in {1:0,3:1,0:2}.items():place(array[i],xs[slot],ay-45,.13,base)
   for j in range(2):place(s.objects[f'Inactive tail slot {j}'],xs[3+j],ay-45,.13,base)
   place(s.objects['Retained range divider'],1100,ay-45,.25,Vector((.035,.55,.09)))
   t=progress(q,12,30)
   roots=[s.objects['Contiguous bucket pointer rail']]+nodes+pegs
   for o in roots:o.scale*=max(.001,t);show(o,t>0)
   for i in range(3):
    for p in paths[i]:p.scale*=max(.001,t);show(p,t>0)
   press(pegs[0],pulse(q,34,44));path_pulse(0,progress(q,44,72),44<=q<=74);press(nodes[0],pulse(q,74,86))
   for i,a in enumerate([array[1],array[3],array[0]]):press(a,pulse(q,94+i*10,110+i*10))
  elif clip_index==7:
   # Start from the comparison, clear the old measured numbers, then preview the next layout.
   t=progress(q,52,70);ay=1960-260*t
   place(s.objects['Single working vector v'],970,ay,scale=Vector((2.06,.64,.39)))
   for i,slot in {1:0,3:1,0:2}.items():place(array[i],xs[slot],ay-45,.13,base)
   for j in range(2):place(s.objects[f'Inactive tail slot {j}'],xs[3+j],ay-45,.13,base)
   place(s.objects['Retained range divider'],1100,ay-45,.25,Vector((.035,.55,.09)))
   for o in results:
    loc,rot,sc,_=poses[6][o.name];o.location=loc;o.rotation_euler=rot;o.scale=sc;text_enter(o,1-progress(q,0,12))
   for name in ['Contiguous bucket pointer rail']+[f'Bucket {i}' for i in range(3)]:
    o=s.objects[name];loc,rot,sc,_=poses[6][name];o.location=loc;o.rotation_euler=rot;o.scale=sc*max(.001,1-progress(q,8,24));show(o,q<24)
   for i in range(3):
    for j,o in enumerate(paths[i]):
     loc,rot,sc,_=poses[6][o.name];o.location=loc;o.rotation_euler=rot;o.scale=sc*max(.001,1-progress(q,8+j,20+j));show(o,q<20+j)
   tray=s.objects['Future flat table'];tray.scale*=max(.001,progress(q,18,34));show(tray,q>=18)
   for i,n in enumerate(nodes):
    show(n,q<66);a=poses[6][n.name][0];target=world([970,1320,620][i],1005,.13)
    begin,end=(20,44) if i==2 else (40,64)
    u=progress(q,begin,end);n.location=a+(target-a)*u;n.location.z+=.80*math.sin(math.pi*u);n.scale=base;n.rotation_euler=(0,.04*math.sin(math.pi*u),0)
    press(n,pulse(q,end-4,end+2))
   for i in range(3):show(s.objects[f'Flat value {i}'],q>=66)
  # Bake every actual authored pose; hold each for two native frames.
  for o in objects:
   for prop in ['location','rotation_euler','scale','hide_render']:o.keyframe_insert(data_path=prop,frame=f)
for action in bpy.data.actions:
 for layer in action.layers:
  for strip in layer.strips:
   for slot in action.slots:
    bag=strip.channelbag(slot)
    if bag:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:k.interpolation='CONSTANT'
allowed={'1','2','3','25.25','2.61','s','9.68× faster','unordered_set<Number> distinct;','distinct.reserve(v.size());','for (auto value : v)','  distinct.insert(value);','return distinct.size();','sort(v.begin(), v.end());','auto end = unique(v.begin(), v.end());','return end - v.begin();'}
assert all(o.data.body in allowed for o in objects if o.type=='FONT')
s.frame_set(1);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(O/'short-08-clay.blend'))
(O/'scene-manifest.json').write_text(json.dumps(manifest,indent=2));(O/'semantic-poses.json').write_text(json.dumps(semantic,indent=2));print('ANIMATION_BUILT',END,'frames',flush=True)
