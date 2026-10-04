"""Compare one native moving pose at 96 and 48 samples, with split composition."""
import os
os.environ['CYCLES_METAL_DISABLE_BINARY_ARCHIVES']='1'
import bpy,time,subprocess
from pathlib import Path
O=Path(__file__).resolve().parent;D=O/'_render';P=D/'native-stills';Q=D/'qa';Q.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(O/'short-08-clay.blend'));s=bpy.context.scene
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.kernel_optimization_level='OFF';prefs.metalrt='OFF';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='METAL'
s.render.resolution_percentage=100;s.render.use_persistent_data=False;s.render.image_settings.file_format='PNG';s.render.image_settings.compression=15;s.cycles.seed=0;s.cycles.use_animated_seed=False;s.cycles.use_denoising=True
model=bpy.data.collections['01 • Clay models'];hud=bpy.data.collections['02 • Code and results'];ground=s.objects['Continuous clay studio ground']
bpy.ops.object.select_all(action='DESELECT');fonts=[o for o in s.objects if o.type=='FONT']
for o in fonts:o.hide_viewport=False;o.select_set(True)
if fonts:bpy.context.view_layer.objects.active=fonts[0];bpy.ops.object.convert(target='MESH')
s.frame_set(357)
def render(path,samples,border=None,text=False):
 if path.exists():return
 hud.hide_render=not text;model.hide_render=text;ground.hide_render=text;s.render.film_transparent=text;s.render.image_settings.color_mode='RGBA' if text else 'RGB';s.cycles.device='CPU' if text else 'GPU';s.cycles.samples=samples;s.cycles.adaptive_threshold=.007 if samples>=96 else .012
 s.render.use_border=border is not None;s.render.use_crop_to_border=border is not None
 if border:
  s.render.border_min_x=0;s.render.border_max_x=1;s.render.border_min_y=border[0];s.render.border_max_y=border[1]
 s.render.filepath=str(path);t=time.time();bpy.ops.render.render(write_still=True);print('QA_RENDER',path.name,time.time()-t,flush=True)
render(P/'0357-plate.png',96)
render(Q/'0357-lower-48.png',48,(0,(1300+.01)/2300))
render(D/'background.png',128,((1300+.01)/2300,1))
render(P/'0357-hud.png',64,text=True)
subprocess.run(['/opt/homebrew/bin/python3',str(O/'compose.py'),str(P/'0357-plate.png'),str(P/'0357-hud.png'),str(P/'0357.png')],check=True)
print('QA_COMPLETE',flush=True)
