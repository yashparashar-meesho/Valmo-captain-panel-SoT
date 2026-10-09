from pathlib import Path
SW, SH, GAP = 330, 382, 22
KW, FW, PAD = 132, 142, 20
S  = [PAD+KW+GAP + i*(SW+GAP) for i in range(4)]
FX = S[3]+SW+GAP
W  = FX+FW+PAD
TOP = 74
H   = TOP+SH+112
MID = TOP+SH/2
C = dict(blue="#2F6FED", ink="#16202E", ink2="#5A6678", ink3="#8A94A6",
         grey="#8A94A6", green="#13874B", red="#D1483C", purple="#7B5BD6")
out=[];A=out.append
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def txt(x,y,s,size=11,fill=C["ink2"],anchor="middle",weight=None,style=None):
    a=['x="%g"'%x,'y="%g"'%y,'text-anchor="%s"'%anchor,'font-size="%g"'%size,'fill="%s"'%fill]
    if weight:a.append('font-weight="%s"'%weight)
    if style:a.append('font-style="%s"'%style)
    A("  <text %s>%s</text>"%(" ".join(a),esc(s)))
def box(x,y,w,h,fill="#FFFFFF",stroke="#D7DCE4",sw=1.4,rx=8,dash=None):
    d=' stroke-dasharray="%s"'%dash if dash else ''
    A('  <rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="%s" stroke="%s" stroke-width="%g"%s/>'%(x,y,w,h,rx,fill,stroke,sw,d))
def arrow(d,col=C["grey"],mk="n",sw=1.6,dash=None):
    dd=' stroke-dasharray="%s"'%dash if dash else ''
    A('  <path d="%s" stroke="%s" stroke-width="%g" fill="none" marker-end="url(#%s)"%s/>'%(d,col,sw,mk,dd))
def section(x,label,note,blocks,foot,footnote):
    box(x,TOP,SW,SH,"none",C["blue"],1.6,11,"7 5")
    txt(x,TOP-10,label,12,C["blue"],"start","700")
    if note: txt(x+SW,TOP-10,note,10,C["green"],"end","600")
    cy=TOP+16; gate=None
    for i,(bf,bs,bw,lines,h) in enumerate(blocks):
        box(x+14,cy,SW-28,h,bf,bs,bw)
        if bf=="#FDEBBE": gate=cy+h/2
        ty=cy+19
        for s,size,fill,weight,style in lines:
            txt(x+SW/2,ty,s,size,fill,"middle",weight,style); ty+=size+4
        cy+=h
        if i<len(blocks)-1: arrow("M%g %g V%g"%(x+SW/2,cy,cy+18)); cy+=20
    assert cy+45 < TOP+SH, "section %s overflows: %g > %g" % (label, cy+45, TOP+SH)
    if foot:     txt(x+SW/2,cy+26,foot,10,C["ink3"],"middle",None,"italic")
    if footnote: txt(x+SW/2,cy+45,footnote,10.5,C["ink2"],"middle","600")
    return gate
A('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
  'font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Inter, system-ui, sans-serif">'%(W,H,W,H))
A('''  <defs>
    <marker id="n" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#8A94A6"/></marker>
    <marker id="g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#13874B"/></marker>
    <marker id="r" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#D1483C"/></marker>
  </defs>''')
A('  <rect width="%d" height="%d" fill="#FFFFFF"/>'%(W,H))
box(PAD,MID-25,KW,50,"#DCE9FF","#2F6FED",1.5,9)
txt(PAD+KW/2,MID-5,"KRD",13,"#143C8C","middle","700")
txt(PAD+KW/2,MID+11,"the problem",9.5,"#2A5099")
arrow("M%g %g H%g"%(PAD+KW+2,MID,S[0]-4),C["grey"])
g0=section(S[0],"SECTION 0 — LOCATE",None,[
 ("#EFF5FF","#AFC8F5",1.4,[("Match the KRD to the catalogue",12,C["ink"],"700",None),
   ("5 modules · 11 screens · 53 components",10.5,C["ink2"],None,None),
   ("fetches nothing — reading only",10,C["red"],None,"italic")],70),
 ("#FFFFFF","#D7DCE4",1.4,[("Four shapes of change",12,C["ink"],"700",None),
   ("1 extend a section · 2 a new section",10.5,C["ink2"],None,None),
   ("3  a new tab in a module",11,C["purple"],"700",None),
   ("4 a new module — say why each is in or out",10.5,C["ink2"],None,None)],88),
 ("#FDEBBE","#C9962B",1.5,[("Confirm the target",12,"#6B4D08","700",None),
   ("seconds — just “yes, that one”",10,"#6B4D08",None,None)],52)],
 "wrong target → say which, re-run","shape 3 is the one that gets missed")
