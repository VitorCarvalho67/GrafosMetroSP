const pptxgen = require("pptxgenjs");
const p = new pptxgen();
p.layout = "LAYOUT_WIDE";                // 13.33 x 7.5
const W = 13.33, H = 7.5;

const C = {bg:"0A1024", card:"141B2E", card2:"1B2540", ink:"FFFFFF", mut:"9AA6C0",
  faint:"5E6B8A", teal:"35D0D6", orange:"EB6834", blue:"2A78D6", green:"1BAF7A",
  red:"E34948", gold:"FFCF7A", white:"FCFCFB"};
const F = "Calibri";
const IMG = "/tmp/work/slides_img/";

function bg(s){ s.background = {color:C.bg}; }
function eyebrow(s,t){ s.addText(t,{x:0.6,y:0.42,w:9,h:0.3,fontFace:F,fontSize:12,
  color:C.teal,charSpacing:3,bold:true}); }
function title(s,t,y=0.72){ s.addText(t,{x:0.6,y:y,w:12.1,h:0.9,fontFace:F,fontSize:32,
  bold:true,color:C.ink}); }
function pageno(s,n){ s.addText(String(n),{x:12.7,y:7.02,w:0.5,h:0.3,fontFace:F,
  fontSize:10,color:C.faint,align:"right"}); }
function card(s,x,y,w,h,fill){ s.addShape(p.ShapeType.roundRect,{x,y,w,h,rectRadius:0.12,
  fill:{color:fill||C.card}, line:{color:"2A3550",width:1}}); }
function imgCard(s,path,x,y,w,h){ // white rounded frame + contained image
  s.addShape(p.ShapeType.roundRect,{x:x-0.08,y:y-0.08,w:w+0.16,h:h+0.16,rectRadius:0.08,
    fill:{color:C.white}, line:{color:"2A3550",width:1}, shadow:{type:"outer",color:"000000",opacity:0.35,blur:8,offset:3,angle:90}});
  s.addImage({path,x,y,w,h,sizing:{type:"contain",w,h}});
}
function dot(s,x,y,col,d=0.14){ s.addShape(p.ShapeType.ellipse,{x,y,w:d,h:d,fill:{color:col},line:{color:col,width:0}}); }

/* ---------- 1. TÍTULO ---------- */
let s = p.addSlide(); bg(s);
s.addImage({path:IMG+"hero_globe.png",x:6.7,y:0,w:6.63,h:7.5,sizing:{type:"cover",w:6.63,h:7.5}});
// leve véu à esquerda para contraste do texto
s.addShape(p.ShapeType.rect,{x:0,y:0,w:8.2,h:7.5,fill:{color:C.bg,transparency:12},line:{width:0}});
s.addText("TEORIA DOS GRAFOS · UFABC",{x:0.7,y:1.5,w:7,h:0.3,fontFace:F,fontSize:13,color:C.teal,charSpacing:3,bold:true});
s.addText("Topologia da Malha\nMetroferroviária de São Paulo",{x:0.7,y:2.0,w:7.4,h:1.9,fontFace:F,fontSize:40,bold:true,color:C.ink,lineSpacingMultiple:1.02});
s.addText("Uma análise via Teoria dos Grafos — e a comparação com Londres e Nova York",
  {x:0.7,y:3.95,w:6.9,h:0.7,fontFace:F,fontSize:16,color:C.mut});
s.addText([
  {text:"Vitor Eduardo Silva de Carvalho   ·   Diego Naoki Sato Hanashiro",options:{breakLine:true}},
  {text:"João Vitor Ribeiro Pereira   ·   Joaquim Argolo Valente de Azambuja",options:{}},
],{x:0.7,y:5.2,w:7.2,h:0.8,fontFace:F,fontSize:13.5,color:C.ink,lineSpacingMultiple:1.3});
s.addText("Comunicação e Redes · BC&T · UFABC · 2026.Q2",{x:0.7,y:6.5,w:7,h:0.3,fontFace:F,fontSize:12,color:C.faint});
s.addNotes("Apresentação do projeto de Comunicação e Redes. Modelamos a malha metroferroviária de São Paulo como grafo e a comparamos com Londres e Nova York. ~15 min.");
pageno(s,1);

