"""Encode each completed scene directly in the episode assets package."""
import json,os,time,subprocess,hashlib
from pathlib import Path
from PIL import Image
O=Path(__file__).resolve().parent;W=O/'_render';FF='/opt/homebrew/bin/ffmpeg';FP='/opt/homebrew/bin/ffprobe'
r=json.loads((O/'scene-verification.json').read_text());m=json.loads((O/'scene-manifest.json').read_text())
for folder in ['previews','stills','safe-zone-proofs']:(O/folder).mkdir(exist_ok=True)
report={}
def run(cmd):subprocess.run(cmd,check=True)
def valid(path):
    try:
        with Image.open(path) as im:im.verify()
        return True
    except (OSError,SyntaxError):return False
def wait(path):
    while not valid(path):time.sleep(2)
def compose_frame(f):
    bg=Image.open(W/'background.png').convert('RGB');model=Image.open(W/'model'/f"{r['frame_maps']['model'][str(f)]:04d}.png").convert('RGB');hud=Image.open(W/'hud'/f"{r['frame_maps']['hud'][str(f)]:04d}.png").convert('RGBA')
    assert bg.size==(2160,990) and model.size==(2160,1310) and hud.size==(2160,2300)
    frame=Image.new('RGBA',(2160,2300));frame.paste(bg,(0,0));frame.paste(model,(0,990));frame.alpha_composite(hud);return frame.convert('RGB')
project=next(p for p in O.parents if (p/'AGENTS.md').exists())
template=Image.open(project/'youtube-series/assets/all-platforms-safe-zone-template-1080x1920.png').convert('RGBA').resize((2160,3840),Image.Resampling.NEAREST)
for clip in m['clips']:
    for part in ['model','hud']:
        folder=W/'sequence'/part;folder.mkdir(parents=True,exist_ok=True)
        for f in range(clip['start'],clip['end']+1):
            source=W/part/f"{r['frame_maps'][part][str(f)]:04d}.png";wait(source)
            dest=folder/f'{f:04d}.png'
            if not dest.exists():os.link(source,dest)
    wait(W/'background.png')
    movie=O/clip['file'];temp=movie.with_name(movie.stem+'.part.mp4')
    run([FF,'-y','-v','warning','-framerate','24','-start_number',str(clip['start']),'-i',str(W/'sequence/model/%04d.png'),'-framerate','24','-start_number',str(clip['start']),'-i',str(W/'sequence/hud/%04d.png'),'-loop','1','-framerate','24','-i',str(W/'background.png'),'-filter_complex','[2:v][0:v]vstack=inputs=2[plate];[plate][1:v]overlay=shortest=1:format=rgb,scale=iw:ih:out_color_matrix=bt709:out_range=tv,format=yuv420p[v]','-map','[v]','-frames:v',str(clip['frames']),'-an','-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',str(temp)])
    os.replace(temp,movie)
    preview=O/'previews'/movie.name
    run([FF,'-y','-v','warning','-i',str(movie),'-vf','scale=1080:1150:flags=lanczos','-an','-c:v','libx264','-preset','medium','-crf','18','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',str(preview)])
    for path in [movie,preview]:
        p=json.loads(subprocess.check_output([FP,'-v','error','-count_frames','-show_streams','-show_format','-of','json',str(path)]));v=p['streams'][0]
        assert len(p['streams'])==1 and v['codec_type']=='video'
        assert v['avg_frame_rate']=='24/1' and int(v['nb_read_frames'])==clip['frames']
        assert (v['width'],v['height'])==((2160,2300) if path==movie else (1080,1150))
        assert abs(float(p['format']['duration'])-clip['seconds'])<.001 and abs(float(p['format']['start_time']))<.001
        run([FF,'-v','error','-i',str(path),'-f','null','-'])
        report[str(path.relative_to(O))]={'resolution':[v['width'],v['height']],'frames':clip['frames'],'seconds':clip['seconds'],'fps':24,'audio':False,'decode':'passed','sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    for f,label in [(clip['start'],'first'),(clip['end'],'last')]:
        frame=compose_frame(f);frame.save(O/'stills'/f'{movie.stem}-{label}.png')
        master=Image.new('RGBA',(2160,3840),(27,22,29,255));master.paste(frame,(0,0));Image.alpha_composite(master,template).convert('RGB').save(O/'safe-zone-proofs'/f'{movie.stem}-{label}.png')
    (O/'export-verification.json').write_text(json.dumps(report,indent=2))
    print('CLIP_VERIFIED',movie.name,flush=True)
print('ALL_SIX_CLIPS_VERIFIED',flush=True)
