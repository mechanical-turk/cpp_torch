"""Exactly seven native keyframes. Never renders animation or starts a supervisor."""
import bpy,json,time,os,sys
from pathlib import Path
O=Path(__file__).resolve().parent;D=O/'_render';D.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(O/'short-08-keyframes.blend'));s=bpy.context.scene
r=json.loads((O/'scene-verification.json').read_text());assert not r['violations']
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='OPTIX'
assert any(d.use for d in prefs.devices)
print('DEVICE',[(d.name,d.type,d.use) for d in prefs.devices],flush=True)
s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.compression=15;s.render.use_border=False;s.render.use_crop_to_border=False;s.render.use_persistent_data=False;s.cycles.seed=0;s.cycles.use_animated_seed=False;s.cycles.use_denoising=True
model=bpy.data.collections['01 • Clay models'];hud=bpy.data.collections['02 • Code and results'];ground=s.objects['Continuous clay studio ground']
bpy.ops.object.select_all(action='DESELECT');fonts=[o for o in s.objects if o.type=='FONT']
for o in fonts:o.hide_viewport=False;o.select_set(True)
if fonts:bpy.context.view_layer.objects.active=fonts[0];bpy.ops.object.convert(target='MESH')
report={'blender':bpy.app.version_string,'device':'OPTIX','gpu':[d.name for d in prefs.devices if d.use],'renders':[],'stills_only':True}
for item in json.loads((O/'keyframes-manifest.json').read_text())['frames']:
 f=item['frame'];s.frame_set(f)
 for part in ['plate','hud']:
  path=D/f'{f:02d}-{part}.png'
  if path.exists():continue
  text=part=='hud';hud.hide_render=not text;model.hide_render=text;ground.hide_render=text
  s.cycles.device='CPU' if text else 'GPU';s.cycles.samples=64 if text else 96;s.cycles.adaptive_threshold=.007
  s.render.film_transparent=text;s.render.image_settings.color_mode='RGBA' if text else 'RGB'
  tmp=path.with_name(path.stem+'.part.png');s.render.filepath=str(tmp);t=time.time();bpy.ops.render.render(write_still=True);os.replace(tmp,path)
  timing={'frame':f,'part':part,'seconds':time.time()-t,'device':s.cycles.device,'samples':s.cycles.samples}
  report['renders'].append(timing);(O/'render-report.json').write_text(json.dumps(report,indent=2));print('KEYFRAME_RENDER',json.dumps(timing),flush=True)
report['complete']=True;(O/'render-report.json').write_text(json.dumps(report,indent=2));print('SEVEN_KEYFRAMES_RENDERED_NO_VIDEO',flush=True)
