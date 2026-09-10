"""Composite a native numeral patch without changing its pixel scale."""
import sys
from PIL import Image
if sys.argv[1]=='--preview':
    plate,overlay,dest=sys.argv[2:];im=Image.open(plate).convert('RGBA');im.alpha_composite(Image.open(overlay).convert('RGBA'));im.convert('RGB').save(dest);sys.exit(0)
base,patch,dest=sys.argv[1:4];l,t,r,b=map(int,sys.argv[4:])
im=Image.open(base).convert('RGB');p=Image.open(patch).convert('RGB')
assert im.size==(2160,1310),im.size
assert p.size==(r-l,b-t),(p.size,(r-l,b-t))
im.paste(p,(l,t-990));im.save(dest,compress_level=2)