/* ---------- 2. CONTEXTO & OBJETIVOS ---------- */
s = p.addSlide(); bg(s); eyebrow(s,"CONTEXTO"); title(s,"Por que estudar a malha como um grafo?");
const stats=[["393 km","extensão integrada"],["15","linhas (Metrô + CPTM)"],["185","estações em 2026"]];
stats.forEach((st,i)=>{const x=0.6+i*2.55; card(s,x,1.75,2.35,1.55);
  s.addText(st[0],{x:x,y:1.95,w:2.35,h:0.75,fontFace:F,fontSize:34,bold:true,color:C.teal,align:"center"});
  s.addText(st[1],{x:x,y:2.72,w:2.35,h:0.45,fontFace:F,fontSize:12.5,color:C.mut,align:"center"});});
s.addText("A maior rede sobre trilhos do Brasil — mas raramente estudada sob a ótica formal da teoria dos grafos. Modelá-la revela onde estão os gargalos e o que mais a fortaleceria.",
  {x:0.6,y:3.5,w:6.9,h:1.0,fontFace:F,fontSize:15,color:C.ink,lineSpacingMultiple:1.2});
s.addText("Objetivos",{x:0.6,y:4.55,w:6,h:0.4,fontFace:F,fontSize:18,bold:true,color:C.orange});
const objs=[["1","Modelar a malha como grafo e caracterizar sua topologia"],
  ["2","Identificar estações críticas e medir a robustez"],
  ["3","Comparar São Paulo com Londres e Nova York"],
  ["4","Avaliar o impacto da Linha 6 e de linhas futuras"]];
objs.forEach((o,i)=>{const y=5.05+i*0.52;
  s.addShape(p.ShapeType.ellipse,{x:0.65,y:y,w:0.34,h:0.34,fill:{color:C.teal},line:{width:0}});
  s.addText(o[0],{x:0.65,y:y,w:0.34,h:0.34,fontFace:F,fontSize:15,bold:true,color:C.bg,align:"center",valign:"middle",margin:0});
  s.addText(o[1],{x:1.12,y:y-0.03,w:6.4,h:0.4,fontFace:F,fontSize:14,color:C.ink,valign:"middle"});});
s.addImage({path:IMG+"hero_globe.png",x:8.4,y:1.75,w:4.5,h:4.5,sizing:{type:"cover",w:4.5,h:4.5}});
s.addText("As três malhas do estudo no globo (SP, Londres, NY).",{x:8.4,y:6.32,w:4.5,h:0.35,fontFace:F,fontSize:11,italic:true,color:C.faint,align:"center"});
pageno(s,2);

/* ---------- 3. MODELAGEM ---------- */
s = p.addSlide(); bg(s); eyebrow(s,"MODELAGEM"); title(s,"Da rede ao grafo");
s.addText([
  {text:"Espaço L — infraestrutura",options:{bold:true,color:C.teal,fontSize:16,breakLine:true,paraSpaceAfter:4}},
  {text:"Vértice = estação · Aresta = trecho direto entre estações consecutivas. Estações de baldeação viram um único vértice de grau maior.",options:{fontSize:13.5,color:C.ink,breakLine:true,paraSpaceAfter:14}},
  {text:"Espaço P — experiência de viagem",options:{bold:true,color:C.orange,fontSize:16,breakLine:true,paraSpaceAfter:4}},
  {text:"Duas estações são vizinhas se estão na mesma linha; a distância conta baldeações.",options:{fontSize:13.5,color:C.ink}},
],{x:0.6,y:1.7,w:6.3,h:3.0,fontFace:F,valign:"top",lineSpacingMultiple:1.1});
const mk=[["185","estações (N)"],["198","trechos (M)"],["2,14","grau médio ⟨k⟩"],["14,0","caminho médio L"]];
mk.forEach((m,i)=>{const x=0.6+(i%2)*3.15, y=4.55+Math.floor(i/2)*1.25; card(s,x,y,2.95,1.05);
  s.addText(m[0],{x:x+0.15,y:y+0.12,w:2.65,h:0.55,fontFace:F,fontSize:26,bold:true,color:C.ink});
  s.addText(m[1],{x:x+0.15,y:y+0.66,w:2.65,h:0.32,fontFace:F,fontSize:12,color:C.mut});});
