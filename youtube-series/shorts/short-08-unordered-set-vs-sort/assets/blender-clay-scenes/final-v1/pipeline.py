"""Supervise resumable native rendering; encode and verify each finished scene."""
import os,subprocess,json,time,hashlib,sys,ast
from pathlib import Path
O=Path(__file__).resolve().parent;D=O/'_render';M=json.loads((O/'scene-manifest.json').read_text());PY='/opt/homebrew/bin/python3';BLENDER='/Applications/Blender.app/Contents/MacOS/Blender';FF='/opt/homebrew/bin/ffmpeg';PROBE='/opt/homebrew/bin/ffprobe'
(D/'encode').mkdir(exist_ok=True);(O/'previews').mkdir(exist_ok=True)
qa=json.loads((O/'production-preflight.json').read_text());assert qa['approved_for_batch']
assert hashlib.sha256((O/'short-08-clay.blend').read_bytes()).hexdigest()==qa['blend_sha256'],'Source changed after preflight'
def status(state,**extra):(D/'pipeline-status.json').write_text(json.dumps({'state':state,'updated_unix':time.time(),**extra},indent=2))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify(p,clip,width,height):
 raw=subprocess.check_output([PROBE,'-v','error','-show_streams','-show_format','-of','json',str(p)]);meta=json.loads(raw);v=[x for x in meta['streams'] if x['codec_type']=='video'];assert len(v)==1 and len(meta['streams'])==1
 v=v[0];assert (v['width'],v['height'])==(width,height);assert v['r_frame_rate']=='24/1';assert int(v['nb_frames'])==clip['frames'];assert abs(float(v['duration'])-clip['seconds'])<.001;assert abs(float(v.get('start_time',0)))<.001
 subprocess.run([FF,'-v','error','-i',str(p),'-f','null','-'],check=True)
 return {'file':str(p.relative_to(O)),'width':width,'height':height,'frames':int(v['nb_frames']),'seconds':float(v['duration']),'fps':24,'audio':False,'sha256':sha(p),'decoded':True}
reports=[];done=set()
def encode_ready():
 for clip in M['clips']:
  name=clip['file']
  if name in done:continue
  frames=[D/'frames'/f'{(f if f%2 else f-1):04d}.png' for f in range(clip['start'],clip['end']+1)]
  if not all(p.exists() for p in frames):continue
  folder=D/'encode'/Path(name).stem;folder.mkdir(exist_ok=True)
  for i,p in enumerate(frames):
   link=folder/f'{i:04d}.png'
   if not link.exists():os.link(p,link)
  target=O/name;temp=O/(Path(name).stem+'.part.mp4')
  if not target.exists():
   subprocess.run([FF,'-v','error','-y','-framerate','24','-i',str(folder/'%04d.png'),'-frames:v',str(clip['frames']),'-c:v','libx264','-crf','16','-preset','medium','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart','-an',str(temp)],check=True);os.replace(temp,target)
  prev=O/'previews'/name;tmp=prev.with_name(prev.stem+'.part.mp4')
  if not prev.exists():
   subprocess.run([FF,'-v','error','-y','-i',str(target),'-vf','scale=1080:1150:flags=lanczos','-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart','-an',str(tmp)],check=True);os.replace(tmp,prev)
  reports.extend([verify(target,clip,2160,2300),verify(prev,clip,1080,1150)]);done.add(name)
  (O/'export-verification.json').write_text(json.dumps(reports,indent=2));status('rendering',clips_complete=len(done),clips_total=7,last_clip=name);print('CLIP_VERIFIED',name,flush=True)
try:
 for attempt in range(1,4):
  status('rendering',attempt=attempt,clips_complete=len(done),clips_total=7)
  env=os.environ.copy();env['CYCLES_METAL_DISABLE_BINARY_ARCHIVES']='1'
  with (D/f'production-attempt-{attempt}.log').open('a') as log:
   proc=subprocess.Popen([BLENDER,'-b','--python',str(O/'produce.py')],stdout=log,stderr=subprocess.STDOUT,env=env)
   while proc.poll() is None:
    encode_ready();time.sleep(5)
   encode_ready()
  if len(done)==7:break
  print('RETRY_MISSING_FRAMES',attempt,proc.returncode,flush=True)
 if len(done)!=7:raise RuntimeError('Missing scene files after three attempts')
 for script in O.glob('*.py'):ast.parse(script.read_text())
 final={'status':'complete','clips':7,'exports':14,'blend_sha256':sha(O/'short-08-clay.blend'),'script_sha256':sha(O.parents[2]/'script.md'),'export_report_sha256':sha(O/'export-verification.json'),'completed_unix':time.time(),'preflight':qa}
 (O/'final-verification.json').write_text(json.dumps(final,indent=2));status('complete',clips_complete=7,exports_verified=14)
 with (O/'README.md').open('a') as f:f.write('\n## Completed render\n\nAll seven native clips and seven previews finished and passed full decode,\ndimensions, frame-count, duration, timestamp and audio checks. See\n`export-verification.json` and `final-verification.json`.\n')
 with (O.parents[2]/'log.md').open('a') as f:f.write('\n## '+time.strftime('%Y-%m-%d %H:%M:%S %Z')+' — Seven clay scenes completed\n\nNative 2160×2300 / 24 fps and 1080×1150 previews completed in\nassets/blender-clay-scenes/final-v1. All 14 files passed full decode and\nstream checks. No combined movie, narration, commit, push or publication.\nFinal editorial timing and actual platform-interface review remain separate.\n')
 print('ALL_SCENES_COMPLETE',flush=True)
except Exception as e:
 if 'proc' in locals() and proc.poll() is None:proc.terminate()
 status('failed',error=str(e),clips_complete=len(done));raise
