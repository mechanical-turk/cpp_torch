"""Render the revised upper region; unchanged lower models reuse native source pixels."""
import bpy,json,time
from pathlib import Path
root=Path('/Users/keremkazan/Documents/Codex/2026-09-05/go-t')
out=root/'outputs/short-06-blender-motion';work=root/'work/short-06-blender-motion'
(work/'upper').mkdir(exist_ok=True)
report=json.loads((out/'scene-verification.json').read_text())
unique=sorted(set(report['frame_map'].values()))
s=bpy.context.scene;s.render.use_border=True;s.render.use_crop_to_border=True
s.render.border_min_x=0;s.render.border_max_x=1
s.render.border_min_y=(2352-1100)/2352;s.render.border_max_y=1
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB'
start=time.monotonic()
for i,f in enumerate(unique):
    path=work/f'upper/frame_{f:04}.png'
    if not path.exists():
        s.frame_set(f);s.render.filepath=str(path);bpy.ops.render.render(write_still=True)
    print(f'PROGRESS {i+1}/{len(unique)} frame={f} elapsed={time.monotonic()-start:.1f}s',flush=True)
print('RENDER_COMPLETE',flush=True)