imgCard(s,IMG+"hero_redes.png",7.35,1.9,5.4,2.7);
s.addText("Rede modelada — São Paulo, Londres e Nova York em suas coordenadas geográficas.",
  {x:7.35,y:4.75,w:5.4,h:0.6,fontFace:F,fontSize:11.5,italic:true,color:C.faint,align:"center"});
pageno(s,3);

/* ---------- 4. MÉTRICAS ---------- */
s = p.addSlide(); bg(s); eyebrow(s,"METODOLOGIA"); title(s,"O que medimos");
const mets=[["Grau & eficiência",C.teal,"Distribuição de grau P(k) e eficiência global E_glob."],
  ["Centralidade",C.orange,"Intermediação e proximidade — quais estações são mais centrais."],
  ["Comunidades",C.green,"Modularidade Q (Louvain) — regiões da malha."],
  ["Mundo pequeno",C.blue,"Índice σ vs. grafos aleatórios equivalentes."],
  ["Robustez",C.red,"Falhas aleatórias vs. ataques dirigidos S(f)."],
  ["Redundância r_T",C.gold,"Índice de Derrible & Kennedy = ciclos por estação."]];
mets.forEach((m,i)=>{const x=0.6+(i%3)*4.13, y=1.85+Math.floor(i/3)*2.35; card(s,x,y,3.9,2.05);
  s.addShape(p.ShapeType.ellipse,{x:x+0.25,y:y+0.28,w:0.5,h:0.5,fill:{color:m[1]},line:{width:0}});
  s.addText(m[0],{x:x+0.95,y:y+0.28,w:2.8,h:0.5,fontFace:F,fontSize:15.5,bold:true,color:C.ink,valign:"middle"});
  s.addText(m[2],{x:x+0.28,y:y+0.95,w:3.35,h:0.95,fontFace:F,fontSize:12.5,color:C.mut,lineSpacingMultiple:1.1});});
s.addText("Tudo calculado com NetworkX, de forma reprodutível (código e dados versionados).",
  {x:0.6,y:6.7,w:12,h:0.35,fontFace:F,fontSize:12,italic:true,color:C.faint});
pageno(s,4);

/* ---------- 5. ESTRUTURA & HUBS ---------- */
s = p.addSlide(); bg(s); eyebrow(s,"RESULTADO · ESTRUTURA"); title(s,"Radial, dominada por Luz e Brás");
imgCard(s,IMG+"fig_hubs-1.png",6.95,1.75,5.9,3.95);
const pts=[["Não é livre de escala","79% das estações têm grau 2; sem cauda longa."],
  ["Não é mundo pequeno (σ = 0,51)","no espaço L — é uma rede espacial quase-planar."],
  ["Luz e Brás concentram os fluxos","intermediação ≈ 0,44: quase metade dos caminhos."],
  ["Pontos de articulação","estações de grau 2 (Juventus-Mooca) que isolam ramais."]];
pts.forEach((pt,i)=>{const y=1.85+i*1.15;
  dot(s,0.65,y+0.05,C.orange);
  s.addText(pt[0],{x:0.95,y:y-0.1,w:5.7,h:0.4,fontFace:F,fontSize:15,bold:true,color:C.ink});
  s.addText(pt[1],{x:0.95,y:y+0.28,w:5.7,h:0.55,fontFace:F,fontSize:12.5,color:C.mut,lineSpacingMultiple:1.05});});
s.addNotes("A malha é fortemente radial: praticamente todo trajeto entre regiões passa pelo centro, o que transforma Luz e Brás em gargalos. Não é small-world nem scale-free no espaço L.");
pageno(s,5);

/* ---------- 6. ROBUSTEZ ---------- */
s = p.addSlide(); bg(s); eyebrow(s,"RESULTADO · ROBUSTEZ"); title(s,"Frágil a ataques dirigidos");
imgCard(s,IMG+"fig_robustez-1.png",6.85,1.9,6.0,3.7);
card(s,0.6,1.9,5.9,1.5,C.card);
s.addText("2%",{x:0.85,y:2.0,w:1.5,h:1.2,fontFace:F,fontSize:52,bold:true,color:C.red,align:"center",valign:"middle"});
s.addText("das estações removidas por ataque (≈4 estações centrais) já derrubam a maior componente de 100% para 57%.",
  {x:2.4,y:2.05,w:3.9,h:1.2,fontFace:F,fontSize:13.5,color:C.ink,valign:"middle",lineSpacingMultiple:1.1});
