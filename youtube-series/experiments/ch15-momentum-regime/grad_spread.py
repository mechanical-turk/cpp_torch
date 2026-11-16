"""Per-weight gradient size at initialisation for network C (784-256-10 ReLU, He init, MSE) on MNIST
inputs standardised then scaled per pixel by 10**(-decades*r). Reports the spread of per-input-pixel
gradient rms (first layer weights, averaged over the 256 hidden units)."""
import numpy as np, torch, torch.nn.functional as F
from regime import load_idx, build
xtr, ytr = load_idx("data/train-images-idx3-ubyte", "data/train-labels-idx1-ubyte")
x = torch.tensor(xtr[:10000], dtype=torch.float32) / 255.0; y = torch.tensor(ytr[:10000], dtype=torch.long)
mu, sd = x.mean(0), x.std(0) + 0.1
for dec in (0, 2):
    g = torch.Generator().manual_seed(1)
    s = 10.0 ** (-dec * torch.rand(784, generator=g))
    X = (x - mu) / sd * s
    net = build("mlp", 1, 256, 1, "relu", "proper")
    F.mse_loss(net(X), F.one_hot(y, 10).float()).backward()
    gw = net[0].weight.grad.pow(2).mean(0).sqrt()          # rms over hidden units, per input pixel
    live = gw[(x.std(0) > 0)]                               # pixels that ever vary
    q = torch.quantile(live, torch.tensor([0.05, 0.5, 0.95]))
    print(f"decades {dec}: per-pixel first-layer gradient rms  5%={q[0]:.2e}  median={q[1]:.2e}  95%={q[2]:.2e}  95%/5% = {q[2]/q[0]:.0f}x   max/min = {live.max()/live.min():.0f}x")
