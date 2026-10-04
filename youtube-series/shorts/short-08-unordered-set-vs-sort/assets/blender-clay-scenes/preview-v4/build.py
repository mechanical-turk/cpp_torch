"""Replace selection frames with thin source-only projected clay contours."""
import bpy,json,hashlib
from pathlib import Path
from mathutils import Vector
O=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(O.parent/'preview-v3/short-08-clay.blend'))
s=bpy.context.scene;cam=s.camera;hud=bpy.data.collections['02 • Code and results']
unit=(7*cam.data.sensor_width/cam.data.lens)/2160
for name in ['Active input white outline','Selected bucket white outline']:
 bpy.data.objects.remove(s.objects[name],do_unlink=True)
M=json.loads((O.parent/'preview-v3/scene-manifest.json').read_text())
M.update(highlight='Thin contour of selected source shell only; no destination highlight.',changed_clips=[1,3,4,6])
M['clips'][2]['purpose']='Source-only contour follows five attempts; new-key landing or duplicate rejection.'
cache={};geometry={};selection=[]

def hull(points):
 pts=sorted(set(points))
 def cross(o,a,b):return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
 lo=[];hi=[]
 for p in pts:
  while len(lo)>=2 and cross(lo[-2],lo[-1],p)<=0:lo.pop()
  lo.append(p)
 for p in reversed(pts):
  while len(hi)>=2 and cross(hi[-2],hi[-1],p)<=0:hi.pop()
  hi.append(p)
 return lo[:-1]+hi[:-1]

def contour(root,f):
 shell=next(c for c in root.children if c.name.endswith('shell'))
 key=shell.data.name
 if key not in geometry:
  evaluated=shell.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=evaluated.to_mesh()
  geometry[key]=[v.co.copy() for v in mesh.vertices];evaluated.to_mesh_clear()
 # Project the actual rounded sculpted shell, not its bounding box. No padding.
 mat=cam.matrix_world.inverted()@shell.matrix_world;pts=[]
 for v in geometry[key]:
  p=mat@v;k=-7/p.z;pts.append((round(p.x*k,7),round(p.y*k,7)))
 boundary=hull(pts);digest=hashlib.sha256(repr(boundary).encode()).hexdigest()
 if digest not in cache:
  d=bpy.data.curves.new('Source contour '+digest[:10],'CURVE');d.dimensions='3D'
  d.bevel_depth=5*unit;d.bevel_resolution=3
  sp=d.splines.new('POLY');sp.points.add(len(boundary)-1)
  for p,(x,y) in zip(sp.points,boundary):p.co=(x,y,0,1)
  sp.use_cyclic_u=True;d.materials.append(bpy.data.materials['S08 plain'])
  o=bpy.data.objects.new(d.name,d);hud.objects.link(o);o.parent=cam;o.location=(0,0,-7)
  o['source_only']=True;o['stroke_native_pixels']=10
  o.hide_render=True;o.keyframe_insert(data_path='hide_render',frame=1)
  cache[digest]=o
 o=cache[digest];o.hide_render=False;o.keyframe_insert(data_path='hide_render',frame=f)
 o.hide_render=True;o.keyframe_insert(data_path='hide_render',frame=f+2)
 selection.append({'frame':f,'source':root.name,'contour':o.name})

for ci,c in enumerate(M['clips'],1):
 for f in range(c['start'],c['end']+1,2):
  s.frame_set(f);bpy.context.view_layer.update();q=f-c['start'];root=None
  if ci==1:root=s.objects['Input 4']
  elif ci==3:root=s.objects[f'Input {min(4,q//48)}']
  elif ci==4:
   for index,a,b in [(1,32,58),(4,68,104),(3,114,146)]:
    if a-8<=q<=b+4:root=s.objects[f'Working {index}']
   if 150<=q<168:root=s.objects['Working 4']
   elif 170<=q<186:root=s.objects['Working 3']
   elif 186<=q<204:root=s.objects['Working 0']
   elif 204<=q<218:root=s.objects['Working 2']
  elif ci==6:
   for i,index in enumerate([1,3,0]):
    if 94+i*14<=q<108+i*14:root=s.objects[f'Working {index}']
  if root is not None and not root.hide_render:contour(root,f)
for action in bpy.data.actions:
 for layer in action.layers:
  for strip in layer.strips:
   for slot in action.slots:
    bag=strip.channelbag(slot)
    if bag:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:k.interpolation='CONSTANT'
for f in range(1,s.frame_end+1,2):
 s.frame_set(f)
 assert sum(not o.hide_render for o in cache.values())<=1
assert all(v['source'].startswith(('Input ','Working ')) for v in selection)
s.frame_set(1);s.render.resolution_percentage=10
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(O/'short-08-clay.blend'))
(O/'scene-manifest.json').write_text(json.dumps(M,indent=2))
(O/'highlight-verification.json').write_text(json.dumps({'source_only':True,'destination_highlights':0,'max_simultaneous_highlights':1,'padding_pixels':0,'stroke_native_pixels':10,'selections':selection},indent=2))
print('SOURCE_CONTOURS_BUILT',len(cache),flush=True)