g1=section(S[1],"SECTION 1 — DIVERGE",None,[
 ("#FFFFFF","#D7DCE4",1.4,[("Interrogate the gaps",12,C["ink"],"700",None),
   ("only what the KRD left out and",10.5,C["ink2"],None,None),
   ("Section 0 could not answer",10.5,C["ink2"],None,None)],70),
 ("#FFFFFF","#D7DCE4",1.4,[("Write the DRD",12,C["ink"],"700",None),
   ("five genuinely different approaches",11,C["purple"],"700",None),
   ("each: what it does, costs, rules out",10.5,C["ink2"],None,None),
   ("rendered as a page, not a raw .md",10.5,C["ink"],None,None)],88),
 ("#FDEBBE","#C9962B",2.4,[("The DRD is approved",12.5,"#6B4D08","700",None),
   ("BLOCKING — nothing fetched or built",10.5,"#A6341F","700",None)],52)],
 "approved in words, not “shared”","no converging yet")
g2=section(S[2],"SECTION 2 — SHAPE",None,[
 ("#F3EEFF","#C9B6F2",1.4,[("Fetch — once, here, in one pass",11.5,"#4A2E9E","700",None),
   ("screen · icons · fonts · kit.css · vendor js",10,"#5B3FB0",None,None)],46),
 ("#FFFFFF","#D7DCE4",1.4,[("2a · Comparison sheet",12,C["ink"],"700",None),
   ("all five as schematics, one page,",10.5,C["ink2"],None,None),
   ("beside what each does / costs / rules out",10.5,C["ink2"],None,None)],68),
 ("#FDEBBE","#C9962B",1.5,[("Pick one or two",12,"#6B4D08","700",None),
   ("the rest go to the Idea Wall",10,"#6B4D08",None,None)],46),
 ("#FFFFFF","#D7DCE4",1.4,[("2b · Full-size wireframes",12,C["ink"],"700",None),
   ("real skeleton · real components, in grey",10.5,C["ink2"],None,None),
   ("dashed boxes only for what is new",10.5,C["ink2"],None,None)],68)],
 "survivors only — the layout that gets built","a shape is unarguable on screen")
section(S[3],"SECTION 3 — PROMOTE","ALREADY WORKS",[
 ("#F3EEFF","#C9B6F2",1.4,[("Every grey box → a component",12,"#4A2E9E","700",None),
   ("built in Crystal, named, and listed",10.5,"#5B3FB0",None,None),
   ("back to you for approval",10.5,"#5B3FB0",None,None),
   ("colour returns here, not before",10,C["ink3"],None,"italic")],88),
 ("#FFFFFF","#D7DCE4",1.4,[("PR 1 — the components",12,C["ink"],"700",None),
   ("library first, on their own",10.5,C["ink2"],None,None)],52),
 ("#FFFFFF","#D7DCE4",1.4,[("PR 2 — the module",12,C["ink"],"700",None),
   ("wired into every screen’s rail",10.5,C["ink2"],None,None)],52)],
 "the loop that shipped #42 → #43 → #44",None)
for i,g in ((0,g0),(1,g1),(2,g2)):
    arrow("M%g %g H%g"%(S[i]+SW+2,g,S[i+1]-4),C["green"],"g",1.8)
    arrow("M%g %g H%g Q%g %g %g %g V%g"%(S[i]+14,g,S[i]+4,S[i]-6,g,S[i]-6,g-12,TOP+52),C["red"],"r",1.4)
box(FX,MID-26,FW,54,"#D8F3E3","#13874B",1.6,9)
txt(FX+FW/2,MID-4,"Final UI",13,"#0B5E35","middle","700")
txt(FX+FW/2,MID+13,"in the catalogue",10,"#0D6B3C")
arrow("M%g %g H%g"%(S[3]+SW+2,MID,FX-4),C["green"],"g",1.8)
LANE = TOP+SH+46
arrow("M%g %g V%g Q%g %g %g %g H%g Q%g %g %g %g V%g"
  %(FX+FW/2,MID+29,LANE-12,FX+FW/2,LANE,FX+FW/2-12,LANE,
    S[0]+SW/2+12,S[0]+SW/2,LANE,S[0]+SW/2,LANE-12,TOP+SH+6),C["green"],"g",1.4,"6 5")
txt(W/2,LANE+26,"every shipped module makes the next Section 0 smarter",11,C["green"],"middle","600")
A("</svg>")
Path('docs/flow.svg').write_text("\n".join(out)+"\n",encoding='utf-8')
import xml.etree.ElementTree as ET; ET.parse('docs/flow.svg')
print("regenerated cleanly: %dx%d  (lane %g, caption %g)" % (W,H,LANE,LANE+26))
