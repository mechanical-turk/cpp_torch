"""Render, checkpoint, encode and fully verify seven standalone clips on the GPU worker."""
import subprocess,json,time,hashlib,os,traceback
from pathlib import Path
O=Path(__file__).resolve().parent;D=O/'_render';M=json.loads((O/'scene-manifest.json').read_text());QA=json.loads((O/'production-preflight.json').read_text())
assert QA['approved_for_batch'];assert hashlib.sha256((O/'short-08-clay.blend').read_bytes()).hexdigest()==QA['blend_sha256']
(O/'previews').mkdir(exist_ok=True);(D/'encode').mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def status(state,**extra):
 p=D/'pipeline-status.json';tmp=p.with_suffix('.part.json');tmp.write_text(json.dumps({'state':state,'updated_unix':time.time(),**extra},indent=2));os.replace(tmp,p)
def verify(p,clip,size):
 meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]));assert len(meta['streams'])==1
 v=meta['streams'][0];assert v['codec_type']=='video';assert [v['width'],v['height']]==size;assert v['r_frame_rate']=='24/1';assert int(v['nb_frames'])==clip['frames'];assert abs(float(v['duration'])-clip['seconds'])<.001;assert abs(float(v.get('start_time',0)))<.001
 subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(p),'-f','null','-'],check=True)
 return {'file':str(p.relative_to(O)),'width':size[0],'height':size[1],'fps':24,'frames':int(v['nb_frames']),'duration':float(v['duration']),'start_time':float(v.get('start_time',0)),'audio':False,'full_decode':True,'sha256':sha(p)}
reports=[];done=set()
def encode_ready():
 for c in M['clips']:
  if c['file'] in done:continue
  frames=[D/'frames'/f'{(f if f%2 else f-1):04d}.png' for f in range(c['start'],c['end']+1)]
  if not all(p.exists() for p in frames):continue
  folder=D/'encode'/Path(c['file']).stem;folder.mkdir(exist_ok=True)
  for i,p in enumerate(frames):
   link=folder/f'{i:04d}.png'
   if not link.exists():os.link(p,link)
  out=O/c['file'];tmp=out.with_name(out.stem+'.part.mp4')
  if not out.exists():
   subprocess.run(['ffmpeg','-v','error','-y','-framerate','24','-i',str(folder/'%04d.png'),'-frames:v',str(c['frames']),'-c:v','libx264','-threads','4','-crf','16','-preset','medium','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart','-an',str(tmp)],check=True);os.replace(tmp,out)
  prev=O/'previews'/c['file'];tmp=prev.with_name(prev.stem+'.part.mp4')
  if not prev.exists():
   subprocess.run(['ffmpeg','-v','error','-y','-i',str(out),'-vf','scale=1080:1150:flags=lanczos','-c:v','libx264','-threads','4','-crf','18','-preset','medium','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart','-an',str(tmp)],check=True);os.replace(tmp,prev)
  reports.extend([verify(out,c,[2160,2300]),verify(prev,c,[1080,1150])]);done.add(c['file']);(O/'export-verification.json').write_text(json.dumps(reports,indent=2));status('rendering',clips_complete=len(done),clips_total=7,last_clip=c['file']);print('CLIP_VERIFIED',c['file'],flush=True)
try:
 for attempt in range(1,4):
  status('rendering',attempt=attempt,clips_complete=len(done),clips_total=7)
  with (D/f'production-{attempt}.log').open('a') as log:
   proc=subprocess.Popen(['blender','-b','--python',str(O/'render.py')],stdout=log,stderr=subprocess.STDOUT)
   while proc.poll() is None:encode_ready();time.sleep(5)
   encode_ready()
  if len(done)==7:break
  print('RETRY',attempt,'exit',proc.returncode,flush=True)
 if len(done)!=7:raise RuntimeError('Incomplete after three attempts')
 (O/'final-verification.json').write_text(json.dumps({'complete':True,'native_clips':7,'previews':7,'blend_sha256':sha(O/'short-08-clay.blend'),'export_report_sha256':sha(O/'export-verification.json'),'completed_unix':time.time(),'source':'approved keyframes-v3','creator_authorized':True},indent=2));status('complete',clips_complete=7,exports_verified=14);print('ALL_SEVEN_CLIPS_VERIFIED',flush=True)
except Exception as e:
 if 'proc' in locals() and proc.poll() is None:proc.terminate()
 status('failed',error=str(e),clips_complete=len(done));traceback.print_exc();raise
