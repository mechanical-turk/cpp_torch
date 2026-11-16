import json, collections
rows=[json.loads(l) for l in open("runs/S9.jsonl")]
def arm(r): return "adam" if r.get("opt")=="adam" else ("mom" if r["momentum"]>0 else "sgd")
g=collections.defaultdict(list)
for r in rows: g[(r["batch"],arm(r))].append(r)
def st(r,t):
    for s,l,_ in r["hist"]:
        if l<=t: return s
    return None
fin=lambda r: float("inf") if r["diverged"] else r["hist"][-1][1]
for b in (64,256,10000):
  print(f"\n=== batch {b}: steps to train CE <= target (best LR) | final CE@2000 best LR | test acc ===")
  for a in ("sgd","mom","adam"):
    rs=sorted(g[(b,a)],key=lambda r:r["lr"]); n=len(rs); line=f"{a:5s}"
    for t in (0.5,0.2,0.1,0.05):
        v=[(st(r,t),i) for i,r in enumerate(rs) if st(r,t) is not None]
        if v: s,i=min(v); line+=f"  <={t}: {s} (lr {rs[i]['lr']:.3g}{' EDGE' if i in (0,n-1) else ''})"
        else: line+=f"  <={t}: never"
    bi=min(range(n),key=lambda k:fin(rs[k])); line+=f" | final {fin(rs[bi]):.4f} lr {rs[bi]['lr']:.3g} test {rs[bi]['test_acc']*100:.1f}"
    print(line)
