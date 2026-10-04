from pathlib import Path
O=Path(__file__).resolve().parent;D=O/'_render';A=D/'pre-clearance';A.mkdir(exist_ok=True)
for name in ['hud','plates','frames','qa','timings.jsonl','qa.log','persistent-test.log']:
 p=D/name
 if p.exists() and not (A/name).exists():p.rename(A/name)
for name in ['hud','plates','frames','qa']:(D/name).mkdir(exist_ok=True)
print('Archived pre-clearance render evidence; native background unchanged.')
