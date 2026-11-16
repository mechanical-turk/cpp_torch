"""Steps-to-target for the Chapter 14 network under different optimizers.

Same network, data order and initialization as the Chapter 14 recording (lab.py reproduces 92.85% on the
first 2,000 test images): 16 tanh layers, width 32, residual, series initialization from std::mt19937,
first 10,000 training images in file order (no shuffle), batch 64 (157 steps per epoch), float64 CPU.

Added for this experiment: a validation set (training images 10,000-14,999, never trained on), evaluated
every --eval_every optimizer steps, so "steps needed to reach a target accuracy" can be read off a curve.
Test accuracy (first 2,000 test images, as in the video) is recorded at the same points but never used to
select anything.

SGD momentum follows torch.optim.SGD: v = beta v + g; w -= lr v (so the effective step is about lr/(1-beta)).
The learning rate is multiplied by --decay after every epoch.
"""
import argparse
import json
import math
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F

from lab import MT19937, SeriesMLP, load_idx
from lab2 import FastMLP

torch.set_num_threads(1)


@torch.no_grad()
def evaluate(model, x, y):
    out = model(x)
    return 100.0 * (out.argmax(1) == y).float().mean().item(), F.cross_entropy(out, y).item()


def run(a):
    t0 = time.time()
    d = Path(a.data)
    xtr, ytr = load_idx(d / "train-images-idx3-ubyte", d / "train-labels-idx1-ubyte")
    xte, yte = load_idx(d / "t10k-images-idx3-ubyte", d / "t10k-labels-idx1-ubyte")

    def t(x):
        return torch.from_numpy(x.astype(np.float64) / 255.0)

    X, Y = t(xtr[:10000]), torch.from_numpy(ytr[:10000].astype(np.int64))
    XV, YV = t(xtr[10000:15000]), torch.from_numpy(ytr[10000:15000].astype(np.int64))
    XT2, YT2 = t(xte[:2000]), torch.from_numpy(yte[:2000].astype(np.int64))
    XT, YT = t(xte), torch.from_numpy(yte.astype(np.int64))

    if a.init == "series":  # the Chapter 14 initialization, bit for bit
        model = SeriesMLP(a.width, a.depth, bool(a.res), a.act, MT19937(a.seed), torch.float64)
    else:  # He normal for ReLU (residual branches scaled by 1/sqrt(depth - 1)), via lab2.FastMLP
        model = FastMLP(a.width, a.depth, bool(a.res), a.act, torch.Generator().manual_seed(a.seed), torch.float64,
                        "auto_scaled" if a.res else "auto")
    if a.opt == "sgd":
        opt = torch.optim.SGD(model.parameters(), lr=a.lr, momentum=a.momentum, nesterov=bool(a.nesterov))
    else:
        opt = torch.optim.Adam(model.parameters(), lr=a.lr, betas=(a.beta1, a.beta2), eps=1e-8)

    history, step, lr, diverged = [], 0, a.lr, False

    def record(epoch_loss=None):
        va, vl = evaluate(model, XV, YV)
        ta, tl = evaluate(model, XT2, YT2)
        rec = {"step": step, "epoch": step / 157.0, "val_acc": va, "val_loss": vl, "test_acc": ta, "test_loss": tl}
        if epoch_loss is not None:
            rec["train_loss"] = epoch_loss
        if a.train_eval:  # loss and accuracy on all 10,000 training images (the optimization objective)
            rec["train_full_acc"], rec["train_full_loss"] = evaluate(model, X, Y)
        history.append(rec)

    record()
    epochs = a.epochs if not a.max_steps else -(-a.max_steps * a.batch // len(X)) + 1  # --max_steps: fixed step budget
    for epoch in range(epochs):
        for g in opt.param_groups:
            g["lr"] = lr
        total, seen = 0.0, 0
        for start in range(0, len(X), a.batch):
            xb, yb = X[start:start + a.batch], Y[start:start + a.batch]
            opt.zero_grad(set_to_none=True)
            loss = F.cross_entropy(model(xb), yb)
            if not math.isfinite(loss.item()):
                diverged = True
                break
            loss.backward()
            opt.step()
            step += 1
            total += loss.item() * len(xb)
            seen += len(xb)
            if step % a.eval_every == 0:
                record()
            if a.max_steps and step >= a.max_steps:
                break
        if diverged:
            break
        if a.max_steps:  # fixed step budget: evaluate on the step grid only
            if step >= a.max_steps:
                break
            continue
        if step % a.eval_every != 0:
            record()
        history[-1]["train_loss"] = total / seen
        lr *= a.decay
        print(f"epoch {epoch + 1} step {step} lr {lr / a.decay:.4g} loss {total / seen:.4f} "
              f"val {history[-1]['val_acc']:.2f} test2000 {history[-1]['test_acc']:.2f}", flush=True)
    final_test_full = evaluate(model, XT, YT)[0] if not diverged else None
    out = {"args": vars(a), "history": history, "diverged": diverged, "steps": step,
           "final_test_full": final_test_full, "total_sec": time.time() - t0}
    print("RESULT " + json.dumps(out), flush=True)


def parser():
    p = argparse.ArgumentParser()
    p.add_argument("--width", type=int, default=32)
    p.add_argument("--depth", type=int, default=16)
    p.add_argument("--res", type=int, default=1)
    p.add_argument("--act", default="tanh", choices=["tanh", "relu"])
    p.add_argument("--init", default="series", choices=["series", "he"])
    p.add_argument("--opt", choices=["sgd", "adam"], default="sgd")
    p.add_argument("--lr", type=float, default=0.08)
    p.add_argument("--momentum", type=float, default=0.0)
    p.add_argument("--nesterov", type=int, default=0)
    p.add_argument("--beta1", type=float, default=0.9)
    p.add_argument("--beta2", type=float, default=0.999)
    p.add_argument("--decay", type=float, default=0.95)
    p.add_argument("--epochs", type=int, default=20)
    p.add_argument("--batch", type=int, default=64)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--max_steps", type=int, default=0, help="stop after this many optimizer steps, cycling the data")
    p.add_argument("--train_eval", type=int, default=0)
    p.add_argument("--eval_every", type=int, default=10)
    p.add_argument("--data", default="data")
    p.add_argument("--device", default="cpu")  # accepted for sweep.py; this script always runs on CPU
    return p


if __name__ == "__main__":
    run(parser().parse_args())
