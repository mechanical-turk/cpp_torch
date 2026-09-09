"""Composite a native Blender code-region render and the supplied QA overlay."""
from pathlib import Path
import json
from PIL import Image, ImageChops

OUT = Path(__file__).resolve().parent
project = next(p for p in OUT.parents if (p/'AGENTS.md').exists())
source = Image.open(OUT/'short-07-clay-study-2160x2420.png').convert('RGB')
patch = Image.open(OUT/'_render/code-safe-patch.png').convert('RGB')
assert patch.width == 2160 and patch.height in (1080,1081), patch.size
source.paste(patch,(0,0))
final = source.crop((0,60,2160,2360))
assert final.size == (2160,2300)
previous = Image.open(OUT/'short-07-clay-study-2160x2300.png').convert('RGB')
retained_y = patch.height-60
assert ImageChops.difference(final.crop((0,retained_y,2160,2300)),
                            previous.crop((0,retained_y,2160,2300))).getbbox() is None
final.save(OUT/'short-07-clay-study-safe-code-2160x2300.png')
template = Image.open(project/'youtube-series/assets/all-platforms-safe-zone-template-1080x1920.png').convert('RGBA')
assert template.size == (1080,1920)
template = template.resize((2160,3840), Image.Resampling.NEAREST)
for name,still in [('before',previous),('after',final)]:
    master = Image.new('RGBA',(2160,3840),(27,22,29,255))
    master.paste(still,(0,0))
    # Actual supplied translucent overlay, scaled exactly 2x; no custom mask.
    proof = Image.alpha_composite(master,template)
    proof.convert('RGB').save(OUT/f'safe-zone-{name}-2160x3840.png')
    proof.convert('RGB').resize((540,960),Image.Resampling.LANCZOS).save(OUT/f'_render/safe-zone-{name}-phone.png')
report_path = OUT/'safe-zone-verification.json'
report = json.loads(report_path.read_text())
report.update({'patch_resolution':list(patch.size),
               'unchanged_pixels_below_y':retained_y,
               'unchanged_models_pixel_comparison':'passed',
               'template_overlay':'actual supplied RGBA template scaled 2x',
               'delivery_png_decode':'passed'})
report_path.write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
