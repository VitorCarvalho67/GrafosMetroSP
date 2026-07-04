# -*- coding: utf-8 -*-
"""Calcula metricas e exporta grafo.json para a visualizacao Three.js."""
import json
import networkx as nx
from rede_sp import build_graph, LINE_COLORS

G = build_graph()
N, M = G.number_of_nodes(), G.number_of_edges()

deg = dict(G.degree())
btw = nx.betweenness_centrality(G, normalized=True)
try:
    comms = nx.community.louvain_communities(G, seed=42)
except Exception:
    comms = nx.community.greedy_modularity_communities(G)
comm_of = {}
for i, c in enumerate(comms):
    for n in c:
        comm_of[n] = i
Q = nx.community.modularity(G, comms)

# layout 3D dirigido por forcas
pos = nx.spring_layout(G, dim=3, seed=7, k=1.15/(N**0.5), iterations=260)
S = 130.0

HUB = "#F2ECD0"  # cor de destaque para baldeacoes

def node_color(n):
    ls = G.nodes[n]["lines"]
    if len(ls) > 1:
        return HUB
    return LINE_COLORS[next(iter(ls))]

def edge_color(d):
    ls = [l for l in d["lines"] if l != "transfer"]
    if not ls:
        return "#8A8FA0"          # baldeacao
    if len(set(ls)) == 1:
        return LINE_COLORS[ls[0]]
    return "#C9CCD6"

nodes = []
for n in G.nodes():
    x, y, z = pos[n]
    nodes.append({
        "id": n,
        "lines": sorted(G.nodes[n]["lines"]),
        "hub": len(G.nodes[n]["lines"]) > 1,
        "color": node_color(n),
        "degree": deg[n],
        "betweenness": round(btw[n], 5),
        "community": comm_of[n],
        "x": round(x * S, 2), "y": round(y * S, 2), "z": round(z * S, 2),
    })

edges = []
for a, b, d in G.edges(data=True):
    edges.append({
        "s": a, "t": b,
        "lines": sorted(d["lines"]),
        "color": edge_color(d),
        "transfer": (d["lines"] == {"transfer"}),
    })

lines_legend = [{"name": k, "color": v} for k, v in LINE_COLORS.items()]

out = {
    "meta": {"N": N, "M": M, "avg_degree": round(2*M/N, 3),
             "modularity": round(Q, 3), "n_communities": len(comms)},
    "lines": lines_legend,
    "nodes": nodes,
    "edges": edges,
}
with open("grafo.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, separators=(",", ":"))

print(f"N={N} M={M} <k>={2*M/N:.3f} Q={Q:.3f} comunidades={len(comms)}")
print("Top-10 intermediacao:")
for n, v in sorted(btw.items(), key=lambda kv: kv[1], reverse=True)[:10]:
    print(f"  {v:.3f}  k={deg[n]:2d}  {n}")
