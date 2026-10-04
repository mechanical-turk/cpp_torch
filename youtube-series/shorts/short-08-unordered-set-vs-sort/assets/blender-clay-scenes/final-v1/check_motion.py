import bpy,json
from pathlib import Path
from mathutils import Vector
O=Path(__file__).resolve().parent;bpy.ops.wm.open_mainfile(filepath=str(O/'short-08-clay.blend'));s=bpy.context.scene
issues=[];details=[]
for f in range(329,372,2):
 s.frame_set(f);bpy.context.view_layer.update();boxes=[]
 for i in range(5):
  o=s.objects[f'Copy {i} shell'];v=[o.matrix_world@Vector(p) for p in o.bound_box]
  boxes.append(([min(p[k] for p in v) for k in range(3)],[max(p[k] for p in v) for k in range(3)]))
 for i in range(5):
  for j in range(i+1,5):
   a,b=boxes[i],boxes[j];over=[min(a[1][k],b[1][k])-max(a[0][k],b[0][k]) for k in range(3)]
   if min(over)>.035:issues.append({'frame':f,'tiles':[i,j],'aabb_overlap':over})
# Check original input transforms, identities and peer baselines throughout.
base=None
for f in range(1,481,2):
 s.frame_set(f);bpy.context.view_layer.update();state=[(s.objects[f'Input {i}']['value'],tuple(round(v,6) for row in s.objects[f'Input {i}'].matrix_world for v in row)) for i in range(5)]
 if base is None:base=state
 assert state==base,'Original input changed'
for f in [407,481,719]:
 s.frame_set(f);bpy.context.view_layer.update();visible=[s.objects[f'Copy {i}'] for i in range(5) if not s.objects[f'Copy {i}'].hide_render]
 assert [o['value'] for o in sorted(visible,key=lambda o:o.location.x)]==[1,2,3,4]
assert all(s.objects[f'Hash node {i}']['value']==v for i,v in enumerate([3,1,4,2]))
r={'sort_aabb_intersections':issues,'original_input_preserved':True,'unique_prefix_verified':True,'method':'Conservative world-space shell AABBs; nonzero intersections need inspection'}
(O/'motion-verification.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
