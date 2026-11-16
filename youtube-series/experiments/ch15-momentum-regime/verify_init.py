import torch, torch.nn as nn
from regime import build
torch.manual_seed(0)
x = torch.randn(4096, 784)
for act in ("relu", "tanh"):
    for init in ("default", "proper"):
        net = build("mlp", 4, 128, 0, act, init)
        h = x; rms = []
        for m in net:
            h = m(h)
            if isinstance(m, (nn.ReLU, nn.Tanh)): rms.append(h.pow(2).mean().sqrt().item())
        print(f"{act:5s} {init:8s} hidden-activation rms by layer: {[round(r,3) for r in rms]}")
