import json, sys
LRS = [10 ** (e / 4) for e in range(-16, 1)]  # 1e-4 .. 1 in quarter decades (17 pts)
out = []
for model in ["softmax", "mlp"]:
    for dec in [0, 1, 2]:
        for batch in [10000, 256]:
            for mom, shift in [(0.0, 1.0), (0.9, 0.1)]:
                for lr in LRS:
                    out.append(dict(stage="S1", model=model, decades=dec, batch=batch, momentum=mom, lr=round(lr * shift * 10 ** 0.5, 6) if mom else round(lr * 10 ** 0.5, 6), seed=0, n=10000, steps=2000, eval=10))
open("jobs_S1.txt", "w").write("\n".join(json.dumps(o) for o in out) + "\n")
print(len(out))
