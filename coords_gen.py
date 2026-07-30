# -*- coding: utf-8 -*-
"""Gera coordenadas geográficas APROXIMADAS para Londres e NY (âncoras reais +
interpolação ao longo das linhas), e monta networks.json com as 3 malhas."""
import json
import rede_london as LN, rede_nyc as NY

def interp(lines, anchors):
    coord = dict(anchors)
    for line, seq in lines.items():
        known=[i for i,s in enumerate(seq) if s in coord]
        if not known: continue
        for i,s in enumerate(seq):
            if s in coord: continue
            left=max([k for k in known if k<i],default=None)
            right=min([k for k in known if k>i],default=None)
            if left is not None and right is not None:
                t=(i-left)/(right-left)
                la=coord[seq[left]][0]+(coord[seq[right]][0]-coord[seq[left]][0])*t
                lo=coord[seq[left]][1]+(coord[seq[right]][1]-coord[seq[left]][1])*t
            elif right is not None:
                la,lo=coord[seq[right]]; la+=0.002*(right-i); lo+=0.002*(right-i)
            else:
                la,lo=coord[seq[left]]; la-=0.002*(i-left); lo-=0.002*(i-left)
            coord[s]=(round(la,5),round(lo,5))
    return coord

LN_ANCHORS={
 "Harrow & Wealdstone":(51.592,-0.335),"Queen's Park":(51.534,-0.205),"Paddington":(51.516,-0.176),
 "Baker Street":(51.522,-0.157),"Oxford Circus":(51.515,-0.142),"Charing Cross":(51.508,-0.123),
 "Waterloo":(51.503,-0.114),"Elephant & Castle":(51.494,-0.100),"Epping":(51.694,0.114),
 "Woodford":(51.607,0.031),"Leytonstone":(51.568,0.008),"Stratford":(51.541,-0.003),
 "Liverpool Street":(51.518,-0.082),"Bank":(51.513,-0.089),"West Ruislip":(51.570,-0.437),
 "North Acton":(51.517,-0.259),"Ealing Broadway":(51.515,-0.301),"Newbury Park":(51.575,0.090),
 "Edgware Road (Circle)":(51.520,-0.170),"Victoria":(51.496,-0.144),"Westminster":(51.501,-0.125),
 "Aldgate":(51.514,-0.076),"Embankment":(51.507,-0.122),"Tower Hill":(51.510,-0.076),
 "King's Cross St. Pancras":(51.530,-0.124),"Farringdon":(51.520,-0.105),"Moorgate":(51.518,-0.089),
 "Upminster":(51.559,0.251),"Barking":(51.539,0.081),"West Ham":(51.528,0.005),"Mile End":(51.525,-0.033),
 "Whitechapel":(51.519,-0.060),"Richmond":(51.463,-0.301),"Turnham Green":(51.495,-0.255),
 "Earl's Court":(51.492,-0.194),"South Kensington":(51.494,-0.174),"Gloucester Road":(51.494,-0.183),
 "Wimbledon":(51.421,-0.206),"Putney Bridge":(51.468,-0.209),"Hammersmith (District)":(51.492,-0.223),
 "High Street Kensington":(51.501,-0.192),"Notting Hill Gate":(51.509,-0.196),"Bayswater":(51.512,-0.188),
 "Hammersmith (H&C)":(51.493,-0.225),"Stanmore":(51.619,-0.303),"Wembley Park":(51.563,-0.279),
 "Finchley Road":(51.547,-0.180),"Green Park":(51.507,-0.143),"London Bridge":(51.505,-0.086),
 "Canada Water":(51.498,-0.050),"Canary Wharf":(51.503,-0.019),"North Greenwich":(51.500,0.004),
 "Canning Town":(51.514,0.008),"Amersham":(51.674,-0.607),"Harrow-on-the-Hill":(51.579,-0.337),
 "Uxbridge":(51.546,-0.478),"Rayners Lane":(51.575,-0.371),"Watford":(51.657,-0.417),"Moor Park":(51.630,-0.432),
 "High Barnet":(51.650,-0.194),"Camden Town":(51.539,-0.143),"Euston":(51.528,-0.133),"Kennington":(51.488,-0.106),
 "Morden":(51.402,-0.195),"Mornington Crescent":(51.534,-0.139),"Mill Hill East":(51.608,-0.209),
 "Battersea Power Station":(51.480,-0.144),"Cockfosters":(51.651,-0.149),"Finsbury Park":(51.564,-0.106),
 "Holborn":(51.517,-0.120),"Leicester Square":(51.511,-0.128),"Piccadilly Circus":(51.510,-0.134),
 "Acton Town":(51.503,-0.280),"Heathrow Terminals 2 & 3":(51.471,-0.454),"Heathrow Terminal 5":(51.472,-0.488),
 "Walthamstow Central":(51.583,-0.020),"Seven Sisters":(51.583,-0.075),"Highbury & Islington":(51.546,-0.104),
 "Warren Street":(51.524,-0.138),"Brixton":(51.463,-0.115),"Vauxhall":(51.486,-0.123),"Stockwell":(51.472,-0.123),
}
NY_ANCHORS={
 "Van Cortlandt Park-242 St":(40.889,-73.899),"South Ferry":(40.702,-74.014),"Times Sq-42 St":(40.755,-73.987),
 "Wakefield-241 St":(40.903,-73.851),"Flatbush Av-Brooklyn College":(40.632,-73.948),"Harlem-148 St":(40.824,-73.936),
 "New Lots Av":(40.666,-73.884),"Woodlawn":(40.886,-73.879),"Crown Hts-Utica Av":(40.669,-73.933),
 "Eastchester-Dyre Av":(40.888,-73.831),"Pelham Bay Park":(40.852,-73.828),"Brooklyn Bridge-City Hall":(40.713,-74.004),
 "Flushing-Main St":(40.760,-73.830),"34 St-Hudson Yards":(40.756,-74.001),"Inwood-207 St":(40.868,-73.919),
 "Ozone Park-Lefferts Blvd":(40.686,-73.826),"Euclid Av":(40.675,-73.872),"Jamaica Center-Parsons/Archer":(40.702,-73.801),
 "World Trade Center":(40.712,-74.011),"Norwood-205 St":(40.875,-73.879),"Coney Island-Stillwell Av":(40.577,-73.981),
 "Jamaica-179 St":(40.712,-73.783),"Middle Village-Metropolitan Av":(40.712,-73.889),"Church Av (F-G)":(40.644,-73.980),
 "Court Sq (G)":(40.746,-73.943),"Canarsie-Rockaway Pkwy":(40.646,-73.902),"8 Av (L)":(40.740,-74.003),
 "Astoria-Ditmars Blvd":(40.775,-73.912),"Bay Ridge-95 St":(40.616,-74.031),"Forest Hills-71 Av":(40.722,-73.845),
 "Grand Central-42 St":(40.752,-73.977),"14 St-Union Sq":(40.735,-73.990),"Atlantic Av-Barclays Ctr":(40.684,-73.978),
 "Broadway Junction":(40.679,-73.905),"125 St (4-5-6)":(40.804,-73.937),"161 St-Yankee Stadium":(40.828,-73.926),
 "149 St-Grand Concourse":(40.818,-73.927),"96 St":(40.794,-73.972),"14 St (1-2-3)":(40.738,-74.000),
 "Chambers St (1-2-3)":(40.715,-74.009),"Fulton St":(40.710,-74.008),"Queensboro Plaza":(40.750,-73.940),
 "34 St-Herald Sq":(40.750,-73.988),"W 4 St-Wash Sq":(40.732,-74.000),"59 St-Columbus Circle":(40.768,-73.982),
 "145 St (A-C-B-D)":(40.824,-73.944),"Jay St-MetroTech":(40.692,-73.987),"DeKalb Av":(40.690,-73.982),
 "36 St (D-N-R)":(40.655,-74.004),"Franklin Av (2-3-4-5)":(40.671,-73.958),"Delancey St-Essex St":(40.718,-73.988),
 "Marcy Av":(40.708,-73.958),"Myrtle-Wyckoff Avs":(40.699,-73.912),"Hoyt-Schermerhorn Sts":(40.688,-73.985),
 "Bedford Park Blvd (B-D)":(40.873,-73.887),"161 St-Yankee Stadium":(40.828,-73.926),"Broad St":(40.706,-74.011),
 "Whitehall St-South Ferry":(40.703,-74.013),"Lexington Av/59 St":(40.762,-73.967),"47-50 Sts-Rockefeller Ctr":(40.759,-73.981),
}

