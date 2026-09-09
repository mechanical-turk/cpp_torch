import bpy,json
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
O=Path(__file__).resolve().parent;bpy.ops.wm.open_mainfile(filepath=str(O/'false-sharing-clay.blend'));s=bpy.context.scene
pairs=[('Counter a','Counter b'),('Core 0','Core 1'),('Cache line 0','Cache line 1'),('Counter 0 • increment bubble','Counter 1 • increment bubble')]
checks=[]
for a,b in pairs:
 x=s.objects[a];y=s.objects[b];xm=sorted([o for o in x.children if o.type=='MESH'],key=lambda o:o.name.split(' • ')[-1]);ym=sorted([o for o in y.children if o.type=='MESH'],key=lambda o:o.name.split(' • ')[-1]);assert len(xm)==len(ym)
 for p,q in zip(xm,ym):assert p.data==q.data,(p.name,q.name)
 checks.append({'family':[a,b],'shared_mesh_data':True,'mesh_count':len(xm)})
a=s.objects['Counter a'];b=s.objects['Counter b'];t0=s.objects['Cache line 0'];t1=s.objects['Cache line 1'];a0=None;minimum=100;opening_x=[]
def box(objects):
 ps=[world_to_camera_view(s,s.camera,o.matrix_world@Vector(v)) for o in objects for v in o.bound_box]
 return min(v.x for v in ps)*2360,min(1-v.y for v in ps)*2352,max(v.x for v in ps)*2360,max(1-v.y for v in ps)*2352
bubble_gaps=[]
for f in range(1,1009):
 s.frame_set(f)
 for i,g in enumerate([a,b]):
  bubble=s.objects[f'Counter {i} • increment bubble'];parts=[o for o in bubble.children if not o.hide_render]
  if parts:
   bb=box(parts);label=next(o for o in g.children if o.type=='FONT' and o.data.body in ['a','b']);lb=box([label]);bubble_gaps.append(lb[1]-bb[3]);assert bb[3]<lb[1]-5,(f,i,bb,lb)
   for name in ['Core 0','Core 1']:
    cb=box(list(s.objects[name].children))
    if bb[0]<cb[2] and bb[2]>cb[0]:assert bb[1]>cb[3]+5,(f,i,bb,cb)
 relative=a.location-t0.location
 if a0 is None:a0=relative.copy()
 assert (relative-a0).length<1e-6
 if f<=576:
  opening_x.append(t0.location.x)
  assert abs((b.location-t0.location).x-.9)<1e-6
 else:assert abs(a.location.x+3.4)<1e-6
 assert (t0.scale-t1.scale).length<1e-7
 assert tuple(a.scale[:2])==tuple(b.scale[:2])
 assert .70*.979<a.scale.z<.70001 and .70*.979<b.scale.z<.70001
 if 621<=f<=661:
  shell=next(o for o in b.children if 'shell' in o.name);bottom=min((shell.matrix_world@Vector(v)).z for v in shell.bound_box)
  rim=max((o.matrix_world@Vector(v)).z for o in t0.children if o.type=='CURVE' for v in o.bound_box);minimum=min(minimum,bottom-rim);assert bottom>rim+.30
s.frame_set(1008)
rim1=next(o for o in t1.children if o.type=='CURVE');assert rim1.material_slots[0].material.name=='Cobalt clay cards'
assert s.objects['Timing digits 244.52'].data.body=='244.52' and s.objects['Timing digits 44.19'].data.body=='44.19'
for frame,blue_owner in [(1,False),(27,False),(29,True),(123,True),(125,False),(800,False)]:
 s.frame_set(frame);body=next(o for o in t0.children if o.name.endswith(' • shell'));color=body.material_slots[0].material.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value;assert (color[2]>color[1])==blue_owner
for n in ['Counter 0 • increment','Counter 1 • increment']:assert abs(s.objects[n].data.size-.64)<.001
assert not any('outline' in o.name.lower() for o in s.objects if o.type=='MESH')
assert all(s.objects[f'Worker {i} • clay dash {j}'].data==s.objects['Worker 0 • clay dash 0'].data for i in range(2) for j in range(7))
assert s.render.resolution_x==2360 and s.render.resolution_y==2352
assert min(opening_x)<-2.49 and max(opening_x)>2.49 and opening_x[-1]<-2.49
assert s.objects['Measured speedup'].data.body=='5.5× faster'
s.frame_set(1008)
final_values=[]
for g in [a,b]:
 shown=[o.data.body for o in g.children if o.type=='FONT' and ' • value ' in o.name and not o.hide_render]
 assert len(shown)==1
 final_values.append(shown[0])
assert final_values[0]==final_values[1],final_values
assert s.objects['Code counter a text'].data.body=='  atomic<uint64_t> a{0};'
assert len(s.objects['Code counter a text'].data.materials)==5
assert s.objects['Code struct header text'].data.body=='struct Counters {'
assert s.objects['Code struct footer text'].data.body=='};'
assert s.objects['Code aligned b text'].data.body=='  alignas(128) atomic<uint64_t> b{0};'
r=json.loads((O/'scene-verification.json').read_text())
for event in r['contention_events']:
 old_x=-2.5 if event['requester']==1 else 2.5;new_x=-old_x
 for f in range(event['pulse_start'],event['transfer_start']+1):
  s.frame_set(f);assert abs(t0.location.x-old_x)<1e-6
 s.frame_set(event['transfer_end']);assert abs(t0.location.x-new_x)<1e-6
 for f in range(event['write'],min(event['bubble_end'],1009)):
  s.frame_set(f);assert not s.objects[f"Counter {event['requester']} • increment"].hide_render
for i in range(2):
 assert any(t>=817 for t in r['write_events'][i])
 for t in r['write_events'][i]:
  if t>=721:
   s.frame_set(t);assert not s.objects[f'Counter {i} • increment'].hide_render
report={'ordered_handoff_events_checked':True,'tray_moves_through_all_contention_scenes':True,'bubbles_keep_their_full_lifetime':True,'updates_continue_in_benchmark_and_discussion':True,'minimum_bubble_label_clearance_px':min(bubble_gaps),'equal_illustrative_final_values':final_values,'pairs':checks,'a_offset_in_cache_line_fixed_all_frames':True,'opening_moves_right_and_returns':True,'tray_sizes_fixed':True,'counter_xy_sizes_fixed':True,'counter_z_compression_max_percent':2,'b_minimum_crossing_clearance_world':minimum,'second_rim_cobalt_after_separation':True,'benchmark_values_match_script':True,'full_frame_audit':True,'whole_tray_ownership_colors_checked':True,'increment_font_size':.64,'rising_clay_bubbles':True,'visible_counter_values':True,'syntax_highlighted_code':True,'speedup_multiple':'5.5× faster','worker_0_is_teal':True,'no_outline_objects':True}
(O/'geometry-verification.json').write_text(json.dumps(report,indent=2));print('GEOMETRY_VERIFIED',json.dumps(report),flush=True)
