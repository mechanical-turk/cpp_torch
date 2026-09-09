import bpy,json,subprocess,os,time
from pathlib import Path
O=Path(__file__).resolve().parent;W=O/'_render/review-v7';W.mkdir(parents=True,exist_ok=True);(O/'review').mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(O/'false-sharing-clay.blend'));s=bpy.context.scene;r=json.loads((O/'scene-verification.json').read_text());mapping=r['frame_maps']['model']
p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='METAL';p.kernel_optimization_level='OFF';p.metalrt='OFF';p.get_devices()
for d in p.devices:d.use=d.type=='METAL'
s.cycles.device='GPU';s.cycles.samples=16;s.cycles.adaptive_threshold=.025;s.render.resolution_percentage=40;s.render.use_border=False;s.render.use_persistent_data=True
frames=sorted({mapping[str(f)] for f in range(1,193)});print('REVIEW_STATES',len(frames),flush=True)
for i,f in enumerate(frames):
 s.frame_set(f);s.render.filepath=str(W/f'{f:04d}.png');bpy.ops.render.render(write_still=True);print('REVIEW_PROGRESS',i+1,len(frames),flush=True)
seq=W/'sequence';seq.mkdir(exist_ok=True)
for i,f in enumerate(range(1,193),1):
 dest=seq/f'{i:04d}.png'
 if dest.exists():dest.unlink()
 os.link(W/f'{mapping[str(f)]:04d}.png',dest)
subprocess.run(['/opt/homebrew/bin/ffmpeg','-y','-v','warning','-framerate','24','-i',str(seq/'%04d.png'),'-frames:v','192','-an','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(O/'review/01-crowded-opening-v7.mp4')],check=True)
print('REVIEW_VIDEO_READY',flush=True)
