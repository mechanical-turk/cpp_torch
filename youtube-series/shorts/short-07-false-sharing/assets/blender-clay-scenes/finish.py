import json,os,subprocess,hashlib,argparse,time
from pathlib import Path
from PIL import Image
P=argparse.ArgumentParser();P.add_argument('--work',default=None);a=P.parse_args();O=Path(__file__).resolve().parent;W=Path(a.work) if a.work else O/'_render/current';assert W.resolve().is_relative_to(O.resolve()), 'Render work must stay inside this Content HQ assets package';FF='/opt/homebrew/bin/ffmpeg';FP='/opt/homebrew/bin/ffprobe'
r=json.loads((O/'scene-verification.json').read_text());manifest=json.loads((O/'scene-manifest.json').read_text());split=r['split_y'];verified={}
for folder in ['previews','stills']:(O/folder).mkdir(exist_ok=True)
def run(cmd):subprocess.run(cmd,check=True)
for clip in manifest['clips']:
 for part in ['model','hud']:
  dest=W/'sequence'/part;dest.mkdir(parents=True,exist_ok=True)
  for f in range(clip['start'],clip['end']+1):
   source=W/part/f"{r['frame_maps'][part][str(f)]:04d}.png";target=dest/f'{f:04d}.png'
   while True:
    try:
     with Image.open(source) as im: im.verify()
     break
    except (FileNotFoundError,OSError,SyntaxError):time.sleep(2)
   if not target.exists():os.link(source,target)
 name=clip['file'];movie=O/name
 run([FF,'-y','-v','warning','-framerate','24','-start_number',str(clip['start']),'-i',str(W/'sequence/model/%04d.png'),'-framerate','24','-start_number',str(clip['start']),'-i',str(W/'sequence/hud/%04d.png'),'-loop','1','-framerate','24','-i',str(W/'background.png'),'-filter_complex','[2:v][1:v]overlay=shortest=1:format=rgb[upper];[upper][0:v]vstack=inputs=2,scale=iw:ih:out_color_matrix=bt709:out_range=tv,format=yuv420p[v]','-map','[v]','-frames:v',str(clip['frames']),'-an','-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',str(movie)])
 preview=O/'previews'/name
 run([FF,'-y','-v','warning','-i',str(movie),'-vf','scale=1180:1176:flags=lanczos','-an','-c:v','libx264','-preset','medium','-crf','18','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',str(preview)])
 for path in [movie,preview]:
  probe=json.loads(subprocess.check_output([FP,'-v','error','-count_frames','-show_streams','-show_format','-of','json',str(path)]));v=probe['streams'][0]
  assert len(probe['streams'])==1 and v['codec_type']=='video';assert v['avg_frame_rate']=='24/1' and int(v['nb_read_frames'])==clip['frames'];assert abs(float(probe['format']['duration'])-clip['seconds'])<.001;assert abs(float(probe['format']['start_time']))<.001
  assert (v['width'],v['height'])==((2360,2352) if path==movie else (1180,1176))
  run([FF,'-v','error','-i',str(path),'-f','null','-'])
  verified[str(path.relative_to(O))]={'width':v['width'],'height':v['height'],'fps':'24/1','frames':clip['frames'],'seconds':clip['seconds'],'start_time':probe['format']['start_time'],'audio':False,'full_decode':'passed','bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
 for frame,tag in [(clip['start'],'first'),(clip['end'],'last')]:
  bg=Image.open(W/'background.png').convert('RGBA');hud=Image.open(W/'sequence/hud'/f'{frame:04d}.png').convert('RGBA');model=Image.open(W/'sequence/model'/f'{frame:04d}.png').convert('RGB');assert bg.size==(2360,split) and hud.size==bg.size and model.size==(2360,2352-split)
  bg.alpha_composite(hud);full=Image.new('RGB',(2360,2352));full.paste(bg.convert('RGB'),(0,0));full.paste(model,(0,split));full.save(O/'stills'/f'{movie.stem}-{tag}.png')
 print('CLIP_VERIFIED',name,flush=True)
(O/'export-verification.json').write_text(json.dumps(verified,indent=2));print('ALL_SIX_CLIPS_VERIFIED',flush=True)
