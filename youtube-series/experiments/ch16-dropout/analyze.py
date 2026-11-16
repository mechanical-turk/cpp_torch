import json, collections, statistics as st
for n in (10000, 55000):
    rows = [json.loads(l) for l in open(f"runs_{'10k' if n==10000 else '55k'}.jsonl")]
    print(f"\n=== train N={n} ===  (mean over 3 seeds; lr chosen per p by mean best validation accuracy)")
    by = collections.defaultdict(list)
    for r in rows: by[(r["p"], r["lr"])].append(r)
    for p in (0.0, 0.2, 0.5):
        best = None
        for (pp, lr), rs in by.items():
            if pp != p: continue
            # per run: epoch of best validation accuracy
            pick = [max(r["hist"], key=lambda h: h[4]) for r in rs]
            fin = [r["hist"][-1] for r in rs]
            mv = st.mean(h[4] for h in pick)
            if best is None or mv > best[0]: best = (mv, lr, pick, fin)
        mv, lr, pick, fin = best
        f = lambda xs, i: st.mean(h[i] for h in xs)
        print(f"p={p} lr={lr:g}: best-val epoch val {100*mv:.2f} test {100*f(pick,6):.2f} | "
              f"final train acc {100*f(fin,2):.2f} val acc {100*f(fin,4):.2f} val loss {f(fin,3):.3f} test {100*f(fin,6):.2f} "
              f"| gap(train-val) {100*(f(fin,2)-f(fin,4)):.2f} | min val loss {st.mean(min(h[3] for h in r['hist']) for r in by[(p,lr)]):.3f} "
              f"| best epoch {[h[0] for h in pick]}")
