# -*- coding: utf-8 -*-
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from mpl_toolkits.mplot3d import Axes3D  # noqa
import networkx as nx
from rede_sp import build_graph, LINE_COLORS

plt.rcParams.update({"font.family": "DejaVu Sans", "svg.fonttype": "none"})

PRETTY = {"Se":"Sé","Bras":"Brás","Tatuape":"Tatuapé","Paraiso":"Paraíso",
    "Republica":"República","Anhangabau":"Anhangabaú","Consolacao":"Consolação",
    "Palmeiras-Barra Funda":"Barra Funda","Sao Bento":"São Bento",
    "Sao Joaquim":"São Joaquim","Julio Prestes":"Júlio Prestes","Belem":"Belém",
    "Pinheiros":"Pinheiros","Luz":"Luz","Ana Rosa":"Ana Rosa","Tamanduatei":"Tamanduateí",
    "Lapa":"Lapa","Paulista":"Paulista","Se ":"Sé"}
def pretty(n): return PRETTY.get(n, n)

# ---------------------------------------------------------------- Fig 1: pipeline
def fig_pipeline():
    fig, ax = plt.subplots(figsize=(11, 2.3))
    ax.set_xlim(0, 100); ax.set_ylim(0, 20); ax.axis("off")
    steps = [
        ("Mapa oficial\nMetro + CPTM", "#E8EEF7", "#2C5F8A"),
        ("Sequencias de\nestacoes por linha", "#E8EEF7", "#2C5F8A"),
        ("Grafo em\nespaco L  (V, E)", "#FDEEE6", "#C0562B"),
        ("Metricas: grau,\nC_B, Q, robustez", "#EAF3EC", "#2E7D48"),
        ("Visualizacao 3D\n(Three.js)", "#F1ECF7", "#6A4C93"),
    ]
    n = len(steps)
    left, right, gap = 2.0, 2.0, 4.2
    w = (100 - left - right - gap*(n-1)) / n     # largura que garante caber
    x = left
    centers = []
    for label, fc, ec in steps:
        box = FancyBboxPatch((x, 5), w, 10, boxstyle="round,pad=0.3,rounding_size=1.1",
                             fc=fc, ec=ec, lw=1.7, clip_on=False)
        ax.add_patch(box)
        ax.text(x + w/2, 10, label, ha="center", va="center", fontsize=9.7, color="#20303f")
        centers.append((x, x+w)); x += w + gap
    for (_, xr), (xl2, _) in zip(centers[:-1], centers[1:]):
        ar = FancyArrowPatch((xr + 0.5, 10), (xl2 - 0.5, 10), arrowstyle="-|>",
                             mutation_scale=15, lw=1.7, color="#5a6472", clip_on=False)
        ax.add_patch(ar)
    fig.savefig("metodologia.pdf", bbox_inches="tight"); plt.close(fig)

# ---------------------------------------------------------------- Fig 2: espaco L vs P
def fig_espacos():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))
    pos = {"A":(0,2),"B":(1,2),"C":(2,2),"D":(3,2),"E":(4,2),"F":(2,3.2),"G":(2,0.8)}
    c1, c2, ch = "#EE3B33", "#0353A4", "#F2C94C"
    ncol = {k:c1 for k in "ABDE"}; ncol.update({"F":c2,"G":c2}); ncol["C"]=ch
    def draw_nodes(ax):
        for nm,(x,y) in pos.items():
            ax.scatter([x],[y], s=780 if nm=="C" else 580, c=ncol[nm],
                       edgecolors="#222" if nm=="C" else "white", linewidths=2.2, zorder=3)
            ax.text(x,y,nm, ha="center", va="center", fontsize=11, fontweight="bold",
                    color="#222" if nm in "FGC" else "white", zorder=4)
    # Espaco L
    axL = axes[0]
    for (u,v) in [("A","B"),("B","C"),("C","D"),("D","E")]:
        axL.plot([pos[u][0],pos[v][0]],[pos[u][1],pos[v][1]], color=c1, lw=3, zorder=1)
    for (u,v) in [("F","C"),("C","G")]:
        axL.plot([pos[u][0],pos[v][0]],[pos[u][1],pos[v][1]], color=c2, lw=3, zorder=1)
    draw_nodes(axL)
    axL.set_title("Espaco L — adjacencia fisica\n(estacoes consecutivas)", fontsize=11)
    axL.set_xlim(-0.8,4.8); axL.set_ylim(0.2,3.8); axL.axis("off")
    # Espaco P
    axP = axes[1]
    def clique(seq): return [(seq[i],seq[j]) for i in range(len(seq)) for j in range(i+1,len(seq))]
    for (u,v) in clique(["A","B","C","D","E"]):
        axP.plot([pos[u][0],pos[v][0]],[pos[u][1],pos[v][1]], color=c1, lw=1.6, alpha=.55, zorder=1)
    for (u,v) in clique(["F","C","G"]):
        axP.plot([pos[u][0],pos[v][0]],[pos[u][1],pos[v][1]], color=c2, lw=1.6, alpha=.55, zorder=1)
    draw_nodes(axP)
    axP.set_title("Espaco P — adjacencia por linha\n(distancia = n. de baldeacoes)", fontsize=11)
    axP.set_xlim(-0.8,4.8); axP.set_ylim(0.2,3.8); axP.axis("off")
    fig.tight_layout(); fig.savefig("espacos.pdf", bbox_inches="tight"); plt.close(fig)

