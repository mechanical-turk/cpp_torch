"""Native production renderer. Run only after QA; no synthesized moving images."""
import os
os.environ['CYCLES_METAL_DISABLE_BINARY_ARCHIVES']='1'
import bpy,json,hashlib,time,subprocess
from pathlib import Path
O=Path(__file__).resolve().parent;D=O/'_render';SPLIT=1000
r=json.loads((O/'scene-verification.json').read_text());assert not r['violations']
motion=json.loads((O/'motion-verification.json').read_text());assert not motion['sort_aabb_intersections']
qa=json.loads((O/'production-preflight.json').read_text());assert qa['approved_for_batch']
bpy.ops.wm.open_mainfile(filepath=str(O/'short-08-clay.blend'));s=bpy.context.scene
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.kernel_optimization_level='OFF';prefs.metalrt='OFF';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='METAL'
s.render.resolution_percentage=100;s.render.use_persistent_data=False;s.render.image_settings.file_format='PNG';s.render.image_settings.compression=15
s.cycles.seed=0;s.cycles.use_animated_seed=False;s.cycles.use_denoising=True;s.cycles.adaptive_threshold=.012
model=bpy.data.collections['01 • Clay models'];hud=bpy.data.collections['02 • Code and results'];ground=s.objects['Continuous clay studio ground']
bpy.ops.object.select_all(action='DESELECT');fonts=[o for o in s.objects if o.type=='FONT']
for o in fonts:o.hide_viewport=False;o.select_set(True)
if fonts:bpy.context.view_layer.objects.active=fonts[0];bpy.ops.object.convert(target='MESH')
for p in ['hud','plates','frames','encode']:(D/p).mkdir(exist_ok=True)
def render(dest,part,full=False):
 if dest.exists():return
 is_hud=part=='hud';hud.hide_render=not is_hud;model.hide_render=is_hud;ground.hide_render=is_hud
 s.cycles.device='CPU' if is_hud else 'GPU';s.cycles.samples=64 if is_hud else 48
 s.render.film_transparent=is_hud;s.render.image_settings.color_mode='RGBA' if is_hud else 'RGB'
 s.render.use_border=not (is_hud or full);s.render.use_crop_to_border=s.render.use_border
 if s.render.use_border:
  s.render.border_min_x=0;s.render.border_max_x=1;s.render.border_min_y=0;s.render.border_max_y=(2300-SPLIT+.01)/2300
 tmp=dest.with_name(dest.stem+'.part.png');s.render.filepath=str(tmp);t=time.time();bpy.ops.render.render(write_still=True);os.replace(tmp,dest);print('RENDERED',dest.name,part,round(time.time()-t,2),flush=True)
# Batch the cheap CPU typography before GPU work to avoid device switches.
for f in sorted(set(r['maps']['hud'].values())):
 s.frame_set(f);render(D/'hud'/f'{f:04d}.png','hud')
print('HUD_COMPLETE',flush=True)
start=time.time();n=0;needed=len(set(r['maps']['model'].values()))
for f in range(1,721,2):
 canonical=r['maps']['model'][str(f)];plate=D/'plates'/f'{canonical:04d}.png';text=D/'hud'/f"{r['maps']['hud'][str(f)]:04d}.png";dest=D/'frames'/f'{f:04d}.png'
 if dest.exists():continue
 s.frame_set(f)
 if not plate.exists():render(plate,'model');n+=1
 subprocess.run(['/opt/homebrew/bin/python3',str(O/'compose_production.py'),str(plate),str(text),str(dest)],check=True)
 (D/'render-progress.json').write_text(json.dumps({'frame':f,'completed_model_states':len(list((D/'plates').glob('[0-9]*.png'))),'total_model_states':needed,'elapsed_seconds':time.time()-start,'updated_unix':time.time()},indent=2))
print('PRODUCTION_FRAMES_COMPLETE',flush=True)
