import json, collections, sys
rows=[json.loads(l) for l in open(sys.argv[1])]
g=collections.defaultdict(list)
for r in rows: g[(r["decades"],r["batch"],r["momentum"])].append(r)
fin=lambda r: float("inf") if r["diverged"] else r["hist"][-1][1]
print("dec batch | SGD lr loss acc test edge | mom lr loss acc test edge | ratio")
for d in sorted({k[0] for k in g}):
  for b in [10000,256]:
    o=[]
    for m in [0.0,0.9]:
      rs=sorted(g[(d,b,m)],key=lambda r:r["lr"]); best=min(rs,key=fin); i=rs.index(best)
      o.append((best["lr"],fin(best),best["hist"][-1][2],best["test_acc"],i in(0,len(rs)-1)))
    s,p=o
    print(d,b,"|",f"{s[0]:.4g} {s[1]:.5f} {s[2]:.3f} {s[3]:.3f} {s[4]}","|",f"{p[0]:.4g} {p[1]:.5f} {p[2]:.3f} {p[3]:.3f} {p[4]}","|",f"{s[1]/max(p[1],1e-9):.2f}x")
