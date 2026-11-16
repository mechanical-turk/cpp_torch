# Stage 2: refine Adam's rate, batch size and epoch budget on the residual network (5 seeds); extend SGD downward. Writes sweep2.json.
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
seeds = [42, 1, 2, 3, 4]
jobs = [('adam', lr, b, e, s) for lr in ['0.0032', '0.0042', '0.0056', '0.0075'] for b in (64, 128, 250) for e in (5, 10, 20) for s in seeds]
jobs += [('sgd', lr, 250, 5, s) for lr in ['0.01', '0.0178', '0.0316', '0.056'] for s in [42, 1, 2]]
with cf.ThreadPoolExecutor(8) as ex:
    res = list(ex.map(run, jobs))
json.dump(res, open(os.path.join(here, 'sweep2.json'), 'w'), indent=1)
print('done', len(res))
