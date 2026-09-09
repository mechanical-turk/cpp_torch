import bpy, json, time
from pathlib import Path
R=Path('/Users/keremkazan/Documents/Codex/2026-09-05/go-t');O=R/'outputs/clay-animation';W=R/'work/clay-animation'
bpy.ops.wm.open_mainfile(filepath=str(O/'cpp-data-layout-clay-animation.blend'))
s=bpy.context.scene;p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='METAL';p.kernel_optimization_level='OFF';p.metalrt='OFF';p.get_devices()
for d in p.devices:d.use=d.type=='METAL'
s.cycles.device='GPU';s.render.use_persistent_data=True;s.render.resolution_percentage=100;s.render.use_border=True;s.render.use_crop_to_border=True;s.render.border_min_x=0;s.render.border_max_x=1
model=bpy.data.collections['01 • Clay models'];hud=bpy.data.collections['02 • Code and results'];floor=s.objects['Continuous clay studio ground']
for mat in floor.data.materials:
    for node in mat.node_tree.nodes:
        if node.type=='AMBIENT_OCCLUSION':node.samples=4
report=json.loads((O/'scene-verification.json').read_text());maps=report['frame_maps'];start=time.time()
for part in ['lower','upper']:(W/part).mkdir(exist_ok=True)
def config(part):
    if part=='lower':
        hud.hide_render=True;model.hide_render=False;floor.hide_render=False;s.render.film_transparent=False;s.render.image_settings.color_mode='RGB'
        s.render.border_min_y=0;s.render.border_max_y=1352/2352;s.cycles.samples=32;s.cycles.adaptive_threshold=.02
    else:
        hud.hide_render=part!='upper';model.hide_render=part=='upper';floor.hide_render=part=='upper';s.render.film_transparent=part=='upper';s.render.image_settings.color_mode='RGBA' if part=='upper' else 'RGB'
        s.render.border_min_y=1352/2352;s.render.border_max_y=1;s.cycles.samples=64 if part=='upper' else 128;s.cycles.adaptive_threshold=.008

def render(part,frame,path,override_samples=None):
    if path.exists():return
    s.frame_set(frame);config(part)
    if part=='lower' and frame in [1,242]:s.cycles.samples=96
    if override_samples:s.cycles.samples=override_samples
    s.render.filepath=str(path);t=time.time();bpy.ops.render.render(write_still=True)
    print('FRAME_DONE',json.dumps({'part':part,'frame':frame,'seconds':round(time.time()-t,2),'elapsed':round(time.time()-start,2)}),flush=True)
render('blank',340,W/'background-upper.png')
render('lower',1,W/'lower/0001.png')
render('upper',1,W/'upper/0001.png')
render('lower',1,W/'optimized-probe.png')
render('lower',1,W/'probe-32.png',32)
print('PROBE_READY',flush=True)
for part in ['lower','upper']:
    frames=sorted(set(maps[part].values()))
    for f in frames:render(part,f,W/part/f'{f:04d}.png')
    print('PART_DONE',part,len(frames),flush=True)
print('ALL_LAYERS_DONE',round(time.time()-start,2),flush=True)
