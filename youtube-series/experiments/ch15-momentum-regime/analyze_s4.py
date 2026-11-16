import json, collections, sys
for d, budget in ((1, 3000), (2, 8000)):
    rows = [json.loads(l) for l in open(f"runs/S4_d{d}.jsonl")]
    g = collections.defaultdict(list)
    for r in rows: g[(r["seed"], r["momentum"])].append(r)
    def steps_to(r, frac=0.01):
        h = r["hist"]; e0 = h[0][1] - r["lstar"]
        for s, l, _ in h:
            if l - r["lstar"] <= frac * e0: return s
        return None
    print(f"\n=== decades {d} (budget {budget}); steps to 1% excess, best LR per instance ===")
    res = {0.0: [], 0.9: []}
    for seed in range(1, 6):
        line = f"instance {seed}:"
        for m in (0.0, 0.9):
            rs = sorted(g[(seed, m)], key=lambda r: r["lr"])
            vals = [(steps_to(r) if steps_to(r) is not None else budget, i) for i, r in enumerate(rs)]
            st, i = min(vals)
            reached = steps_to(rs[i]) is not None
            res[m].append(st)
            line += f"  {'SGD' if m == 0 else 'mom'} {st}{'' if reached else '+(censored)'} lr {rs[i]['lr']:.3g} idx {i}{' EDGE' if i in (0, 6) else ''}"
        print(line)
    s, p = res[0.0], res[0.9]
    print("SGD", s, "mom", p, "| ratios", [round(a / b, 1) for a, b in zip(s, p)], "| ranges disjoint:", max(p) < min(s))
