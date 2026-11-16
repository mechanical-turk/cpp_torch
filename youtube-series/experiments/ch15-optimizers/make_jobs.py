"""Write the job files (one labsteps.py argument line per run) for every Chapter 15 optimizer experiment stage.

usage: python make_jobs.py   (writes jobs/stage*.txt)    run: python sweep.py jobs/stageM4.txt --workers 7 --out runs/stageM4 --device cpu --script labsteps.py
Stages (see docs/logs/content-experiments.md, entries dated 2026-10-26):
  M1  phase 1: Chapter 14 network, SGD and momentum, learning-rate sweeps, decay on/off, seeds 42, 1, 2
  M1b finer learning rates and seeds 3-7 for the best configurations;  M1c seeds 3-7 for SGD 0.06 and momentum 0.9 at 0.015
  M2  phase 1b: seven network variants, SGD vs momentum 0.9, seeds 42, 1
  M3  confirmation of setup F on seeds 3-7
  M4  phase 1c: batch-size sweep (16 to 10,000), 3,000 steps, constant rate;  M4b momentum grid extension for batches 256, 1024, 10000;  M5 batch-size confirmation, seeds 3-7
"""
from pathlib import Path

out = Path("jobs")
out.mkdir(exist_ok=True)


def write(name, lines):
    (out / f"{name}.txt").write_text("\n".join(lines) + "\n")
    print(name, len(lines))


# M1
L = []
for decay in (1.0, 0.95):
    for lr in (0.005, 0.01, 0.02, 0.04, 0.08, 0.12, 0.2, 0.3):
        for s in (42, 1, 2):
            L.append(f"--opt sgd --momentum 0 --lr {lr} --decay {decay} --seed {s}")
    for m in (0.5, 0.9, 0.95):
        for lr in (0.001, 0.002, 0.005, 0.01, 0.02, 0.04, 0.08, 0.12, 0.2):
            for s in (42, 1, 2):
                L.append(f"--opt sgd --momentum {m} --lr {lr} --decay {decay} --seed {s}")
write("stageM1", L)

# M1b
L = []
fine = {0.0: (0.06, 0.1), 0.5: (0.03, 0.05, 0.06), 0.9: (0.015, 0.03), 0.95: (0.0075, 0.015)}
for m, lrs in fine.items():
    for lr in lrs:
        for s in (42, 1, 2):
            L.append(f"--opt sgd --momentum {m} --lr {lr} --decay 0.95 --seed {s}")
for m, lr in ((0.0, 0.08), (0.5, 0.04), (0.9, 0.02), (0.95, 0.01)):
    for s in (3, 4, 5, 6, 7):
        L.append(f"--opt sgd --momentum {m} --lr {lr} --decay 0.95 --seed {s}")
write("stageM1b", L)

# M1c
L = [f"--opt sgd --momentum {m} --lr {lr} --decay 0.95 --seed {s}" for m, lr in ((0.0, 0.06), (0.9, 0.015)) for s in (3, 4, 5, 6, 7)]
write("stageM1c", L)

# M2
setups = {"A": "--width 32 --depth 4 --res 0 --act tanh --init series", "B": "--width 32 --depth 8 --res 0 --act tanh --init series",
          "C": "--width 32 --depth 8 --res 0 --act relu --init he", "D": "--width 32 --depth 16 --res 0 --act relu --init he",
          "E": "--width 32 --depth 16 --res 1 --act relu --init he", "F": "--width 128 --depth 16 --res 1 --act tanh --init series",
          "G": "--width 128 --depth 4 --res 0 --act relu --init he"}
sgd = (0.002, 0.005, 0.01, 0.02, 0.04, 0.06, 0.08, 0.12, 0.2, 0.3)
mom = (0.0002, 0.0005, 0.001, 0.002, 0.004, 0.006, 0.01, 0.015, 0.02, 0.03, 0.04)
L = []
for v in setups.values():
    for s in (42, 1):
        L += [f"{v} --opt sgd --momentum 0 --lr {lr} --decay 0.95 --seed {s}" for lr in sgd]
        L += [f"{v} --opt sgd --momentum 0.9 --lr {lr} --decay 0.95 --seed {s}" for lr in mom]
write("stageM2", L)

# M3
v = setups["F"]
L = []
for s in (3, 4, 5, 6, 7):
    L += [f"{v} --opt sgd --momentum 0 --lr {lr} --decay 0.95 --seed {s}" for lr in (0.01, 0.015, 0.02, 0.03, 0.04)]
    L += [f"{v} --opt sgd --momentum 0.9 --lr {lr} --decay 0.95 --seed {s}" for lr in (0.003, 0.004, 0.006, 0.008, 0.01)]
write("stageM3", L)

# M4, M4b
common = "--max_steps 3000 --eval_every 20 --train_eval 1 --decay 1.0"
sgd = (0.003, 0.005, 0.007, 0.01, 0.014, 0.02, 0.03, 0.04, 0.06, 0.08, 0.12, 0.16, 0.24)
mom = (0.0003, 0.0005, 0.0007, 0.001, 0.0014, 0.002, 0.003, 0.004, 0.006, 0.008, 0.012, 0.016, 0.024)
L = []
for b in (10000, 1024, 256, 64, 16):
    for s in (42, 1):
        L += [f"--batch {b} {common} --opt sgd --momentum 0 --lr {lr} --seed {s}" for lr in sgd]
        L += [f"--batch {b} {common} --opt sgd --momentum 0.9 --lr {lr} --seed {s}" for lr in mom]
write("stageM4", L)
L = [f"--batch {b} {common} --opt sgd --momentum 0.9 --lr {lr} --seed {s}" for b in (10000, 1024, 256) for s in (42, 1) for lr in (0.034, 0.048, 0.068, 0.096)]
write("stageM4b", L)

# M5: confirmation of the batch-size result on fresh seeds 3-7 (best learning rate and its grid neighbours from M4/M4b)
cfg = {64: ((0.04, 0.06, 0.08), (0.006, 0.008, 0.012)), 1024: ((0.04, 0.06, 0.08), (0.016, 0.024, 0.034)),
       10000: ((0.06, 0.08, 0.12), (0.034, 0.048, 0.068))}
L = []
for b, (sg, mo) in cfg.items():
    for s in (3, 4, 5, 6, 7):
        L += [f"--batch {b} {common} --opt sgd --momentum 0 --lr {lr} --seed {s}" for lr in sg]
        L += [f"--batch {b} {common} --opt sgd --momentum 0.9 --lr {lr} --seed {s}" for lr in mo]
write("stageM5", L)
