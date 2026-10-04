"""Native pose audit and exact-state render plan. No rendering."""
import bpy,json,hashlib,math
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
O=Path(__file__).resolve().parent;bpy.ops.wm.open_mainfile(filepath=str(O/'short-08-clay.blend'));s=bpy.context.scene;cam=s.camera
M=json.loads((O/'scene-manifest.json').read_text());maps={'model':{},'hud':{}};seen={'model':{},'hud':{}};violations=[];intersections=[];all_intersections=[];crops={'model':{},'hud':{}};extents={};model=bpy.data.collections['01 • Clay models'];hud=bpy.data.collections['02 • Code and results']
def bounds(o):
 vs=[world_to_camera_view(s,cam,o.matrix_world@Vector(v)) for v in o.bound_box]
 return [min(v.x for v in vs)*2160,min(1-v.y for v in vs)*2300,max(v.x for v in vs)*2160,max(1-v.y for v in vs)*2300]
def roundbox(b,padding):
 return [max(0,math.floor((b[0]-padding)/2)*2),max(0,math.floor((b[1]-padding)/2)*2),min(2160,math.ceil((b[2]+padding)/2)*2),min(2300,math.ceil((b[3]+padding)/2)*2)]
for f in range(1,s.frame_end+1,2):
 s.frame_set(f);bpy.context.view_layer.update()
 for tag,col in [('model',model),('hud',hud)]:
  state=[];total=[2160,2300,0,0]
  for o in sorted(col.all_objects,key=lambda o:o.name):
   if o.hide_render or o.type not in {'MESH','FONT','CURVE'}:continue
   state.append((o.name,tuple(round(v,6) for row in o.matrix_world for v in row),o.data.name,tuple(sl.material.name if sl.material else '' for sl in o.material_slots)))
   b=bounds(o);total=[min(total[0],b[0]),min(total[1],b[1]),max(total[2],b[2]),max(total[3],b[3])]
   if o.type=='FONT':
    guard=(180,480,1812,1180) if tag=='hud' else (120,440,1872,2260)
    if b[0]<guard[0]-.5 or b[1]<guard[1]-.5 or b[2]>guard[2]+.5 or b[3]>guard[3]+.5:violations.append({'frame':f,'object':o.name,'bounds':b,'guard':guard})
    extents.setdefault(o.name,[2160,2300,0,0]);v=extents[o.name];extents[o.name]=[min(v[0],b[0]),min(v[1],b[1]),max(v[2],b[2]),max(v[3],b[3])]
  digest=hashlib.sha256(repr(state).encode()).hexdigest();seen[tag].setdefault(digest,f);canonical=seen[tag][digest];maps[tag][str(f)]=canonical;maps[tag][str(f+1)]=canonical
  if str(canonical) not in crops[tag]:
   # Model crop spans full width, with a generous shadow margin above the highest geometry.
   crops[tag][str(canonical)]=[0,max(0,int((total[1]-240)//2)*2),2160,2300] if tag=='model' else roundbox(total,12) if state else None
 # Every visible value shell against every other visible value shell, in all scenes.
 visible_shells=[]
 for root in model.all_objects:
  if root.get('family')!='value tile' or root.hide_render:continue
  shell=next(c for c in root.children if c.name.endswith('shell'))
  vs=[shell.matrix_world@Vector(v) for v in shell.bound_box]
  visible_shells.append((root.name,[min(v[k] for v in vs) for k in range(3)],[max(v[k] for v in vs) for k in range(3)]))
 for i,(name,a0,a1) in enumerate(visible_shells):
  for other,b0,b1 in visible_shells[i+1:]:
   overlap=[min(a1[k],b1[k])-max(a0[k],b0[k]) for k in range(3)]
   if min(overlap)>.005:all_intersections.append({'frame':f,'objects':[name,other],'overlap':overlap})
# Same canonical shell and baseline dimensions throughout; value identity unchanged.
roots=[o for o in model.all_objects if o.get('family')=='value tile'];shells=[next(c for c in o.children if c.name.endswith('shell')) for o in roots]
assert len({o.data.as_pointer() for o in shells})==1
for f,expected in [(1,[]),(72,[]),(73,[]),(120,[3]),(168,[1,3]),(216,[1,3]),(264,[1,2,3]),(312,[1,2,3])]:
 s.frame_set(f)
 actual=sorted(s.objects[f'Hash node {i}']['value'] for i in range(3) if not s.objects[f'Hash node {i}'].hide_render)
 assert actual==expected,(f,actual,expected)
 assert [s.objects[f'Input {i}']['value'] for i in range(5)]==[3,1,3,2,1]
 assert all(not s.objects[f'Input {i}'].hide_render for i in range(5))
 assert sum(not o.hide_render for o in hud.all_objects if o.get('source_only'))==1
assert not any(o.name.startswith(('Bucket','Insertion query','Duplicate insertion')) for o in s.objects)
report={'violations':violations,'sort_aabb_intersections':intersections,'all_value_shell_intersections':all_intersections,'maps':maps,'crops':crops,'unique_states':{k:len(v) for k,v in seen.items()},'extents':extents,'shared_shells':len(shells),'input':[3,1,3,2,1],'retained':[1,2,3],'poses':s.frame_end//2,'source_sha256':hashlib.sha256((O/'short-08-clay.blend').read_bytes()).hexdigest()}
(O/'scene-verification.json').write_text(json.dumps(report,indent=2));print('AUDIT',json.dumps({'violations':len(violations),'first_violations':violations[:5],'all_value_shell_intersections':len(all_intersections),'first_all_intersections':all_intersections[:10],'sort_intersections':len(intersections),'first_intersections':intersections[:5],'unique_states':report['unique_states']}),flush=True)
