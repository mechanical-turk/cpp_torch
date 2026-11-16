# Batch 64: does the SGD / momentum / Adam ordering depend on the epoch budget? Writes epochs.json.
import json, os, concurrent.futures as cf
from run import run  # build/small is compiled by importing run.py (its main is guarded)
here = os.path.dirname(os.path.abspath(__file__))
seeds = [42, 1, 2, 3, 4]
cfgs = [('sgd', '0.562'), ('momentum', '0.1'), ('adam', '0.0056')]
jobs = [(o, lr, 64, e, s) for o, lr in cfgs for e in (2, 3, 5, 10) for s in seeds]
with cf.ThreadPoolExecutor(8) as ex:
    res = list(ex.map(run, jobs))
json.dump(res, open(os.path.join(here, 'epochs.json'), 'w'), indent=1)
print('done', len(res))
