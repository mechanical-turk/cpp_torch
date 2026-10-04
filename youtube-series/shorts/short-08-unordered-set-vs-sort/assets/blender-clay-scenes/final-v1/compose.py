from PIL import Image
from pathlib import Path
import sys,os
plate,over,dest=map(Path,sys.argv[1:])
a=Image.open(plate).convert('RGBA');b=Image.open(over).convert('RGBA');assert a.size==b.size
out=dest.with_name(dest.stem+'.part.png');Image.alpha_composite(a,b).convert('RGB').save(out);os.replace(out,dest)
