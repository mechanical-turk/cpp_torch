"""Eight standalone Blender diagrams; no animated transitions or video render."""
import bpy,math,json,re,hashlib
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
O=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(O.parent/'keyframes-v3/short-08-keyframes.blend'))
s=bpy.context.scene;s.frame_set(5);cam=s.camera
model=bpy.data.collections['01 • Clay models'];hud=bpy.data.collections['02 • Code and results']
W,H=2160,2300;unit=(7*cam.data.sensor_width/cam.data.lens)/W
# Retain the native sculpture/material/typography assets; discard all choreography.
def copy_template(root):
 result=[]
 for o in [root]+list(root.children_recursive):
  n=o.copy();n.animation_data_clear();result.append((o,n))
 mapping=dict(result)
 for o,n in result:n.parent=mapping.get(o.parent)
 return [n for o,n in result]
T={v:copy_template(s.objects[f'Hash node {v-1}']) for v in [1,2,3]}
trayT=copy_template(s.objects['Hash input tray'])
tailT=copy_template(s.objects['Inactive tail slot 0'])
arrowT=s.objects['Benchmark arrow'].copy();arrowT.animation_data_clear()
codeT=s.objects['hash code 0'].copy();codeT.data=codeT.data.copy();codeT.animation_data_clear()
resultsT={n:s.objects[n].copy() for n in ['Hash time','Hash unit','Sort time','Sort unit','Measured ratio','Early speedup']}
for o in resultsT.values():o.animation_data_clear()
for o in list(model.all_objects)+list(hud.all_objects):bpy.data.objects.remove(o,do_unlink=True)
for m in bpy.data.materials:
 if m.node_tree:m.node_tree.animation_data_clear()
s.frame_start=1;s.frame_end=8;s.render.resolution_x=W;s.render.resolution_y=H;s.render.resolution_percentage=10
s.render.use_border=False;s.render.use_crop_to_border=False;s.render.film_transparent=False
s.render.use_motion_blur=False;cam.data.dof.use_dof=False
slides=[];allobjects=[];row_records=[]

def group(template,name):
 mapping={o:o.copy() for o in template}
 for old,o in mapping.items():
  o.name=name+' '+('root' if old.parent is None else old.name.split()[-1]);o.animation_data_clear();model.objects.link(o)
  o.parent=mapping.get(old.parent);o.hide_render=False;o.hide_viewport=False
  allobjects.append(o)
 root=mapping[template[0]];root.name=name
 return root

def world(x,y,z):
 ray=cam.matrix_world.to_quaternion()@Vector(((x-W/2)*unit,(H/2-y)*unit,-7))
 return cam.location+ray*((z-cam.location.z)/ray.z)
def bounds(o):
 vv=[world_to_camera_view(s,cam,o.matrix_world@Vector(v)) for v in o.bound_box]
 return [min(v.x for v in vv)*W,min(1-v.y for v in vv)*H,max(v.x for v in vv)*W,max(1-v.y for v in vv)*H]
def center_object(root,x,y,z=.13):
 # Align actual projected shell centers, including perspective and raised geometry.
 root.location=world(x,y,z);root.rotation_euler=(0,0,0)
 shell=next((c for c in root.children if 'shell' in c.name),root.children[0])
 for _ in range(4):
  bpy.context.view_layer.update();b=bounds(shell);cx=(b[0]+b[2])/2;cy=(b[1]+b[3])/2
  root.location+=world(x,y,root.location.z)-world(cx,cy,root.location.z)
 return bounds(shell)
def ui_clone(template,name):
 o=template.copy();o.animation_data_clear();o.name=name;hud.objects.link(o);o.parent=cam;o.hide_render=False;allobjects.append(o);return o
