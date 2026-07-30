# -*- coding: utf-8 -*-
"""Compara SP, Nova York e Londres com a MESMA pipeline (espaço L)."""
import json, statistics as st, random
import networkx as nx
import rede_sp, rede_london, rede_nyc

def metrics(G, label):
    N=G.number_of_nodes(); M=G.number_of_edges()
    Gc=G.subgraph(max(nx.connected_components(G),key=len)).copy()
    L=nx.average_shortest_path_length(Gc); D=nx.diameter(Gc)
    Eg=nx.global_efficiency(G); C=nx.average_clustering(G)
    # small-world sigma
    rng=random.Random(1); Cr=[]; Lr=[]
    for _ in range(80):
        Rr=nx.gnm_random_graph(Gc.number_of_nodes(),Gc.number_of_edges(),seed=rng.randint(0,1<<30))
        if not nx.is_connected(Rr): Rr=Rr.subgraph(max(nx.connected_components(Rr),key=len)).copy()
        Cr.append(nx.average_clustering(Rr)); Lr.append(nx.average_shortest_path_length(Rr))
    Crand=st.mean(Cr) or 1e-9; Lrand=st.mean(Lr)
    sigma=(C/Crand)/(L/Lrand) if Crand>0 else float('nan')
    comms=nx.community.louvain_communities(G,seed=42); Q=nx.community.modularity(G,comms)
    ntrans=sum(1 for n in G if len(G.nodes[n]["lines"])>=2)
    mu=M-N+nx.number_connected_components(G); rT=mu/N
    btw=nx.betweenness_centrality(G)
    top=sorted(btw.items(),key=lambda kv:kv[1],reverse=True)[:5]
    # robustez: ataque por betweenness recalculado (blocos) vs aleatório
    def lcc(H): return len(max(nx.connected_components(H),key=len))/N if H.number_of_nodes() else 0
    fr=[i/100 for i in range(0,31,3)]
    # aleatório médio
    rnd2=random.Random(7); randS={f:[] for f in fr}
    for _ in range(15):
        order=list(G.nodes()); rnd2.shuffle(order); H=G.copy(); removed=0
        for f in fr:
            tgt=int(round(f*N))
            while removed<tgt and order: H.remove_node(order.pop()); removed+=1
            randS[f].append(lcc(H))
    randS={f:st.mean(v) for f,v in randS.items()}
    # ataque
    H=G.copy(); atkS={0.0:1.0}; rem=0
    for f in fr[1:]:
        tgt=int(round(f*N))
        while rem<tgt and H.number_of_nodes()>0:
            bc=nx.betweenness_centrality(H); v=max(bc,key=bc.get); H.remove_node(v); rem+=1
        atkS[f]=lcc(H)
    def auc(d):
        ks=sorted(d); s=0
        for i in range(1,len(ks)): s+=(ks[i]-ks[i-1])*(d[ks[i]]+d[ks[i-1]])/2
        return s
    return {"label":label,"N":N,"M":M,"avg_degree":2*M/N,"L":L,"D":D,"Eglob":Eg,"C":C,
            "sigma":sigma,"Q":Q,"n_comm":len(comms),"n_transfer":ntrans,
            "transfer_ratio":ntrans/N,"mu":mu,"rT":rT,
            "top_btw":[(n,round(v,3)) for n,v in top],
            "R_random":auc(randS),"R_attack":auc(atkS),
            "randS":randS,"atkS":atkS}

G_sp=rede_sp.build_graph(); G_ln=rede_london.build_graph(); G_ny=rede_nyc.build_graph()
res={"SP":metrics(G_sp,"São Paulo"),"NY":metrics(G_ny,"Nova York"),"LN":metrics(G_ln,"Londres")}
# validação com Derrible & Kennedy (2010) publicado
DK={"SP":{"N":176,"rT":0.080},"NY":{"N":422,"rT":0.0877},"LN":{"N":306,"rT":0.1405}}

for k in ["SP","NY","LN"]:
    m=res[k]
    print(f"\n=== {m['label']} ===")
    print(f"  N={m['N']} M={m['M']} <k>={m['avg_degree']:.2f} L={m['L']:.2f} D={m['D']} "
          f"Eglob={m['Eglob']:.4f}")
    print(f"  C={m['C']:.3f} sigma={m['sigma']:.2f} Q={m['Q']:.3f} comm={m['n_comm']} "
          f"transfer_ratio={m['transfer_ratio']:.3f}")
    print(f"  mu={m['mu']} rT={m['rT']:.4f}  (Derrible publicado rT={DK[k]['rT']})")
    print(f"  R_random={m['R_random']:.3f} R_attack={m['R_attack']:.3f}")
    print(f"  top betweenness: {m['top_btw']}")

clean={k:{kk:vv for kk,vv in v.items() if kk not in ('randS','atkS')} for k,v in res.items()}
for k in res: clean[k]["randS"]={str(a):round(b,3) for a,b in res[k]["randS"].items()}
for k in res: clean[k]["atkS"]={str(a):round(b,3) for a,b in res[k]["atkS"].items()}
json.dump(clean,open("compare3.json","w"),ensure_ascii=False,indent=1)
print("\nOK -> compare3.json")
