import json, collections
rows=[json.loads(l) for l in open("runs/S8.jsonl")]
def arm(r): return "adam" if r.get("opt")=="adam" else ("mom" if r["momentum"]>0 else "sgd")
g=collections.defaultdict(list)
for r in rows: g[(r["decades"],r["batch"],r["seed"],arm(r))].append(r)
T=0.003
def st(r):
    for s,l,_ in r["hist"]:
        if l<=T: return s
    return None
fin=lambda r: float("inf") if r["diverged"] else r["hist"][-1][1]
def best(rs):
    reached=[(st(r),i) for i,r in enumerate(rs) if st(r) is not None]
    if reached: s,i=min(reached); return i,s
    return min(range(len(rs)),key=lambda k:fin(rs[k])),None
for d in (2,0):
  for b in (256,10000):
    res={};print(f"\n=== decades {d} batch {b}: steps to train MSE <= {T} ===")
    for a in ("sgd","mom","adam"):
        S=[];E=[];ta=[];lr=[];fl=[]
        for seed in (1,2,3):
            rs=sorted(g[(d,b,seed,a)],key=lambda r:r["lr"]); i,s=best(rs)
            S.append(s); ta.append(round(rs[i]["test_acc"]*100,2)); lr.append(round(rs[i]["lr"],4)); fl.append(round(fin(rs[i]),4))
            nd = i+1<len(rs) and rs[i+1]["diverged"]
            if (i==0) or (i==len(rs)-1): E.append((seed,"edge",i))
        res[a]=S
        print(f"{a:5s} steps {S} final MSE {fl} test acc {ta} best LR {lr} {'EDGE '+str(E) if E else ''}")
    P,A=res["mom"],res["adam"]
    if None not in A and None not in P:
        ratios=[round(p/a,2) for p,a in zip(P,A)]; disj=max(A)<min(P)
        print(f"Adam vs momentum: ratios {ratios} disjoint {disj} -> rule(>=2x all seeds) {all(r>=2 for r in ratios) and disj}")
    else: print("Adam vs momentum: not computable (censored arm) ->", {k:v for k,v in res.items()})
