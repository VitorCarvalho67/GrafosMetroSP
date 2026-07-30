# -*- coding: utf-8 -*-
import json, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams
BLUE="#2a78d6"; ORANGE="#eb6834"; AQUA="#1baf7a"; RED="#e34948"; INK="#0b0b0b"; INK2="#52514e"
MUTED="#898781"; GRID="#e1e0d9"; SURF="#fcfcfb"
rcParams.update({"font.family":"DejaVu Sans","font.size":10,"figure.facecolor":SURF,
 "axes.facecolor":SURF,"axes.edgecolor":"#c3c2b7","axes.linewidth":.8,"axes.grid":True,
 "grid.color":GRID,"grid.linewidth":.7,"axes.spines.top":False,"axes.spines.right":False,
 "text.color":INK,"axes.labelcolor":INK2,"xtick.color":MUTED,"ytick.color":MUTED,"savefig.bbox":"tight"})
R=json.load(open("/tmp/work/compare3.json"))
order=["SP","LN","NY"]; names={"SP":"São Paulo","LN":"Londres","NY":"Nova York"}
cols={"SP":ORANGE,"LN":BLUE,"NY":AQUA}
OUT="/tmp/work/"

# 1) small-world sigma
fig,ax=plt.subplots(figsize=(5.0,3.0))
xs=[names[k] for k in order]; ys=[R[k]["sigma"] for k in order]
bars=ax.bar(xs,ys,color=[cols[k] for k in order],width=.6,zorder=3)
ax.axhline(1.0,color=RED,lw=1.4,ls="--",zorder=2)
ax.text(2.35,1.06,"σ = 1 (limiar)",color=RED,fontsize=8,ha="right")
for b,v in zip(bars,ys): ax.text(b.get_x()+b.get_width()/2,v+0.05,f"{v:.2f}",ha="center",fontsize=9,color=INK2)
ax.set_ylabel("Índice de mundo pequeno σ"); ax.grid(axis="x",visible=False); ax.set_ylim(0,max(ys)*1.18)
ax.set_title("Mundo pequeno: só SP fica abaixo de σ=1",fontsize=10.5,pad=8)
fig.savefig(OUT+"fig_sw3.pdf"); plt.close(fig)

# 2) robustez sob ataque
fig,ax=plt.subplots(figsize=(5.2,3.2))
for k in order:
    d=R[k]["atkS"]; xs=sorted(float(x) for x in d); ys=[d[f"{x}" if f"{x}" in d else str(x)] for x in xs]
    ys=[d[str(x)] for x in xs]
    ax.plot(xs,ys,color=cols[k],lw=2,marker="o",ms=3.5,label=names[k],zorder=3)
ax.set_xlabel("Fração de estações removidas (ataque dirigido)")
ax.set_ylabel("Maior componente S(f)"); ax.set_xlim(0,0.3); ax.set_ylim(0,1.02)
ax.legend(frameon=False,fontsize=9); ax.set_title("Robustez a ataques: as três colapsam cedo",fontsize=10.5,pad=8)
fig.savefig(OUT+"fig_robust3.pdf"); plt.close(fig)

# 3) painel de indicadores (grau, clustering, transfer, rT)
fig,axes=plt.subplots(1,4,figsize=(7.6,2.6))
specs=[("avg_degree","Grau médio ⟨k⟩",1),("C","Agrupamento C",1000),
       ("transfer_ratio","Razão de baldeações",100),("rT","Robustez r_T",1000)]
for ax,(key,title,_sc) in zip(axes,specs):
    ys=[R[k][key] for k in order]
    bars=ax.bar([names[k].split()[0] for k in order],ys,color=[cols[k] for k in order],width=.62,zorder=3)
    for b,v in zip(bars,ys): ax.text(b.get_x()+b.get_width()/2,v,f"{v:.3f}".rstrip('0').rstrip('.') if v<1 else f"{v:.2f}",
        ha="center",va="bottom",fontsize=7.5,color=INK2)
    ax.set_title(title,fontsize=9); ax.grid(axis="x",visible=False)
    ax.set_ylim(0,max(ys)*1.22); ax.tick_params(axis="x",labelsize=8)
fig.suptitle("Indicadores estruturais: São Paulo vs. Londres vs. Nova York",fontsize=10.5,y=1.04)
fig.savefig(OUT+"fig_ind3.pdf"); plt.close(fig)
print("figuras: fig_sw3, fig_robust3, fig_ind3")
