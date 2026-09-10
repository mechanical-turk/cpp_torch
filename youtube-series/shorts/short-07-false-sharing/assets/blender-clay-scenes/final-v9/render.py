"""Native Metal/Cycles rendering with verified static-state reuse.

Preview mode renders conventional full frames. Production separates the static
upper ground, transparent full-height typography, and lower native model region.
Numeral patches retain all scene geometry, light and shadows. No frame synthesis.
"""
import os
# Avoid the observed Blender 5.1.2 Metal path_cache_get invalid-free crash.
# This process-local option bypasses shader binary archives, not GPU rendering.
os.environ['CYCLES_METAL_DISABLE_BINARY_ARCHIVES']='1'
import bpy,json,time,hashlib,sys,argparse,math,subprocess
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
P=argparse.ArgumentParser();P.add_argument('--preview',action='store_true');P.add_argument('--native',action='store_true');P.add_argument('--frames',default='13,37,59,77,455,491,551,625,849');P.add_argument('--qa',type=int);P.add_argument('--samples',type=int);P.add_argument('--model-frame',type=int);P.add_argument('--part',choices=['all','hud','model'],default='all')
a=P.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
O=Path(__file__).resolve().parent;W=O/'_render';WIDTH,HEIGHT,SPLIT=2160,2300,990
bpy.ops.wm.open_mainfile(filepath=str(O/'false-sharing-final.blend'));s=bpy.context.scene
r=json.loads((O/'scene-verification.json').read_text());assert r['violation_count']==0
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.kernel_optimization_level='OFF';prefs.metalrt='OFF';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='METAL'
s.cycles.device='GPU';s.cycles.use_animated_seed=False;s.cycles.seed=0;s.render.use_persistent_data=False
s.render.image_settings.file_format='PNG';s.render.image_settings.compression=15
model=bpy.data.collections['01 • Clay models'];hud=bpy.data.collections['02 • Code and results'];ground=s.objects['Continuous clay studio ground']
# Freeze glyph tessellation once per renderer. Blender 5.1.2 dropped parts of
# animated FONT glyphs between consecutive frames even on the CPU. The saved
# source retains editable native text; only this render session uses its meshes.
bpy.ops.object.select_all(action='DESELECT')
fonts=[o for o in s.objects if o.type=='FONT']
for o in fonts:o.hide_viewport=False;o.select_set(True)
if fonts:
    bpy.context.view_layer.objects.active=fonts[0]
    bpy.ops.object.convert(target='MESH')
numbers=[o for o in model.objects if ' • value ' in o.name]
# Animated object hide flags are re-evaluated by Blender at render time. Use a
# non-animated collection switch so cached base poses truly contain no numerals.
number_collection=bpy.data.collections.new('Render-only counter numerals')
model.children.link(number_collection)
for o in numbers:
    for c in list(o.users_collection):c.objects.unlink(o)
    number_collection.objects.link(o)
for material in ground.data.materials:
    for node in material.node_tree.nodes:
        if node.type=='AMBIENT_OCCLUSION':node.samples=8
for part in ['base','patch','model','hud','review','qa']:(W/part).mkdir(exist_ok=True)
begin=time.time()
def device():
    print('RENDER_DEVICE',s.cycles.device,[(d.name,d.type,d.use) for d in prefs.devices],flush=True)
device()
def render(path,box=None,samples=48,percent=100):
    if path.exists():return
    s.render.resolution_percentage=percent;s.cycles.samples=samples;s.cycles.adaptive_threshold=.018 if samples==32 else .012 if samples<96 else .008
    s.render.use_border=box is not None;s.render.use_crop_to_border=box is not None
    if box:
        l,t,rr,b=box
        s.render.border_min_x=(l+.01)/WIDTH if l else 0;s.render.border_max_x=(rr+.01)/WIDTH if rr<WIDTH else 1
        s.render.border_min_y=(HEIGHT-b+.01)/HEIGHT if b<HEIGHT else 0;s.render.border_max_y=(HEIGHT-t+.01)/HEIGHT if t else 1
    temporary=path.with_name(path.stem+'.part.png')
    s.render.filepath=str(temporary);t=time.time();bpy.ops.render.render(write_still=True)
    os.replace(temporary,path)
    print('NATIVE_RENDER',str(path.relative_to(O)),round(time.time()-t,2),'elapsed',round(time.time()-begin,2),flush=True)
