from pathlib import Path
import os,json,subprocess,hashlib
from PIL import Image
R=Path('/Users/keremkazan/Documents/Codex/2026-09-05/go-t');O=R/'outputs/clay-animation-v2';W=R/'work/clay-animation-v2';FF='/opt/homebrew/bin/ffmpeg';FP='/opt/homebrew/bin/ffprobe'
report=json.loads((O/'scene-verification.json').read_text());maps=report['frame_maps'];frames=report['frames'];fps=report['fps'];width,height=report['resolution'];split=report['partition_y']
def run(args):subprocess.run(args,check=True)
for part in ['lower','upper']:
    dest=W/'sequence'/part;dest.mkdir(parents=True,exist_ok=True)
    for f in range(1,frames+1):
        canonical=maps[part][str(f)];src=W/part/f'{canonical:04d}.png';assert src.exists(),src
        with Image.open(src) as im:assert im.size==(width,height-split if part=='lower' else split);im.verify()
        link=dest/f'{f:04d}.png'
        if link.exists():link.unlink()
        os.link(src,link)
movie=O/'cpp-data-layout-clay-animation.mp4'
run([FF,'-y','-v','warning','-framerate',str(fps),'-start_number','1','-i',str(W/'sequence/lower/%04d.png'),'-framerate',str(fps),'-start_number','1','-i',str(W/'sequence/upper/%04d.png'),'-loop','1','-framerate',str(fps),'-i',str(W/'background-upper.png'),'-filter_complex','[2:v][1:v]overlay=shortest=1:format=rgb[upper];[upper][0:v]vstack=inputs=2,scale=iw:ih:out_color_matrix=bt709:out_range=tv,format=yuv420p[v]','-map','[v]','-frames:v',str(frames),'-an','-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',str(movie)])
run([FF,'-y','-v','warning','-i',str(movie),'-vf','scale=1180:1176:flags=lanczos','-an','-c:v','libx264','-preset','medium','-crf','18','-movflags','+faststart',str(O/'preview.mp4')])
(O/'stills').mkdir(exist_ok=True)
for f,name in [(1,'01-opening'),(178,'02-code-transition'),(202,'03-gathering'),(242,'04-separated'),(301,'05-arrow-reveal'),(frames,'06-final-result')]:
    run([FF,'-y','-v','error','-i',str(W/'background-upper.png'),'-i',str(W/'sequence/upper'/f'{f:04d}.png'),'-i',str(W/'sequence/lower'/f'{f:04d}.png'),'-filter_complex','[0:v][1:v]overlay=format=rgb[u];[u][2:v]vstack','-frames:v','1',str(O/'stills'/f'{name}.png')])
metadata={}
for path in [movie,O/'preview.mp4']:
    probe=json.loads(subprocess.check_output([FP,'-v','error','-count_frames','-show_streams','-show_format','-of','json',str(path)]))
    videos=[s for s in probe['streams'] if s['codec_type']=='video'];assert len(videos)==1 and not any(s['codec_type']=='audio' for s in probe['streams'])
    v=videos[0];assert int(v['nb_read_frames'])==frames and v['avg_frame_rate']==f'{fps}/1';assert abs(float(probe['format']['duration'])-frames/fps)<.001
    assert (v['width'],v['height'])==((width,height) if path==movie else (1180,1176))
    run([FF,'-v','error','-i',str(path),'-f','null','-'])
    metadata[path.name]={'width':v['width'],'height':v['height'],'frames':v['nb_read_frames'],'fps':v['avg_frame_rate'],'duration':probe['format']['duration'],'size':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'decode_errors':False,'audio':False}
assert maps['upper'][str(frames)]==maps['upper']['340'] and maps['lower'][str(frames)]==maps['lower']['340']
metadata.update({'native_resolution':True,'interpolated_motion_frames':False,'ends_on_benchmark':True,'return_to_code_removed':True,'code_font_multiplier':1.5,'code_top_origin_shift_px':100,'gradient_highlight_shift_px':100,'uniform_geometry_verified':True})
(O/'export-verification.json').write_text(json.dumps(metadata,indent=2));print('ENCODE_VERIFIED',json.dumps(metadata),flush=True)
