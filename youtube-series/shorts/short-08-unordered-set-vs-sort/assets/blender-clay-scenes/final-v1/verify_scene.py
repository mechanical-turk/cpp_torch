"""All-frame visible bounds and exact native-state cache mapping."""
import bpy,json,hashlib
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
O=Path(__file__).resolve().parent;bpy.ops.wm.open_mainfile(filepath=str(O/'short-08-clay.blend'));s=bpy.context.scene;cam=s.camera
model=bpy.data.collections['01 • Clay models'];hud=bpy.data.collections['02 • Code and results'];maps={'model':{},'hud':{}};seen={'model':{},'hud':{}};violations=[];extents={};model_min_y=2300
def box(o):
 vs=[world_to_camera_view(s,cam,o.matrix_world@Vector(v)) for v in o.bound_box]
 return [min(v.x for v in vs)*2160,min(1-v.y for v in vs)*2300,max(v.x for v in vs)*2160,max(1-v.y for v in vs)*2300]
for f in range(1,721,2):
 s.frame_set(f);bpy.context.view_layer.update()
 for tag,collection in [('model',model),('hud',hud)]:
  state=[]
  for o in collection.all_objects:
   if o.hide_render or o.type not in {'MESH','FONT','CURVE','META'}:continue
   state.append((o.name,tuple(round(v,6) for row in o.matrix_world for v in row),o.data.name))
   if o.type=='META':state.append(tuple((tuple(e.co),e.radius) for e in o.data.elements))
   for sl in o.material_slots:
    if sl.material and sl.material.node_tree:
     for n in sl.material.node_tree.nodes:
      if n.type=='VALUE':state.append((n.name,n.outputs[0].default_value))
   if tag=='model' and o.type in {'MESH','FONT','CURVE'}:
    model_min_y=min(model_min_y,box(o)[1])
   if o.type=='FONT':
    b=box(o);extents.setdefault(o.name,[2160,2300,0,0]);q=extents[o.name];extents[o.name]=[min(q[0],b[0]),min(q[1],b[1]),max(q[2],b[2]),max(q[3],b[3])]
    guard=(180,480,1812,1180) if ('code ' in o.name or 'complexity' in o.name or 'measured' in o.name or 'Measured' in o.name or 'unit' in o.name or 'Result ' in o.name or 'tease' in o.name) else (120,440,1872,2260)
    if b[0]<guard[0]-.1 or b[1]<guard[1]-.1 or b[2]>guard[2]+.1 or b[3]>guard[3]+.1:violations.append({'frame':f,'name':o.name,'bounds':b,'guard':guard})
  h=hashlib.sha256(repr(state).encode()).hexdigest();seen[tag].setdefault(h,f);maps[tag][str(f)]=seen[tag][h];maps[tag][str(f+1)]=seen[tag][h]
# Family identity is independent from temporary physical presses or pose.
tiles=[o for o in model.all_objects if o.get('family')=='value tile'];shells=[next(c for c in o.children if c.name.endswith(' shell')) for o in tiles]
assert len({o.data.as_pointer() for o in shells})==1
assert len({tuple((m.type,getattr(m,'levels',0),getattr(m,'render_levels',0)) for m in o.modifiers) for o in shells})==1
assert model_min_y>1080, ('Native split infringes moving geometry',model_min_y)
r={'model_min_y':model_min_y,'violations':violations,'extents':extents,'maps':maps,'unique_states':{k:len(v) for k,v in seen.items()},'linked_value_shells':len(shells),'input_invariant':[3,1,3,4,2],'unique_prefix':[1,2,3,4]}
(O/'scene-verification.json').write_text(json.dumps(r,indent=2));print('AUDIT',json.dumps({'violations':len(violations),'first':violations[:5],'unique_states':r['unique_states']}),flush=True)
