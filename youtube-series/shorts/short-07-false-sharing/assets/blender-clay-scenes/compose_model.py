from pathlib import Path
from PIL import Image
import sys
base,patch,dest=map(Path,sys.argv[1:4]);l,t,r,b,split=map(int,sys.argv[4:]);im=Image.open(base).convert('RGB');p=Image.open(patch).convert('RGB');assert p.size==(r-l,b-t),(p.size,(r-l,b-t));im.paste(p,(l,t-split));tmp=dest.with_suffix('.partial.png');im.save(tmp);tmp.replace(dest)
