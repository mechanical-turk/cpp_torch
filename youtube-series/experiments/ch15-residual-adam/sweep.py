# Stage 1 sweep on the Chapter 14 residual network. Run after build_harness.py. Writes sweep1.json.
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
seeds = [42, 1, 2]
adam = ['0.00056', '0.001', '0.0018', '0.0032', '0.0056', '0.01', '0.018', '0.032', '0.056', '0.1']
sgd = ['0.1', '0.178', '0.316', '0.562', '1.0', '1.78', '3.16', '5.62']
mom = ['0.01', '0.0178', '0.0316', '0.0562', '0.1', '0.178', '0.316', '0.562', '1.0']
jobs = [('adam', lr, b, 5, s) for lr in adam for b in (250, 64) for s in seeds]
jobs += [('sgd', lr, 250, 5, s) for lr in sgd for s in seeds] + [('momentum', lr, 250, 5, s) for lr in mom for s in seeds]
with cf.ThreadPoolExecutor(8) as ex:
    res = list(ex.map(run, jobs))
json.dump(res, open(os.path.join(here, 'sweep1.json'), 'w'), indent=1)
print('done', len(res))
