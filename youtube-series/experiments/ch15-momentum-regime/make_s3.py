import json
LRS = [10 ** (e / 4) for e in range(-16, 9)]  # 1e-4 .. 100, quarter decades (25 pts)
out = []
for dec in [0, 1, 2]:
    for mom, shift in [(0.0, 1.0), (0.9, 0.1)]:
        for lr in LRS:
            out.append(dict(stage="S3", model="softmax", loss="mse", dtype="float64", decades=dec, batch=10000, momentum=mom,
                            lr=round(lr * shift, 8), seed=0, n=10000, steps=3000, eval=10))
open("jobs_S3.txt", "w").write("\n".join(json.dumps(o) for o in out) + "\n"); print(len(out))
