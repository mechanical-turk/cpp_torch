import bpy,json,time
from pathlib import Path
R=Path('/Users/keremkazan/Documents/Codex/2026-09-05/go-t');O=R/'outputs/clay-animation-v2';W=R/'work/clay-animation-v2'
bpy.ops.wm.open_mainfile(filepath=str(O/'cpp-data-layout-clay-animation.blend'))
s=bpy.context.scene;p=bpy.context.preferences.addons['cycles'].preferences
p.compute_device_type='METAL';p.kernel_optimization_level='OFF';p.metalrt='OFF';p.get_devices()
for d in p.devices:d.use=d.type=='METAL'
s.cycles.device='GPU';s.render.use_persistent_data=True;s.render.resolution_percentage=100
s.render.use_border=True;s.render.use_crop_to_border=True;s.render.border_min_x=0;s.render.border_max_x=1
s.render.image_settings.file_format='PNG';s.render.image_settings.compression=15
model=bpy.data.collections['01 • Clay models'];hud=bpy.data.collections['02 • Code and results'];floor=s.objects['Continuous clay studio ground']
for mat in floor.data.materials:
    for node in mat.node_tree.nodes:
        if node.type=='AMBIENT_OCCLUSION':node.samples=4
report=json.loads((O/'scene-verification.json').read_text());maps=report['frame_maps'];split=report['partition_y'];height=report['resolution'][1];start=time.time()
for part in ['lower','upper']:(W/part).mkdir(exist_ok=True)
def render(part,frame,path):
    if path.exists():return
    s.frame_set(frame)
    hud.hide_render=part!='upper';model.hide_render=part=='upper';floor.hide_render=part=='upper'
    s.render.film_transparent=part=='upper';s.render.image_settings.color_mode='RGBA' if part=='upper' else 'RGB'
    if part=='lower':
        s.render.border_min_y=0;s.render.border_max_y=(height-split)/height
        s.cycles.samples=96 if frame==1 else 256 if frame==242 else 32
        s.cycles.adaptive_threshold=.004 if frame==242 else .012 if frame==1 else .02
    else:
        s.render.border_min_y=(height-split)/height;s.render.border_max_y=1
        s.cycles.samples=64 if part=='upper' else 128;s.cycles.adaptive_threshold=.008
    s.render.filepath=str(path);t=time.time();bpy.ops.render.render(write_still=True)
    print('FRAME_DONE',json.dumps({'part':part,'frame':frame,'seconds':round(time.time()-t,2),'elapsed':round(time.time()-start,2)}),flush=True)
render('blank',340,W/'background-upper.png')
for part in ['upper','lower']:
    frames=sorted(set(maps[part].values()))
    for f in frames:render(part,f,W/part/f'{f:04d}.png')
    print('PART_DONE',part,len(frames),flush=True)
print('ALL_LAYERS_DONE',round(time.time()-start,2),flush=True)
