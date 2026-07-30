# -*- coding: utf-8 -*-
"""Figuras de resultados do artigo (PDF vetorial). Paleta validada (dataviz)."""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams

# ---- paleta / estilo ----
BLUE = "#2a78d6"; ORANGE = "#eb6834"; RED = "#e34948"
INK = "#0b0b0b"; INK2 = "#52514e"; MUTED = "#898781"
GRID = "#e1e0d9"; SURF = "#fcfcfb"
BLUE_RAMP = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10,
    "figure.facecolor": SURF, "axes.facecolor": SURF,
    "axes.edgecolor": "#c3c2b7", "axes.linewidth": 0.8,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.7,
    "axes.spines.top": False, "axes.spines.right": False,
    "text.color": INK, "axes.labelcolor": INK2, "xtick.color": MUTED,
    "ytick.color": MUTED, "axes.titlecolor": INK, "savefig.bbox": "tight",
})

R = json.load(open("/tmp/work/resultados.json"))
R2 = json.load(open("/tmp/work/resultados2.json"))
OUT = "/tmp/work/"

# ---- 1) Distribuicao de grau ----
dd = {int(k): v for k, v in R["baseline"]["degree_dist"].items()}
ks = sorted(dd)
vals = [dd[k] for k in ks]
fig, ax = plt.subplots(figsize=(5.2, 3.0))
bars = ax.bar([str(k) for k in ks], vals, color=BLUE, width=0.62, zorder=3)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + 2, str(v), ha="center",
            va="bottom", fontsize=9, color=INK2)
ax.set_xlabel("Grau $k$"); ax.set_ylabel("Número de estações")
ax.set_ylim(0, max(vals) * 1.15); ax.grid(axis="x", visible=False)
ax.set_title("Distribuição de grau (espaço L)", fontsize=10.5, pad=8)
fig.savefig(OUT + "fig_grau.pdf"); plt.close(fig)

# ---- 2) Robustez S(f) aleatorio vs ataque ----
rs = R["robustness"]
keys = sorted(rs["random_S"], key=lambda x: float(x))
fx = [float(k) for k in keys]
Sr = [rs["random_S"][k] for k in keys]
Sa = [rs["attack_S"].get(k, None) for k in keys]
fig, ax = plt.subplots(figsize=(5.2, 3.2))
ax.plot(fx, Sr, color=BLUE, lw=2, marker="o", ms=4, label="Falha aleatória", zorder=3)
ax.plot(fx, Sa, color=RED, lw=2, marker="s", ms=4, label="Ataque dirigido (intermediação)", zorder=3)
ax.set_xlabel("Fração de estações removidas $f$")
ax.set_ylabel("Tamanho relativo da maior\ncomponente $S(f)$")
ax.set_xlim(0, 0.5); ax.set_ylim(0, 1.02)
ax.legend(frameon=False, fontsize=8.5, loc="upper right")
ax.set_title("Robustez: falha aleatória vs. ataque dirigido", fontsize=10.5, pad=8)
fig.savefig(OUT + "fig_robustez.pdf"); plt.close(fig)

# ---- 3) Top hubs por intermediacao ----
bt = R["centralities"]["betweenness_top"][:12][::-1]
names = [x[0] for x in bt]; bvals = [x[1] for x in bt]
fig, ax = plt.subplots(figsize=(5.4, 3.6))
bars = ax.barh(names, bvals, color=BLUE, height=0.68, zorder=3)
for b, v in zip(bars, bvals):
    ax.text(v + 0.006, b.get_y() + b.get_height() / 2, f"{v:.3f}",
            va="center", fontsize=8, color=INK2)
ax.set_xlabel("Centralidade de intermediação $C_B$")
ax.set_xlim(0, max(bvals) * 1.16); ax.grid(axis="y", visible=False)
ax.set_title("As 12 estações mais centrais (hubs)", fontsize=10.5, pad=8)
fig.savefig(OUT + "fig_hubs.pdf"); plt.close(fig)

