"""Render only the eight 10% storyboard PNGs."""
import bpy,json,hashlib,time
from pathlib import Path
O=Path(__file__).resolve().parent
R=json.loads((O/'storyboard-verification.json').read_text());assert not R['text_violations'] and not R['value_overlaps']
M=json.loads((O/'storyboard-manifest.json').read_text())
bpy.ops.wm.open_mainfile(filepath=str(O/'short-08-storyboard.blend'));s=bpy.context.scene
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='OPTIX'
assert any(d.use for d in prefs.devices)
bpy.ops.object.select_all(action='DESELECT');fonts=[o for o in s.objects if o.type=='FONT']
for o in fonts:o.hide_viewport=False;o.select_set(True)
if fonts:bpy.context.view_layer.objects.active=fonts[0];bpy.ops.object.convert(target='MESH')
s.render.resolution_percentage=10;s.render.use_persistent_data=True;s.render.use_border=False;s.render.film_transparent=False
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB'
s.cycles.device='GPU';s.cycles.samples=32;s.cycles.use_denoising=True;s.cycles.seed=0;s.cycles.use_animated_seed=False
reports=[]
for slide in M['slides']:
 s.frame_set(slide['slide']);p=O/slide['file'];s.render.filepath=str(p);bpy.ops.render.render(write_still=True)
 im=bpy.data.images.load(str(p),check_existing=False);assert tuple(im.size)==(216,230);bpy.data.images.remove(im)
 reports.append({'file':p.name,'size':[216,230],'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 (O/'render-verification.json').write_text(json.dumps(reports,indent=2))
print('EIGHT_STORYBOARD_STILLS_COMPLETE',flush=True)
