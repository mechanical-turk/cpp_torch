"""PyTorch port of the Deep Learning, All the Way Down experiment harnesses.

MLP: the Chapter 14 network (Linear + tanh hidden layers, optional Residual, final Linear), with
     the series' own initialization reproduced bit for bit from libc++ std::mt19937 and
     std::uniform_real_distribution<double>, so epoch losses can be compared with the video.
CNN: the standalone harness used for the convolution experiments (stem conv, K same-padded
     conv -> norm -> ReLU blocks with optional residual and start scale, final pool and linear).

Run one configuration:   python lab.py --model mlp --res 1 --lr 0.5 --decay 0.9 --epochs 10 ...
Run many in parallel:    python sweep.py jobs.txt --workers 6
"""
import argparse
import json
import math
import struct
import sys
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


# ----------------------------------------------------------------------------------------------
# libc++-compatible Mersenne Twister, so the MLP starts from the same weights as the C++ series.
# ----------------------------------------------------------------------------------------------
class MT19937:
    def __init__(self, seed):
        self.mt = [0] * 624
        self.mt[0] = seed & 0xFFFFFFFF
        for i in range(1, 624):
            prev = self.mt[i - 1]
            self.mt[i] = (1812433253 * (prev ^ (prev >> 30)) + i) & 0xFFFFFFFF
        self.index = 624

    def _twist(self):
        mt = self.mt
        for i in range(624):
            y = (mt[i] & 0x80000000) | (mt[(i + 1) % 624] & 0x7FFFFFFF)
            mt[i] = mt[(i + 397) % 624] ^ (y >> 1) ^ (0x9908B0DF if y & 1 else 0)
        self.index = 0

    def next_u32(self):
        if self.index >= 624:
            self._twist()
        y = self.mt[self.index]
        self.index += 1
        y ^= y >> 11
        y ^= (y << 7) & 0x9D2C5680
        y ^= (y << 15) & 0xEFC60000
        y ^= y >> 18
        return y & 0xFFFFFFFF

    def uniform(self, low, high):
        """std::uniform_real_distribution<double> as implemented by libc++ (two 32-bit draws)."""
        s = float(self.next_u32())
        s += float(self.next_u32()) * 4294967296.0
        u = s / 18446744073709551616.0
        if u >= 1.0:
            u = math.nextafter(1.0, 0.0)
        return (high - low) * u + low


def series_linear_weights(rng, n_in, n_out):
    limit = 1.0 / math.sqrt(n_in)
    return torch.tensor([rng.uniform(-limit, limit) for _ in range(n_in * n_out)],
                        dtype=torch.float64).reshape(n_in, n_out)


# ----------------------------------------------------------------------------------------------
# Data
# ----------------------------------------------------------------------------------------------
def load_idx(images_path, labels_path):
    with open(images_path, "rb") as f:
        magic, n, rows, cols = struct.unpack(">IIII", f.read(16))
        assert magic == 2051 and rows == 28 and cols == 28
        x = np.frombuffer(f.read(), dtype=np.uint8).reshape(n, 784)
    with open(labels_path, "rb") as f:
        magic, n2 = struct.unpack(">II", f.read(8))
        assert magic == 2049 and n2 == n
        y = np.frombuffer(f.read(), dtype=np.uint8)
    return x, y


# ----------------------------------------------------------------------------------------------
# Models
# ----------------------------------------------------------------------------------------------
class SeriesMLP(nn.Module):
    """First hidden layer (784 -> width), `depth - 1` more hidden layers optionally wrapped in
    Residual, then a final Linear. Hidden layer = Linear + activation, as in Chapter 14."""

    def __init__(self, width, depth, residual, act, rng, dtype):
        super().__init__()
        self.residual = residual
        self.act = {"tanh": torch.tanh, "relu": torch.relu}[act]
        shapes = [(784, width)] + [(width, width)] * (depth - 1)
        self.weights = nn.ParameterList()
        self.biases = nn.ParameterList()
        for n_in, n_out in shapes + [(width, 10)]:
            self.weights.append(nn.Parameter(series_linear_weights(rng, n_in, n_out).to(dtype)))
            self.biases.append(nn.Parameter(torch.zeros(n_out, dtype=dtype)))
        self.n_hidden = depth

    def forward(self, x, trace=None):
        for i in range(self.n_hidden):
            h = self.act(x @ self.weights[i] + self.biases[i])
            x = x + h if (self.residual and i > 0) else h
            if trace is not None:
                x.retain_grad()
                trace.append(x)
        out = x @ self.weights[-1] + self.biases[-1]
        if trace is not None:
            out.retain_grad()
            trace.append(out)
        return out


