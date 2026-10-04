"""Bounded OptiX cache test; keep the source scene and normal profile unchanged."""
from pathlib import Path
import sys
sys.argv=['blender','--','--qa']
source=(Path(__file__).resolve().parent/'render.py').read_text();exec(compile(source.split("render(D/'background.png'")[0],__file__,'exec'))
s.render.use_persistent_data=True
for f in [1,3,5]:
 s.frame_set(f);canonical=R['maps']['model'][str(f)];render(D/'qa'/f'persistent-{f:04d}.png','model',R['crops']['model'][str(canonical)],48)
print('PERSISTENT_TEST_COMPLETE',flush=True)
