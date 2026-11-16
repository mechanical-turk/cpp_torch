"""Seconds per optimizer step for the Chapter 14 network at several batch sizes, plain SGD vs momentum 0.9.

usage: python timing.py   (float64, one CPU thread; 20 warm-up steps then --steps timed steps; median of --repeats)
Training steps only: no evaluation inside the timed region. Run on an otherwise idle machine for usable numbers.
"""
import argparse
import statistics
import time

import numpy as np
import torch
import torch.nn.functional as F

from lab import MT19937, SeriesMLP, load_idx

torch.set_num_threads(1)
p = argparse.ArgumentParser()
p.add_argument("--steps", type=int, default=100)
p.add_argument("--repeats", type=int, default=5)
a = p.parse_args()
x, y = load_idx("data/train-images-idx3-ubyte", "data/train-labels-idx1-ubyte")
X = torch.from_numpy(x[:10000].astype(np.float64) / 255.0)
Y = torch.from_numpy(y[:10000].astype(np.int64))
print("batch  sgd s/step  momentum s/step  ratio(mom/sgd)  s per 1000 samples (sgd)")
for b in (16, 64, 256, 1024, 10000):
    res = {}
    for m in (0.0, 0.9):
        model = SeriesMLP(32, 16, True, "tanh", MT19937(42), torch.float64)
        opt = torch.optim.SGD(model.parameters(), lr=0.01, momentum=m)
        times = []
        for rep in range(a.repeats):
            for k in range(20 + a.steps):
                if k == 20:
                    t0 = time.perf_counter()
                i = (k * b) % (10000 - b + 1) if b < 10000 else 0
                opt.zero_grad(set_to_none=True)
                F.cross_entropy(model(X[i:i + b]), Y[i:i + b]).backward()
                opt.step()
            times.append((time.perf_counter() - t0) / a.steps)
        res[m] = statistics.median(times)
    print(f"{b:6d} {res[0.0]:11.5f} {res[0.9]:16.5f} {res[0.9] / res[0.0]:15.2f} {res[0.0] / b * 1000:24.3f}", flush=True)
