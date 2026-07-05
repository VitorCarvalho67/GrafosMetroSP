# Topologia da Malha Metroferroviária de São Paulo

**Uma análise via Teoria dos Grafos** — Disciplina de Comunicação e Redes, Bacharelado em Ciência e Tecnologia (BC&T), Universidade Federal do ABC (UFABC).

A malha metroferroviária metropolitana de São Paulo — a maior do país — é modelada como um grafo em que os **vértices são estações** e as **arestas são conexões diretas** entre estações consecutivas de cada linha. Estações de baldeação tornam-se vértices compartilhados de alta ordem. A partir das representações em **espaço L** e **espaço P**, o trabalho caracteriza a topologia (grau, caminho característico, eficiência global, agrupamento, centralidade de intermediação e proximidade, mundo pequeno e estrutura de comunidades) e avalia a robustez da rede sob falhas aleatórias e ataques direcionados aos hubs.

Este repositório reúne o **artigo** (padrão SBC), os **scripts** que constroem e medem o grafo, e uma **visualização 3D interativa** (Three.js) da rede.

## Autores

Vitor Eduardo Silva de Carvalho · Diego Naoki Sato Hanashiro · João Vitor Ribeiro Pereira · Joaquim Argolo Valente de Azambuja

## A rede em números

| Métrica | Valor |
|---|---|
| Estações (vértices, N) | 176 |
| Conexões (arestas, M) | 189 |
| Grau médio ⟨k⟩ | 2.15 |
| Modularidade (Q) | 0.811 |
| Comunidades detectadas | 15 |
| Linhas (metrô + CPTM) | 15 |

## Estrutura do repositório

| Arquivo | Descrição |
|---|---|
| `artigo.tex` | Artigo no padrão SBC (fonte principal) |
| `refs.bib` | Referências (BibTeX) |
| `sbc-template.sty`, `sbc.bst` | Estilo SBC e estilo de bibliografia |
| `rede_sp.py` | Definição da rede (linhas/estações) + `build_graph()` |
| `export_grafo.py` | Cálculo de métricas e exportação do `grafo.json` |
| `figuras.py` | Geração das figuras vetoriais do artigo |
| `grafo.json` | Grafo serializado (dados da rede) |
| `visualizacao_3d-2.html` | Visualização 3D interativa (Three.js) — **é o site** |
| `metodologia.pdf`, `espacos.pdf`, `central.pdf` | Figuras do artigo |
| `viz_screenshot.png` | Captura de tela da visualização |

## Reproduzir métricas e figuras

Requer Python 3 com `networkx` e `matplotlib`:

```bash
python3 export_grafo.py   # imprime N, M, ⟨k⟩, Q e o ranking de intermediação
python3 figuras.py        # regenera metodologia.pdf, espacos.pdf, central.pdf
```

## Compilar o artigo

```bash
pdflatex artigo.tex
bibtex   artigo
pdflatex artigo.tex
pdflatex artigo.tex
```

No Overleaf: faça upload de todos os arquivos, defina `artigo.tex` como documento principal e use o compilador **pdfLaTeX**.

## Visualização 3D (site)

A visualização é um único HTML **auto-contido** — os dados do grafo já estão embutidos no arquivo e o Three.js é carregado via CDN. Para ver localmente, basta abrir `visualizacao_3d-2.html` num navegador (ou servir a pasta com qualquer servidor estático).

### Deploy com Docker

O site é servido por um container `nginx:alpine` que monta este diretório como conteúdo estático. Ele se conecta à rede externa `solveweb-site_web` (a mesma do `nginx-proxy-manager`), permitindo o roteamento por domínio sem publicar portas sensíveis — este compose **não cria nem altera** nenhuma outra rede ou serviço.

```bash
docker compose up -d
```

- Container: `grafos-metro-sp`
- Porta no host: `8888` → `80` (acesso direto: `http://SEU_HOST:8888`)
- Rede: `solveweb-site_web` (externa) — o proxy alcança o container em `grafos-metro-sp:80`

Para expor via domínio, adicione um *Proxy Host* no nginx-proxy-manager apontando para `grafos-metro-sp` na porta `80`.

```bash
docker compose logs -f      # acompanhar logs
docker compose down         # parar e remover o container
```

## Licença

Distribuído sob a licença MIT. Veja [LICENSE](LICENSE).