# ---------------------------------------------------------------- Fig 3: sub-rede central
def fig_central():
    G = build_graph(); deg = dict(G.degree())
    core = ["Palmeiras-Barra Funda","Marechal Deodoro","Santa Cecilia","Republica",
        "Anhangabau","Se","Pedro II","Bras","Bresser-Mooca","Luz","Sao Bento",
        "Tiradentes","Armenia","Higienopolis-Mackenzie","Paulista","Consolacao",
        "Trianon-Masp","Brigadeiro","Paraiso","Ana Rosa","Vergueiro","Sao Joaquim",
        "Liberdade","Tatuape","Belem","Juventus-Mooca","Julio Prestes","Oscar Freire"]
    H = G.subgraph([n for n in core if n in G]).copy()
    def col(n):
        ls = G.nodes[n]["lines"]
        return "#3a3f4b" if len(ls) > 1 else LINE_COLORS[next(iter(ls))]
    pos = nx.kamada_kawai_layout(H, scale=1.0)

    fig, ax = plt.subplots(figsize=(11, 8.4))
    for a,b,d in H.edges(data=True):
        ls=[l for l in d["lines"] if l!="transfer"]
        ec = "#9aa0a6" if not ls else LINE_COLORS[ls[0]]
        st = (0,(4,3)) if d["lines"]=={"transfer"} else "-"
        ax.plot([pos[a][0],pos[b][0]],[pos[a][1],pos[b][1]], color=ec, lw=2.6,
                linestyle=st, alpha=.9, zorder=1, solid_capstyle="round")
    for n in H.nodes():
        hub = len(G.nodes[n]["lines"])>1
        ax.scatter([pos[n][0]],[pos[n][1]], s=260+deg[n]*250, c=col(n),
                   edgecolors="white", linewidths=2.0, zorder=2)
    # rotulos com caixa branca semitransparente, deslocados, sem corte
    import numpy as np
    for n in H.nodes():
        hub = len(G.nodes[n]["lines"])>1
        if not (hub or deg[n] >= 3): continue
        x,y = pos[n]
        dy = 0.075 if y >= 0 else -0.075
        ax.annotate(pretty(n), (x,y), xytext=(0, 15 if dy>0 else -15),
                    textcoords="offset points", ha="center",
                    va="bottom" if dy>0 else "top", fontsize=9.5, fontweight="bold",
                    color="#18202c", zorder=5,
                    bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none", alpha=0.82))
    ax.margins(0.16)
    ax.set_title("Sub-rede central (recorte ilustrativo) — vertice proporcional ao grau; "
                 "cinza = baldeacao", fontsize=11, pad=12)
    ax.axis("off"); fig.tight_layout()
    fig.savefig("central.pdf", bbox_inches="tight"); plt.close(fig)

# ---------------------------------------------------------------- Fig 4: modelo 3D
def fig_modelo3d():
    d = json.load(open("grafo.json", encoding="utf-8"))
    P = {n["id"]: n for n in d["nodes"]}
    BG = "#0A0E1A"
    top = sorted(d["nodes"], key=lambda n: n["betweenness"], reverse=True)[:7]
    top_ids = {n["id"] for n in top}

    fig = plt.figure(figsize=(12, 6.2)); fig.patch.set_facecolor(BG)
    views = [(20, 35), (26, -68)]
    for i, (elev, azim) in enumerate(views, 1):
        ax = fig.add_subplot(1, 2, i, projection="3d")
        ax.set_facecolor(BG)
        for e in d["edges"]:
            a, b = P[e["s"]], P[e["t"]]
            ax.plot([a["x"],b["x"]],[a["y"],b["y"]],[a["z"],b["z"]],
                    color=e["color"], lw=0.9 if e["transfer"] else 1.5,
                    alpha=0.45 if e["transfer"] else 0.75, zorder=1)
        # nao-hubs
        nh = [n for n in d["nodes"] if not n["hub"]]
        ax.scatter([n["x"] for n in nh],[n["y"] for n in nh],[n["z"] for n in nh],
                   c=[n["color"] for n in nh],
                   s=[10+n["degree"]*7+n["betweenness"]*180 for n in nh],
                   depthshade=True, edgecolors="none", zorder=2)
        # hubs por cima
        hb = [n for n in d["nodes"] if n["hub"]]
        ax.scatter([n["x"] for n in hb],[n["y"] for n in hb],[n["z"] for n in hb],
                   c="#F2ECD0", s=[26+n["degree"]*10+n["betweenness"]*240 for n in hb],
                   depthshade=False, edgecolors="#6b6650", linewidths=0.5, zorder=3)
        for n in top:
            ax.text(n["x"], n["y"], n["z"]+6, pretty(n["id"]), color="#EAF0FB",
                    fontsize=8, fontweight="bold", ha="center", zorder=5)
        ax.set_axis_off()
        ax.view_init(elev=elev, azim=azim)
        try: ax.set_box_aspect((1,1,0.9))
        except Exception: pass
    fig.suptitle("Modelo 3D da malha — esferas claras = baldeações (tamanho ∝ intermediação)",
                 color="#AEB7CC", fontsize=11, y=0.965)
    fig.subplots_adjust(left=0, right=1, top=0.93, bottom=0, wspace=0.0)
    fig.savefig("modelo3d.pdf", facecolor=BG, bbox_inches="tight", pad_inches=0.15)
    fig.savefig("modelo3d.png", facecolor=BG, dpi=150, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)

fig_pipeline(); fig_espacos(); fig_central(); fig_modelo3d()
print("OK: metodologia.pdf, espacos.pdf, central.pdf, modelo3d.pdf/.png")