s.addText([
  {text:"Falha aleatória: degradação gradual (a 10% removido, ainda 56%).",options:{bullet:{code:"2022",indent:16},breakLine:true,paraSpaceAfter:10}},
  {text:"Ataque dirigido: colapso abrupto — a 4%, a maior componente cai a 19%.",options:{bullet:{code:"2022",indent:16},breakLine:true,paraSpaceAfter:10}},
  {text:"Robustez integrada: 0,15 (falha) vs. 0,04 (ataque).",options:{bullet:{code:"2022",indent:16}}},
],{x:0.65,y:3.6,w:5.95,h:2.2,fontFace:F,fontSize:14,color:C.ink,lineSpacingMultiple:1.1});
s.addNotes("A rede resiste a falhas difusas, mas é muito vulnerável à perda simultânea de poucas estações de alta centralidade — implicação direta para planos de contingência.");
pageno(s,6);

/* ---------- 7. REGIÕES ---------- */
s = p.addSlide(); bg(s); eyebrow(s,"RESULTADO · TERRITÓRIO"); title(s,"Eficiência não é homogênea");
imgCard(s,IMG+"fig_regioes-1.png",7.0,1.75,5.85,4.4);
s.addText("15",{x:0.6,y:1.85,w:2.4,h:0.9,fontFace:F,fontSize:40,bold:true,color:C.green});
s.addText("comunidades (Louvain), Q = 0,81 — com claro sentido geográfico.",{x:0.6,y:2.7,w:6.0,h:0.7,fontFace:F,fontSize:14,color:C.ink,lineSpacingMultiple:1.1});
s.addText("≈ 2×",{x:0.6,y:3.6,w:2.4,h:0.9,fontFace:F,fontSize:40,bold:true,color:C.orange});
s.addText("O centro expandido (Luz, Brás, República, Barra Funda) é cerca de duas vezes mais acessível que a periferia (sul, oeste, leste).",
  {x:0.6,y:4.45,w:6.1,h:1.2,fontFace:F,fontSize:14,color:C.ink,lineSpacingMultiple:1.15});
s.addNotes("A modularidade recupera regiões geográficas e mostra um gradiente de acessibilidade do centro à periferia — a conhecida concentração radial, quantificada.");
pageno(s,7);

/* ---------- 8. COMPARAÇÃO INTERNACIONAL ---------- */
s = p.addSlide(); bg(s); eyebrow(s,"COMPARAÇÃO"); title(s,"São Paulo × Londres × Nova York");
imgCard(s,IMG+"hero_redes.png",0.6,1.75,7.2,3.6);
const sw=[["São Paulo","0,51",C.orange],["Londres","1,86",C.blue],["Nova York","3,14",C.green]];
sw.forEach((c,i)=>{const y=1.8+i*1.15; card(s,8.05,y,4.85,1.0,C.card);
  s.addText(c[0],{x:8.25,y:y,w:2.4,h:1.0,fontFace:F,fontSize:15,bold:true,color:C.ink,valign:"middle"});
  s.addText("σ = "+c[1],{x:10.5,y:y,w:2.25,h:1.0,fontFace:F,fontSize:22,bold:true,color:c[2],align:"right",valign:"middle"});});
s.addText("São Paulo é a única das três com σ < 1 — a única que não é uma rede de mundo pequeno. É a mais esparsa, radial e menos redundante (rT 0,08, junto de Berlim; longe de Paris e Tóquio).",
  {x:0.6,y:5.55,w:12.2,h:1.2,fontFace:F,fontSize:14,color:C.ink,lineSpacingMultiple:1.15});
s.addNotes("Modelamos Londres e NY do mesmo modo. Validação: nosso rT bate com Derrible para SP e Londres. NY foi modelada por serviços (inflaciona redundância). Achado: SP é a única fora do regime small-world.");
pageno(s,8);

