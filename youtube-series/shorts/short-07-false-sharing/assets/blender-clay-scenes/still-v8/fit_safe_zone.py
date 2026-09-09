"""Revise native code only; retain the approved 2160x2300 model pixels.

Render the top 1080 rows of the existing 2420-high native camera, then use
compose_safe_zone.py to replace that region and apply the approved 60px crop.
The 1080x1920 reference is doubled on the 2160x3840 destination master.
"""
import bpy, json
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

OUT = Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(OUT/'short-07-clay-study.blend'))
s = bpy.context.scene
cam = s.camera
W, H = 2160, 2420
unit = (7*cam.data.sensor_width/cam.data.lens)/W
texts = sorted(bpy.data.collections['02 • Code and results'].objects, key=lambda o:o.name)
assert len(texts) == 4
for i, o in enumerate(texts):
    o.data.size = 150*unit
    o.location = ((200-W/2)*unit,(H/2-(650+i*125))*unit,-7)
bpy.context.view_layer.update()
vs = [world_to_camera_view(s,cam,o.matrix_world@Vector(v)) for o in texts for v in o.bound_box]
b = [min(v.x for v in vs)*W,min(1-v.y for v in vs)*H-60,
     max(v.x for v in vs)*W,max(1-v.y for v in vs)*H-60]
# Safe rectangle is x=120..1872,y=440..2840 on the full master.
# Inner padding prevents letters touching the border; models start at y=1050.
assert b[0] >= 180 and b[2] <= 1812 and b[1] >= 500 and b[3] <= 1000, b
s['delivery_resolution'] = [2160,2300]
s['delivery_crop_top_bottom'] = [60,60]
s['safe_zone_template'] = 'youtube-series/assets/all-platforms-safe-zone-template-1080x1920.png'
s['still_revision'] = 'v8 code fit to supplied safe-zone template; still only'
s.render.use_border = False
s.render.filepath = str(OUT/'_render/code-safe-native.png')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'short-07-clay-study-safe-code.blend'))
report = {'delivery_resolution':[2160,2300], 'master_resolution':[2160,3840],
          'master_placement':[0,0], 'template_scale':2,
          'safe_rectangle_px':[120,440,1872,2840], 'code_bounds_px':b,
          'font_units':150,'previous_font_units':180,
          'single_still_only':True, 'native_camera_resolution':[W,H]}
(OUT/'safe-zone-verification.json').write_text(json.dumps(report,indent=2))
print('SAFE_CODE',json.dumps(report),flush=True)
s.render.use_border = True
s.render.use_crop_to_border = True
s.render.border_min_x = 0
s.render.border_max_x = 1
s.render.border_min_y = (H-1080)/H
s.render.border_max_y = 1
s.render.filepath = str(OUT/'_render/code-safe-patch.png')
bpy.ops.render.render(write_still=True)
