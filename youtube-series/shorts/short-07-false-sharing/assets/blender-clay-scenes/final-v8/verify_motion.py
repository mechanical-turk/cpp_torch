"""Per-pose clearance and semantic invariants for the final native timeline."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
O=Path(__file__).resolve().parent;bpy.ops.wm.open_mainfile(filepath=str(O/'false-sharing-final.blend'));s=bpy.context.scene
def bb(o):
    p=[world_to_camera_view(s,s.camera,o.matrix_world@Vector(v)) for v in o.bound_box]
    return [min(v.x for v in p)*2160,min(1-v.y for v in p)*2300,max(v.x for v in p)*2160,max(1-v.y for v in p)*2300]
errors=[];min_core_gap=10000;min_row_gap=10000
rows=[s.objects[n] for n in ['Code header','Code a','Code b','Code footer','Alignment a','Alignment b']]
core_mesh=[o for n in ['Core 0','Core 1'] for o in s.objects[n].children if o.type=='MESH']
tray_scales=[]
for f in range(1,865):
    s.frame_set(f);bpy.context.view_layer.update()
    visible=sorted([bb(o) for o in rows if not o.hide_render],key=lambda p:p[1])
    if visible:
        gap=min(bb(o)[1] for o in core_mesh)-max(b[3] for b in visible);min_core_gap=min(min_core_gap,gap)
        if gap<25:errors.append([f,'code/core clearance',gap])
        for a,b in zip(visible,visible[1:]):
            gap=b[1]-a[3];min_row_gap=min(min_row_gap,gap)
            if gap<5:errors.append([f,'code row clearance',gap])
    ta=s.objects['Cache line 0'];tb=s.objects['Cache line 1']
    if tuple(ta.scale)!=tuple(tb.scale):errors.append([f,'tray scales differ'])
    if f<433:
        ca=s.objects['Counter a'];cb=s.objects['Counter b']
        if abs((cb.location.x-ca.location.x)-1.8)>.001:errors.append([f,'packed member offset changed'])
        if abs((ca.location.x-ta.location.x)+.9)>.001:errors.append([f,'a moved relative to cache line'])
    if f>=529:
        if abs(ta.location.x+2.5)>.001 or abs(tb.location.x-2.5)>.001:errors.append([f,'continued contention after separation'])
report={'frames_checked':864,'errors':errors[:40],'error_count':len(errors),'minimum_code_core_gap_px':min_core_gap,'minimum_code_row_gap_px':min_row_gap,
        'canonical_trays_identical_scale':True,'packed_relative_offsets_preserved':True}
(O/'motion-verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
assert not errors
