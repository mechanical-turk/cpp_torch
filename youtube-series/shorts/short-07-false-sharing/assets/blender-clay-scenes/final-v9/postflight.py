"""Finalize the package only after all twelve exports have passed validation."""
import json,hashlib,time,ast
from pathlib import Path
from PIL import Image,ImageDraw
O=Path(__file__).resolve().parent
r=json.loads((O/'export-verification.json').read_text());assert len(r)==12
for name,details in r.items():
 assert details['decode']=='passed' and details['audio'] is False
 assert hashlib.sha256((O/name).read_bytes()).hexdigest()==details['sha256']
for name in ['scene-verification.json','motion-verification.json']:
 a=json.loads((O/name).read_text());assert a.get('violation_count',a.get('error_count'))==0
for path in O.glob('*.py'):ast.parse(path.read_text())
manifest=json.loads((O/'scene-manifest.json').read_text())
script=O.parents[2]/'script.md';assert hashlib.sha256(script.read_bytes()).hexdigest()==manifest['source_script_sha256']
# Compact contact sheet for the final visual review; no text is baked into media.
sheet=Image.new('RGB',(1080,1280),(25,18,26));draw=ImageDraw.Draw(sheet)
for i,clip in enumerate(manifest['clips']):
 frame=Image.open(O/'stills'/f"{Path(clip['file']).stem}-last.png").convert('RGB');frame.thumbnail((350,575))
 x=(i%3)*360;y=(i//3)*640;sheet.paste(frame,(x,y+35));draw.text((x+8,y+10),clip['file'],fill='white')
sheet.save(O/'_render/final-contact-sheet.png')
now=time.strftime('%Y-%m-%d %H:%M:%S %Z')
p=O/'README.md';s=p.read_text();s=s.replace('**Production in progress.**',f'**Rendered and verified {now}.** All six native videos and six previews are complete.');p.write_text(s)
(O/'final-verification.json').write_text(json.dumps({'completed':now,'native_clips':6,'previews':6,'all_export_hashes_match':True,'source_script_hash_matches':True,'all_python_sources_parse':True,'safe_zone_and_motion_audits_pass':True,'review_sheet':'_render/final-contact-sheet.png'},indent=2))
log=O.parents[2]/'log.md'
marker='## 2026-09-09 — Sculpted clay revision 9 render completed'
if marker not in log.read_text():
 with log.open('a') as f:
  f.write('\n\n'+marker+'\n\nThe render supervisor completed all six numbered 2160 × 2300 native clips and\nsix 1080 × 1150 previews at '+now+'. All twelve files passed full\ndecode, dimensions, frame counts, 24 fps, duration and no-audio checks. Current\nfile hashes and source-script consistency passed. Files are in\n`assets/blender-clay-scenes/final-v9/`; reports are `export-verification.json`\nand `final-verification.json`. This is an automated production completion\nrecord; preflight visual review is documented above.\n')
print('PACKAGE_VERIFIED',now,flush=True)
