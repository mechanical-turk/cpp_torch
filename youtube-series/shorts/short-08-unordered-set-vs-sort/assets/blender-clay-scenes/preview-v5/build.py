"""Two-scene comprehension test: intact input, then visibly build a logical set."""
import bpy,json,math,hashlib
from pathlib import Path
from mathutils import Vector
O=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(O.parent/'preview-v3/short-08-clay.blend'))
s=bpy.context.scene;s.frame_set(1);cam=s.camera
model=bpy.data.collections['01 • Clay models'];hud=bpy.data.collections['02 • Code and results']
unit=(7*cam.data.sensor_width/cam.data.lens)/2160;base=Vector((.46,.38,.43))
inputs=[s.objects[f'Input {i}'] for i in range(5)]
nodes=[s.objects[f'Hash node {i}'] for i in range(3)]
tray=s.objects['Hash input tray'];code=[s.objects[f'hash code {i}'] for i in range(5)]
keep={o for root in [tray,*inputs,*nodes,*code] for o in [root]+list(root.children_recursive)}
for o in list(model.all_objects)+list(hud.all_objects):
 if o not in keep:bpy.data.objects.remove(o,do_unlink=True)
for o in keep:o.animation_data_clear();o.hide_render=False
for m in bpy.data.materials:
 if m.node_tree:m.node_tree.animation_data_clear()
def world(x,y,z=0):
 ray=cam.matrix_world.to_quaternion()@Vector(((x-1080)*unit,(1150-y)*unit,-7))
 return cam.location+ray*(-cam.location.z/ray.z)+Vector((0,0,z))
positions={3:(600,1850),1:(1320,1900),2:(930,2080)}
for value,n in enumerate(nodes,1):
 n.location=world(*positions[value],.13);n.rotation_euler=(0,0,0);n.scale=base
for i,r in enumerate(inputs):r.location=world([450,710,970,1230,1490][i],1380,.13);r.scale=base;r.rotation_euler=(0,0,0)
def show(root,on):
 for o in [root]+list(root.children_recursive):o.hide_render=not on
def ease(q,a,b):t=max(0,min(1,(q-a)/(b-a)));return t*t*(3-2*t)
def pulse(q,a,b):return math.sin(math.pi*max(0,min(1,(q-a)/(b-a))))**2 if a<=q<=b else 0
M={'width':2160,'height':2300,'preview_width':216,'preview_height':230,'preview_percentage':10,'fps':24,'poses_on_twos':True,'full_render_authorized':False,'status':'two_scene_comprehension_test','clips':[
 {'file':'01-input-opening.mp4','start':1,'end':72,'frames':72,'seconds':3,'purpose':'Original code and intact input only; first source outlined.'},
 {'file':'02-build-the-set.mp4','start':73,'end':312,'frames':240,'seconds':10,'purpose':'Five source attempts in order; stored key counts 1,2,2,3,3.'}]}
s.frame_start=1;s.frame_end=312;s.render.fps=24;s.render.resolution_percentage=10
cache={};geometry={};selection=[]
exec(compile((O/'contour.py').read_text(),str(O/'contour.py'),'exec'))
semantics=[];values=[3,1,3,2,1]
for ci,c in enumerate(M['clips'],1):
 for f in range(c['start'],c['end']+1,2):
  s.frame_set(f);q=f-c['start'];index=0 if ci==1 else min(4,q//48);local=q%48
  previous=set(values[:index]) if ci==2 else set();value=values[index]
  for v,node in enumerate(nodes,1):
   node.scale=base;node.rotation_euler=(0,0,0);show(node,ci==2 and v in previous)
  if ci==2:
   node=nodes[value-1]
   if value not in previous:
    show(node,local>=10)
    grow=ease(local,10,26);compression=.16*pulse(local,24,38)
    node.scale=base*max(.001,grow)
    node.scale.x*=1+.055*pulse(local,24,38);node.scale.z*=1-compression
   else:
    # Equality recognition: existing key presses and settles; no second box.
    press=pulse(local,14,36);node.scale=Vector((base.x*(1+.08*press),base.y*(1+.04*press),base.z*(1-.23*press)))
  for root in nodes:
   for o in [root]+list(root.children_recursive):
    for prop in ['location','rotation_euler','scale','hide_render']:o.keyframe_insert(data_path=prop,frame=f)
  bpy.context.view_layer.update();contour(inputs[index],f)
  semantics.append({'frame':f,'source_index':index,'source_value':value,'stored':sorted(n['value'] for n in nodes if not n.hide_render),'duplicate':ci==2 and value in previous})
for action in bpy.data.actions:
 for layer in action.layers:
  for strip in layer.strips:
   for slot in action.slots:
    bag=strip.channelbag(slot)
    if bag:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:k.interpolation='CONSTANT'
for f in range(1,313,2):
 s.frame_set(f);assert sum(not o.hide_render for o in cache.values())==1
s.frame_set(1);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(O/'short-08-clay.blend'))
(O/'scene-manifest.json').write_text(json.dumps(M,indent=2))
(O/'semantic-poses.json').write_text(json.dumps(semantics,indent=2))
print('TWO_SCENE_TEST_BUILT',flush=True)
