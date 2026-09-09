from pathlib import Path
from PIL import Image, ImageChops, ImageStat
import json, subprocess, shutil

root = Path('/Users/keremkazan/Documents/Codex/2026-09-05/go-t')
out = root / 'outputs/short-06-blender-wide'
work = root / 'work/short-06-blender-wide'
source = root / 'outputs/short-06-blender-v2'

def run(args):
    return subprocess.run(args, check=True, capture_output=True, text=True)

frames = sorted((work / 'frames').glob('frame_*.png'))
assert len(frames) == 456
run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-framerate', '24', '-start_number', '1', '-i', str(work / 'frames/frame_%04d.png'), '-frames:v', '456', '-an', '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(out / 'cpp-data-layout-clean-wide.mp4')])
print('Native video encoded', flush=True)
run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(out / 'cpp-data-layout-clean-wide.mp4'), '-vf', 'scale=1180:1176:flags=lanczos', '-an', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(out / 'preview.mp4')])
report = {'camera': json.loads((out / 'camera-verification.json').read_text()), 'videos': {}, 'central_crop_comparisons': {}}
for name, dims in [('cpp-data-layout-clean-wide.mp4', [2360, 2352]), ('preview.mp4', [1180, 1176])]:
    info = json.loads(run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_name,codec_type,width,height,r_frame_rate,nb_frames:format=duration,size', '-of', 'json', str(out / name)]).stdout)
    assert len(info['streams']) == 1
    v = info['streams'][0]
    assert v['codec_type'] == 'video' and v['r_frame_rate'] == '24/1' and v['nb_frames'] == '456'
    assert [v['width'], v['height']] == dims
    assert abs(float(info['format']['duration']) - 19) < .001
    run(['ffmpeg', '-v', 'error', '-i', str(out / name), '-f', 'null', '-'])
    report['videos'][name] = info
for path in sorted((out / 'stills').glob('*.png')):
    original = Image.open(source / 'stills' / path.name).convert('RGB')
    wide = Image.open(path).convert('RGB')
    assert wide.size == (2360, 2352)
    diff = ImageChops.difference(original, wide.crop((100, 0, 2260, 2352)))
    means = ImageStat.Stat(diff).mean
    assert max(means) < 2, (path.name, means)
    report['central_crop_comparisons'][path.name] = {'mean_absolute_rgb_difference_out_of_255': means}
report['decoded_without_errors'] = True
report['note'] = 'Camera projection preserves pixel scale and placement. Tiny raster differences come from rerendering at a different image width; original models, animation, lights, materials and code are unchanged.'
(out / 'export-verification.json').write_text(json.dumps(report, indent=2))
for name in ['widen_scene.py', 'render_animation.py', 'finish.py']:
    shutil.copy2(work / name, out / name)
print('VERIFIED', json.dumps(report), flush=True)
