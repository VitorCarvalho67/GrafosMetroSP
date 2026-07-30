# -*- coding: utf-8 -*-
"""Analise topologica completa da malha metroferroviaria da RMSP.
Gera todos os numeros usados no artigo. 100% reproduzivel a partir de rede_sp.py.
"""
import json
import math
import statistics as st
import networkx as nx
from rede_sp import LINES, LINE_COLORS, TRANSFERS, build_graph

RESULTS = {}


def build_graph_from(lines_dict, transfers=TRANSFERS):
    G = nx.Graph()
    for line, seq in lines_dict.items():
        for stt in seq:
            if stt not in G:
                G.add_node(stt, lines=set())
            G.nodes[stt]["lines"].add(line)
        for a, b in zip(seq, seq[1:]):
            if G.has_edge(a, b):
                G[a][b]["lines"].add(line)
            else:
                G.add_edge(a, b, lines={line})
    for a, b in transfers:
        if a in G and b in G and not G.has_edge(a, b):
            G.add_edge(a, b, lines={"transfer"})
    return G


def space_p_graph(lines_dict):
    """Espaco P: todas as estacoes de uma mesma linha sao mutuamente adjacentes."""
    G = nx.Graph()
    for line, seq in lines_dict.items():
        for stt in seq:
            G.add_node(stt)
        for i in range(len(seq)):
            for j in range(i + 1, len(seq)):
                G.add_edge(seq[i], seq[j])
    # baldeacoes por nome diferente
    for a, b in TRANSFERS:
        if a in G and b in G:
            G.add_edge(a, b)
    return G


def basic_metrics(G, label):
    N = G.number_of_nodes()
    M = G.number_of_edges()
    degs = [d for _, d in G.degree()]
    connected = nx.is_connected(G)
    if connected:
        Gc = G
    else:
        Gc = G.subgraph(max(nx.connected_components(G), key=len)).copy()
    L = nx.average_shortest_path_length(Gc)
    D = nx.diameter(Gc)
    Eglob = nx.global_efficiency(G)
    C = nx.average_clustering(G)
    trans = nx.transitivity(G)
    try:
        assort = nx.degree_assortativity_coefficient(G)
    except Exception:
        assort = float("nan")
    # conectividade algebrica (segundo menor autovalor do laplaciano) no maior componente
    lam2 = nx.algebraic_connectivity(Gc, seed=42) if Gc.number_of_nodes() > 2 else float("nan")
    deg_dist = {}
    for d in degs:
        deg_dist[d] = deg_dist.get(d, 0) + 1
    m = {
        "label": label, "N": N, "M": M,
        "avg_degree": 2 * M / N,
        "max_degree": max(degs), "min_degree": min(degs),
        "connected": connected,
        "n_components": nx.number_connected_components(G),
        "L": L, "diameter": D,
        "global_efficiency": Eglob,
        "avg_clustering": C, "transitivity": trans,
        "assortativity": assort,
        "algebraic_connectivity": lam2,
        "degree_dist": deg_dist,
    }
    return m


def small_world(G, n_random=200, seed=1):
    """sigma e omega comparando com grafos aleatorios (ER) e reticulado equivalente."""
    Gc = G.subgraph(max(nx.connected_components(G), key=len)).copy()
    N = Gc.number_of_nodes()
    M = Gc.number_of_edges()
    C = nx.average_clustering(Gc)
    L = nx.average_shortest_path_length(Gc)
    import random
    rng = random.Random(seed)
    Cr, Lr = [], []
    for i in range(n_random):
        R = nx.gnm_random_graph(N, M, seed=rng.randint(0, 10 ** 9))
        if not nx.is_connected(R):
            R = R.subgraph(max(nx.connected_components(R), key=len)).copy()
        Cr.append(nx.average_clustering(R))
        try:
            Lr.append(nx.average_shortest_path_length(R))
        except Exception:
            pass
    Crand = st.mean(Cr)
    Lrand = st.mean(Lr)
    sigma = (C / Crand) / (L / Lrand) if Crand > 0 else float("inf")
    return {"C": C, "L": L, "C_rand": Crand, "L_rand": Lrand,
            "sigma": sigma, "n_random": n_random}


