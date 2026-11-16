import json, sys, collections
rows = [json.loads(l) for l in open(sys.argv[1])]
g = collections.defaultdict(list)
for r in rows: g[(r["model"], r["decades"], r["batch"], r["momentum"])].append(r)
def final(r): return r["hist"][-1][1] if not r["diverged"] else float("inf")
print("model decades batch | SGD best lr, final loss, acc | mom0.9 best lr, final loss, acc | loss ratio | edge?")
for m in ["softmax", "mlp"]:
    for d in [0, 1, 2]:
        for b in [10000, 256]:
            res = {}
            for mom in [0.0, 0.9]:
                rs = sorted(g[(m, d, b, mom)], key=lambda r: r["lr"])
                best = min(rs, key=final); i = rs.index(best)
                res[mom] = (best["lr"], final(best), best["hist"][-1][2], i in (0, len(rs) - 1))
            s, p = res[0.0], res[0.9]
            print(f"{m:8s} {d} {b:6d} | {s[0]:.4g} {s[1]:.4f} {s[2]:.3f} | {p[0]:.4g} {p[1]:.4f} {p[2]:.3f} | {s[1]/p[1]:.2f}x | edge sgd={s[3]} mom={p[3]}")
