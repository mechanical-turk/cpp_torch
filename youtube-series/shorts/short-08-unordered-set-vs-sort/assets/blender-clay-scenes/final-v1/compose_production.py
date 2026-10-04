from PIL import Image
from pathlib import Path
import sys,os
O=Path(__file__).resolve().parent;plate,hud,dest=map(Path,sys.argv[1:]);lower=Image.open(plate).convert('RGBA');bg=Image.open(O/'_render/background.png').convert('RGBA');text=Image.open(hud).convert('RGBA')
assert lower.size==(2160,1300) and bg.size==(2160,1000) and text.size==(2160,2300)
out=Image.new('RGBA',(2160,2300));out.paste(bg,(0,0));out.paste(lower,(0,1000));out=Image.alpha_composite(out,text).convert('RGB');tmp=dest.with_name(dest.stem+'.part.png');out.save(tmp);os.replace(tmp,dest)
