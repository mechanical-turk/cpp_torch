"""Native model rendering with cached blank-numeral poses and native numeral patches.
Every patch is rendered with the complete scene present, preserving lighting/occlusion.
No motion interpolation or generated pixels. The compose QA checks the native result.
"""
import bpy,json,time,hashlib,subprocess,sys,argparse,math
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
P=argparse.ArgumentParser();P.add_argument('--qa',type=int);P.add_argument('--inventory',action='store_true');a=P.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
O=Path(__file__).resolve().parent;W=O/'_render/current';PY='/opt/homebrew/bin/python3'
bpy.ops.wm.open_mainfile(filepath=str(O/'archive/v6/false-sharing-clay.blend'));s=bpy.context.scene;r=json.loads((O/'archive/v6/scene-verification.json').read_text());split=r['split_y'];width=2360;height=2352
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.kernel_optimization_level='OFF';prefs.metalrt='OFF';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='METAL'
s.cycles.device='GPU';s.cycles.use_animated_seed=False;s.cycles.seed=0;s.render.use_persistent_data=True;s.render.resolution_percentage=100;s.render.use_border=True;s.render.use_crop_to_border=True;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.image_settings.compression=15;s.render.film_transparent=False
model=bpy.data.collections['01 • Clay models'];bpy.data.collections['02 • Code and results'].hide_render=True
numbers=[o for o in model.objects if ' • value ' in o.name]
own=bpy.data.materials['Whole line • ownership tint'].node_tree.nodes.get('Principled BSDF');faces=[bpy.data.materials[n+' update face'].node_tree.nodes.get('Principled BSDF') for n in ['Counter a','Counter b']]
for mat in s.objects['Continuous clay studio ground'].data.materials:
 for n in mat.node_tree.nodes:
  if n.type=='AMBIENT_OCCLUSION':n.samples=4
for part in ['base','patch','model','qa']:(W/part).mkdir(exist_ok=True)
def setup(f):
 s.frame_set(f);bpy.context.view_layer.update()
 return [o for o in numbers if not o.hide_render]
def base_key():
 state=[(o.name,tuple(round(v,6) for row in o.matrix_world for v in row)) for o in model.objects if o.type in ['MESH','FONT','CURVE'] and not o.hide_render and o not in numbers]
 state += [tuple(own.inputs['Base Color'].default_value),tuple(n.inputs['Emission Strength'].default_value for n in faces)]
 return hashlib.sha256(repr(state).encode()).hexdigest()[:20]
def crop_box(objs):
 pts=[world_to_camera_view(s,s.camera,o.matrix_world@Vector(v)) for o in objs for v in o.bound_box]
 # Include raised lettering's nearby contact shadow and a broad quiet border.
 return (max(0,int(min(p.x for p in pts)*width)-32),max(split,int(min(1-p.y for p in pts)*height)-32),min(width,math.ceil(max(p.x for p in pts)*width)+32),min(height,math.ceil(max(1-p.y for p in pts)*height)+32))
def render(path,box,samples=32):
 if path.exists():return
 l,t,rr,b=box
 s.render.border_min_x=(l+.01)/width if l else 0;s.render.border_max_x=(rr+.01)/width if rr<width else 1
 s.render.border_min_y=(height-b+.01)/height if b<height else 0;s.render.border_max_y=(height-t+.01)/height
 s.cycles.samples=samples;s.cycles.adaptive_threshold=.018;s.render.filepath=str(path);bpy.ops.render.render(write_still=True)
def frame(f,qa=False):
 shown=setup(f);key=base_key();base=W/'base'/f'{key}.png';patch=W/'patch'/f'{f:04d}.png';dest=W/'model'/f'{f:04d}.png'
 for o in numbers:o.hide_render=True
 render(base,(0,split,width,height))
 for o in shown:o.hide_render=False
 box=crop_box(shown);render(patch,box)
 subprocess.run([PY,str(O/'compose_model.py'),str(base),str(patch),str(dest),*map(str,box),str(split)],check=True)
 if qa:render(W/'qa'/f'full-{f:04d}.png',(0,split,width,height))
 return key
if a.inventory:
 keys={}
 for f in sorted(set(r['frame_maps']['model'].values())):setup(f);keys[str(f)]=base_key()
 (W/'v6-base-inventory.json').write_text(json.dumps(keys,indent=2));print('BASE_INVENTORY',len(set(keys.values())),'poses for',len(keys),'numbered states',flush=True);sys.exit(0)
raise SystemExit("Inventory-only helper: use --inventory")
