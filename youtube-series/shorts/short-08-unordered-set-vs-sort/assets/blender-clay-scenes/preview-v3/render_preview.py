"""10%-dimension motion previews only. No native/full-resolution render path."""
import bpy,json,hashlib,os,subprocess,time
from pathlib import Path
O=Path(__file__).resolve().parent;D=O/'_render';D.mkdir(exist_ok=True)
R=json.loads((O/'scene-verification.json').read_text())
assert not R['violations'] and not R['all_value_shell_intersections'] and not R['sort_aabb_intersections']
assert R['source_sha256']==hashlib.sha256((O/'short-08-clay.blend').read_bytes()).hexdigest()
M=json.loads((O/'scene-manifest.json').read_text())
bpy.ops.wm.open_mainfile(filepath=str(O/'short-08-clay.blend'));s=bpy.context.scene
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='OPTIX'
assert any(d.use for d in prefs.devices)
bpy.ops.object.select_all(action='DESELECT')
fonts=[o for o in s.objects if o.type=='FONT']
for o in fonts:o.hide_viewport=False;o.select_set(True)
if fonts:bpy.context.view_layer.objects.active=fonts[0];bpy.ops.object.convert(target='MESH')
s.render.resolution_x=2160;s.render.resolution_y=2300;s.render.resolution_percentage=10
s.render.use_border=False;s.render.use_crop_to_border=False;s.render.use_persistent_data=True
s.render.film_transparent=False;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB'
s.render.image_settings.compression=15;s.cycles.device='GPU';s.cycles.samples=16;s.cycles.adaptive_threshold=.04
s.cycles.use_denoising=True;s.cycles.seed=0;s.cycles.use_animated_seed=False
frames=D/'frames';frames.mkdir(exist_ok=True);seen={};reports=[]
def status(**kw):(D/'status.json').write_text(json.dumps({'updated_unix':time.time(),**kw},indent=2))
try:
 for ci,c in enumerate(M['clips'],1):
  sequence=D/f'sequence-{ci}';sequence.mkdir(exist_ok=True)
  for f in range(c['start'],c['end']+1,2):
   key=(R['maps']['model'][str(f)],R['maps']['hud'][str(f)])
   seen.setdefault(key,f);canonical=seen[key];p=frames/f'{canonical:04d}.png'
   if not p.exists():
    s.frame_set(f);s.render.filepath=str(p);bpy.ops.render.render(write_still=True)
   for j in (f-c['start'],f-c['start']+1):
    dest=sequence/f'{j:04d}.png'
    if not dest.exists():dest.symlink_to(p)
   status(state='rendering',frame=f,total_frames=s.frame_end,clips_complete=ci-1,clips_total=7)
  out=O/c['file'];part=out.with_suffix('.part.mp4')
  subprocess.run(['ffmpeg','-y','-v','error','-framerate','24','-i',str(sequence/'%04d.png'),'-frames:v',str(c['frames']),'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-movflags','+faststart','-an',str(part)],check=True)
  probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(part)]))
  v=probe['streams'][0]
  assert len(probe['streams'])==1 and (v['width'],v['height'])==(216,230)
  assert v['r_frame_rate']=='24/1' and int(v['nb_read_frames'])==c['frames']
  assert abs(float(probe['format']['duration'])-c['seconds'])<.01
  assert float(v.get('start_time',0))==0
  subprocess.run(['ffmpeg','-v','error','-i',str(part),'-f','null','-'],check=True)
  os.replace(part,out);reports.append({'file':out.name,'width':216,'height':230,'fps':24,'frames':c['frames'],'seconds':c['seconds'],'fully_decoded':True,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()})
  (O/'preview-verification.json').write_text(json.dumps(reports,indent=2))
  status(state='rendering',clips_complete=ci,clips_total=7)
 status(state='complete',clips_complete=7,clips_total=7,resolution=[216,230],full_resolution_rendered=False)
 print('ALL_TINY_PREVIEWS_COMPLETE',flush=True)
except Exception as e:
 status(state='failed',error=repr(e),clips_complete=len(reports),clips_total=7);raise
