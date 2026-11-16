"""Momentum regime hunt: SGD vs SGD+momentum on MNIST under controllable conditions.

Conditioning knob: each input pixel is multiplied by 10**(-decades * r_i), r_i ~ U(0,1)
fixed by --scale_seed, so the first-layer problem is ill-conditioned by up to 10**(2*decades).
Models: softmax regression (convex) or relu MLP. float32 on CUDA. Train subset = first N images.
Writes one JSON line per run. Metric: full-train-subset loss every --eval steps.
"""
import argparse, json, struct, sys, time
from pathlib import Path
import numpy as np, torch, torch.nn as nn, torch.nn.functional as F

def load_idx(ip, lp):
    with open(ip, "rb") as f:
        _, n, r, c = struct.unpack(">IIII", f.read(16)); x = np.frombuffer(f.read(), np.uint8).reshape(n, r * c)
    with open(lp, "rb") as f:
        f.read(8); y = np.frombuffer(f.read(), np.uint8)
    return x, y

def build(model, depth, width, seed, act="relu", init="default"):
    torch.manual_seed(seed)
    if model == "softmax":
        return nn.Linear(784, 10)
    layers, d = [], 784
    for _ in range(depth):
        layers += [nn.Linear(d, width), nn.ReLU() if act == "relu" else nn.Tanh()]; d = width
    layers.append(nn.Linear(d, 10))
    net = nn.Sequential(*layers)
    if init == "series":
        for m in net:
            if isinstance(m, nn.Linear):
                lim = 1.0 / m.in_features ** 0.5
                nn.init.uniform_(m.weight, -lim, lim); nn.init.zeros_(m.bias)
    if init == "proper":
        for m in net:
            if isinstance(m, nn.Linear):
                if act == "relu": nn.init.kaiming_normal_(m.weight, nonlinearity="relu")
                else: nn.init.xavier_uniform_(m.weight, gain=nn.init.calculate_gain("tanh"))
                nn.init.zeros_(m.bias)
    return net

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("jobs"); ap.add_argument("--out", required=True); ap.add_argument("--data", default="data")
    a = ap.parse_args()
    dev = "cuda"
    data = Path(a.data)
    xtr, ytr = load_idx(data / "train-images-idx3-ubyte", data / "train-labels-idx1-ubyte")
    xte, yte = load_idx(data / "t10k-images-idx3-ubyte", data / "t10k-labels-idx1-ubyte")
    cache = {}
    out = open(a.out, "a")
    for line in open(a.jobs):
        line = line.strip()
        if not line or line.startswith("#"): continue
        j = json.loads(line)
        dt = getattr(torch, j.get("dtype", "float32")); mse = j.get("loss", "ce") == "mse"
        key = (j["n"], j["decades"], j.get("scale_seed", 0), str(dt))
        if key not in cache:
            x = torch.tensor(xtr[:j["n"]], dtype=torch.float32) / 255.0
            xt = torch.tensor(xte, dtype=torch.float32) / 255.0
            mu, sd = x.mean(0), x.std(0) + 0.1
            if j.get("inputs") == "raw": mu, sd = torch.zeros(784), torch.ones(784)
            g = torch.Generator().manual_seed(key[2])
            s = 10.0 ** (-j["decades"] * torch.rand(784, generator=g))
            cache[key] = (((x - mu) / sd * s).to(dev, dt), torch.tensor(ytr[:j["n"]], dtype=torch.long).to(dev),
                          ((xt - mu) / sd * s).to(dev, dt), torch.tensor(yte, dtype=torch.long).to(dev))
        X, Y, XT, YT = cache[key]
        lossf = (lambda o, y: F.mse_loss(o, F.one_hot(y, 10).to(o.dtype))) if mse else F.cross_entropy
        lstar = None
        if mse:
            A = np.concatenate([X.cpu().numpy(), np.ones((len(X), 1))], 1); T = np.eye(10)[Y.cpu().numpy()]
            W = np.linalg.lstsq(A, T, rcond=None)[0]; lstar = float(((A @ W - T) ** 2).mean())
        net = build(j["model"], j.get("depth", 2), j.get("width", 128), j["seed"], j.get("act", "relu"), j.get("init", "default")).to(dev, dt)
        opt = torch.optim.Adam(net.parameters(), lr=j["lr"], betas=(0.9, 0.999)) if j.get("opt") == "adam" else torch.optim.SGD(net.parameters(), lr=j["lr"], momentum=j["momentum"])
        gen = torch.Generator(device=dev).manual_seed(1000 + j["seed"])
        n, bs, steps, ev = j["n"], j["batch"], j["steps"], j.get("eval", 10)
        hist, t0, diverged = [], time.time(), False
        for step in range(steps + 1):
            if step % ev == 0:
                with torch.no_grad():
                    lo = net(X); loss = lossf(lo, Y).item(); acc = (lo.argmax(1) == Y).float().mean().item()
                if not np.isfinite(loss): diverged = True; break
                hist.append((step, loss, acc))
            if step == steps: break
            idx = torch.arange(n, device=dev) if bs >= n else torch.randint(0, n, (bs,), device=dev, generator=gen)
            opt.zero_grad(set_to_none=True)
            lossf(net(X[idx]), Y[idx]).backward(); opt.step()
        with torch.no_grad():
            tl = net(XT); tacc = (tl.argmax(1) == YT).float().mean().item() if not diverged else None
        rec = dict(j, lstar=lstar, diverged=diverged, hist=hist, test_acc=tacc, secs=round(time.time() - t0, 2))
        out.write(json.dumps(rec) + "\n"); out.flush()
if __name__ == "__main__":
    main()
