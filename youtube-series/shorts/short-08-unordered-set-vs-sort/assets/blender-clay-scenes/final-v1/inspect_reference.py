import bpy,json
from pathlib import Path
O=Path(__file__).resolve().parent
src=O.parents[3]/'short-07-false-sharing/assets/blender-clay-scenes/final-v9/false-sharing-final.blend'
bpy.ops.wm.open_mainfile(filepath=str(src));s=bpy.context.scene;s.frame_set(551)
r={}
for o in s.objects:
 if o.type in {'CAMERA','LIGHT'} or o.name in ['Foreground • common placement','Counter a','Core 0','Cache line 0','Continuous clay studio ground'] or o.parent and o.parent.name in ['Counter a','Core 0','Cache line 0']:
  if ' • value ' in o.name and not o.name.endswith(' 6'):continue
  r[o.name]={'type':o.type,'parent':o.parent.name if o.parent else None,'location':list(o.location),'rotation':list(o.rotation_euler),'scale':list(o.scale),'dimensions':list(o.dimensions),'materials':[m.name if m else None for m in o.data.materials] if o.type in {'MESH','FONT','CURVE'} else [],'hidden':o.hide_render,'body':o.data.body if o.type=='FONT' else None}
(O/'_render/reference-objects.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
