"""Review-only contact sheets and exact native stills; never alters delivered video."""
from pathlib import Path
import subprocess,json
from PIL import Image,ImageDraw,ImageFont
O=Path(__file__).resolve().parent;D=O/'_render'/'clip-review';D.mkdir(exist_ok=True)
M=json.loads((O/'scene-manifest.json').read_text());font=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',18)
for clip in M['clips']:
 path=O/clip['file'];stem=path.stem;sheetpath=D/(stem+'.jpg')
 if not path.exists() or sheetpath.exists():continue
 folder=D/stem;folder.mkdir(exist_ok=True)
 subprocess.run(['/opt/homebrew/bin/ffmpeg','-v','error','-y','-i',str(path),'-vf','fps=4,scale=360:384:flags=lanczos',str(folder/'%03d.png')],check=True)
 files=sorted(folder.glob('*.png'));rows=(len(files)+5)//6;sheet=Image.new('RGB',(2160,rows*420),(20,13,25));draw=ImageDraw.Draw(sheet)
 for i,file in enumerate(files):
  x=(i%6)*360;y=(i//6)*420;sheet.paste(Image.open(file),(x,y+30));draw.text((x+10,y+6),f'{i/4:.2f}s',font=font,fill='white')
 sheet.save(sheetpath,quality=94)
 for name,ts in [('first',0),('last',clip['seconds']-1/24)]:
  subprocess.run(['/opt/homebrew/bin/ffmpeg','-v','error','-y','-ss',str(ts),'-i',str(path),'-frames:v','1',str(D/f'{stem}-{name}.png')],check=True)
 print('REVIEW_READY',stem,flush=True)
