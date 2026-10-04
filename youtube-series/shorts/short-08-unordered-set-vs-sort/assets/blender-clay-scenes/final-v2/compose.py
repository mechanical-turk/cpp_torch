from pathlib import Path
from PIL import Image
import json,sys,os
O=Path(__file__).resolve().parent;D=O/'_render';R=json.loads((O/'scene-verification.json').read_text());f=int(sys.argv[1]);out=Image.open(D/'background.png').convert('RGBA')
for part in ['model','hud']:
 c=R['maps'][part][str(f)];crop=R['crops'][part][str(c)]
 if crop is None:continue
 x0,y0,x1,y1=crop;im=Image.open(D/('plates' if part=='model' else 'hud')/f'{c:04d}.png').convert('RGBA')
 assert im.size==(x1-x0,y1-y0),(part,c,im.size,crop)
 if part=='model':out.paste(im,(x0,y0))
 else:out.alpha_composite(im,(x0,y0))
target=D/'frames'/f'{f:04d}.png';temp=target.with_name(target.stem+'.part.png');out.convert('RGB').save(temp,compress_level=1);os.replace(temp,target)