if a.preview:
    review=W/('native-stills' if a.native else 'review');review.mkdir(exist_ok=True)
    percent=100 if a.native else 50
    for f in map(int,a.frames.split(',')):
        s.frame_set(f);s.render.film_transparent=False;s.render.image_settings.color_mode='RGB'
        hud.hide_render=True;model.hide_render=False;ground.hide_render=False;s.cycles.device='GPU'
        plate=review/f'{f:04d}-plate.png';overlay=review/f'{f:04d}-hud.png';dest=review/f'{f:04d}.png'
        render(plate,samples=a.samples or (96 if a.native else 48),percent=percent)
        hud.hide_render=False;model.hide_render=True;ground.hide_render=True;s.render.film_transparent=True;s.render.image_settings.color_mode='RGBA';s.cycles.device='CPU'
        render(overlay,samples=64,percent=percent)
        subprocess.run(['/opt/homebrew/bin/python3',str(O/'compose.py'),'--preview',str(plate),str(overlay),str(dest)],check=True)
    print('PREVIEW_COMPLETE',flush=True);sys.exit(0)
def model_setup(f):
    s.frame_set(f);hud.hide_render=True;model.hide_render=False;ground.hide_render=False
    s.render.film_transparent=False;s.render.image_settings.color_mode='RGB';bpy.context.view_layer.update()
    return [o for o in numbers if not o.hide_render]
def base_key():
    state=[]
    for o in model.objects:
        if o.hide_render or o in numbers or o.type not in {'MESH','FONT','CURVE','META'}:continue
        state.append((o.name,tuple(round(v,6) for row in o.matrix_world for v in row)))
        if o.type=='META':state.append(tuple(tuple(round(v,6) for v in e.co)+(round(e.radius,6),) for e in o.data.elements))
        for slot in o.material_slots:
            mat=slot.material
            if mat and mat.node_tree:
                for n in mat.node_tree.nodes:
                    if n.type=='BSDF_PRINCIPLED':state.append((mat.name,tuple(n.inputs['Base Color'].default_value),n.inputs['Emission Strength'].default_value))
    return hashlib.sha256(repr(state).encode()).hexdigest()[:24]
def box_for(obs):
    vs=[world_to_camera_view(s,s.camera,o.matrix_world@Vector(v)) for o in obs for v in o.bound_box]
    return [max(0,int(min(v.x for v in vs)*WIDTH)-32),max(SPLIT,int(min(1-v.y for v in vs)*HEIGHT)-32),min(WIDTH,math.ceil(max(v.x for v in vs)*WIDTH)+32),min(HEIGHT,math.ceil(max(1-v.y for v in vs)*HEIGHT)+32)]
if a.qa:
    model_setup(a.qa);render(W/'qa'/f'full-{a.qa:04d}.png',(0,SPLIT,WIDTH,HEIGHT));sys.exit(0)
if a.part in ['all','hud']:
    s.frame_set(1);hud.hide_render=True;model.hide_render=False;ground.hide_render=False;s.render.film_transparent=False;s.render.image_settings.color_mode='RGB'
    render(W/'background.png',(0,0,WIDTH,SPLIT),128)
    for f in sorted(set(r['frame_maps']['hud'].values())):
        s.frame_set(f);hud.hide_render=False;model.hide_render=True;ground.hide_render=True;s.render.film_transparent=True;s.render.image_settings.color_mode='RGBA'
        s.cycles.device='CPU'
        render(W/'hud'/f'{f:04d}.png',samples=64)
    print('HUD_COMPLETE',flush=True)
if a.part in ['all','model']:
    s.cycles.device='GPU'
    frames=[a.model_frame] if a.model_frame else sorted(set(r['frame_maps']['model'].values()));records={}
    for index,f in enumerate(frames):
        dest=W/'model'/f'{f:04d}.png'
        if dest.exists():continue
        shown=model_setup(f);k=base_key();base=W/'base'/f'{k}.png';patch=W/'patch'/f'{f:04d}.png'
        number_collection.hide_render=True
        render(base,(0,SPLIT,WIDTH,HEIGHT))
        number_collection.hide_render=False
        box=box_for(shown);render(patch,box)
        subprocess.run(['/opt/homebrew/bin/python3',str(O/'compose.py'),str(base),str(patch),str(dest),*map(str,box)],check=True)
        records[str(f)]=k
        (W/'render-progress.json').write_text(json.dumps({'model_state':f,'completed':index+1,'total':len(frames),'elapsed_seconds':time.time()-begin},indent=2))
        print('MODEL_DONE',f,index+1,len(frames),flush=True)
    (W/'base-keys.json').write_text(json.dumps(records,indent=2));print('MODEL_COMPLETE',flush=True)
print('RENDER_COMPLETE',round(time.time()-begin,2),flush=True)
