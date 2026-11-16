import json, collections, sys
rows=[json.loads(l) for l in open(sys.argv[1])]
g=collections.defaultdict(list)
for r in rows: g[(r["decades"],r["momentum"])].append(r)
def steps_to(r, frac):
    h=r["hist"]; e0=h[0][1]-r["lstar"]
    for s,l,_ in h:
        if l-r["lstar"] <= frac*e0: return s
    return None
def final_ex(r): return float("inf") if r["diverged"] else r["hist"][-1][1]-r["lstar"]
for frac in (0.1, 0.01):
    print(f"\n--- steps to excess loss <= {frac} x initial excess (None = not reached in 3000) ---")
    for d in sorted({k[0] for k in g}):
        o={}
        for m in (0.0,0.9):
            rs=sorted(g[(d,m)],key=lambda r:r["lr"])
            ok=[(steps_to(r,frac),i) for i,r in enumerate(rs) if steps_to(r,frac) is not None]
            if ok: st,i=min(ok); o[m]=(st,rs[i]["lr"],i in (0,len(rs)-1))
            else: o[m]=(None,None,None)
        print(f"decades {d}: SGD {o[0.0]}  momentum0.9 {o[0.9]}")
print("\n--- best final excess loss at step 3000 ---")
for d in sorted({k[0] for k in g}):
    t=[]
    for m in (0.0,0.9):
        rs=sorted(g[(d,m)],key=lambda r:r["lr"]); b=min(rs,key=final_ex); t.append((b["lr"],final_ex(b),b is rs[0] or b is rs[-1]))
    print(f"decades {d}: SGD lr {t[0][0]:.4g} excess {t[0][1]:.3e} edge {t[0][2]} | mom lr {t[1][0]:.4g} excess {t[1][1]:.3e} edge {t[1][2]}")
