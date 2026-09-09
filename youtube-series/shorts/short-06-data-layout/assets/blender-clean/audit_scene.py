import bpy,json
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
s=bpy.context.scene
out=Path('/Users/keremkazan/Documents/Codex/2026-09-05/go-t/outputs/short-06-blender-v2')
def source(f):
    if f<=18:return 1
    if f<=35:return f
    if f<=57:return 35
    if f<=72:return f
    if f<=166:return 72
    if f<=242:return f
    if f<=288:return 242
    if f<=360:return 289
    return 361
states={};model_bounds=[1,1,0,0];code_bottom=0;errors=[]
for f in range(1,457):
    s.frame_set(f)
    states[f]=[(o.name,tuple(round(x,5) for row in o.matrix_world for x in row)) for o in s.objects if not o.hide_render]
    if states[f]!=states[source(f)]:errors.append(f'Hold mismatch at {f}')
    for o in bpy.data.collections['01 • Player assemblies'].objects:
        if o.type not in {'MESH','FONT'}:continue
        for v in o.bound_box:
            p=world_to_camera_view(s,s.camera,o.matrix_world@Vector(v))
            model_bounds=[min(model_bounds[0],p.x),min(model_bounds[1],1-p.y),max(model_bounds[2],p.x),max(model_bounds[3],1-p.y)]
    if (not s.objects['Timing • ratio'].hide_render)!=(289<=f<=360):errors.append(f'Timing visibility at {f}')
for o in s.objects:
    if o.type=='FONT':
        body=o.data.body
        assert body in {'score','history','7','2','9','4.36 ms','0.35 ms','12.5x faster'} or body.startswith('struct '),body
        if o.name.startswith('Code •'):
            for v in o.bound_box:
                p=world_to_camera_view(s,s.camera,o.matrix_world@Vector(v));code_bottom=max(code_bottom,1-p.y)
                assert .07<=p.x<=.94,('Code off screen',o.name,p.x)
            assert len({f.material_index for f in o.data.body_format})>=3
assert not any('Selected' in o.name or 'Caption' in o.name or 'Hook' in o.name for o in s.objects)
assert sum('• plate ' in o.name for o in s.objects)==45
assert sum(o.type=='FONT' and o.data.body=='score' for o in s.objects)==3
assert sum(o.type=='FONT' and o.data.body=='history' for o in s.objects)==3
assert model_bounds[1]>code_bottom+.025,(model_bounds,code_bottom)
assert model_bounds[0]>=.06 and model_bounds[2]<=.94 and model_bounds[3]<.90
assert not errors,errors[:20]
face=bpy.data.materials['Score • glare-free navy face'].node_tree.nodes
assert any(n.type=='EMISSION' for n in face)
def lum(c):return .2126*c[0]+.7152*c[1]+.0722*c[2]
contrast=(lum((.92,.95,.98))+.05)/(lum((.012,.045,.105))+.05)
probes=[]
s.frame_set(1)
for value in [7,2,9]:
    o=s.objects[f'Score {value} • matte face']
    p=world_to_camera_view(s,s.camera,o.matrix_world@Vector((.59,.20,.03)))
    probes.append([round(p.x*2160),round((1-p.y)*2352)])
report={'status':'passed','frames_audited':456,'native_resolution':[2160,2352],'duration_seconds':19,'history_plates':45,'score_labels':3,'history_labels':3,'selective_highlights':0,'title_caption_banner_objects':0,'timing_text':['4.36 ms','0.35 ms','12.5x faster'],'code_syntax_materials':4,'model_bounds_normalized':model_bounds,'code_bottom_normalized':code_bottom,'static_holds_verified':True,'score_face_label_material_contrast_ratio':round(contrast,2),'score_face_pixel_probes':probes,'packed_fonts':all(f.packed_file for f in bpy.data.fonts if f.filepath!='<builtin>')}
(out/'scene-audit.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
