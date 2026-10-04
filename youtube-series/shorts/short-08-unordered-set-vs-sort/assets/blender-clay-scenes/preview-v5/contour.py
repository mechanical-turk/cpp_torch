"""Shared source-contour functions; initialized by build.py with its Blender context."""
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

