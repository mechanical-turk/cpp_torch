"""Per-setup SGD vs momentum screen (stage M2). usage: python analyze_screen.py results.jsonl [...]

For each setup and arm: the learning rate with the lowest mean steps to 90% (all seeds must reach it), with
per-seed values, how many learning rates reach each target, and the best final validation accuracy.
Rule from the log: momentum "clearly helps" if it needs >= 33% fewer steps to 90% on every seed pair, or reaches
90% where plain SGD never does.
"""
import json
import sys
from collections import defaultdict
from statistics import mean

from analyze_steps import steps_to

NAMES = {("tanh", 0, 4, 32): "A tanh plain d4 w32", ("tanh", 0, 8, 32): "B tanh plain d8 w32",
         ("relu", 0, 8, 32): "C relu plain d8 w32", ("relu", 0, 16, 32): "D relu plain d16 w32",
         ("relu", 1, 16, 32): "E relu res d16 w32", ("tanh", 1, 16, 128): "F tanh res d16 w128",
         ("relu", 0, 4, 128): "G relu plain d4 w128"}
TARGETS = (85.0, 90.0, 93.0)


def main():
    runs = defaultdict(dict)  # (setup, arm, lr) -> seed -> result
    for f in sys.argv[1:]:
        for line in open(f):
            r = json.loads(line)["result"]
            a = r["args"]
            setup = NAMES.get((a["act"], a["res"], a["depth"], a["width"]), str((a["act"], a["res"], a["depth"], a["width"])))
            runs[(setup, "momentum 0.9" if a["momentum"] else "plain SGD", a["lr"])][a["seed"]] = r
    for setup in sorted({k[0] for k in runs}):
        print(f"\n## {setup}")
        best = {}
        for arm in ("plain SGD", "momentum 0.9"):
            cfgs = {k[2]: v for k, v in runs.items() if k[0] == setup and k[1] == arm}
            row = [arm]
            for t in TARGETS:
                sc = {lr: [steps_to(r["history"], t) for _, r in sorted(bs.items())] for lr, bs in cfgs.items()}
                ok = {lr: s for lr, s in sc.items() if all(x is not None for x in s)}
                if ok:
                    lr = min(ok, key=lambda k: mean(ok[k]))
                    row.append(f"{t:g}%: lr {lr:g} steps {ok[lr]} ({len(ok)}/{len(sc)} lrs)")
                    if t == 90.0:
                        best[arm] = ok[lr]
                else:
                    row.append(f"{t:g}%: not reached ({len(ok)}/{len(sc)} lrs)")
            fin = max(mean(r["history"][-1]["val_acc"] for r in bs.values()) for bs in cfgs.values() if all(not r["diverged"] for r in bs.values()))
            row.append(f"best final val {fin:.2f}")
            print("  " + " | ".join(row))
        s, m = best.get("plain SGD"), best.get("momentum 0.9")
        if m and not s:
            print("  RULE: momentum reaches 90%, plain SGD does not -> counts")
        elif s and m:
            fewer = [1 - b / a for a, b in zip(s, m)]
            print(f"  RULE: momentum fewer steps by seed: {[round(x, 2) for x in fewer]} -> {'PASS' if all(x >= 0.33 for x in fewer) else 'no'}")
        else:
            print("  RULE: neither arm reaches 90% (or only SGD does)")


if __name__ == "__main__":
    main()
