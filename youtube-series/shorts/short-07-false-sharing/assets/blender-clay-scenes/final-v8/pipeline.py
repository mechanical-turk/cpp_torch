"""Resumable render/encode supervisor. Run after native preview review passes."""
import os,sys,json,time,subprocess
from pathlib import Path
O=Path(__file__).resolve().parent;W=O/'_render';PY='/opt/homebrew/bin/python3';BLENDER='/Applications/Blender.app/Contents/MacOS/Blender'
assert json.loads((O/'scene-verification.json').read_text())['violation_count']==0
assert (W/'preview-approved.json').exists(),'Native preview and overlay audit must precede production.'
def status(**data):
    data.update(updated=time.strftime('%Y-%m-%dT%H:%M:%S%z'),supervisor_pid=os.getpid())
    t=W/'pipeline-status.part.json';t.write_text(json.dumps(data,indent=2));os.replace(t,W/'pipeline-status.json')
env=os.environ.copy();env['CYCLES_METAL_DISABLE_BINARY_ARCHIVES']='1'
with (W/'production.log').open('a') as render_log,(W/'encoding.log').open('a') as encode_log:
    encoder=subprocess.Popen([PY,str(O/'finish.py')],cwd=O,stdout=encode_log,stderr=subprocess.STDOUT)
    try:
        for attempt in range(1,4):
            renderer=subprocess.Popen([BLENDER,'-b','--python',str(O/'render.py')],cwd=O,env=env,stdout=render_log,stderr=subprocess.STDOUT)
            status(state='rendering',attempt=attempt,renderer_pid=renderer.pid,encoder_pid=encoder.pid)
            while renderer.poll() is None:
                if encoder.poll() is not None and encoder.returncode!=0:
                    renderer.terminate();raise RuntimeError(f'Encoder exited early: {encoder.returncode}')
                time.sleep(5)
            rc=renderer.returncode
            if rc==0:break
            status(state='retrying',attempt=attempt,render_exit_code=rc)
        if rc!=0:raise RuntimeError(f'Native renderer exited {rc} after three resumable attempts')
        status(state='encoding',encoder_pid=encoder.pid)
        ec=encoder.wait()
        if ec:raise RuntimeError(f'Encoder exited {ec}')
        status(state='complete',clips=6)
    except BaseException as e:
        encoder.terminate();status(state='failed',error=str(e));raise