def centralities(G, topn=15):
    btw = nx.betweenness_centrality(G, normalized=True)
    clo = nx.closeness_centrality(G)
    deg = dict(G.degree())
    def top(d):
        return [(n, round(v, 4), deg[n]) for n, v in
                sorted(d.items(), key=lambda kv: kv[1], reverse=True)[:topn]]
    return {"betweenness_top": top(btw), "closeness_top": top(clo),
            "degree_top": [(n, deg[n]) for n in
                           sorted(deg, key=deg.get, reverse=True)[:topn]],
            "_btw": btw, "_clo": clo, "_deg": deg}


def communities(G):
    comms = nx.community.louvain_communities(G, seed=42)
    Q = nx.community.modularity(G, comms)
    sizes = sorted([len(c) for c in comms], reverse=True)
    return {"n_communities": len(comms), "modularity": Q,
            "sizes": sizes, "_comms": comms}


def robustness(G, fractions=None, seed=7):
    """S(f) e E(f) sob remocao aleatoria vs ataque por betweenness (recalculado)."""
    import random
    if fractions is None:
        fractions = [i / 100 for i in range(0, 51, 2)]
    N0 = G.number_of_nodes()
    E0 = nx.global_efficiency(G)

    def lcc_frac(H):
        if H.number_of_nodes() == 0:
            return 0.0
        return len(max(nx.connected_components(H), key=len)) / N0

    # aleatorio: media de varias realizacoes
    rng = random.Random(seed)
    n_real = 30
    rand_S = {f: [] for f in fractions}
    rand_E = {f: [] for f in fractions}
    for _ in range(n_real):
        order = list(G.nodes())
        rng.shuffle(order)
        H = G.copy()
        removed = 0
        for f in fractions:
            target = int(round(f * N0))
            while removed < target and order:
                H.remove_node(order.pop())
                removed += 1
            rand_S[f].append(lcc_frac(H))
            rand_E[f].append(nx.global_efficiency(H) / E0 if E0 > 0 else 0)
    rand_S = {f: st.mean(v) for f, v in rand_S.items()}
    rand_E = {f: st.mean(v) for f, v in rand_E.items()}

    # ataque: remove recalculando betweenness a cada passo (aproxima por blocos)
    H = G.copy()
    atk_S, atk_E = {}, {}
    fset = set(fractions)
    step_removed = 0
    atk_S[0.0] = lcc_frac(H); atk_E[0.0] = 1.0
    order_targets = sorted(fractions)
    idx = 1
    while idx < len(order_targets):
        target = int(round(order_targets[idx] * N0))
        while step_removed < target and H.number_of_nodes() > 0:
            bc = nx.betweenness_centrality(H)
            v = max(bc, key=bc.get)
            H.remove_node(v)
            step_removed += 1
        atk_S[order_targets[idx]] = lcc_frac(H)
        atk_E[order_targets[idx]] = nx.global_efficiency(H) / E0 if E0 > 0 else 0
        idx += 1

    # robustez R = area sob curva S(f) (aproximacao trapezoidal) - metrica de Schneider-like
    def auc(d):
        fs = sorted(d)
        s = 0.0
        for i in range(1, len(fs)):
            s += (fs[i] - fs[i - 1]) * (d[fs[i]] + d[fs[i - 1]]) / 2
        return s
    return {"fractions": fractions,
            "random_S": rand_S, "random_E": rand_E,
            "attack_S": atk_S, "attack_E": atk_E,
            "R_random": auc(rand_S), "R_attack": auc(atk_S),
            "E0": E0}


