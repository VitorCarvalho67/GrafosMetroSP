# -*- coding: utf-8 -*-
"""Indices de Derrible (metro-a-metro), impacto da Linha 6 completa e
simulacao das linhas propostas. Reproduzivel a partir de rede_sp.py."""
import json
import networkx as nx
from rede_sp import LINES, TRANSFERS
from analise import build_graph_from

G0 = build_graph_from(LINES)
N0 = G0.number_of_nodes()
M0 = G0.number_of_edges()
V0 = set(G0.nodes())

# ---------------------------------------------------------------
# 1) INDICES DE DERRIBLE & KENNEDY (2010) para SP (metro-a-metro)
# ---------------------------------------------------------------
# transfer stations = estacoes servidas por >= 2 linhas
transfer_nodes = [n for n in G0 if len(G0.nodes[n]["lines"]) >= 2]
termini = [n for n in G0 if G0.degree(n) == 1]
n_transfer = len(transfer_nodes)
transfer_ratio = n_transfer / N0
# numero ciclomatico mu = M - N + componentes  (ciclos independentes)
comp = nx.number_connected_components(G0)
mu = M0 - N0 + comp
# rT de Derrible = (mu - |D^m|)/|V| ; |D^m| = arestas multiplas (=0 no grafo simples)
rT_sp = mu / N0
# grafo reduzido (contrai estacoes de grau 2): arestas entre nos diatonicos
def reduced_edges(G):
    H = nx.MultiGraph()
    diat = [n for n in G if G.degree(n) != 2]
    H.add_nodes_from(diat)
    visited = set()
    for u in diat:
        for nb in G.neighbors(u):
            # caminha ao longo da cadeia de grau 2 ate o proximo no diatonico
            prev, cur = u, nb
            path = [u]
            guard = 0
            while G.degree(cur) == 2 and guard < 10000:
                path.append(cur)
                nxt = [x for x in G.neighbors(cur) if x != prev]
                if not nxt:
                    break
                prev, cur = cur, nxt[0]
                guard += 1
            key = tuple(sorted((u, cur)))
            if cur in diat and key not in visited:
                visited.add((u, cur, tuple(path[1:])))
                H.add_edge(u, cur)
    return H
Hr = reduced_edges(G0)
e_reduced = Hr.number_of_edges()

# Tabela publicada (Derrible & Kennedy 2010, Physica A 389:3678) - metro-a-metro
DK = {
    # cidade: (estacoes, linhas, rT_robustez, transfer_ratio)
    "Berlim":       (170, 9,  0.0706, 0.1059),
    "Nova York":    (422, 9,  0.0877, 0.1114),
    "Moscou":       (173, 12, 0.1387, 0.1618),
    "Madri":        (190, 13, 0.1895, 0.1895),
    "Osaka":        (121, 8,  0.1488, 0.1983),
    "Seul":         (286, 11, 0.2238, 0.1888),
    "Paris":        (297, 14, 0.1684, 0.1818),
    "Londres":      (306, 13, 0.1405, 0.1830),
    "Toquio":       (202, 13, 0.2525, 0.2228),
}

print("=" * 64)
print("INDICES DE DERRIBLE & KENNEDY (2010) - Sao Paulo (metro+CPTM)")
print(f"  estacoes N            = {N0}")
print(f"  linhas                = {len(LINES)}")
print(f"  estacoes de baldeacao = {n_transfer}  (ratio = {transfer_ratio:.4f})")
print(f"  terminais             = {len(termini)}")
print(f"  numero ciclomatico mu = {mu}   (arestas reduzidas e_r = {e_reduced})")
print(f"  robustez rT = mu/N    = {rT_sp:.4f}")
print("\n  Comparacao (rT robustez / transfer ratio):")
print(f"    {'Sao Paulo':12s} rT={rT_sp:.4f}  transfer={transfer_ratio:.4f}  (N={N0}, L={len(LINES)})")
for c, (n, l, rt, tr) in sorted(DK.items(), key=lambda kv: kv[1][2]):
    print(f"    {c:12s} rT={rt:.4f}  transfer={tr:.4f}  (N={n}, L={l})")

