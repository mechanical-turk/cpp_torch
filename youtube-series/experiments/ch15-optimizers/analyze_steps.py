"""Steps-to-target analysis for labsteps.py sweeps, following the rules written in the experiment log.

usage: python analyze_steps.py runs/stageM1/results.jsonl [more.jsonl ...]

Steps to target = first evaluation step whose validation accuracy, and the next two, are all >= target.
Not reached within the run = None. Per arm and target: the (learning rate, decay) configuration with the lowest
mean steps over seeds (all seeds must reach it), with per-seed values; plus how many learning rates reach it.
"""
import json
import sys
from collections import defaultdict
from statistics import mean

TARGETS = (90.0, 92.0, 93.0, 93.5)


def steps_to(history, target):
    for i, e in enumerate(history):
        w = history[i:i + 3]
        if len(w) == 3 and all(x["val_acc"] >= target for x in w):
            return e["step"]
    return None


def arm_name(a):
    if a["opt"] == "adam":
        return f"adam b1={a['beta1']:g}"
    return "sgd" if not a["momentum"] else f"sgd+momentum {a['momentum']:g}"


def main():
    runs = defaultdict(dict)  # (arm, decay, lr) -> seed -> result
    for f in sys.argv[1:]:
        for line in open(f):
            r = json.loads(line)["result"]
            a = r["args"]
            runs[(arm_name(a), a["decay"], a["lr"])][a["seed"]] = r
    arms = sorted({k[0] for k in runs})
    for target in TARGETS:
        print(f"\n### Target {target}% validation (best configuration per arm and decay setting)")
        print("| Arm | Decay | Best lr | Mean steps | Per-seed steps | LRs reaching target (of swept) | Final test@2000 (mean) |")
        print("|---|---|---|---|---|---|---|")
        for arm in arms:
            for decay in sorted({k[1] for k in runs if k[0] == arm}, reverse=True):
                cfgs = {k[2]: v for k, v in runs.items() if k[0] == arm and k[1] == decay}
                scored = {}
                for lr, by_seed in cfgs.items():
                    st = [steps_to(r["history"], target) for _, r in sorted(by_seed.items())]
                    scored[lr] = (st, by_seed)
                ok = {lr: v for lr, v in scored.items() if all(s is not None for s in v[0])}
                reach = f"{len(ok)} of {len(scored)}"
                if not ok:
                    print(f"| {arm} | {decay:g} | none | not reached | | {reach} | |")
                    continue
                lr = min(ok, key=lambda k: mean(ok[k][0]))
                st, by_seed = ok[lr]
                fin = mean(r["history"][-1]["test_acc"] for r in by_seed.values())
                print(f"| {arm} | {decay:g} | {lr:g} | {mean(st):.0f} | {', '.join(map(str, st))} | {reach} | {fin:.2f} |")


if __name__ == "__main__":
    main()
