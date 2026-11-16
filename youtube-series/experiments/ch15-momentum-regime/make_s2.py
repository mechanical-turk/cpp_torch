import json
LRS = [10 ** (e / 4) for e in range(2, 25)]  # 3.2 .. 1e6, quarter decades (23 pts)
out = []
for dec in [0, 1, 2, 3]:
    for batch in [10000, 256]:
        for mom, shift in [(0.0, 1.0), (0.9, 0.1)]:
            for lr in LRS:
                out.append(dict(stage="S2", model="softmax", decades=dec, batch=batch, momentum=mom, lr=round(lr * shift, 6), seed=0, n=10000, steps=2000, eval=10))
open("jobs_S2.txt", "w").write("\n".join(json.dumps(o) for o in out) + "\n"); print(len(out))
