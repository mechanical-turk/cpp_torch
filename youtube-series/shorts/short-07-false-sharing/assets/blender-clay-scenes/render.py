"""Render verified native states. Identical authored holds reuse identical renders."""
import bpy, json, time, argparse, sys
from pathlib import Path
P=argparse.ArgumentParser();P.add_argument('--work',default=None);a=P.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []);O=Path(__file__).resolve().parent;W=Path(a.work) if a.work else O/'_render/current';assert W.resolve().is_relative_to(O.resolve()), 'Render work must stay inside this Content HQ assets package'
bpy.ops.wm.open_mainfile(filepath=str(O/'false-sharing-clay.blend'));s=bpy.context.scene
p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='METAL';p.kernel_optimization_level='OFF';p.metalrt='OFF';p.get_devices()
for d in p.devices:d.use=d.type=='METAL'
s.cycles.device='GPU';s.render.use_persistent_data=True;s.render.resolution_percentage=100;s.render.use_border=True;s.render.use_crop_to_border=True;s.render.border_min_x=0;s.render.border_max_x=1;s.render.image_settings.file_format='PNG';s.render.image_settings.compression=15
model=bpy.data.collections['01 • Clay models'];hud=bpy.data.collections['02 • Code and results'];ground=s.objects['Continuous clay studio ground'];r=json.loads((O/'scene-verification.json').read_text());split=r['split_y'];height=2352
for mat in ground.data.materials:
 for n in mat.node_tree.nodes:
  if n.type=='AMBIENT_OCCLUSION':n.samples=4
for part in ['model','hud']:(W/part).mkdir(exist_ok=True)
start=time.time()
def render(part,f,path):
 if path.exists():return
 s.frame_set(f);hud.hide_render=part!='hud';model.hide_render=part=='hud';ground.hide_render=part=='hud';s.render.film_transparent=part=='hud';s.render.image_settings.color_mode='RGBA' if part=='hud' else 'RGB'
 s.render.border_min_y=0 if part=='model' else (height-split)/height;s.render.border_max_y=(height-split)/height if part=='model' else 1
 s.cycles.samples=32 if part=='model' else 64 if part=='hud' else 128
 if part=='model' and f in [1,457]:s.cycles.samples=128
 s.cycles.adaptive_threshold=.018 if part=='model' else .008;s.render.filepath=str(path);t=time.time();bpy.ops.render.render(write_still=True);print('FRAME_DONE',part,f,round(time.time()-t,2),'elapsed',round(time.time()-start,2),flush=True)
render('background',1,W/'background.png')
for part in ['hud','model']:
 frames=sorted(set(r['frame_maps'][part].values()))
 for i,f in enumerate(frames):render(part,f,W/part/f'{f:04d}.png');print('PROGRESS',part,i+1,len(frames),flush=True)
print('RENDER_COMPLETE',round(time.time()-start,2),flush=True)