# ---- 4) Comparacao internacional (robustez rT Derrible) ----
dk = R2["derrible_table"]
data = [("São Paulo", R2["derrible_sp"]["rT"], True)]
for c, v in dk.items():
    data.append((c, v[2], False))
data.sort(key=lambda x: x[1])
labels = [d[0] for d in data]; rts = [d[1] for d in data]
cols = [ORANGE if d[2] else BLUE for d in data]
fig, ax = plt.subplots(figsize=(5.4, 3.6))
bars = ax.barh(labels, rts, color=cols, height=0.68, zorder=3)
for b, v, d in zip(bars, rts, data):
    ax.text(v + 0.004, b.get_y() + b.get_height() / 2, f"{v:.3f}",
            va="center", fontsize=8, color=INK2)
ax.set_xlabel("Índice de robustez $r_T = \\mu/N$ (Derrible e Kennedy)")
ax.set_xlim(0, max(rts) * 1.16); ax.grid(axis="y", visible=False)
ax.set_title("Robustez topológica: SP vs. metrôs internacionais", fontsize=10.5, pad=8)
fig.savefig(OUT + "fig_intl.pdf"); plt.close(fig)

# ---- 5) Eficiencia por regiao (comunidades, mean closeness) ----
reg = sorted(R["region_efficiency"], key=lambda c: c["mean_closeness"])
rlabels = [f"{c['sample'][0]} …" for c in reg]
clos = [c["mean_closeness"] for c in reg]
cmax = max(clos); cmin = min(clos)
def ramp(v):
    t = (v - cmin) / (cmax - cmin + 1e-9)
    return BLUE_RAMP[1 + int(t * (len(BLUE_RAMP) - 2))]
fig, ax = plt.subplots(figsize=(5.6, 4.0))
bars = ax.barh(rlabels, clos, color=[ramp(v) for v in clos], height=0.7, zorder=3)
for b, v in zip(bars, clos):
    ax.text(v + 0.0015, b.get_y() + b.get_height() / 2, f"{v:.3f}",
            va="center", fontsize=7.5, color=INK2)
ax.set_xlabel("Proximidade média $\\overline{C_C}$ da comunidade (acessibilidade)")
ax.set_xlim(0, cmax * 1.18); ax.grid(axis="y", visible=False)
ax.tick_params(axis="y", labelsize=7.5)
ax.set_title("Acessibilidade por região (comunidade), do centro à periferia",
             fontsize=10, pad=8)
fig.savefig(OUT + "fig_regioes.pdf"); plt.close(fig)

# ---- 6) Linhas propostas: custo estimado x extensao ----
prop = R2["proposed"]
order = sorted(prop, key=lambda p: p["cost_bi"])
plabels = [p["name"].replace(" (completa)", "\n(completa)") for p in order]
costs = [p["cost_bi"] for p in order]
kms = [p["km"] for p in order]
fig, ax = plt.subplots(figsize=(5.6, 3.3))
bars = ax.barh(plabels, costs, color=BLUE, height=0.66, zorder=3)
for b, c, km in zip(bars, costs, kms):
    ax.text(c + 0.4, b.get_y() + b.get_height() / 2, f"R\\${c:.0f} bi · {km:.0f} km",
            va="center", fontsize=7.5, color=INK2)
ax.set_xlabel("Custo estimado (R\\$ bilhões, valores 2024/26)")
ax.set_xlim(0, max(costs) * 1.28); ax.grid(axis="y", visible=False)
ax.tick_params(axis="y", labelsize=8)
ax.set_title("Custo estimado das linhas em projeto (≈ R\\$1,18 bi/km subterrâneo)",
             fontsize=9.5, pad=8)
fig.savefig(OUT + "fig_linhas.pdf"); plt.close(fig)

print("Figuras geradas:", "fig_grau, fig_robustez, fig_hubs, fig_intl, fig_regioes, fig_linhas")