# ---------------------------------------------------------------
# 2) LINHA 6 COMPLETA (Brasilandia -> Sao Joaquim) - impacto
# ---------------------------------------------------------------
# Sequencia planejada; baldeacoes em estacoes ja existentes:
#   Agua Branca (7-Rubi/8), Higienopolis-Mackenzie (4-Amarela), Sao Joaquim (1-Azul)
LINE6_FULL = ["Brasilandia", "Itaberaba-Hospital Vila Penteado", "Joao Paulo I",
              "Freguesia do O", "Santa Marina", "Agua Branca", "SESC-Pompeia",
              "Perdizes", "PUC-Cardoso de Almeida", "FAAP-Pacaembu",
              "Higienopolis-Mackenzie", "14 Bis-Saracura", "Sao Joaquim"]

def eff_over(G, nodeset):
    """Eficiencia global restrita a pares dentro de nodeset (nos ja existentes)."""
    nodes = [n for n in nodeset if n in G]
    sp = dict(nx.all_pairs_shortest_path_length(G))
    tot, cnt = 0.0, 0
    for i in nodes:
        for j in nodes:
            if i != j:
                d = sp[i].get(j)
                if d and d > 0:
                    tot += 1.0 / d
                cnt += 1
    return tot / cnt if cnt else 0.0

lines_full6 = dict(LINES)
lines_full6["6-Laranja"] = LINE6_FULL
Gfull6 = build_graph_from(lines_full6)

base_eff = eff_over(G0, V0)
full6_eff = eff_over(Gfull6, V0)          # eficiencia entre os MESMOS 176 nos
base_L = nx.average_shortest_path_length(G0)
full6_L = nx.average_shortest_path_length(Gfull6.subgraph(
    max(nx.connected_components(Gfull6), key=len)))
base_Eg = nx.global_efficiency(G0)
full6_Eg = nx.global_efficiency(Gfull6)

print("\n" + "=" * 64)
print("IMPACTO DA LINHA 6 COMPLETA (vs. rede atual)")
print(f"  N: {N0} -> {Gfull6.number_of_nodes()}  (+{Gfull6.number_of_nodes()-N0} estacoes novas)")
print(f"  Eficiencia entre os 176 nos existentes: {base_eff:.5f} -> {full6_eff:.5f} "
      f"({100*(full6_eff-base_eff)/base_eff:+.2f}%)")
print(f"  Eglob (rede toda): {base_Eg:.5f} -> {full6_Eg:.5f} "
      f"({100*(full6_Eg-base_Eg)/base_Eg:+.2f}%)")
print(f"  L (caminho medio): {base_L:.3f} -> {full6_L:.3f} "
      f"({100*(full6_L-base_L)/base_L:+.2f}%)")

# ---------------------------------------------------------------
# 3) LINHAS PROPOSTAS - ganho de conectividade e custo-efetividade
# ---------------------------------------------------------------
# Cada linha e modelada por seus pontos de baldeacao CONHECIDOS com a rede
# existente (ancoras), preenchidos com estacoes novas ate a contagem anunciada.
# A eficiencia e medida SEMPRE entre os 176 nos existentes (isola o efeito
# de "atalho" que a nova linha cria na malha atual).
def make_line(anchors_and_fill):
    return anchors_and_fill

