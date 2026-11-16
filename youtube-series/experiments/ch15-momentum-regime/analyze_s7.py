import json, collections
rows=[json.loads(l) for l in open("runs/S7.jsonl")]
g=collections.defaultdict(list)
for r in rows: g[(r["cand"],r["seed"],r["momentum"])].append(r)
T=0.003
def st(r):
    for s,l,_ in r["hist"]:
        if l<=T: return s
    return None
def fin(r): return float("inf") if r["diverged"] else r["hist"][-1][1]
def best(rs):
    reached=[(st(r),i) for i,r in enumerate(rs) if st(r) is not None]
    if reached: s,i=min(reached); return i,s
    i=min(range(len(rs)),key=lambda k:fin(rs[k])); return i,None   # censored: lowest final loss, divergers excluded
names={"A":"2x128 ReLU He","B":"4x128 ReLU He","C":"1x256 ReLU He","D":"2x128 tanh Xavier","A0":"2x128 ReLU default (S6 control)"}
for c in ["A","B","C","D","A0"]:
    S=[];P=[];edge=[];ta={0.0:[],0.9:[]};fl={0.0:[],0.9:[]};lrs={0.0:[],0.9:[]}
    for seed in range(1,6):
      for m in (0.0,0.9):
        rs=sorted(g[(c,seed,m)],key=lambda r:r["lr"]); i,s=best(rs)
        (S if m==0 else P).append(s)
        nxt_div = i+1<len(rs) and rs[i+1]["diverged"]
        if i==0 or (i==len(rs)-1): edge.append((seed,m,i))
        b=rs[i]; ta[m].append(round(b["test_acc"]*100,2)); fl[m].append(round(fin(b),4)); lrs[m].append(round(b["lr"],2))
    lb=lambda a,b: (a if a else 3001)/b   # censored SGD steps counted as 3001 -> lower bound on ratio
    ratios=[round(lb(a,b),2) for a,b in zip(S,P)] if None not in P else "n/a"
    cens=any(a is None for a in S)
    disj= None not in P and max(P)<min(a if a else 3001 for a in S)
    qual= None not in P and min(ratios)>=2 and disj and not edge
    print(f"{c} {names[c]}\n  steps SGD {S} mom {P}\n  ratios {'>= ' if cens else ''}{ratios} worst {'>= ' if cens else ''}{min(ratios) if ratios!='n/a' else None} disjoint {disj} edge {edge or 'none'} QUALIFIES {bool(qual)}\n  final train MSE @3000 SGD {fl[0.0]} mom {fl[0.9]}\n  test acc @3000 SGD {ta[0.0]} mom {ta[0.9]}\n  best LR SGD {lrs[0.0]} mom {lrs[0.9]}")
