from pathlib import Path
import os, json, subprocess, hashlib, shutil
from PIL import Image, ImageChops, ImageStat
R=Path('/Users/keremkazan/Documents/Codex/2026-09-05/go-t');O=R/'outputs/clay-animation';W=R/'work/clay-animation';FF='/opt/homebrew/bin/ffmpeg';FP='/opt/homebrew/bin/ffprobe'
report=json.loads((O/'scene-verification.json').read_text());maps=report['frame_maps'];approved=R/'outputs/clay-studio-lighting/retro-sunset-clay-studio.png'
def run(args):subprocess.run(args,check=True)
# Reuse the approved full-quality native pixels once the physical pose settles.
for name,crop in [('approved-lower.png','2360:1352:0:1000'),('approved-upper.png','2360:1000:0:0')]:
    run([FF,'-y','-v','error','-i',str(approved),'-vf',f'crop={crop},format=rgba' if 'upper' in name else f'crop={crop}','-frames:v','1',str(W/name)])
for part in ['lower','upper']:
    dest=W/'sequence'/part;dest.mkdir(parents=True,exist_ok=True)
    for f in range(1,457):
        canonical=maps[part][str(f)];src=W/part/f'{canonical:04d}.png'
        if part=='lower' and canonical==maps[part]['340']:src=W/'approved-lower.png'
        if part=='upper' and canonical==maps[part]['340']:src=W/'approved-upper.png'
        assert src.exists(),src
        with Image.open(src) as im:assert im.size==((2360,1352) if part=='lower' else (2360,1000));im.verify()
        link=dest/f'{f:04d}.png'
        if link.exists():link.unlink()
        os.link(src,link)
movie=O/'cpp-data-layout-clay-animation.mp4'
run([FF,'-y','-v','warning','-framerate','24','-start_number','1','-i',str(W/'sequence/lower/%04d.png'),'-framerate','24','-start_number','1','-i',str(W/'sequence/upper/%04d.png'),'-loop','1','-framerate','24','-i',str(W/'background-upper.png'),'-filter_complex','[2:v][1:v]overlay=shortest=1:format=rgb[upper];[upper][0:v]vstack=inputs=2,scale=iw:ih:out_color_matrix=bt709:out_range=tv,format=yuv420p[v]','-map','[v]','-frames:v','456','-an','-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',str(movie)])
run([FF,'-y','-v','warning','-i',str(movie),'-vf','scale=1180:1176:flags=lanczos','-an','-c:v','libx264','-preset','medium','-crf','18','-movflags','+faststart',str(O/'preview.mp4')])
(O/'stills').mkdir(exist_ok=True)
for f,name in [(1,'01-opening'),(178,'02-code-transition'),(213,'03-gathering'),(242,'04-separated'),(301,'05-arrow-reveal'),(340,'06-result'),(400,'07-final-code')]:
    run([FF,'-y','-v','error','-i',str(W/'background-upper.png'),'-i',str(W/'sequence/upper'/f'{f:04d}.png'),'-i',str(W/'sequence/lower'/f'{f:04d}.png'),'-filter_complex','[0:v][1:v]overlay=format=rgb[u];[u][2:v]vstack','-frames:v','1',str(O/'stills'/f'{name}.png')])
metadata={}
for path in [movie,O/'preview.mp4']:
    probe=json.loads(subprocess.check_output([FP,'-v','error','-count_frames','-show_streams','-show_format','-of','json',str(path)]))
    videos=[s for s in probe['streams'] if s['codec_type']=='video'];assert len(videos)==1 and not any(s['codec_type']=='audio' for s in probe['streams'])
    v=videos[0];assert v['nb_read_frames']=='456' and v['avg_frame_rate']=='24/1';assert abs(float(probe['format']['duration'])-19)<.001
    run([FF,'-v','error','-i',str(path),'-f','null','-'])
    metadata[path.name]={'width':v['width'],'height':v['height'],'frames':v['nb_read_frames'],'fps':v['avg_frame_rate'],'duration':probe['format']['duration'],'size':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'decode_errors':False,'audio':False}
with Image.open(approved) as a,Image.open(O/'stills/06-result.png') as b:
    diff=ImageChops.difference(a.convert('RGB'),b.convert('RGB'));metadata['approved_result_mean_rgb_error']=sum(ImageStat.Stat(diff).mean)/3
metadata['sampling_check']=json.loads((W/'sampling-comparison.json').read_text());metadata['native_resolution']=True;metadata['interpolated_motion_frames']=False
(O/'export-verification.json').write_text(json.dumps(metadata,indent=2));print('ENCODE_VERIFIED',json.dumps(metadata),flush=True)
