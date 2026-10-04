from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
import json
O=Path(__file__).resolve().parent;M=json.loads((O/'keyframes-manifest.json').read_text());done=[]
for item in M['frames']:
 f=item['frame'];a=O/'_render'/f'{f:02d}-plate.png';b=O/'_render'/f'{f:02d}-hud.png'
 if not (a.exists() and b.exists()):continue
 out=Image.alpha_composite(Image.open(a).convert('RGBA'),Image.open(b).convert('RGBA')).convert('RGB');assert out.size==(2160,2300);out.save(O/item['file'],compress_level=1);done.append(item)
# Review-only sheet: labels belong to the sheet margins, never native stills.
if done:
 sheet=Image.new('RGB',(1920,2*740),(24,15,28));draw=ImageDraw.Draw(sheet);font=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',17)
 for i,item in enumerate(done):
  x=(i%4)*480;y=(i//4)*740;im=Image.open(O/item['file']);im.thumbnail((468,650));sheet.paste(im,(x+6,y+40));draw.text((x+14,y+12),item['file'].replace('.png',''),fill='white',font=font)
 sheet.save(O/'review-contact-sheet.jpg',quality=94)
print('COMPOSITED',len(done),'of 7')

# Actual creator-supplied template at 2x, laid over the complete vertical master.
proofs=O/'safe-zone-proofs';proofs.mkdir(exist_ok=True)
template=Image.open(O.parents[4]/'assets'/'all-platforms-safe-zone-template-1080x1920.png').convert('RGBA').resize((2160,3840),Image.Resampling.LANCZOS)
for item in done:
 master=Image.new('RGBA',(2160,3840),(24,15,28,255));master.paste(Image.open(O/item['file']).convert('RGBA'),(0,0))
 Image.alpha_composite(master,template).convert('RGB').save(proofs/item['file'],compress_level=1)