def px(x,y):return Vector(((x-W/2)*unit,(H/2-y)*unit,-7))
def code(lines,y=590,size=96):
 out=[]
 for i,body in enumerate(lines):
  o=ui_clone(codeT,f'S{len(slides)+1} code {i}');o.data=o.data.copy();o.data.body=body;o.data.size=size*unit;o.scale=(1,1,1);o.location=px(205,y+125*i)
  for fmt in o.data.body_format:fmt.material_index=0
  for match in re.finditer(r'[A-Za-z_]\w*|\d+',body):
   token=match.group();idx=1 if token in ['auto','for','return'] else 2 if token in ['Number','unordered_set'] else 3 if token.isdigit() else 0
   for j in range(match.start(),match.end()):o.data.body_format[j].material_index=idx
  out.append(o)
 # Keep one consistent font size per block and fit complete expressions inside safe guard.
 bpy.context.view_layer.update();right=max(bounds(o)[2] for o in out)
 if right>1810:
  factor=(1810-205)/(right-205)
  for o in out:o.data.size*=factor
 return out

def row(values,y,container=False,xs=None,tag='row'):
 xs=xs or [450,710,970,1230,1490]
 roots=[]
 if container:
  tr=group(trayT,f'S{len(slides)+1} {tag} vector');tr.scale=(2.06,.64,.39)
  center_object(tr,970,y+36,0)
 for i,v in enumerate(values):
  r=group(T[v] if v is not None else tailT,f'S{len(slides)+1} {tag} {i}')
  r.scale=(.46,.38,.43)
  # All baseline objects remain literal linked canonical copies.
  if v is not None:r['value']=v;r['family']='value tile'
  b=center_object(r,xs[i],y,.13);roots.append(r)
  row_records.append({'slide':len(slides)+1,'name':r.name,'target':[xs[i],y],'center':[(b[0]+b[2])/2,(b[1]+b[3])/2],'value':v})
 return roots

def arrow(x,y,down=True,scale=1):
 o=ui_clone(arrowT,f'S{len(slides)+1} operation arrow');o.location=px(x,y);o.scale=(scale,scale,scale);o.rotation_euler=(0,0,-math.pi/2 if down else 0);return o

def result(name):return ui_clone(resultsT[name],f'S{len(slides)+1} '+name)

def finish(name,cue,meaning):
 frame=len(slides)+1
 # Objects created since previous slide get visibility only in this static pose.
 owned=[o for o in allobjects if o.get('slide') is None]
 for o in owned:
  o['slide']=frame
  for f in range(1,9):o.hide_render=f!=frame;o.keyframe_insert(data_path='hide_render',frame=f)
 slides.append({'slide':frame,'file':name+'.png','spoken_cue':cue,'meaning':meaning,'objects':[o.name for o in owned]})

