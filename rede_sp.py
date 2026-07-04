# -*- coding: utf-8 -*-
"""Definicao da malha metroferroviaria da RMSP (config. inicio de 2026).
Espaco L: estacoes = vertices; estacoes consecutivas de uma linha = arestas.
Estacoes de baldeacao aparecem com o MESMO nome em varias linhas -> vertice unico.
"""

# Cores oficiais aproximadas das linhas
LINE_COLORS = {
    "1-Azul":      "#0353A4",
    "2-Verde":     "#00825E",
    "3-Vermelha":  "#EE3B33",
    "4-Amarela":   "#FFD500",
    "5-Lilas":     "#7C4D9F",
    "15-Prata":    "#9AA0A6",
    "17-Ouro":     "#C6A951",
    "7-Rubi":      "#9E1B4B",
    "8-Diamante":  "#7FA99B",
    "9-Esmeralda": "#009E9E",
    "10-Turquesa": "#12A0C8",
    "11-Coral":    "#EF5B4C",
    "12-Safira":   "#14387F",
    "13-Jade":     "#12AE5A",
}

LINES = {
    "1-Azul": ["Tucuruvi","Parada Inglesa","Jardim Sao Paulo-Ayrton Senna","Santana",
        "Carandiru","Portuguesa-Tiete","Armenia","Tiradentes","Luz","Sao Bento","Se",
        "Liberdade","Sao Joaquim","Vergueiro","Paraiso","Ana Rosa","Vila Mariana",
        "Santa Cruz","Praca da Arvore","Saude","Sao Judas","Conceicao","Jabaquara"],

    "2-Verde": ["Vila Madalena","Sumare","Clinicas","Consolacao","Trianon-Masp",
        "Brigadeiro","Paraiso","Ana Rosa","Chacara Klabin","Santos-Imigrantes",
        "Alto do Ipiranga","Sacoma","Tamanduatei","Vila Prudente"],

    "3-Vermelha": ["Palmeiras-Barra Funda","Marechal Deodoro","Santa Cecilia","Republica",
        "Anhangabau","Se","Pedro II","Bras","Bresser-Mooca","Belem","Tatuape","Carrao",
        "Penha","Vila Matilde","Guilhermina-Esperanca","Patriarca","Artur Alvim",
        "Corinthians-Itaquera"],

    "4-Amarela": ["Luz","Republica","Higienopolis-Mackenzie","Paulista","Oscar Freire",
        "Fradique Coutinho","Faria Lima","Pinheiros","Butanta","Sao Paulo-Morumbi",
        "Vila Sonia"],

    "5-Lilas": ["Capao Redondo","Campo Limpo","Vila das Belezas","Giovanni Gronchi",
        "Santo Amaro","Largo Treze","Adolfo Pinheiro","Alto da Boa Vista","Borba Gato",
        "Brooklin","Campo Belo","Eucaliptos","Moema","AACD-Servidor","Hospital Sao Paulo",
        "Santa Cruz","Chacara Klabin"],

    "15-Prata": ["Vila Prudente","Oratorio","Sao Lucas","Camilo Haddad","Vila Tolstoi",
        "Vila Uniao","Jardim Planalto","Sapopemba","Fazenda da Juta","Sao Mateus",
        "Jardim Colonial"],

    "17-Ouro": ["Morumbi","Vereador Jose Diniz","Brooklin Paulista","Campo Belo"],

    "7-Rubi": ["Luz","Palmeiras-Barra Funda","Agua Branca","Lapa","Piqueri","Pirituba",
        "Vila Clarice","Jaragua","Vila Aurora","Perus","Caieiras","Franco da Rocha",
        "Baltazar Fidelis","Francisco Morato","Botujuru","Campo Limpo Paulista",
        "Varzea Paulista","Jundiai"],

    "8-Diamante": ["Julio Prestes","Palmeiras-Barra Funda","Lapa","Domingos de Moraes",
        "Imperatriz Leopoldina","Presidente Altino","Osasco","Comandante Sampaio",
        "Quitauna","General Miguel Costa","Carapicuiba","Santa Terezinha","Antonio Joao",
        "Barueri","Jardim Belval","Jardim Silveira","Jandira","Sagrado Coracao",
        "Engenheiro Cardoso","Itapevi"],

    "9-Esmeralda": ["Osasco","Presidente Altino","Ceasa","Villa Lobos-Jaguare",
        "Cidade Universitaria","Pinheiros","Hebraica-Reboucas","Cidade Jardim",
        "Vila Olimpia","Berrini","Morumbi","Granja Julieta","Santo Amaro","Socorro",
        "Jurubatuba","Autodromo","Primavera-Interlagos","Grajau"],

    "10-Turquesa": ["Luz","Bras","Juventus-Mooca","Ipiranga","Tamanduatei",
        "Sao Caetano do Sul","Utinga","Prefeito Saladino","Santo Andre","Capuava","Maua",
        "Guapituba","Ribeirao Pires","Rio Grande da Serra"],

    "11-Coral": ["Luz","Bras","Tatuape","Corinthians-Itaquera","Dom Bosco","Jose Bonifacio",
        "Guaianases","Antonio Gomes","Ferraz de Vasconcelos","Poa","Calmon Viana","Suzano",
        "Jundiapeba","Braz Cubas","Mogi das Cruzes","Estudantes"],

    "12-Safira": ["Bras","Tatuape","Engenheiro Goulart","USP Leste","Comendador Ermelino",
        "Sao Miguel Paulista","Jardim Helena-Vila Mara","Itaim Paulista","Jardim Romano",
        "Engenheiro Manoel Feio","Itaquaquecetuba","Aracare","Calmon Viana"],

    "13-Jade": ["Engenheiro Goulart","Guarulhos-CECAP","Aeroporto-Guarulhos"],
}

# Baldeacoes entre estacoes de NOMES diferentes (complexos integrados)
TRANSFERS = [
    ("Consolacao", "Paulista"),     # L2 <-> L4
    ("Luz", "Julio Prestes"),       # complexo Luz <-> L8
]

def build_graph():
    import networkx as nx
    G = nx.Graph()
    for line, seq in LINES.items():
        for st in seq:
            if st not in G:
                G.add_node(st, lines=set())
            G.nodes[st]["lines"].add(line)
        for a, b in zip(seq, seq[1:]):
            if G.has_edge(a, b):
                G[a][b]["lines"].add(line)
            else:
                G.add_edge(a, b, lines={line})
    for a, b in TRANSFERS:
        if a in G and b in G:
            if G.has_edge(a, b):
                G[a][b]["lines"].add("transfer")
            else:
                G.add_edge(a, b, lines={"transfer"})
    return G

if __name__ == "__main__":
    G = build_graph()
    print(f"N = {G.number_of_nodes()}  M = {G.number_of_edges()}")
