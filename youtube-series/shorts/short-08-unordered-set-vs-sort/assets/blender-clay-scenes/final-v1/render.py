"""Conventional native Cycles plates and CPU typography. Resumable per state."""
import os
os.environ['CYCLES_METAL_DISABLE_BINARY_ARCHIVES']='1'
import bpy,sys,argparse,json,time,hashlib,subprocess
from pathlib import Path
P=argparse.ArgumentParser();P.add_argument('--frames',default='1,155,365,405,455,543,709');P.add_argument('--native',action='store_true');P.add_argument('--production',action='store_true');P.add_argument('--samples',type=int,default=48)
a=P.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
O=Path(__file__).resolve().parent;D=O/'_render';bpy.ops.wm.open_mainfile(filepath=str(O/'short-08-clay.blend'));s=bpy.context.scene
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.kernel_optimization_level='OFF';prefs.metalrt='OFF';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='METAL'
s.render.resolution_percentage=100 if a.native or a.production else 50
s.render.use_persistent_data=False;s.render.use_border=False;s.render.use_crop_to_border=False
s.render.image_settings.file_format='PNG';s.render.image_settings.compression=15
s.cycles.seed=0;s.cycles.use_animated_seed=False;s.cycles.use_denoising=True
model=bpy.data.collections['01 • Clay models'];hud=bpy.data.collections['02 • Code and results'];ground=s.objects['Continuous clay studio ground']
# Preserve editable fonts in .blend; freeze tessellation only in this process.
bpy.ops.object.select_all(action='DESELECT');fonts=[o for o in s.objects if o.type=='FONT']
for o in fonts:o.hide_viewport=False;o.select_set(True)
if fonts:bpy.context.view_layer.objects.active=fonts[0];bpy.ops.object.convert(target='MESH')
for name in ['review','native-stills','plates','hud','frames']:(D/name).mkdir(exist_ok=True)
def render(path,layer):
 if path.exists():return
 is_hud=layer=='hud';hud.hide_render=not is_hud;model.hide_render=is_hud;ground.hide_render=is_hud
 s.cycles.device='CPU' if is_hud else 'GPU';s.cycles.samples=64 if is_hud else a.samples;s.cycles.adaptive_threshold=.012
 s.render.film_transparent=is_hud;s.render.image_settings.color_mode='RGBA' if is_hud else 'RGB'
 temp=path.with_name(path.stem+'.part.png');s.render.filepath=str(temp);t=time.time();bpy.ops.render.render(write_still=True);os.replace(temp,path);print('RENDERED',path.name,layer,round(time.time()-t,2),flush=True)
frames=range(1,721,2) if a.production else [int(x) for x in a.frames.split(',')]
report=json.loads((O/'scene-verification.json').read_text()) if a.production else None
if a.production:assert report['violations']==[], 'Preflight has unresolved violations'
begin=time.time()
for index,f in enumerate(frames):
 s.frame_set(f);bpy.context.view_layer.update()
 if a.production:
  plate=D/'plates'/f"{report['maps']['model'][str(f)]:04d}.png";over=D/'hud'/f"{report['maps']['hud'][str(f)]:04d}.png";dest=D/'frames'/f'{f:04d}.png'
 else:
  folder=D/('native-stills' if a.native else 'review');plate=folder/f'{f:04d}-plate.png';over=folder/f'{f:04d}-hud.png';dest=folder/f'{f:04d}.png'
 if dest.exists():continue
 render(plate,'model');render(over,'hud')
 subprocess.run(['/opt/homebrew/bin/python3',str(O/'compose.py'),str(plate),str(over),str(dest)],check=True)
 if a.production:(D/'render-progress.json').write_text(json.dumps({'frame':f,'total_frames':720,'elapsed_seconds':time.time()-begin,'updated_unix':time.time()},indent=2))
print('RENDER_COMPLETE',flush=True)
