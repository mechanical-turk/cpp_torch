"""Place rendered review frames under the actual supplied safe-zone overlay."""
import json,hashlib
from pathlib import Path
from PIL import Image
O=Path(__file__).resolve().parent;project=next(p for p in O.parents if (p/'AGENTS.md').exists())
template=Image.open(project/'youtube-series/assets/all-platforms-safe-zone-template-1080x1920.png').convert('RGBA')
dest=O/'safe-zone-proofs';dest.mkdir(exist_ok=True)
for folder in ['review','native-stills']:
    for p in sorted((O/'_render'/folder).glob('[0-9][0-9][0-9][0-9].png')):
        frame=Image.open(p).convert('RGBA');scale=frame.width/1080
        master=Image.new('RGBA',(frame.width,round(1920*scale)),(27,22,29,255));master.paste(frame,(0,0))
        guide=template.resize(master.size,Image.Resampling.NEAREST)
        Image.alpha_composite(master,guide).convert('RGB').save(dest/f'{folder}-{p.name}')
print('TEMPLATE_PROOFS_WRITTEN')