/* ---------- 9. LINHA 6 & LINHAS FUTURAS ---------- */
s = p.addSlide(); bg(s); eyebrow(s,"EXPANSÃO"); title(s,"O que mais ajudaria a malha?");
card(s,0.6,1.8,6.0,2.2,C.card);
s.addText("Linha 6-Laranja (radial)",{x:0.85,y:2.0,w:5.5,h:0.4,fontFace:F,fontSize:16,bold:true,color:C.orange});
s.addText("+0,6%",{x:0.85,y:2.45,w:5.5,h:0.9,fontFace:F,fontSize:44,bold:true,color:C.ink});
s.addText("de eficiência global — ganho modesto; seu valor é de cobertura (633 mil pax/dia).",{x:0.85,y:3.35,w:5.5,h:0.55,fontFace:F,fontSize:12.5,color:C.mut,lineSpacingMultiple:1.05});
card(s,6.75,1.8,6.0,2.2,C.card2);
s.addText("Linha 20-Rosa (orbital)",{x:7.0,y:2.0,w:5.5,h:0.4,fontFace:F,fontSize:16,bold:true,color:C.teal});
s.addText("+2,1%",{x:7.0,y:2.45,w:5.5,h:0.9,fontFace:F,fontSize:44,bold:true,color:C.ink});
s.addText("mais que o triplo — cria atalhos entre eixos que hoje só se ligam pelo centro.",{x:7.0,y:3.35,w:5.5,h:0.55,fontFace:F,fontSize:12.5,color:C.mut,lineSpacingMultiple:1.05});
card(s,0.6,4.25,12.15,2.05,"14203A");
s.addText("Achado central",{x:0.9,y:4.45,w:11.5,h:0.4,fontFace:F,fontSize:14,bold:true,color:C.teal});
s.addText("O maior déficit estrutural de São Paulo não é a falta de mais raios — é a ausência de linhas circulares que interliguem os eixos radiais e aliviem o centro.",
  {x:0.9,y:4.85,w:11.5,h:1.3,fontFace:F,fontSize:19,bold:true,color:C.ink,lineSpacingMultiple:1.12});
s.addNotes("Custos estimados por obras análogas: metrô subterrâneo ~R$1,18 bi/km (Linha 6), monotrilho ~R$0,89 bi/km (Linha 17). A orbital 20-Rosa custaria ~R$37 bi, mas é a que mais melhora a conectividade por real.");
pageno(s,9);

/* ---------- 10. CONCLUSÕES ---------- */
s = p.addSlide(); bg(s); eyebrow(s,"CONCLUSÕES"); title(s,"O que a topologia revela");
const cc=[["Esparsa e radial",C.teal,"⟨k⟩=2,15; nem livre de escala, nem mundo pequeno no espaço L."],
  ["Dependente de poucas estações centrais",C.orange,"Luz e Brás concentram os fluxos; frágil a ataques dirigidos."],
  ["A menos redundante das três",C.blue,"Ao lado de Berlim; Londres e NY são mais densas e malhadas."],
  ["Próximo salto: linhas circulares",C.green,"Uma orbital ajuda ~3× mais que novos raios."]];
cc.forEach((o,i)=>{const y=1.85+i*1.2; card(s,0.6,y,12.15,1.05);
  s.addShape(p.ShapeType.ellipse,{x:0.85,y:y+0.28,w:0.5,h:0.5,fill:{color:o[1]},line:{width:0}});
  s.addText(String(i+1),{x:0.85,y:y+0.28,w:0.5,h:0.5,fontFace:F,fontSize:18,bold:true,color:C.bg,align:"center",valign:"middle",margin:0});
  s.addText(o[0],{x:1.6,y:y+0.13,w:4.6,h:0.8,fontFace:F,fontSize:17,bold:true,color:C.ink,valign:"middle"});
  s.addText(o[2],{x:6.2,y:y+0.13,w:6.4,h:0.8,fontFace:F,fontSize:13.5,color:C.mut,valign:"middle",lineSpacingMultiple:1.05});});
pageno(s,10);

/* ---------- 11. FERRAMENTAS & IMPLEMENTAÇÃO ---------- */
s = p.addSlide(); bg(s); eyebrow(s,"IMPLEMENTAÇÃO"); title(s,"Como construímos — análise e visualização");
// Card A — NetworkX (uso real)
card(s,0.6,1.8,6.0,4.15,C.card);
s.addText("Análise · Python + NetworkX",{x:0.85,y:2.0,w:5.5,h:0.4,fontFace:F,fontSize:16,bold:true,color:C.teal});
s.addText("O grafo (espaços L e P) e todas as métricas do artigo foram calculados com NetworkX:",
  {x:0.85,y:2.48,w:5.5,h:0.6,fontFace:F,fontSize:12.5,color:C.mut,lineSpacingMultiple:1.1});
