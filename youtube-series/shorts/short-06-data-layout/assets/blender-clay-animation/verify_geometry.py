import bpy,json
from mathutils import Vector
from pathlib import Path
R=Path('/Users/keremkazan/Documents/Codex/2026-09-05/go-t');O=R/'outputs/clay-animation-v2'
bpy.ops.wm.open_mainfile(filepath=str(O/'cpp-data-layout-clay-animation.blend'))
s=bpy.context.scene
scores=[s.objects[f'Score {v} assembly'] for v in [7,2,9]]
histories=[s.objects[f'History {i} assembly'] for i in range(3)]
def box(g):
    pts=[o.matrix_world@Vector(v) for o in g.children if o.type=='MESH' for v in o.bound_box]
    return [(min(p[i] for p in pts),max(p[i] for p in pts)) for i in range(3)]
collisions=[]
dimensions={}
for f in range(1,243):
    s.frame_set(f)
    for a in scores:
        for b in histories:
            aa,bb=box(a),box(b)
            depth=[min(aa[i][1],bb[i][1])-max(aa[i][0],bb[i][0]) for i in range(3)]
            if min(depth)>.06:collisions.append([f,a.name,b.name,[round(x,4) for x in depth]])
    if f in [1,166,185,202,213,230,242]:
        dimensions[f]={}
        for family in [scores,histories]:
            dims=[]
            for g in family:
                b=box(g);dims.append([b[i][1]-b[i][0] for i in range(3)])
            assert max(abs(d[i]-dims[0][i]) for d in dims for i in range(3))<2e-6,(f,dims)
            dimensions[f]['score' if family is scores else 'history']=dims
assert not collisions,collisions
assert s.frame_end==360
assert not any(o.name.startswith('Code • final') for o in s.objects)
s.frame_set(360)
assert all(o.hide_render for o in s.objects if o.name.startswith('Code •'))
assert not s.objects['Speedup'].hide_render
result={'peer_world_dimensions_equal':True,'dimensions_by_frame':dimensions,'score_history_crossings':collisions,'checked_clearance_frames':[1,242],'ends_on_results':True,'no_final_code_objects':True}
(O/'geometry-verification.json').write_text(json.dumps(result,indent=2))
print('GEOMETRY_VERIFIED',json.dumps(result),flush=True)