# ============ EXECUCAO ============
if __name__ == "__main__":
    G = build_graph()
    RESULTS["baseline"] = basic_metrics(G, "SP completa (2026)")
    RESULTS["small_world"] = small_world(G, n_random=300)
    cen = centralities(G)
    RESULTS["centralities"] = {k: v for k, v in cen.items() if not k.startswith("_")}
    com = communities(G)
    RESULTS["communities"] = {k: v for k, v in com.items() if not k.startswith("_")}
    RESULTS["robustness"] = robustness(G)

    # Espaco P
    GP = space_p_graph(LINES)
    GPc = GP.subgraph(max(nx.connected_components(GP), key=len)).copy()
    RESULTS["space_p"] = {
        "N": GP.number_of_nodes(), "M": GP.number_of_edges(),
        "L": nx.average_shortest_path_length(GPc),
        "diameter": nx.diameter(GPc),
        "avg_degree": 2 * GP.number_of_edges() / GP.number_of_nodes(),
    }

    # ---- Impacto da Linha 6 (trecho atual em operacao) ----
    lines_no6 = {k: v for k, v in LINES.items() if k != "6-Laranja"}
    G_no6 = build_graph_from(lines_no6)
    base = RESULTS["baseline"]
    m_no6 = basic_metrics(G_no6, "SP sem Linha 6 (atual)")
    RESULTS["line6_current"] = {
        "with": {"N": base["N"], "M": base["M"], "Eglob": base["global_efficiency"],
                 "L": base["L"], "components": base["n_components"]},
        "without": {"N": m_no6["N"], "M": m_no6["M"], "Eglob": m_no6["global_efficiency"],
                    "L": m_no6["L"], "components": m_no6["n_components"]},
    }

    # ---- Eficiencia por comunidade (proxy de regiao) ----
    comms = com["_comms"]
    clo = cen["_clo"]
    btw = cen["_btw"]
    comm_eff = []
    for i, c in enumerate(sorted(comms, key=len, reverse=True)):
        members = list(c)
        comm_eff.append({
            "id": i, "size": len(members),
            "mean_closeness": round(st.mean(clo[n] for n in members), 4),
            "mean_betweenness": round(st.mean(btw[n] for n in members), 4),
            "sample": sorted(members, key=lambda n: clo[n], reverse=True)[:4],
        })
    RESULTS["region_efficiency"] = comm_eff

    # ---- salvar ----
    def clean(o):
        if isinstance(o, dict):
            return {str(k): clean(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [clean(x) for x in o]
        if isinstance(o, float):
            return round(o, 6)
        return o
    with open("resultados.json", "w", encoding="utf-8") as f:
        json.dump(clean(RESULTS), f, ensure_ascii=False, indent=1)

    # ---- impressao legivel ----
    b = RESULTS["baseline"]
    print("=" * 60)
    print("BASELINE (espaco L, rede completa 2026)")
    print(f"  N={b['N']} M={b['M']} <k>={b['avg_degree']:.3f} "
          f"kmax={b['max_degree']}")
    print(f"  conexo={b['connected']} componentes={b['n_components']}")
    print(f"  L={b['L']:.3f}  D={b['diameter']}  Eglob={b['global_efficiency']:.4f}")
    print(f"  C={b['avg_clustering']:.4f}  transitividade={b['transitivity']:.4f}")
    print(f"  assortatividade={b['assortativity']:.4f}  lambda2={b['algebraic_connectivity']:.5f}")
    print(f"  dist. grau={b['degree_dist']}")
    sw = RESULTS["small_world"]
    print(f"\nSMALL-WORLD: C={sw['C']:.4f} Crand={sw['C_rand']:.4f} "
          f"L={sw['L']:.3f} Lrand={sw['L_rand']:.3f} sigma={sw['sigma']:.2f}")
    p = RESULTS["space_p"]
    print(f"\nESPACO P: N={p['N']} M={p['M']} <k>={p['avg_degree']:.2f} "
          f"L_P={p['L']:.3f} D_P={p['diameter']}")
    print("\nTOP INTERMEDIACAO:")
    for n, v, k in RESULTS["centralities"]["betweenness_top"][:10]:
        print(f"  {v:.4f}  k={k:2d}  {n}")
    print("\nTOP PROXIMIDADE:")
    for n, v, k in RESULTS["centralities"]["closeness_top"][:10]:
        print(f"  {v:.4f}  k={k:2d}  {n}")
    c = RESULTS["communities"]
    print(f"\nCOMUNIDADES: {c['n_communities']}  Q={c['modularity']:.4f} "
          f"tamanhos={c['sizes']}")
    r = RESULTS["robustness"]
    print(f"\nROBUSTEZ: R_aleat={r['R_random']:.4f} R_ataque={r['R_attack']:.4f}")
    print("  f     S_rand  E_rand  S_atk   E_atk")
    for f in [0.0, 0.05, 0.1, 0.2, 0.3, 0.5]:
        if f in r["random_S"]:
            print(f"  {f:.2f}  {r['random_S'][f]:.3f}   {r['random_E'][f]:.3f}   "
                  f"{r['attack_S'].get(f, float('nan')):.3f}   {r['attack_E'].get(f, float('nan')):.3f}")
    l6 = RESULTS["line6_current"]
    print(f"\nLINHA 6 (trecho atual): com Eglob={l6['with']['Eglob']:.4f} N={l6['with']['N']} | "
          f"sem Eglob={l6['without']['Eglob']:.4f} N={l6['without']['N']} comp={l6['without']['components']}")
