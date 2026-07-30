# -*- coding: utf-8 -*-
"""Malha do London Underground modelada a partir do mapa oficial (11 linhas).
Mesmo método do rede_sp.py: espaço L, estações consecutivas = arestas,
baldeações = vértice único por nome canônico. Ramais modelados como sequências
que compartilham estações. Validar N/M contra literatura (~270 estações)."""

LINE_COLORS = {
 "Bakerloo":"#B36305","Central":"#E32017","Circle":"#FFD300","District":"#00782A",
 "Hammersmith & City":"#F3A9BB","Jubilee":"#A0A5A9","Metropolitan":"#9B0056",
 "Northern":"#000000","Piccadilly":"#003688","Victoria":"#0098D4","Waterloo & City":"#95CDBA",
}

LINES = {
 "Bakerloo": ["Harrow & Wealdstone","Kenton","South Kenton","North Wembley","Wembley Central",
   "Stonebridge Park","Harlesden","Willesden Junction","Kensal Green","Queen's Park","Kilburn Park",
   "Maida Vale","Warwick Avenue","Paddington","Edgware Road (Bakerloo)","Marylebone","Baker Street",
   "Regent's Park","Oxford Circus","Piccadilly Circus","Charing Cross","Embankment","Waterloo",
   "Lambeth North","Elephant & Castle"],

 "Central-main": ["Epping","Theydon Bois","Debden","Loughton","Buckhurst Hill","Woodford",
   "South Woodford","Snaresbrook","Leytonstone","Leyton","Stratford","Mile End","Bethnal Green",
   "Liverpool Street","Bank","St. Paul's","Chancery Lane","Holborn","Tottenham Court Road",
   "Oxford Circus","Bond Street","Marble Arch","Lancaster Gate","Queensway","Notting Hill Gate",
   "Holland Park","Shepherd's Bush","White City","East Acton","North Acton","Hanger Lane","Perivale",
   "Greenford","Northolt","South Ruislip","Ruislip Gardens","West Ruislip"],
 "Central-hainault": ["Woodford","Roding Valley","Chigwell","Grange Hill","Hainault","Fairlop",
   "Barkingside","Newbury Park","Gants Hill","Redbridge","Wanstead","Leytonstone"],
 "Central-ealing": ["North Acton","West Acton","Ealing Broadway"],

 "Circle": ["Edgware Road (Circle)","Paddington","Bayswater","Notting Hill Gate","High Street Kensington",
   "Gloucester Road","South Kensington","Sloane Square","Victoria","St. James's Park","Westminster",
   "Embankment","Temple","Blackfriars","Mansion House","Cannon Street","Monument","Tower Hill","Aldgate",
   "Liverpool Street","Moorgate","Barbican","Farringdon","King's Cross St. Pancras","Euston Square",
   "Great Portland Street","Baker Street","Great Portland Street"],

 "District-main": ["Upminster","Upminster Bridge","Hornchurch","Elm Park","Dagenham East",
   "Dagenham Heathway","Becontree","Upney","Barking","East Ham","Upton Park","Plaistow","West Ham",
   "Bromley-by-Bow","Bow Road","Mile End","Stepney Green","Whitechapel","Aldgate East","Tower Hill",
   "Monument","Cannon Street","Mansion House","Blackfriars","Temple","Embankment","Westminster",
   "St. James's Park","Victoria","Sloane Square","South Kensington","Gloucester Road","Earl's Court",
   "West Kensington","Barons Court","Hammersmith (District)","Ravenscourt Park","Stamford Brook",
   "Turnham Green","Gunnersbury","Kew Gardens","Richmond"],
 "District-ealing": ["Earl's Court","West Brompton","Fulham Broadway","Parsons Green","Putney Bridge",
   "East Putney","Southfields","Wimbledon Park","Wimbledon"],
 "District-edgware": ["Earl's Court","High Street Kensington","Notting Hill Gate","Bayswater",
   "Paddington","Edgware Road (Circle)"],

 "Hammersmith & City": ["Hammersmith (H&C)","Goldhawk Road","Shepherd's Bush Market","Wood Lane",
   "Latimer Road","Ladbroke Grove","Westbourne Park","Royal Oak","Paddington","Edgware Road (Circle)",
   "Baker Street","Great Portland Street","Euston Square","King's Cross St. Pancras","Farringdon",
   "Barbican","Moorgate","Liverpool Street","Aldgate East","Whitechapel","Stepney Green","Mile End",
   "Bow Road","Bromley-by-Bow","West Ham","Plaistow","Upton Park","East Ham","Barking"],

 "Jubilee": ["Stanmore","Canons Park","Queensbury","Kingsbury","Wembley Park","Neasden","Dollis Hill",
   "Willesden Green","Kilburn","West Hampstead","Finchley Road","Swiss Cottage","St. John's Wood",
   "Baker Street","Bond Street","Green Park","Westminster","Waterloo","Southwark","London Bridge",
   "Bermondsey","Canada Water","Canary Wharf","North Greenwich","Canning Town","West Ham","Stratford"],

 "Metropolitan-main": ["Amersham","Chalfont & Latimer","Chorleywood","Rickmansworth","Moor Park",
   "Northwood","Northwood Hills","Pinner","North Harrow","Harrow-on-the-Hill","Northwick Park",
   "Preston Road","Wembley Park","Finchley Road","Baker Street","Great Portland Street","Euston Square",
   "King's Cross St. Pancras","Farringdon","Barbican","Moorgate","Liverpool Street","Aldgate"],
 "Metropolitan-uxbridge": ["Uxbridge","Hillingdon","Ickenham","Ruislip","Ruislip Manor","Eastcote",
   "Rayners Lane","West Harrow","Harrow-on-the-Hill"],
 "Metropolitan-watford": ["Watford","Croxley","Moor Park"],

 "Northern-bank": ["High Barnet","Totteridge & Whetstone","Woodside Park","West Finchley","Finchley Central",
   "East Finchley","Highgate","Archway","Tufnell Park","Kentish Town","Camden Town","Euston","King's Cross St. Pancras",
   "Angel","Old Street","Moorgate","Bank","London Bridge","Borough","Elephant & Castle","Kennington",
   "Oval","Stockwell","Clapham North","Clapham Common","Clapham South","Balham","Tooting Bec",
   "Tooting Broadway","Colliers Wood","South Wimbledon","Morden"],
 "Northern-charing": ["Camden Town","Mornington Crescent","Euston","Warren Street","Goodge Street",
   "Tottenham Court Road","Leicester Square","Charing Cross","Embankment","Waterloo","Kennington"],
 "Northern-mill": ["Finchley Central","Mill Hill East"],
 "Northern-battersea": ["Kennington","Nine Elms","Battersea Power Station"],

 "Piccadilly-main": ["Cockfosters","Oakwood","Southgate","Arnos Grove","Bounds Green","Wood Green",
   "Turnpike Lane","Manor House","Finsbury Park","Arsenal","Holloway Road","Caledonian Road",
   "King's Cross St. Pancras","Russell Square","Holborn","Covent Garden","Leicester Square",
   "Piccadilly Circus","Green Park","Hyde Park Corner","Knightsbridge","South Kensington","Gloucester Road",
   "Earl's Court","Barons Court","Hammersmith (District)","Acton Town","South Ealing","Northfields",
   "Boston Manor","Osterley","Hounslow East","Hounslow Central","Hounslow West","Hatton Cross",
   "Heathrow Terminals 2 & 3","Heathrow Terminal 5"],
 "Piccadilly-uxbridge": ["Acton Town","Ealing Common","North Ealing","Park Royal","Alperton","Sudbury Town",
   "Sudbury Hill","South Harrow","Rayners Lane"],

 "Victoria": ["Walthamstow Central","Blackhorse Road","Tottenham Hale","Seven Sisters","Finsbury Park",
   "Highbury & Islington","King's Cross St. Pancras","Euston","Warren Street","Oxford Circus","Green Park",
   "Victoria","Pimlico","Vauxhall","Stockwell","Brixton"],

 "Waterloo & City": ["Waterloo","Bank"],
}


def build_graph(lines=None):
    import networkx as nx
    lines = lines or LINES
    G = nx.Graph()
    # nome de linha "base" (antes do hífen de ramal) para cor/serviço
    def base(l): return l.split("-")[0]
    for line, seq in lines.items():
        b = base(line)
        for st in seq:
            if st not in G:
                G.add_node(st, lines=set())
            G.nodes[st]["lines"].add(b)
        for a, c in zip(seq, seq[1:]):
            if a == c:
                continue
            if G.has_edge(a, c):
                G[a][c]["lines"].add(b)
            else:
                G.add_edge(a, c, lines={b})
    return G

if __name__ == "__main__":
    import networkx as nx
    G = build_graph()
    print(f"Londres: N={G.number_of_nodes()} M={G.number_of_edges()} "
          f"<k>={2*G.number_of_edges()/G.number_of_nodes():.3f} conexo={nx.is_connected(G)}")
