"""Keep completed delivery assets/status in Content HQ while the authorized worker runs."""
from pathlib import Path
import subprocess,json,time
O=Path(__file__).resolve().parent;remote='gpu-worker:Projects/content-hq-render-worker/short-08/final-v2/'
while True:
 cmd=['rsync','-a','--exclude=*.part.mp4','--include=*.mp4','--include=*.json','--include=previews/','--include=previews/*.mp4','--include=_render/','--include=_render/pipeline-status.json','--include=_render/render-progress.json','--exclude=*',remote,str(O)+'/']
 try:
  subprocess.run(cmd,check=True,timeout=60)
  p=O/'_render/pipeline-status.json';state=json.loads(p.read_text()) if p.exists() else {}
  print(json.dumps(state),flush=True)
  if state.get('state') in ['complete','failed']:break
 except Exception as e:print('SYNC_RETRY',str(e),flush=True)
 time.sleep(20)
