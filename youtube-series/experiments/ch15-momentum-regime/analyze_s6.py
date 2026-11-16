import json, collections
rows=[json.loads(l) for l in open("runs/S6.jsonl")]
g=collections.defaultdict(list)
for r in rows: g[(r["decades"],r["batch"],r["seed"],r["momentum"])].append(r)
def st(r,t):
    for s,l,_ in r["hist"]:
        if l<=t: return s
    return None
for t in (0.003,0.01):
  print(f"\n=== steps to train MSE <= {t} (3000 budget; None=never) ===")
  for d in (1,2):
    for b in (10000,256):
      res={0.0:[],0.9:[]}; edges=[]
      for seed in range(1,6):
        for m in (0.0,0.9):
          rs=sorted(g[(d,b,seed,m)],key=lambda r:r["lr"])
          v=[(st(r,t) if st(r,t) is not None else 3001,i) for i,r in enumerate(rs)]
          s,i=min(v); res[m].append(s if s<3001 else None)
          if i in (0,6): edges.append((seed,m,i))
      S,P=res[0.0],res[0.9]
      ok=None not in S+P
      ratios=[round(a/c,1) for a,c in zip(S,P)] if ok else "n/a"
      disj=bool(ok) and max(P)<min(S)
      rule=ok and all(a/c>=2 for a,c in zip(S,P)) and disj and not edges
      print(f"decades {d} batch {b}: SGD {S} mom {P} ratios {ratios} disjoint {disj} edge-best {edges or 'none'} RULE MET: {bool(rule)}")
