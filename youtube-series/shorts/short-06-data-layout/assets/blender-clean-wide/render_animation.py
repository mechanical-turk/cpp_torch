"""Render every moving frame at native resolution; reuse exact static holds."""
import bpy, os, sys, argparse, time, json
p=argparse.ArgumentParser();p.add_argument('--frames',required=True);p.add_argument('--stills',required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);os.makedirs(a.frames,exist_ok=True);os.makedirs(a.stills,exist_ok=True)
s=bpy.context.scene;s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=32
s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB'
def source(f):
    if f<=18:return 1
    if f<=35:return f
    if f<=57:return 35
    if f<=72:return f
    if f<=166:return 72
    if f<=242:return f
    if f<=288:return 242
    if f<=360:return 289
    return 361
mapping={f:source(f) for f in range(1,457)}
unique=sorted(set(mapping.values()))
start=time.monotonic()
for i,f in enumerate(unique):
    dest=os.path.join(a.frames,f'frame_{f:04}.png')
    if not os.path.exists(dest):
        s.frame_set(f);s.render.filepath=dest;bpy.ops.render.render(write_still=True)
    print(f'PROGRESS {i+1}/{len(unique)} frame={f} elapsed={time.monotonic()-start:.1f}s',flush=True)
for f,src in mapping.items():
    dest=os.path.join(a.frames,f'frame_{f:04}.png')
    if f!=src and not os.path.exists(dest):os.link(os.path.join(a.frames,f'frame_{src:04}.png'),dest)
import shutil
for name,f in [('01-hook',1),('02-score-spacing',72),('03-extraction',200),('04-split-layout',242),('05-measured-result',289),('06-next-test',361)]:
    shutil.copy2(os.path.join(a.frames,f'frame_{f:04}.png'),os.path.join(a.stills,name+'.png'))
with open(os.path.join(a.stills,'render-manifest.json'),'w') as fp:
    json.dump({'width':s.render.resolution_x,'height':s.render.resolution_y,'fps':24,'frames':456,'duration_seconds':19,'native_rendered_frames':len(unique),'holds_reused':456-len(unique),'frame_map':mapping},fp,indent=2)
print('RENDER_COMPLETE',flush=True)
