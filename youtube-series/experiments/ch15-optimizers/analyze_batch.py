"""Batch-size sweep (stage M4): momentum vs plain SGD steps to target. usage: python analyze_batch.py results.jsonl [...]

Per batch size and arm: the learning rate with the lowest mean steps to the primary target (validation 92%) over seeds,
per-seed steps, grid-edge warnings, and momentum's saving per seed. Also the secondary targets at the same learning
rates and at each target's own best rate. Rule from the log: supported if at batch 10,000 momentum saves >= 33% on both
seeds and the saving at 1,024 and at 10,000 each exceeds the saving at 64 by >= 15 points.
"""
import json
import sys
from collections import defaultdict
from statistics import mean

from analyze_steps import steps_to


def train_loss_steps(history, target):
    for i, e in enumerate(history):
        w = history[i:i + 3]
        if len(w) == 3 and all(x["train_full_loss"] <= target for x in w):
            return e["step"]
    return None


TARGETS = [("val 90%", lambda h: steps_to(h, 90.0)), ("val 92%", lambda h: steps_to(h, 92.0)),
           ("val 93%", lambda h: steps_to(h, 93.0)), ("train loss 0.1", lambda h: train_loss_steps(h, 0.1))]


def main():
    runs = defaultdict(dict)  # (batch, momentum, lr) -> seed -> history
    for f in sys.argv[1:]:
        for line in open(f):
            r = json.loads(line)["result"]
            a = r["args"]
            runs[(a["batch"], a["momentum"], a["lr"])][a["seed"]] = r["history"] if not r["diverged"] else r["history"]
    batches = sorted({k[0] for k in runs})
    saving_primary = {}
    for b in batches:
        print(f"\n## batch {b}")
        for tname, fn in TARGETS:
            best = {}
            for m in (0.0, 0.9):
                cfg = {k[2]: v for k, v in runs.items() if k[0] == b and k[1] == m}
                sc = {lr: [fn(h) for _, h in sorted(bs.items())] for lr, bs in cfg.items()}
                ok = {lr: s for lr, s in sc.items() if all(x is not None for x in s)}
                if not ok:
                    print(f"  {tname:15s} {'SGD' if m == 0 else 'mom0.9':6s} not reached at any lr")
                    continue
                lr = min(ok, key=lambda k: mean(ok[k]))
                grid = sorted(sc)
                edge = " EDGE" if lr in (grid[0], grid[-1]) else ""
                best[m] = (lr, ok[lr])
                print(f"  {tname:15s} {'SGD' if m == 0 else 'mom0.9':6s} lr {lr:g}{edge} steps {ok[lr]} ({len(ok)}/{len(sc)} lrs reach)")
            if len(best) == 2:
                sav = [1 - y / x for x, y in zip(best[0.0][1], best[0.9][1])]
                print(f"  {'':15s} momentum saving per seed: {[round(s, 2) for s in sav]}")
                if tname == "val 92%":
                    saving_primary[b] = sav
    print("\n## rule check (primary target val 92%)")
    for b, s in saving_primary.items():
        print(f"  batch {b}: saving {[round(x, 2) for x in s]} mean {mean(s):.2f}")
    if all(k in saving_primary for k in (64, 1024, 10000)):
        s64, s1k, sfull = (mean(saving_primary[k]) for k in (64, 1024, 10000))
        c1 = all(x >= 0.33 for x in saving_primary[10000])
        c2 = s1k - s64 >= 0.15 and sfull - s64 >= 0.15
        print(f"  full batch >= 33% on both seeds: {c1}; savings at 1024 / 10000 exceed 64 by >= 15 pts: {c2} -> {'SUPPORTED' if c1 and c2 else 'not supported'}")


if __name__ == "__main__":
    main()
