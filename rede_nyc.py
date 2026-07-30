# -*- coding: utf-8 -*-
"""Malha do metrô de Nova York (MTA Subway) modelada a partir do mapa oficial.
Mesmo método do rede_sp.py: espaço L, estações consecutivas = arestas, nome
canônico por estação (complexos de transferência = vértice único). Modelado por
serviço/linha; ramais como sequências que compartilham estações. É a rede mais
complexa das três — modelo fiel best-effort, validado contra ~472 estações.
Estações são identificadas por 'Nome@Rua' quando necessário para desambiguar."""

LINE_COLORS = {
 "1":"#EE352E","2":"#EE352E","3":"#EE352E","4":"#00933C","5":"#00933C","6":"#00933C",
 "7":"#B933AD","A":"#0039A6","C":"#0039A6","E":"#0039A6","B":"#FF6319","D":"#FF6319",
 "F":"#FF6319","M":"#FF6319","G":"#6CBE45","J":"#996633","Z":"#996633","L":"#A7A9AC",
 "N":"#FCCC0A","Q":"#FCCC0A","R":"#FCCC0A","W":"#FCCC0A",
}

LINES = {
 # ---- IRT (numeradas) ----
 "1": ["Van Cortlandt Park-242","238 St","231 St","Marble Hill-225 St","215 St","207 St",
   "Dyckman St","191 St","181 St","168 St","157 St","145 St","137 St-City College","125 St (1)",
   "116 St-Columbia","Cathedral Pkwy-110 St","103 St (1)","96 St","86 St (1)","79 St","72 St (1-2-3)",
   "66 St-Lincoln Center","59 St-Columbus Circle","50 St (1)","Times Sq-42 St","34 St-Penn Station (1-2-3)",
   "28 St (1)","23 St (1)","18 St","14 St (1-2-3)","Christopher St-Sheridan Sq","Houston St","Canal St (1)",
   "Franklin St","Chambers St (1-2-3)","WTC Cortlandt","Rector St (1)","South Ferry"],
 "2": ["Wakefield-241 St","Nereid Av","233 St","225 St","219 St","Gun Hill Rd (2-5)","Pelham Pkwy (2-5)",
   "Bronx Park East","E 180 St","West Farms Sq-E Tremont Av","174 St","Freeman St","Simpson St",
   "Intervale Av","Prospect Av (2-5)","Jackson Av","3 Av-149 St","149 St-Grand Concourse","135 St (2-3)",
   "125 St (2-3)","116 St (2-3)","Central Park North-110 St","96 St","72 St (1-2-3)","Times Sq-42 St",
   "34 St-Penn Station (1-2-3)","14 St (1-2-3)","Chambers St (1-2-3)","Park Place","Fulton St","Wall St (2-3)",
   "Clark St","Borough Hall (2-3)","Hoyt St","Nevins St","Atlantic Av-Barclays Ctr","Bergen St (2-3)",
   "Grand Army Plaza","Eastern Pkwy-Brooklyn Museum","Franklin Av (2-3-4-5)","President St","Sterling St",
   "Winthrop St","Church Av (2-5)","Beverly Rd","Newkirk Av","Flatbush Av-Brooklyn College"],
 "3": ["Harlem-148 St","145 St (3)","135 St (2-3)","125 St (2-3)","116 St (2-3)","Central Park North-110 St",
   "96 St","72 St (1-2-3)","Times Sq-42 St","34 St-Penn Station (1-2-3)","14 St (1-2-3)","Chambers St (1-2-3)",
   "Park Place","Fulton St","Wall St (2-3)","Clark St","Borough Hall (2-3)","Hoyt St","Nevins St",
   "Atlantic Av-Barclays Ctr","Bergen St (2-3)","Grand Army Plaza","Eastern Pkwy-Brooklyn Museum",
   "Franklin Av (2-3-4-5)","Nostrand Av","Kingston Av","Crown Hts-Utica Av","Sutter Av-Rutland Rd",
   "Saratoga Av","Rockaway Av (3)","Junius St","Pennsylvania Av","Van Siclen Av","New Lots Av"],
 "4": ["Woodlawn","Mosholu Pkwy","Bedford Park Blvd-Lehman College","Kingsbridge Rd (4)","Fordham Rd (4)",
   "183 St","Burnside Av","176 St","Mt Eden Av","170 St (4)","167 St (4)","161 St-Yankee Stadium",
   "149 St-Grand Concourse","138 St-Grand Concourse","125 St (4-5-6)","86 St (4-5-6)","59 St (4-5-6)",
   "Grand Central-42 St","14 St-Union Sq","Brooklyn Bridge-City Hall","Fulton St","Wall St (4-5)",
   "Bowling Green","Borough Hall (4-5)","Nevins St","Atlantic Av-Barclays Ctr","Franklin Av (2-3-4-5)",
   "Crown Hts-Utica Av"],
 "5": ["Eastchester-Dyre Av","Baychester Av","Gun Hill Rd (2-5)","Pelham Pkwy (2-5)","Morris Park",
   "E 180 St","West Farms Sq-E Tremont Av","174 St","Freeman St","Simpson St","Intervale Av",
   "Prospect Av (2-5)","149 St-Grand Concourse","138 St-Grand Concourse","125 St (4-5-6)","86 St (4-5-6)",
   "59 St (4-5-6)","Grand Central-42 St","14 St-Union Sq","Brooklyn Bridge-City Hall","Fulton St",
   "Wall St (4-5)","Bowling Green","Borough Hall (4-5)","Nevins St","Atlantic Av-Barclays Ctr",
   "Franklin Av (2-3-4-5)","Nostrand Av","Kingston Av","Crown Hts-Utica Av","Sutter Av-Rutland Rd",
   "Saratoga Av","Church Av (2-5)"],
 "6": ["Pelham Bay Park","Buhre Av","Middletown Rd","Westchester Sq-E Tremont Av","Zerega Av","Castle Hill Av",
   "Parkchester","St Lawrence Av","Morrison Av-Soundview","Elder Av","Whitlock Av","Hunts Point Av",
   "Longwood Av","E 149 St","E 143 St-St Marys St","Cypress Av","Brook Av","3 Av-138 St","125 St (4-5-6)",
   "116 St (6)","110 St (6)","103 St (6)","96 St (6)","86 St (4-5-6)","77 St","68 St-Hunter College",
   "59 St (4-5-6)","51 St","Grand Central-42 St","33 St","28 St (6)","23 St (6)","14 St-Union Sq",
   "Astor Pl","Bleecker St","Spring St (6)","Canal St (6)","Brooklyn Bridge-City Hall"],
 "7": ["Flushing-Main St","Mets-Willets Point","111 St","103 St-Corona Plaza","Junction Blvd",
   "90 St-Elmhurst Av","82 St-Jackson Hts","74 St-Broadway","69 St","61 St-Woodside","52 St","46 St-Bliss St",
   "40 St-Lowery St","33 St-Rawson St","Queensboro Plaza","Court Sq (7)","Hunters Point Av","Vernon Blvd-Jackson Av",
   "Grand Central-42 St","5 Av-Bryant Park","Times Sq-42 St","34 St-Hudson Yards"],

 # ---- IND / BMT (letras) ----
 "A": ["Inwood-207 St","Dyckman St (A)","190 St","181 St (A)","175 St","168 St","145 St (A-C-B-D)",
   "125 St (A-C-B-D)","59 St-Columbus Circle","42 St-Port Authority","34 St-Penn Station (A-C-E)",
   "14 St (A-C-E)","W 4 St-Wash Sq","Fulton St","High St","Jay St-MetroTech","Hoyt-Schermerhorn Sts",
   "Utica Av (A-C)","Broadway Junction","Euclid Av","Grant Av","80 St","88 St","Rockaway Blvd",
   "104 St","111 St (A)","Ozone Park-Lefferts Blvd"],
 "C": ["168 St","145 St (A-C-B-D)","135 St (C)","125 St (A-C-B-D)","116 St (C)","Cathedral Pkwy (C)",
   "103 St (C)","96 St (C)","86 St (C)","81 St-Museum","72 St (C)","59 St-Columbus Circle",
   "42 St-Port Authority","34 St-Penn Station (A-C-E)","23 St (C-E)","14 St (A-C-E)","W 4 St-Wash Sq",
   "Spring St (C-E)","Canal St (A-C-E)","Chambers St (A-C)","Fulton St","High St","Jay St-MetroTech",
   "Hoyt-Schermerhorn Sts","Lafayette Av","Clinton-Washington Avs (C)","Franklin Av (C)","Nostrand Av (A-C)",
   "Kingston-Throop Avs","Utica Av (A-C)","Ralph Av","Rockaway Av (C)","Broadway Junction","Euclid Av"],
 "E": ["Jamaica Center-Parsons/Archer","Sutphin Blvd-Archer Av","Jamaica-Van Wyck","Briarwood",
   "Kew Gardens-Union Tpke","75 Av","Forest Hills-71 Av","Jackson Hts-Roosevelt Av","Court Sq (E-M)",
   "Queens Plaza","Lexington Av/53 St","5 Av/53 St","7 Av (B-D-E)","50 St (E)","42 St-Port Authority",
   "34 St-Penn Station (A-C-E)","23 St (C-E)","14 St (A-C-E)","W 4 St-Wash Sq","Spring St (C-E)",
   "Canal St (A-C-E)","World Trade Center"],
 "B": ["Bedford Park Blvd (B-D)","Kingsbridge Rd (B-D)","Fordham Rd (B-D)","182-183 Sts","Tremont Av",
   "174-175 Sts","170 St (B-D)","167 St (B-D)","161 St-Yankee Stadium","155 St (B-D)","145 St (A-C-B-D)",
   "116 St (B-C)","Cathedral Pkwy (C)","103 St (C)","96 St (C)","86 St (C)","81 St-Museum","72 St (C)",
   "59 St-Columbus Circle","7 Av (B-D-E)","47-50 Sts-Rockefeller Ctr","42 St-Bryant Pk","34 St-Herald Sq",
   "W 4 St-Wash Sq","Broadway-Lafayette St","Grand St","Atlantic Av-Barclays Ctr","7 Av (B-Q)","Prospect Park",
   "Church Av (B-Q)","Newkirk Plaza","Brighton Beach"],
 "D": ["Norwood-205 St","Bedford Park Blvd (B-D)","Kingsbridge Rd (B-D)","Fordham Rd (B-D)","182-183 Sts",
   "Tremont Av","174-175 Sts","170 St (B-D)","167 St (B-D)","161 St-Yankee Stadium","155 St (B-D)",
   "145 St (A-C-B-D)","125 St (A-C-B-D)","59 St-Columbus Circle","7 Av (B-D-E)","47-50 Sts-Rockefeller Ctr",
   "42 St-Bryant Pk","34 St-Herald Sq","W 4 St-Wash Sq","Broadway-Lafayette St","Grand St",
   "Atlantic Av-Barclays Ctr","36 St (D-N-R)","9 Av","Fort Hamilton Pkwy (D)","50 St (D)","55 St","62 St (D)",
   "71 St","79 St (D)","18 Av (D)","20 Av (D)","Bay Pkwy (D)","25 Av","Bay 50 St","Coney Island-Stillwell Av"],
 "F": ["Jamaica-179 St","169 St","Parsons Blvd","Sutphin Blvd","Briarwood","Kew Gardens-Union Tpke","75 Av",
   "Forest Hills-71 Av","Jackson Hts-Roosevelt Av","Court Sq (E-M)","21 St-Queensbridge","Roosevelt Island",
   "Lexington Av/63 St","57 St","47-50 Sts-Rockefeller Ctr","42 St-Bryant Pk","34 St-Herald Sq","23 St (F-M)",
   "14 St (F-M)","W 4 St-Wash Sq","Broadway-Lafayette St","2 Av","Delancey St-Essex St","East Broadway",
   "York St","Jay St-MetroTech","Bergen St (F-G)","Carroll St","Smith-9 Sts","4 Av-9 St","7 Av (F-G)",
   "15 St-Prospect Park","Fort Hamilton Pkwy (F-G)","Church Av (F-G)","Ditmas Av","18 Av (F)","Avenue I",
   "Bay Pkwy (F)","Avenue N","Avenue P","Kings Hwy (F)","Avenue U (F)","Avenue X","Neptune Av",
   "West 8 St-NY Aquarium","Coney Island-Stillwell Av"],
 "M": ["Middle Village-Metropolitan Av","Fresh Pond Rd","Forest Av","Seneca Av","Myrtle-Wyckoff Avs",
   "Knickerbocker Av","Central Av","Myrtle Av","Flushing Av (J-M)","Marcy Av","Hewes St","Lorimer St (J-M)",
   "Delancey St-Essex St","2 Av","Broadway-Lafayette St","W 4 St-Wash Sq","34 St-Herald Sq","23 St (F-M)",
   "14 St (F-M)","23 St (F-M)","42 St-Bryant Pk","47-50 Sts-Rockefeller Ctr","5 Av/53 St","Lexington Av/53 St",
   "Court Sq (E-M)","Forest Hills-71 Av"],
 "G": ["Court Sq (G)","21 St","Greenpoint Av","Nassau Av","Metropolitan Av (G)","Broadway (G)","Flushing Av (G)",
   "Myrtle-Willoughby Avs","Bedford-Nostrand Avs","Classon Av","Clinton-Washington Avs (G)","Fulton St (G)",
   "Hoyt-Schermerhorn Sts","Bergen St (F-G)","Carroll St","Smith-9 Sts","4 Av-9 St","7 Av (F-G)",
   "15 St-Prospect Park","Fort Hamilton Pkwy (F-G)","Church Av (F-G)"],
 "J": ["Jamaica Center-Parsons/Archer","Sutphin Blvd-Archer Av","121 St","111 St (J)","104 St (J)","Woodhaven Blvd (J)",
   "85 St-Forest Pkwy","75 St-Elderts Ln","Cypress Hills","Crescent St","Norwood Av","Cleveland St","Van Siclen Av (J)",
   "Alabama Av","Broadway Junction","Chauncey St","Halsey St","Gates Av","Kosciuszko St","Myrtle Av",
   "Flushing Av (J-M)","Marcy Av","Hewes St","Lorimer St (J-M)","Delancey St-Essex St","Bowery","Canal St (J-Z)",
   "Chambers St (J-Z)","Fulton St","Broad St"],
 "L": ["8 Av (L)","6 Av (L)","14 St-Union Sq","3 Av (L)","1 Av (L)","Bedford Av","Lorimer St (L)","Graham Av",
   "Grand St (L)","Montrose Av","Morgan Av","Jefferson St","DeKalb Av (L)","Myrtle-Wyckoff Avs","Halsey St (L)",
   "Wilson Av","Bushwick Av-Aberdeen St","Broadway Junction","Atlantic Av (L)","Sutter Av (L)","Livonia Av",
   "New Lots Av (L)","East 105 St","Canarsie-Rockaway Pkwy"],
 "N": ["Astoria-Ditmars Blvd","Astoria Blvd","30 Av","Broadway (N-W)","36 Av","39 Av-Dutch Kills","Queensboro Plaza",
   "Lexington Av/59 St","5 Av/59 St","57 St-7 Av","49 St","Times Sq-42 St","34 St-Herald Sq","28 St (N-R-W)",
   "23 St (N-R-W)","14 St-Union Sq","8 St-NYU","Prince St","Canal St (N-Q-R-W)","City Hall (N-R-W)","Cortlandt St",
   "Rector St (N-R-W)","Whitehall St-South Ferry","Court St","Jay St-MetroTech","DeKalb Av","Atlantic Av-Barclays Ctr",
   "36 St (D-N-R)","59 St (N-R)","8 Av (N)","Fort Hamilton Pkwy (N)","New Utrecht Av","18 Av (N)","20 Av (N)",
   "Bay Pkwy (N)","Kings Hwy (N)","Avenue U (N)","86 St (N)","Coney Island-Stillwell Av"],
 "Q": ["96 St (Q)","86 St (Q)","72 St (Q)","Lexington Av/63 St","57 St-7 Av","Times Sq-42 St","34 St-Herald Sq",
   "14 St-Union Sq","Canal St (N-Q-R-W)","Atlantic Av-Barclays Ctr","7 Av (B-Q)","Prospect Park","Parkside Av",
   "Church Av (B-Q)","Beverley Rd","Cortelyou Rd","Newkirk Plaza","Avenue H","Avenue J","Avenue M","Kings Hwy (Q)",
   "Avenue U (Q)","Neck Rd","Sheepshead Bay","Brighton Beach","Ocean Pkwy","West 8 St-NY Aquarium","Coney Island-Stillwell Av"],
 "R": ["Forest Hills-71 Av","67 Av","63 Dr-Rego Park","Woodhaven Blvd (R)","Grand Av-Newtown","Elmhurst Av",
   "Jackson Hts-Roosevelt Av","65 St","Northern Blvd","46 St","Steinway St","36 St (Queens)","Queens Plaza",
   "Lexington Av/59 St","5 Av/59 St","57 St-7 Av","49 St","Times Sq-42 St","34 St-Herald Sq","28 St (N-R-W)",
   "23 St (N-R-W)","14 St-Union Sq","8 St-NYU","Prince St","Canal St (N-Q-R-W)","City Hall (N-R-W)","Cortlandt St",
   "Rector St (N-R-W)","Whitehall St-South Ferry","Court St","Jay St-MetroTech","DeKalb Av","Atlantic Av-Barclays Ctr",
   "Union St","4 Av-9 St","Prospect Av (R)","25 St","36 St (D-N-R)","45 St","53 St","59 St (N-R)","Bay Ridge Av",
   "77 St","86 St (R)","Bay Ridge-95 St"],
 "W": ["Astoria-Ditmars Blvd","Astoria Blvd","30 Av","Broadway (N-W)","36 Av","39 Av-Dutch Kills","Queensboro Plaza",
   "Lexington Av/59 St","5 Av/59 St","57 St-7 Av","49 St","Times Sq-42 St","34 St-Herald Sq","28 St (N-R-W)",
   "23 St (N-R-W)","14 St-Union Sq","8 St-NYU","Prince St","Canal St (N-Q-R-W)","City Hall (N-R-W)","Cortlandt St",
   "Rector St (N-R-W)","Whitehall St-South Ferry"],
 "Z": ["Jamaica Center-Parsons/Archer","Sutphin Blvd-Archer Av","Broadway Junction","Marcy Av",
   "Delancey St-Essex St","Canal St (J-Z)","Chambers St (J-Z)","Fulton St","Broad St"],
}


def build_graph(lines=None):
    import networkx as nx
    lines = lines or LINES
    G = nx.Graph()
    for line, seq in lines.items():
        for st in seq:
            if st not in G:
                G.add_node(st, lines=set())
            G.nodes[st]["lines"].add(line)
        for a, c in zip(seq, seq[1:]):
            if a == c:
                continue
            if G.has_edge(a, c):
                G[a][c]["lines"].add(line)
            else:
                G.add_edge(a, c, lines={line})
    return G

if __name__ == "__main__":
    import networkx as nx
    G = build_graph()
    print(f"NYC: N={G.number_of_nodes()} M={G.number_of_edges()} "
          f"<k>={2*G.number_of_edges()/G.number_of_nodes():.3f} conexo={nx.is_connected(G)}")
    if not nx.is_connected(G):
        comps=sorted(nx.connected_components(G),key=len,reverse=True)
        print(f"  componentes={len(comps)} maiores={[len(c) for c in comps[:5]]}")
