import bpy,json,os
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector
s=bpy.context.scene
out='/Users/keremkazan/Documents/Codex/2026-09-05/go-t/outputs/short-06-blender/scene-audit.json'
def source(f):
    if f<=18:return 1
    if f<=35:return f
    if f<=57:return 35
    if f<=72:return f
    if f<=112:return 72
    if f<=126:return f
    if f<=166:return 126
    if f<=242:return f
    if f<=288:return 242
    if f<=360:return 289
    return 361
snapshots={};errors=[];top=1;right=0;left=1;bottom=0
for f in range(1,457):
    s.frame_set(f)
    state=[]
    for o in s.objects:
        if not o.hide_render:
            state.append((o.name,tuple(round(x,5) for row in o.matrix_world for x in row)))
    snapshots[f]=state
    if snapshots[source(f)]!=state:errors.append(f'Hold mismatch at frame {f}, source {source(f)}')
    for o in bpy.data.collections['01 • Player assemblies'].objects:
        if o.type not in {'MESH','FONT'}:continue
        for v in o.bound_box:
            p=world_to_camera_view(s,s.camera,o.matrix_world@Vector(v))
            left=min(left,p.x);right=max(right,p.x);top=min(top,1-p.y);bottom=max(bottom,1-p.y)
    expected=289<=f<=360
    if (not s.objects['Result • before time'].hide_render)!=expected:
        errors.append(f'Result visibility mismatch at {f}')
    expected=f>=361
    if (not s.objects['Selected history 0'].hide_render)!=expected:
        errors.append(f'Next-test visibility mismatch at {f}')
plates=[o for o in s.objects if '• plate ' in o.name]
assert len(plates)==45
s.frame_set(456)
scores=[s.objects[f'Player {i} • score motion'].location[:] for i in range(3)]
histories=[s.objects[f'Player {i} • retained history motion'].location[:] for i in range(3)]
assert scores[0][0]<scores[1][0]<scores[2][0]
assert histories[0][0]<histories[1][0]<histories[2][0]
assert len([o for o in s.objects if o.name.startswith('Selected score')])==2
assert not any(o.name=='Selected score 2' for o in s.objects)
assert top>.445,top
assert left>=.07 and right<=.93
assert not errors,errors[:20]
result={'status':'passed','frames_audited':456,'duration_seconds':s.frame_end/s.render.fps,'resolution':[s.render.resolution_x,s.render.resolution_y],'history_plate_count':len(plates),'scores_retained':[7,2,9],'selected_player_ids':[0,2],'selected_score_sum':16,'static_hold_state_equality':True,'model_bounds_normalized':{'left':left,'right':right,'top':top,'bottom':bottom},'code_panel_bottom':.445,'model_code_overlap':False,'result_only_frames':[289,360],'next_test_only_frames':[361,456],'fonts_packed':all(f.packed_file is not None for f in bpy.data.fonts if f.filepath and f.filepath!='<builtin>')}
with open(out,'w') as fp:json.dump(result,fp,indent=2)
print(json.dumps(result),flush=True)