old=['unordered_set<Number> distinct;','distinct.reserve(v.size());','for (auto value : v)','  distinct.insert(value);','return distinct.size();']
# 1: The input/result relation is visible in one image, rather than starting mid-insertion.
code(old);row([3,1,3,2,1],1360,True,tag='input');arrow(970,1630)
row([3,1,2],1940,xs=[570,970,1370],tag='distinct output')
finish('01-distinct-task','Stop choosing algorithms by Big O alone.','Five source values map to three distinct values; both states visible.')
# 2: Same complete task, early measured payoff without revealing the replacement.
result('Early speedup');row([3,1,3,2,1],1360,True,tag='input');arrow(970,1630)
row([3,1,2],1940,xs=[570,970,1370],tag='distinct output')
finish('02-speedup-tease','In this test, the worse Big O gave me almost ten times the speed.','9.68x over the same distinct-count task; replacement withheld.')
# 3: Literal code shows the attempted duplicate; unchanged before/after states prove no new key.
code(['unordered_set<Number> distinct;','distinct = {3, 1};','distinct.insert(3);'],y=640)
row([3,1],1300,xs=[770,1170],tag='before');arrow(970,1630)
row([3,1],1970,xs=[770,1170],tag='after')
finish('03-duplicate-keeps-set','We\'re counting distinct numbers. This C++ unordered set inserts each value once: expected linear time. So where\'s the time going?','Inserting an existing 3 leaves the two-key set unchanged. Illustrative values, not benchmark input.')
# 4 and 5 deliberately separate reorder from compaction.
code(['sort(v.begin(), v.end());'],y=780)
row([3,1,3,2,1],1330,True,tag='before');arrow(970,1630)
row([1,1,2,3,3],1970,True,tag='after')
finish('04-sort','I replaced it with sorting and counting the changes.','Sorting preserves all five values and places duplicates beside one another.')
code(['auto end = unique(v.begin(), v.end());','return end - v.begin();'],y=700)
row([1,1,2,3,3],1330,True,tag='before');arrow(970,1630)
row([1,2,3,None,None],1970,True,tag='retained prefix')
finish('05-unique','N log N, but it finished in 2.6 seconds instead of 25.','Three retained keys; two unnumbered tail positions preserve vector allocation without asserting tail values.')
# 6: Minimal, already established native result composition.
for name in ['Hash time','Hash unit','Sort time','Sort unit','Measured ratio']:result(name)
arrow(1030,662,False)
row([1,2,3,None,None],1730,True,tag='retained prefix')
finish('06-benchmark','...2.6 seconds instead of 25.','25.25 s to 2.61 s; 9.68x, with the retained result.')
# 7: Code anchors the two representations. Equal rows, no floating names or bucket shells.
code(['unordered_set<Number> distinct;'],y=590)
row([3,1,2],1100,xs=[450,970,1490],tag='separate nodes')
code(['sort(v.begin(), v.end());','auto end = unique(v.begin(), v.end());'],y=1440,size=90)
row([1,2,3,None,None],2010,True,tag='contiguous values')
finish('07-memory-layout','Why does sorting win when it has the worse Big O? Look at how the two versions use memory.','Separate node allocations versus values in one contiguous allocation; schematic, not measured addresses or causal proof.')
# 8: Unmeasured flat layout; no unsupported library name or old benchmark.
code(['distinct.insert(value);'],y=800)
row([3,None,1,None,2],1630,True,tag='flat slots')
finish('08-flat-table-next','Next, we\'re testing a flat hash table.','Keys stored directly among empty slots in one table; illustrative layout, no timing.')
for action in bpy.data.actions:
 for layer in action.layers:
  for strip in layer.strips:
   for slot in action.slots:
    bag=strip.channelbag(slot)
    if bag:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:k.interpolation='CONSTANT'
# Numeric checks on the actual standalone poses.
violations=[];overlaps=[]
for f in range(1,9):
 s.frame_set(f);bpy.context.view_layer.update();shells=[]
 for o in allobjects:
  if o.hide_render:continue
  if o.type=='FONT':
   b=bounds(o)
   if b[0]<120 or b[1]<480 or b[2]>1872 or b[3]>2260:violations.append({'slide':f,'object':o.name,'bounds':b})
  if o.get('family')=='value tile':
   sh=next((c for c in o.children if 'shell' in c.name),None)
   assert sh is not None,(o.name,[c.name for c in o.children])
   vs=[sh.matrix_world@Vector(v) for v in sh.bound_box]
   shells.append((o.name,[min(v[k] for v in vs) for k in range(3)],[max(v[k] for v in vs) for k in range(3)]))
 for i,(name,a0,a1) in enumerate(shells):
  for other,b0,b1 in shells[i+1:]:
   if min(min(a1[k],b1[k])-max(a0[k],b0[k]) for k in range(3))>.005:overlaps.append([f,name,other])
alignment_error=max(max(abs(a-b) for a,b in zip(r['target'],r['center'])) for r in row_records)
report={'text_violations':violations,'value_overlaps':overlaps,'max_projected_center_error_px':alignment_error,'rows':row_records}
(O/'storyboard-verification.json').write_text(json.dumps(report,indent=2))
assert not violations,violations
assert not overlaps,overlaps
assert alignment_error<.5,alignment_error
s.frame_set(1);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(O/'short-08-storyboard.blend'))
(O/'storyboard-manifest.json').write_text(json.dumps({'native_size':[2160,2300],'preview_size':[216,230],'render_percentage':10,'slides':slides,'medium':'static slideshow','no_video_render':True},indent=2))
print('STORYBOARD_BUILT',len(slides),'alignment_error',alignment_error,flush=True)
