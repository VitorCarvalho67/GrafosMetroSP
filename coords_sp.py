# -*- coding: utf-8 -*-
"""Gera coordenadas geográficas APROXIMADAS das 176 estações: ancora
terminais/baldeações conhecidos (lat,lon reais aproximados) e interpola
linearmente as estações intermediárias ao longo da sequência de cada linha."""
import json
from rede_sp import LINES, LINE_COLORS

# Âncoras: (lat, lon) aproximados de estações reais (terminais e baldeações).
A = {
 "Tucuruvi":(-23.480,-46.602),"Santana":(-23.502,-46.625),"Luz":(-23.534,-46.635),
 "Se":(-23.550,-46.634),"Ana Rosa":(-23.581,-46.638),"Jabaquara":(-23.646,-46.641),
 "Vila Madalena":(-23.546,-46.690),"Consolacao":(-23.557,-46.660),"Paraiso":(-23.576,-46.640),
 "Chacara Klabin":(-23.590,-46.628),"Vila Prudente":(-23.583,-46.578),
 "Palmeiras-Barra Funda":(-23.527,-46.665),"Republica":(-23.543,-46.642),"Bras":(-23.545,-46.615),
 "Tatuape":(-23.540,-46.577),"Corinthians-Itaquera":(-23.543,-46.472),
 "Paulista":(-23.555,-46.661),"Pinheiros":(-23.567,-46.702),"Butanta":(-23.571,-46.708),
 "Vila Sonia":(-23.596,-46.731),
 "Capao Redondo":(-23.667,-46.781),"Santo Amaro":(-23.654,-46.710),"Moema":(-23.610,-46.663),
 "Sao Mateus":(-23.610,-46.475),"Jardim Colonial":(-23.628,-46.454),
 "Morumbi":(-23.622,-46.702),"Campo Belo":(-23.622,-46.664),
 "Joao Paulo I":(-23.478,-46.685),"Agua Branca":(-23.520,-46.680),"Perdizes":(-23.535,-46.676),
 "Sao Joaquim":(-23.567,-46.639),
 "Lapa":(-23.520,-46.702),"Jundiai":(-23.189,-46.884),
 "Julio Prestes":(-23.534,-46.640),"Osasco":(-23.532,-46.792),"Itapevi":(-23.548,-46.934),
 "Grajau":(-23.771,-46.685),
 "Tamanduatei":(-23.586,-46.605),"Santo Andre":(-23.652,-46.532),"Rio Grande da Serra":(-23.744,-46.398),
 "Guaianases":(-23.540,-46.413),"Mogi das Cruzes":(-23.523,-46.188),"Estudantes":(-23.528,-46.170),
 "Engenheiro Goulart":(-23.510,-46.522),"Sao Miguel Paulista":(-23.497,-46.443),"Calmon Viana":(-23.532,-46.360),
 "Guarulhos-CECAP":(-23.455,-46.533),"Aeroporto-Guarulhos":(-23.435,-46.472),
 "Higienopolis-Mackenzie":(-23.547,-46.652),
}

coord = dict(A)
for line, seq in LINES.items():
    known = [i for i, s in enumerate(seq) if s in coord]
    if not known:
        continue
    for i, s in enumerate(seq):
        if s in coord:
            continue
        # âncoras à esquerda e à direita na sequência
        left = max([k for k in known if k < i], default=None)
        right = min([k for k in known if k > i], default=None)
        if left is not None and right is not None:
            t = (i - left) / (right - left)
            la = coord[seq[left]][0] + (coord[seq[right]][0]-coord[seq[left]][0])*t
            lo = coord[seq[left]][1] + (coord[seq[right]][1]-coord[seq[left]][1])*t
        elif right is not None:  # antes da primeira âncora
            la, lo = coord[seq[right]]; la += 0.004*(right-i); lo -= 0.004*(right-i)
        else:                    # depois da última âncora
            la, lo = coord[seq[left]]; la -= 0.004*(i-left); lo += 0.004*(i-left)
        coord[s] = (round(la, 5), round(lo, 5))
    # registra recém-calculadas para reuso em baldeações
    for s in seq:
        known2 = [j for j, x in enumerate(seq) if x in coord]

# monta saída com linha/cor
from rede_sp import build_graph  # noqa
stations = []
seen = set()
for line, seq in LINES.items():
    for s in seq:
        if s in seen:
            continue
        seen.add(s)
        # linhas que servem a estação
        ls = [ln for ln, sq in LINES.items() if s in sq]
        stations.append({"id": s, "lat": coord[s][0], "lon": coord[s][1],
                         "lines": ls, "color": LINE_COLORS[ls[0]], "hub": len(ls) > 1})
# arestas geográficas (para desenhar os trilhos no globo)
edges = []
for line, seq in LINES.items():
    for a, b in zip(seq, seq[1:]):
        edges.append([a, b, LINE_COLORS[line]])
out = {"stations": stations, "edges": edges, "line_colors": LINE_COLORS}
json.dump(out, open("coords_sp.json", "w"), ensure_ascii=False, separators=(",", ":"))
print("estações:", len(stations), "| arestas:", len(edges),
      "| sem coord:", [s['id'] for s in stations if s['lat'] is None])
# checagem de bounding box
las=[s['lat'] for s in stations]; los=[s['lon'] for s in stations]
print(f"lat [{min(las):.3f},{max(las):.3f}] lon [{min(los):.3f},{max(los):.3f}]")
