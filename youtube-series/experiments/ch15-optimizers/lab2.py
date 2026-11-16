"""Full-dataset training with a held-out validation split, per-epoch train / validation / test metrics.

Reuses the models and data loader from lab.py. Split: a fixed random permutation (seed 0) of the 60,000
training images; the first --val images are validation, the rest are training. --full 1 trains on all
60,000 images instead (no validation), for a final retrain with already-chosen hyperparameters.
Per epoch (eval mode, whole sets): train loss/acc, validation loss/acc, test loss/acc.
"""
import argparse
import json
import math
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from lab import ConvNet, MT19937, SeriesMLP, load_idx


ACTS = {"tanh": torch.tanh, "relu": torch.relu, "leaky_relu": lambda z: F.leaky_relu(z, 0.01),
        "gelu": F.gelu, "silu": F.silu, "elu": F.elu, "mish": F.mish, "softplus": F.softplus}
CATEGORY = {"tanh": "saturating", "relu": "rectifier", "leaky_relu": "rectifier",
            "gelu": "smooth", "silu": "smooth", "mish": "smooth", "elu": "smooth", "softplus": "smooth"}


def second_moment(act):
    """E[f(z)^2] for z ~ N(0, 1), by quadrature, so a smooth activation gets a variance-preserving gain."""
    z = torch.linspace(-10, 10, 400001, dtype=torch.float64)
    pdf = torch.exp(-z * z / 2) / math.sqrt(2 * math.pi)
    return torch.trapz(ACTS[act](z) ** 2 * pdf, z).item()


def init_description(act):
    cat = CATEGORY[act]
    if cat == "saturating":
        return f"{act}: Xavier uniform, gain 5/3"
    if act == "relu":
        return "relu: He normal, std sqrt(2/fan_in)"
    if act == "leaky_relu":
        return "leaky_relu: He normal with slope 0.01, std sqrt(2/((1+0.01^2) fan_in))"
    return f"{act}: variance-preserving normal, std 1/sqrt(fan_in * {second_moment(act):.4f}) (E[f(z)^2] measured)"


def init_weight(act, n_in, n_out, gen, output_layer):
    if output_layer:  # linear layer feeding softmax: LeCun normal
        return torch.randn(n_in, n_out, generator=gen, dtype=torch.float64) / math.sqrt(n_in)
    cat = CATEGORY[act]
    if cat == "saturating":
        limit = (5.0 / 3.0) * math.sqrt(6.0 / (n_in + n_out))
        return (torch.rand(n_in, n_out, generator=gen, dtype=torch.float64) * 2 - 1) * limit
    if act == "relu":
        std = math.sqrt(2.0 / n_in)
    elif act == "leaky_relu":
        std = math.sqrt(2.0 / ((1 + 0.01 ** 2) * n_in))
    else:
        std = 1.0 / math.sqrt(n_in * second_moment(act))
    return torch.randn(n_in, n_out, generator=gen, dtype=torch.float64) * std


class FastMLP(SeriesMLP):
    """Same architecture and initialization distribution (uniform +-1/sqrt(in), zero bias) as the series,
    drawn with torch's generator so wide networks initialize quickly."""

    def __init__(self, width, depth, residual, act, gen, dtype, init="series"):
        nn.Module.__init__(self)
        self.residual = residual
        self.act = ACTS[act]
        shapes = [(784, width)] + [(width, width)] * (depth - 1) + [(width, 10)]
        self.weights, self.biases = nn.ParameterList(), nn.ParameterList()
        for k, (n_in, n_out) in enumerate(shapes):
            if init in ("auto", "auto_scaled"):
                w = init_weight(act, n_in, n_out, gen, output_layer=(k == len(shapes) - 1))
                if init == "auto_scaled" and residual and 1 <= k < depth:  # the residual branches
                    w = w / math.sqrt(depth - 1)
            else:
                limit = 1.0 / math.sqrt(n_in)
                w = (torch.rand(n_in, n_out, generator=gen, dtype=torch.float64) * 2 - 1) * limit
            self.weights.append(nn.Parameter(w.to(dtype)))
            self.biases.append(nn.Parameter(torch.zeros(n_out, dtype=dtype)))
        self.n_hidden = depth


@torch.no_grad()
def metrics(model, x, y, batch=5000):
    model.eval()
    loss_sum, correct = 0.0, 0
    for i in range(0, len(x), batch):
        out = model(x[i:i + batch])
        loss_sum += F.cross_entropy(out.double(), y[i:i + batch], reduction="sum").item()
        correct += (out.argmax(1) == y[i:i + batch]).sum().item()
    model.train()
    return loss_sum / len(x), 100.0 * correct / len(x)


