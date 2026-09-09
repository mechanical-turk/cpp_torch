from pathlib import Path
from PIL import Image, ImageChops, ImageStat
import json,subprocess,shutil,os
root=Path('/Users/keremkazan/Documents/Codex/2026-09-05/go-t')
out=root/'outputs/short-06-blender-motion';work=root/'work/short-06-blender-motion'
source=root/'work/short-06-blender-wide/frames'
report=json.loads((out/'scene-verification.json').read_text());mapping={int(k):v for k,v in report['frame_map'].items()}
(work/'frames').mkdir(exist_ok=True);(out/'stills').mkdir(exist_ok=True)
for f in sorted(set(mapping.values())):
    old=Image.open(source/f'frame_{f:04}.png').convert('RGB')
    top=Image.open(work/f'upper/frame_{f:04}.png').convert('RGB')
    assert top.width==2360 and top.height in {1100,1101},top.size
    result=Image.new('RGB',(2360,2352))
    result.paste(old.crop((0,0,2360,2152)),(0,200))
    result.paste(top.crop((0,0,2360,1100)),(0,0))
    result.save(work/f'frames/frame_{f:04}.png',compress_level=2)
for f,src in mapping.items():
    p=work/f'frames/frame_{f:04}.png'
    if f!=src and not p.exists():os.link(work/f'frames/frame_{src:04}.png',p)
for name,f in [('01-opening',1),('02-code-transition',178),('03-code-settled',220),('04-arrow-drawing',300),('05-result',340),('06-final',400)]:
    shutil.copy2(work/f'frames/frame_{f:04}.png',out/f'stills/{name}.png')
def run(a):return subprocess.run(a,capture_output=True,text=True,check=True)
run(['ffmpeg','-hide_banner','-loglevel','error','-y','-framerate','24','-start_number','1','-i',str(work/'frames/frame_%04d.png'),'-frames:v','456','-an','-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart',str(out/'cpp-data-layout-motion.mp4')])
print('ENCODED_NATIVE',flush=True)
run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(out/'cpp-data-layout-motion.mp4'),'-vf','scale=1180:1176:flags=lanczos','-an','-c:v','libx264','-preset','medium','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(out/'preview.mp4')])
verification={'videos':{},'lower_region_exact_translation':True,'shift_down_px':200,'composition_scene_report':'scene-verification.json','decoded_without_errors':True}
for name,dims in [('cpp-data-layout-motion.mp4',[2360,2352]),('preview.mp4',[1180,1176])]:
    info=json.loads(run(['ffprobe','-v','error','-show_entries','stream=codec_name,codec_type,width,height,r_frame_rate,nb_frames:format=duration,size','-of','json',str(out/name)]).stdout)
    assert len(info['streams'])==1
    v=info['streams'][0]
    assert v['codec_type']=='video' and v['r_frame_rate']=='24/1' and v['nb_frames']=='456'
    assert [v['width'],v['height']]==dims and float(info['format']['duration'])==19
    run(['ffmpeg','-v','error','-i',str(out/name),'-f','null','-'])
    verification['videos'][name]=info
comparisons={}
for f in [1,178,340]:
    full=Image.open(work/f'check-{f}.png').convert('RGB')
    assembled=Image.open(work/f'frames/frame_{f:04}.png').convert('RGB')
    diff=ImageChops.difference(full.crop((0,1100,2360,2352)),assembled.crop((0,1100,2360,2352)))
    means=ImageStat.Stat(diff).mean
    assert max(means)<2,(f,means)
    comparisons[f]=means
verification['full_scene_vs_reused_lower_region_mean_rgb_difference']=comparisons
(out/'export-verification.json').write_text(json.dumps(verification,indent=2))
for name in ['revise_scene.py','render_upper.py','finish.py']:
    shutil.copy2(work/name,out/name)
print('VERIFIED',json.dumps(verification),flush=True)