class ConvNet(nn.Module):
    """Stem conv(1->C, 3x3 valid) + ReLU + maxpool, then K blocks of conv(C->C, 3x3 same)
    -> norm -> ReLU (plus the block input when residual), maxpool, linear to 10 classes.
    norm: 0 none, 1 layer norm over (C,H,W) with per-channel affine, 2 batch norm."""

    def __init__(self, channels, blocks, residual, norm, start_scale, gen, dtype):
        super().__init__()
        self.residual, self.norm_kind = residual, norm
        self.stem = nn.Conv2d(1, channels, 3)
        self.blocks = nn.ModuleList([nn.Conv2d(channels, channels, 3, padding=1) for _ in range(blocks)])
        self.norms = nn.ModuleList()
        for _ in range(blocks):
            if norm == 1:
                self.norms.append(nn.GroupNorm(1, channels, eps=1e-5))
            elif norm == 2:
                self.norms.append(nn.BatchNorm2d(channels, eps=1e-5, momentum=0.1))
            else:
                self.norms.append(nn.Identity())
        flat = channels * 6 * 6
        self.head = nn.Linear(flat, 10)
        with torch.no_grad():
            for conv in [self.stem, *self.blocks]:
                fan_in = conv.in_channels * 9
                conv.weight.copy_(torch.randn(conv.weight.shape, generator=gen) * math.sqrt(2.0 / fan_in))
                conv.bias.zero_()
            self.head.weight.copy_(torch.randn(self.head.weight.shape, generator=gen) * math.sqrt(1.0 / flat))
            self.head.bias.zero_()
            for n in self.norms:
                if norm:
                    n.weight.fill_(start_scale)
                    n.bias.zero_()
        self.to(dtype)

    def forward(self, x, trace=None):
        x = x.view(-1, 1, 28, 28)
        x = F.max_pool2d(F.relu(self.stem(x)), 2)
        for conv, norm in zip(self.blocks, self.norms):
            h = F.relu(norm(conv(x)))
            x = x + h if self.residual else h
            if trace is not None:
                x.retain_grad()
                trace.append(x)
        x = F.max_pool2d(x, 2).flatten(1)
        return self.head(x)


def rms_per_sample(t):
    return t.detach().float().pow(2).flatten(1).mean(1).sqrt().mean().item()


# ----------------------------------------------------------------------------------------------
# Train / evaluate
# ----------------------------------------------------------------------------------------------
@torch.no_grad()
def evaluate(model, x, y, n, batch=1000):
    model.eval()
    correct = 0
    for i in range(0, n, batch):
        j = min(i + batch, n)
        correct += (model(x[i:j]).argmax(1) == y[i:j]).sum().item()
    model.train()
    return 100.0 * correct / n