s.addText([
  {text:"betweenness_centrality — Luz e Brás como pontos críticos",options:{bullet:{code:"2022",indent:14},breakLine:true,paraSpaceAfter:7}},
  {text:"global_efficiency · average_shortest_path_length — E_glob e L",options:{bullet:{code:"2022",indent:14},breakLine:true,paraSpaceAfter:7}},
  {text:"community (Louvain) — modularidade Q e as 15 regiões",options:{bullet:{code:"2022",indent:14},breakLine:true,paraSpaceAfter:7}},
  {text:"gnm_random_graph — índice de mundo pequeno σ",options:{bullet:{code:"2022",indent:14},breakLine:true,paraSpaceAfter:7}},
  {text:"connected_components — robustez sob falha e ataque",options:{bullet:{code:"2022",indent:14}}},
],{x:0.9,y:3.2,w:5.55,h:2.6,fontFace:F,fontSize:12.5,color:C.ink,lineSpacingMultiple:1.05});
// Card B — Three.js
card(s,6.75,1.8,6.0,4.15,C.card2);
s.addText("Visualização · Three.js / WebGL",{x:7.0,y:2.0,w:5.5,h:0.4,fontFace:F,fontSize:16,bold:true,color:C.orange});
s.addText("Artefatos interativos, no navegador, para explorar os resultados:",
  {x:7.0,y:2.48,w:5.5,h:0.6,fontFace:F,fontSize:12.5,color:C.mut,lineSpacingMultiple:1.1});
s.addText([
  {text:"Grafo 3D force-directed da malha, navegável",options:{bullet:{code:"2022",indent:14},breakLine:true,paraSpaceAfter:7}},
  {text:"Explorador: resultados, mapa de calor e planejador de rota",options:{bullet:{code:"2022",indent:14},breakLine:true,paraSpaceAfter:7}},
  {text:"Comparação lado a lado das três malhas",options:{bullet:{code:"2022",indent:14},breakLine:true,paraSpaceAfter:7}},
  {text:"Globo 3D com São Paulo, Londres e Nova York",options:{bullet:{code:"2022",indent:14}}},
],{x:7.05,y:3.2,w:5.55,h:2.6,fontFace:F,fontSize:12.5,color:C.ink,lineSpacingMultiple:1.05});
s.addText("NetworkX faz toda a parte quantitativa; Three.js/WebGL, a camada interativa — tudo reprodutível e versionado.",
  {x:0.6,y:6.15,w:12.2,h:0.4,fontFace:F,fontSize:12,italic:true,color:C.faint,align:"center"});
s.addNotes("Separação clara de responsabilidades técnicas: NetworkX calcula todas as métricas reportadas no artigo (centralidade, eficiência, comunidades, small-world, robustez), e Three.js/WebGL constrói a camada de visualização interativa no navegador. Tudo versionado e disponível online.");
pageno(s,11);

/* ---------- 12. ENCERRAMENTO ---------- */
s = p.addSlide(); bg(s);
s.addImage({path:IMG+"hero_globe.png",x:6.7,y:0,w:6.63,h:7.5,sizing:{type:"cover",w:6.63,h:7.5}});
s.addShape(p.ShapeType.rect,{x:0,y:0,w:8.0,h:7.5,fill:{color:C.bg,transparency:10},line:{width:0}});
s.addText("Obrigado!",{x:0.7,y:2.5,w:7,h:1.0,fontFace:F,fontSize:44,bold:true,color:C.ink});
s.addText("Perguntas?",{x:0.7,y:3.6,w:7,h:0.6,fontFace:F,fontSize:20,color:C.teal});
s.addText([
  {text:"Visualização 3D interativa e código:",options:{breakLine:true,color:C.mut,fontSize:13,paraSpaceAfter:4}},
  {text:"github.com/VitorCarvalho67/GrafosMetroSP",options:{breakLine:true,color:C.ink,fontSize:14,bold:true,paraSpaceAfter:2}},
  {text:"metro-sp.solveweb.com.br",options:{color:C.ink,fontSize:14,bold:true}},
],{x:0.7,y:4.7,w:7,h:1.2,fontFace:F,valign:"top"});
pageno(s,12);

p.writeFile({fileName:"/tmp/work/Seminario_GrafosMetroSP.pptx"}).then(f=>console.log("SAVED",f));