def build(lines, anchors, colors):
    coord=interp(lines, anchors)
    seen=set(); stations=[]
    for line,seq in lines.items():
        for s in seq:
            if s in seen: continue
            seen.add(s)
            ls=[l for l,sq in lines.items() if s in sq]
            # cor da primeira linha base
            base0=ls[0].split("-")[0]
            stations.append({"id":s,"lat":coord[s][0],"lon":coord[s][1],
                             "lines":sorted(set(l.split('-')[0] for l in ls)),
                             "color":colors.get(base0,"#35D0D6"),"hub":len(set(l.split('-')[0] for l in ls))>1})
    edges=[]
    for line,seq in lines.items():
        b=line.split("-")[0]
        for a,c in zip(seq,seq[1:]):
            if a!=c: edges.append([a,c,colors.get(b,"#888")])
    return {"stations":stations,"edges":edges,"line_colors":colors}

ln=build(LN.LINES, LN_ANCHORS, LN.LINE_COLORS)
ny=build(NY.LINES, NY_ANCHORS, NY.LINE_COLORS)
sp=json.load(open("coords_sp.json"))
out={"SP":{"center":[-23.55,-46.63],"data":sp},
     "LN":{"center":[51.51,-0.12],"data":ln},
     "NY":{"center":[40.73,-73.97],"data":ny}}
json.dump(out, open("networks.json","w"), ensure_ascii=False, separators=(",",":"))
for k,v in [("SP",sp),("LN",ln),("NY",ny)]:
    las=[s['lat'] for s in v['stations']]; los=[s['lon'] for s in v['stations']]
    print(f"{k}: {len(v['stations'])} est, lat[{min(las):.2f},{max(las):.2f}] lon[{min(los):.2f},{max(los):.2f}]")
print("bytes", len(open('networks.json').read()))
