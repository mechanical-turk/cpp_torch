"""Compose native Blender passes and retain a separate actual-template proof."""
from pathlib import Path
from PIL import Image,ImageChops,ImageStat
import json,hashlib
O=Path(__file__).resolve().parent;W=O/'_render'
plate=Image.open(W/'final-plate.png').convert('RGBA');code=Image.open(W/'final-code.png').convert('RGBA')
assert plate.size==code.size==(2160,2300)
plate.alpha_composite(code);final=plate.convert('RGB');dest=O/'hand-sculpted-clay-sample-2160x2300.png';final.save(dest)
root=next(p for p in O.parents if (p/'AGENTS.md').exists())
template=Image.open(root/'youtube-series/assets/all-platforms-safe-zone-template-1080x1920.png').convert('RGBA').resize((2160,3840),Image.Resampling.NEAREST)
master=Image.new('RGBA',(2160,3840),(27,22,29,255));master.paste(final,(0,0));master=Image.alpha_composite(master,template).convert('RGB');master.save(O/'safe-zone-proof.png')
master.resize((1080,1920),Image.Resampling.LANCZOS).save(W/'safe-zone-review.png')
final.resize((1080,1150),Image.Resampling.LANCZOS).save(W/'final-review.png')
report=json.loads((O/'verification.json').read_text());report.update({'image_decode':'passed','rgb_opaque':True,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'native_scene':'extreme-clay-study.blend'})
reference=O.parent/'final-v8/_render/native-stills/0551-hud.png'
if reference.exists():
 previous=Image.open(reference).convert('RGBA');diff=ImageChops.difference(code,previous);report['code_pass_mean_channel_difference']=sum(ImageStat.Stat(diff).mean)/4
(O/'verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
