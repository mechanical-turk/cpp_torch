# Stage 3: confirmation on fresh seeds 5-9 (not used for tuning), batch 250. Writes sweep3.json.
import json, os, re, subprocess, concurrent.futures as cf
here = os.path.dirname(os.path.abspath(__file__))
binary = os.path.join(here, 'build/residual')
repo = '/Users/keremkazan/Documents/Projects/deep-learning-all-the-way-down'
def run(job):
    opt, lr, batch, epochs, seed = job
    r = subprocess.run([binary, opt, str(lr), str(batch), str(epochs), str(seed)], cwd=repo, capture_output=True, text=True, timeout=1800)
    m = re.search(r'Test accuracy: \S+% \((\d+)/2000\)', r.stdout)
    return {'opt': opt, 'lr': lr, 'batch': batch, 'epochs': epochs, 'seed': seed, 'code': r.returncode,
            'epoch_loss': [float(x) for x in re.findall(r'Epoch \d+ loss: (\S+)', r.stdout)],
            'correct': int(m.group(1)) if m else None}
seeds = [5, 6, 7, 8, 9]
cfgs = [('adam', '0.0056'), ('momentum', '0.0178'), ('momentum', '0.0316'), ('momentum', '0.0562'), ('sgd', '0.056'), ('sgd', '0.1')]
jobs = [(o, lr, 250, e, s) for o, lr in cfgs for e in (5, 20) for s in seeds]
with cf.ThreadPoolExecutor(8) as ex:
    res = list(ex.map(run, jobs))
json.dump(res, open(os.path.join(here, 'sweep3.json'), 'w'), indent=1)
print('done', len(res))
