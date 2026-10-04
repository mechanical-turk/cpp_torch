"""Resumable native Cycles/OptiX renderer; exact-state caching, native crop only."""
import bpy,json,os,time,sys,argparse,subprocess,hashlib
from pathlib import Path
O=Path(__file__).resolve().parent;D=O/'_render';P=argparse.ArgumentParser();P.add_argument('--qa',action='store_true');P.add_argument('--frames',default='1,323,471,603,777,881');args=P.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
R=json.loads((O/'scene-verification.json').read_text());assert not R['violations'] and not R['sort_aabb_intersections'] and not R['all_value_shell_intersections'];assert R['source_sha256']==hashlib.sha256((O/'short-08-clay.blend').read_bytes()).hexdigest()
if not args.qa:assert json.loads((O/'production-preflight.json').read_text())['approved_for_batch']
bpy.ops.wm.open_mainfile(filepath=str(O/'short-08-clay.blend'));s=bpy.context.scene
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='OPTIX'
assert any(d.use for d in prefs.devices)
model=bpy.data.collections['01 • Clay models'];hud=bpy.data.collections['02 • Code and results'];ground=s.objects['Continuous clay studio ground']
bpy.ops.object.select_all(action='DESELECT');fonts=[o for o in s.objects if o.type=='FONT']
for o in fonts:o.hide_viewport=False;o.select_set(True)
if fonts:bpy.context.view_layer.objects.active=fonts[0];bpy.ops.object.convert(target='MESH')
s.render.image_settings.file_format='PNG';s.render.image_settings.compression=15;s.render.use_persistent_data=False;s.render.resolution_percentage=100
s.cycles.seed=0;s.cycles.use_animated_seed=False;s.cycles.use_denoising=True
for folder in ['plates','hud','frames','qa','encode']:(D/folder).mkdir(exist_ok=True)

def render(path,part,crop=None,samples=48,percentage=100):
 if path.exists():return
 is_hud=part=='hud';s.render.use_persistent_data=not is_hud;hud.hide_render=not is_hud;model.hide_render=is_hud or part=='background';ground.hide_render=is_hud
 s.cycles.device='CPU' if is_hud else 'GPU';s.cycles.samples=samples;s.cycles.adaptive_threshold=.012 if samples<=64 else .007
 s.render.resolution_percentage=percentage;s.render.film_transparent=is_hud;s.render.image_settings.color_mode='RGBA' if is_hud else 'RGB'
 s.render.use_border=crop is not None;s.render.use_crop_to_border=crop is not None
 if crop:
  x0,y0,x1,y1=crop;s.render.border_min_x=(x0+.001)/2160;s.render.border_max_x=min(1,(x1+.001)/2160);s.render.border_min_y=(2300-y1+.001)/2300;s.render.border_max_y=min(1,(2300-y0+.001)/2300)
 tmp=path.with_name(path.stem+'.part.png');s.render.filepath=str(tmp);t=time.time();bpy.ops.render.render(write_still=True);os.replace(tmp,path)
 record={'frame':s.frame_current,'part':part,'file':str(path.relative_to(O)),'seconds':time.time()-t,'samples':samples,'percentage':percentage,'crop':crop}
 with (D/'timings.jsonl').open('a') as f:f.write(json.dumps(record)+'\n')
 print('RENDERED',json.dumps(record),flush=True)

def compose(f):subprocess.run(['python',str(O/'compose.py'),str(f)],check=True)

render(D/'background.png','background',samples=128)
if args.qa:
 for frame in [int(x) for x in args.frames.split(',')]:
  s.frame_set(frame)
  if frame==1:
   # Native production crop and a conventional 96-sample full plate for comparison.
   render(D/'qa/reference-0001.png','model',samples=96)
   for part in ['hud','model']:
    canonical=R['maps'][part][str(frame)];crop=R['crops'][part][str(canonical)]
    if crop:render(D/('hud' if part=='hud' else 'plates')/f'{canonical:04d}.png',part,crop,64 if part=='hud' else 48)
   compose(frame)
  else:
   render(D/'qa'/f'{frame:04d}-plate.png','model',samples=32,percentage=50)
   render(D/'qa'/f'{frame:04d}-hud.png','hud',samples=64,percentage=50)
 print('QA_RENDER_COMPLETE',flush=True)
else:
 # Render native unlit typography crops first; reduce CPU pixel work, not font quality.
 for canonical in sorted(set(R['maps']['hud'].values())):
  crop=R['crops']['hud'][str(canonical)]
  if crop:s.frame_set(canonical);render(D/'hud'/f'{canonical:04d}.png','hud',crop,64)
 print('ALL_HUD_COMPLETE',flush=True)
 total=len(set(R['maps']['model'].values()));begin=time.time()
 for f in range(1,s.frame_end+1,2):
  dest=D/'frames'/f'{f:04d}.png'
  if dest.exists():continue
  canonical=R['maps']['model'][str(f)];s.frame_set(canonical);render(D/'plates'/f'{canonical:04d}.png','model',R['crops']['model'][str(canonical)],48)
  compose(f)
  (D/'render-progress.json').write_text(json.dumps({'frame':f,'total_frames':s.frame_end,'unique_model_complete':len(list((D/'plates').glob('[0-9]*.png'))),'unique_model_total':total,'updated_unix':time.time(),'elapsed_seconds':time.time()-begin},indent=2))
 print('ALL_NATIVE_FRAMES_COMPLETE',flush=True)