def run(a):
    t0 = time.time()
    dev = torch.device(a.device)
    dtype = torch.float64 if a.dtype == "f64" else torch.float32
    d = Path(a.data)
    xtr, ytr = load_idx(d / "train-images-idx3-ubyte", d / "train-labels-idx1-ubyte")
    xte, yte = load_idx(d / "t10k-images-idx3-ubyte", d / "t10k-labels-idx1-ubyte")
    X = torch.from_numpy(xtr.astype(np.float64) / 255.0).to(dev, dtype)
    Y = torch.from_numpy(ytr.astype(np.int64)).to(dev)
    XT = torch.from_numpy(xte.astype(np.float64) / 255.0).to(dev, dtype)
    YT = torch.from_numpy(yte.astype(np.int64)).to(dev)
    perm = torch.randperm(60000, generator=torch.Generator().manual_seed(0)).to(dev)
    if a.full:
        tr_idx, va_idx = perm, None
    else:
        va_idx, tr_idx = perm[:a.val], perm[a.val:]
    Xtr, Ytr = X[tr_idx], Y[tr_idx]
    Xva, Yva = (X[va_idx], Y[va_idx]) if va_idx is not None else (None, None)
    n = len(Xtr)

    gen = torch.Generator().manual_seed(a.seed)
    if a.model == "mlp":
        model = FastMLP(a.width, a.depth, bool(a.res), a.act, gen, dtype, a.init).to(dev)
    else:
        model = ConvNet(a.width, a.depth, bool(a.res), a.norm, a.start_scale, gen, dtype).to(dev)
    n_params = sum(p.numel() for p in model.parameters())
    if a.opt == "sgd":
        opt = torch.optim.SGD(model.parameters(), lr=a.lr, momentum=a.momentum, weight_decay=a.wd)
    elif a.opt == "adamw":
        opt = torch.optim.AdamW(model.parameters(), lr=a.lr, betas=(0.9, 0.999), eps=1e-8, weight_decay=a.wd)
    else:
        opt = torch.optim.Adam(model.parameters(), lr=a.lr, betas=(0.9, 0.999), eps=1e-8, weight_decay=a.wd)
    if a.model == "mlp" and a.init != "series":
        print(f"# init {a.init}: {init_description(a.act)}; output layer LeCun normal; biases zero"
              + (f"; residual branches scaled by 1/sqrt({a.depth - 1})" if a.init == "auto_scaled" and a.res else ""), flush=True)
    print(f"# {vars(a)} params={n_params} train={n}", flush=True)

    shuffler = torch.Generator().manual_seed(a.seed * 7919 + 1)
    history = []
    for epoch in range(a.epochs):
        if a.sched == "cosine":
            lr = 0.5 * a.lr * (1 + math.cos(math.pi * epoch / a.epochs))
        else:
            lr = a.lr * (a.decay ** epoch)
        for g in opt.param_groups:
            g["lr"] = lr
        order = torch.randperm(n, generator=shuffler).to(dev) if a.shuffle else None
        e0 = time.time()
        for start in range(0, n, a.batch):
            idx = order[start:start + a.batch] if order is not None else slice(start, start + a.batch)
            xb, yb = Xtr[idx], Ytr[idx]
            opt.zero_grad(set_to_none=True)
            loss = F.cross_entropy(model(xb), yb)
            loss.backward()
            opt.step()
        tr_loss, tr_acc = metrics(model, Xtr, Ytr)
        te_loss, te_acc = metrics(model, XT, YT)
        rec = {"epoch": epoch + 1, "lr": lr, "train_loss": tr_loss, "train_acc": tr_acc,
               "test_loss": te_loss, "test_acc": te_acc, "sec": time.time() - e0}
        if va_idx is not None:
            rec["val_loss"], rec["val_acc"] = metrics(model, Xva, Yva)
        if not math.isfinite(tr_loss):
            rec["diverged"] = True
        history.append(rec)
        v = f" val {rec['val_loss']:.4f}/{rec['val_acc']:.2f}" if "val_loss" in rec else ""
        print(f"epoch {epoch + 1} lr {lr:.4g} train {tr_loss:.4f}/{tr_acc:.2f}{v} "
              f"test {te_loss:.4f}/{te_acc:.2f} ({rec['sec']:.1f}s)", flush=True)
        if rec.get("diverged"):
            break
    out = {"args": vars(a), "params": n_params, "n_train": n, "history": history, "total_sec": time.time() - t0}
    print("RESULT " + json.dumps(out), flush=True)


def parser():
    p = argparse.ArgumentParser()
    p.add_argument("--model", choices=["mlp", "cnn"], default="mlp")
    p.add_argument("--width", type=int, default=32)
    p.add_argument("--depth", type=int, default=16)
    p.add_argument("--res", type=int, default=1)
    p.add_argument("--act", default="tanh")
    p.add_argument("--init", default="series", choices=["series", "auto", "auto_scaled"])
    p.add_argument("--norm", type=int, default=0)
    p.add_argument("--start_scale", type=float, default=1.0)
    p.add_argument("--val", type=int, default=5000)
    p.add_argument("--full", type=int, default=0)
    p.add_argument("--epochs", type=int, default=20)
    p.add_argument("--batch", type=int, default=64)
    p.add_argument("--lr", type=float, default=0.001)
    p.add_argument("--decay", type=float, default=0.95)
    p.add_argument("--sched", default="exp", choices=["exp", "cosine"])
    p.add_argument("--opt", default="adam", choices=["sgd", "adam", "adamw"])
    p.add_argument("--momentum", type=float, default=0.0)
    p.add_argument("--wd", type=float, default=0.0)
    p.add_argument("--seed", type=int, default=1)
    p.add_argument("--shuffle", type=int, default=1)
    p.add_argument("--device", default="cuda")
    p.add_argument("--dtype", default="f32", choices=["f32", "f64"])
    p.add_argument("--data", default="data")
    return p


if __name__ == "__main__":
    run(parser().parse_args())