def run(args):
    t_start = time.time()
    dev = torch.device(args.device)
    dtype = torch.float64 if args.dtype == "f64" else torch.float32
    data = Path(args.data)
    xtr, ytr = load_idx(data / "train-images-idx3-ubyte", data / "train-labels-idx1-ubyte")
    xte, yte = load_idx(data / "t10k-images-idx3-ubyte", data / "t10k-labels-idx1-ubyte")
    def to_t(x): return torch.from_numpy(x.astype(np.float64) / 255.0).to(dev, dtype)
    xtr_t, xte_t = to_t(xtr[: max(args.n_train, 10000)]), to_t(xte)
    ytr_t = torch.from_numpy(ytr[: max(args.n_train, 10000)].astype(np.int64)).to(dev)
    yte_t = torch.from_numpy(yte.astype(np.int64)).to(dev)

    if args.model == "mlp":
        model = SeriesMLP(args.width, args.depth, bool(args.res), args.act, MT19937(args.seed), dtype)
        model = model.to(dev)
    else:
        gen = torch.Generator().manual_seed(args.seed)
        model = ConvNet(args.width, args.depth, bool(args.res), args.norm, args.start_scale, gen, dtype).to(dev)
    if args.perturb:
        with torch.no_grad():
            model.weights[0][0, 0] += args.perturb
    n_params = sum(p.numel() for p in model.parameters())
    if args.opt == "sgd":
        opt = torch.optim.SGD(model.parameters(), lr=args.lr)
    else:
        opt = torch.optim.Adam(model.parameters(), lr=args.lr, betas=(0.9, 0.999), eps=1e-8)
    print(f"# {args.model} params={n_params} device={args.device} {args.dtype} opt={args.opt} "
          f"width={args.width} depth={args.depth} res={args.res} norm={args.norm} "
          f"start_scale={args.start_scale} n={args.n_train} epochs={args.epochs} lr={args.lr} "
          f"decay={args.decay} seed={args.seed}", flush=True)

    lr = args.lr
    history = []
    for epoch in range(args.epochs):
        for g in opt.param_groups:
            g["lr"] = lr
        total_loss, seen = 0.0, 0
        e_start = time.time()
        order = torch.randperm(args.n_train, generator=torch.Generator().manual_seed(args.seed * 1000 + epoch)).to(dev) \
            if args.shuffle else None
        while seen < args.n_train:
            bs = min(args.batch, args.n_train - seen)
            if order is None:
                xb, yb = xtr_t[seen:seen + bs], ytr_t[seen:seen + bs]
            else:
                idx = order[seen:seen + bs]
                xb, yb = xtr_t[idx], ytr_t[idx]
            report = args.report and epoch == 0 and seen == 0
            trace = [] if report else None
            opt.zero_grad(set_to_none=True)
            logits = model(xb, trace)
            if args.naive_softmax:
                probs = logits.exp() / logits.exp().sum(1, keepdim=True)
                per_sample = -probs.gather(1, yb[:, None]).log().squeeze(1)
            else:
                per_sample = F.cross_entropy(logits, yb, reduction="none")
            loss = per_sample.mean()
            if report:
                # report gradients of the per-sample-summed loss, as the C++ harness does
                (per_sample.sum()).backward(retain_graph=True)
                print("report (first batch): layer signal gradient")
                for k, t in enumerate(trace):
                    print(f"  {k + 1:2d} {rms_per_sample(t):.2e} {rms_per_sample(t.grad):.2e}")
                opt.zero_grad(set_to_none=True)
            loss.backward()
            opt.step()
            total_loss += loss.item() * bs
            seen += bs
        lr *= args.decay
        test = evaluate(model, xte_t, yte_t, args.test_n)
        rec = {"epoch": epoch + 1, "loss": total_loss / seen, "test": test, "sec": time.time() - e_start}
        if epoch + 1 == args.epochs or (epoch + 1) % 5 == 0:
            rec["train10k"] = evaluate(model, xtr_t, ytr_t, 10000)
        history.append(rec)
        extra = f" train10k {rec['train10k']:.2f}" if "train10k" in rec else ""
        print(f"epoch {rec['epoch']} loss {rec['loss']:.6g} test {test:.2f}{extra} ({rec['sec']:.1f}s)", flush=True)
    result = {"args": vars(args), "params": n_params, "history": history, "total_sec": time.time() - t_start}
    print("RESULT " + json.dumps(result), flush=True)
    return result


def parser():
    p = argparse.ArgumentParser()
    p.add_argument("--model", choices=["mlp", "cnn"], default="mlp")
    p.add_argument("--width", type=int, default=32, help="MLP width, or CNN channels")
    p.add_argument("--depth", type=int, default=16, help="MLP hidden layers, or CNN blocks")
    p.add_argument("--res", type=int, default=0)
    p.add_argument("--act", default="tanh")
    p.add_argument("--norm", type=int, default=0)
    p.add_argument("--start_scale", type=float, default=1.0)
    p.add_argument("--n_train", type=int, default=10000)
    p.add_argument("--test_n", type=int, default=10000)
    p.add_argument("--epochs", type=int, default=10)
    p.add_argument("--batch", type=int, default=64)
    p.add_argument("--lr", type=float, default=0.08)
    p.add_argument("--decay", type=float, default=0.95)
    p.add_argument("--opt", choices=["sgd", "adam"], default="sgd")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--shuffle", type=int, default=0)
    p.add_argument("--report", type=int, default=0)
    p.add_argument("--naive_softmax", type=int, default=0)
    p.add_argument("--perturb", type=float, default=0.0)
    p.add_argument("--device", default="cpu")
    p.add_argument("--dtype", choices=["f32", "f64"], default="f32")
    p.add_argument("--data", default="data")
    return p


if __name__ == "__main__":
    run(parser().parse_args())
