import bpy,json
from pathlib import Path
p=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(p.parent/'false-sharing-clay.blend'))
s=bpy.context.scene;s.frame_set(13)
print('CAMERA',s.camera.name,s.camera.data.sensor_fit,s.camera.data.lens)
for o in s.objects:
 if o.type=='LIGHT': print('LIGHT',o.name,o.data.energy,tuple(o.location))
for m in bpy.data.materials:
 if m.use_nodes and any(n.type=='BSDF_PRINCIPLED' for n in m.node_tree.nodes):
  print('MATERIAL',m.name)
print('MODELROOT',tuple(s.objects['Foreground • common placement'].scale))
