"""Chapter 16 scoping: does dropout help the series network (784-256-10 ReLU, series init,
raw pixels, cross-entropy, Adam, batch 64)?  PyTorch float32 CPU, not the C++ engine.

Train set: first N images of the 60,000 (N=10000), or images 0..54999 (N=55000).
Validation: images 55000..59999 (always held out). Test: the 10,000 official test images.
Selection uses validation only. Writes one JSON line per run.
"""
import json, struct, sys, itertools, time
import numpy as np, torch, torch.nn as nn, torch.nn.functional as F

D = "/Users/keremkazan/Documents/Projects/deep-learning-all-the-way-down/data/"
def load(i, l):
    with open(D + i, "rb") as f:
        _, n, r, c = struct.unpack(">IIII", f.read(16)); x = np.frombuffer(f.read(), np.uint8).reshape(n, r * c)
    with open(D + l, "rb") as f:
        f.read(8); y = np.frombuffer(f.read(), np.uint8)
    return torch.tensor(x, dtype=torch.float32) / 255.0, torch.tensor(y.astype(np.int64))

xtr, ytr = load("train-images-idx3-ubyte", "train-labels-idx1-ubyte")
xte, yte = load("t10k-images-idx3-ubyte", "t10k-labels-idx1-ubyte")
xva, yva = xtr[55000:], ytr[55000:]

def run(n, p, lr, seed, epochs, out):
    torch.manual_seed(seed)
    net = nn.Sequential(nn.Linear(784, 256), nn.ReLU(), nn.Dropout(p), nn.Linear(256, 10))
    for m in net:
        if isinstance(m, nn.Linear):
            lim = 1.0 / m.in_features ** 0.5
            nn.init.uniform_(m.weight, -lim, lim); nn.init.zeros_(m.bias)
    opt = torch.optim.Adam(net.parameters(), lr=lr)
    x, y = xtr[:n], ytr[:n]
    hist = []
    def ev(xs, ys):
        net.eval()
        with torch.no_grad():
            s = net(xs); return F.cross_entropy(s, ys).item(), (s.argmax(1) == ys).float().mean().item()
    for e in range(epochs):
        net.train()
        perm = torch.randperm(n)
        for i in range(0, n, 64):
            idx = perm[i:i + 64]
            opt.zero_grad(); F.cross_entropy(net(x[idx]), y[idx]).backward(); opt.step()
        tl, ta = ev(x[:10000], y[:10000]); vl, va = ev(xva, yva); sl, sa = ev(xte, yte)
        hist.append([e + 1, tl, ta, vl, va, sl, sa])
    out.write(json.dumps({"n": n, "p": p, "lr": lr, "seed": seed, "hist": hist}) + "\n"); out.flush()

if __name__ == "__main__":
    n, epochs, outpath = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    torch.set_num_threads(2)
    out = open(outpath, "a")
    for p, lr, seed in itertools.product([0.0, 0.2, 0.5], [3e-4, 1e-3, 3e-3], [1, 2, 3]):
        t = time.time(); run(n, p, lr, seed, epochs, out); print(n, p, lr, seed, round(time.time() - t, 1), flush=True)