PROPOSED = {
    # nome: (sequencia de estacoes [ancoras existentes + novas], km, tipo)
    "6-Laranja (completa)": (LINE6_FULL, 15.3, "subterraneo"),
    "19-Celeste": (["Anhangabau", "L19_a", "L19_b", "L19_c", "L19_d", "L19_e",
                    "L19_f", "L19_g", "L19_h", "L19_i", "L19_j", "L19_k",
                    "L19_l", "L19_m", "L19_n"], 17.6, "subterraneo"),
    "20-Rosa": (["Santa Marina", "L20_a", "L20_b", "Pinheiros", "L20_c", "L20_d",
                 "Moema", "L20_e", "L20_f", "L20_g", "L20_h", "L20_i", "L20_j",
                 "L20_k", "L20_l", "L20_m", "L20_n", "L20_o", "L20_p", "L20_q",
                 "L20_r", "L20_s", "L20_t", "Santo Andre"], 31.1, "subterraneo"),
    "22-Marrom": (["Sumare", "L22_a", "L22_b", "L22_c", "L22_d", "L22_e", "L22_f",
                   "L22_g", "L22_h", "L22_i", "L22_j", "L22_k", "L22_l", "L22_m",
                   "L22_n", "L22_o", "L22_p", "L22_q", "L22_r"], 29.0, "subterraneo"),
    "16-Violeta": (["Oscar Freire", "L16_a", "L16_b", "L16_c", "L16_d", "L16_e",
                    "L16_f", "L16_g", "L16_h", "L16_i", "L16_j", "L16_k", "L16_l",
                    "L16_m", "L16_n", "L16_o", "L16_p", "L16_q", "L16_r", "L16_s",
                    "L16_t", "L16_u", "L16_v", "L16_w", "Sao Mateus"], 32.0, "subterraneo"),
}

# custo unitario de referencia (valores atualizados 2024/26):
#   subterraneo pesado: Linha 6 = R$18,1 bi / 15,3 km = 1,18 bi/km
#   monotrilho:        Linha 17 = R$5,97 bi / 6,7 km = 0,89 bi/km
UNIT = {"subterraneo": 18.1 / 15.3, "monotrilho": 5.97 / 6.7}

print("\n" + "=" * 64)
print("LINHAS PROPOSTAS: ganho de eficiencia da malha e custo estimado")
print(f"  (base: eficiencia entre 176 nos = {base_eff:.5f})")
print(f"  {'Linha':22s} {'dEff%':>7s} {'anc':>4s} {'km':>6s} {'R$bi':>7s} {'dEff%/R$bi':>10s}")
rows = []
for name, (seq, km, tipo) in PROPOSED.items():
    lines_p = dict(LINES)
    if name.startswith("6"):
        lines_p["6-Laranja"] = seq
    else:
        lines_p[name] = seq
    Gp = build_graph_from(lines_p)
    eff = eff_over(Gp, V0)
    d = 100 * (eff - base_eff) / base_eff
    anchors = sum(1 for s in seq if s in V0)
    cost = km * UNIT[tipo]
    rows.append((name, d, anchors, km, cost, d / cost))
    print(f"  {name:22s} {d:>7.2f} {anchors:>4d} {km:>6.1f} {cost:>7.1f} {d/cost:>10.3f}")

print("\n  Ranking por ganho de eficiencia da malha existente:")
for name, d, a, km, cost, ce in sorted(rows, key=lambda r: r[1], reverse=True):
    print(f"    {name:22s} dEff={d:+.2f}%  ancoras={a}  ~R${cost:.1f}bi")

# salvar
out = {
    "derrible_sp": {"N": N0, "lines": len(LINES), "n_transfer": n_transfer,
                    "transfer_ratio": round(transfer_ratio, 4), "termini": len(termini),
                    "mu": mu, "e_reduced": e_reduced, "rT": round(rT_sp, 4)},
    "derrible_table": DK,
    "line6_full": {"new_stations": Gfull6.number_of_nodes() - N0,
                   "eff_existing_before": round(base_eff, 5),
                   "eff_existing_after": round(full6_eff, 5),
                   "eff_gain_pct": round(100 * (full6_eff - base_eff) / base_eff, 2),
                   "Eglob_before": round(base_Eg, 5), "Eglob_after": round(full6_Eg, 5),
                   "L_before": round(base_L, 3), "L_after": round(full6_L, 3)},
    "proposed": [{"name": r[0], "eff_gain_pct": round(r[1], 2), "anchors": r[2],
                  "km": r[3], "cost_bi": round(r[4], 1),
                  "eff_per_bi": round(r[5], 3)} for r in rows],
    "unit_cost": {"subterraneo_bi_per_km": round(UNIT["subterraneo"], 3),
                  "monotrilho_bi_per_km": round(UNIT["monotrilho"], 3)},
}
with open("resultados2.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("\nOK -> resultados2.json")
