import json, collections
rows=[json.loads(l) for l in open("runs/S11.jsonl")]
def arm(r): return "adam" if r.get("opt")=="adam" else ("mom" if r["momentum"]>0 else "sgd")
g=collections.defaultdict(list)
for r in rows: g[(r["batch"],r["seed"],arm(r))].append(r)
T=0.1
def st(r):
    for s,l,_ in r["hist"]:
        if l<=T: return s
    return None
res={};edge={}
for b in (64,256,10000):
  for a in ("sgd","mom","adam"):
    S=[];E=[];lr=[]
    for seed in range(2,7):
      rs=sorted(g[(b,seed,a)],key=lambda r:r["lr"])
      v=[(st(r),i) for i,r in enumerate(rs) if st(r) is not None]
      s,i=min(v) if v else (None,None)
      S.append(s); lr.append(round(rs[i]["lr"],3) if v else None)
      if i in (0,len(rs)-1): E.append((seed,i))
    res[(b,a)]=S; edge[(b,a)]=E
    print(f"batch {b:5d} {a:5s} steps {S} best LR {lr} {'EDGE '+str(E) if E else ''}")
print()
for b in (64,256,10000):
  S,M,A=res[(b,"sgd")],res[(b,"mom")],res[(b,"adam")]
  if None in S+M+A: print(b,"censored"); continue
  r1=[round(x/y,2) for x,y in zip(S,M)]; d1=max(M)<min(S)
  r2=[round(x/y,2) for x,y in zip(M,A)]; d2=max(A)<min(M)
  print(f"batch {b}: SGD/mom {r1} disjoint {d1} edges {edge[(b,'sgd')] or edge[(b,'mom')] or 'none'} -> rule(a) {all(x>=2 for x in r1) and d1 and not (edge[(b,'sgd')] or edge[(b,'mom')])}")
  print(f"          mom/Adam {r2} disjoint {d2} edges {edge[(b,'adam')] or edge[(b,'mom')] or 'none'} -> rule(b) {all(x>=1.2 for x in r2) and d2 and not (edge[(b,'adam')] or edge[(b,'mom')])}")
