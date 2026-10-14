#!/usr/bin/env python3
"""Render the docs/ pack as one readable page on the site: pack/index.html.

    python3 scripts/build_pack_pages.py            # -> pack/index.html
    python3 scripts/build_pack_pages.py --check    # fail if stale (CI)

GENERATED. Never hand-edit pack/index.html - edit the markdown in docs/ (or
examples/capacity-cut/) and run this. The markdown is the source; a second
copy of a fact drifts.

One page, every document as a section, with a doc rail down the left - the
same shape as the throwaway review page, which is the shape people actually
read in. Seventeen separate pages made you navigate to find out whether a
rule existed.

Two rails, never both unless asked. The pack's own rail is what you came for,
so it is the one that shows. The Slipstream rail is collapsed behind an
arrow: open it and you have both, which is the only time two rails earn
their width.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from md_to_html import md  # noqa: E402  one converter, shared with render_doc.py

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
RUN = ROOT / "examples" / "capacity-cut"
OUT = ROOT / "pack"

# (source, slug, nav label, tag)   tag: "" | "new" | "gen" | "run"
GROUPS = [
    ("Start here", [
        (DOCS / "README.md", "readme", "Index of the pack", ""),
        (DOCS / "panel-principles.md", "panel-principles", "Who the captain is", "new"),
        (DOCS / "design-method.md", "design-method", "The design method", "new"),
    ]),
    ("Rules", [
        (DOCS / "page-framework.md", "page-framework", "What a page is made of", ""),
        (DOCS / "layout-rules.md", "layout-rules", "Rail, header, work area", ""),
        (DOCS / "section-rules.md", "section-rules", "New section vs bake in", ""),
        (DOCS / "never-do-this.md", "never-do-this", "Never do this", "new"),
    ]),
    ("What exists", [
        (DOCS / "pages.md", "pages", "All 11 screens", "gen"),
        (DOCS / "components.md", "components", "All 53 components", "gen"),
    ]),
    ("Foundations", [
        (DOCS / "color-foundation.md", "color-foundation", "Colour", ""),
        (DOCS / "spacing-foundation.md", "spacing-foundation", "Spacing", ""),
        (DOCS / "typography-audit.md", "typography-audit", "Typography", ""),
        (DOCS / "fidelity-checklist.md", "fidelity-checklist", "Matching live", ""),
    ]),
    ("A worked run", [
        (RUN / "BRIEF.md", "run-brief", "The brief", "run"),
        (RUN / "APPROACHES.md", "run-approaches", "The DRD", "run"),
    ]),
]
SLUGS = {p.name: slug for _, items in GROUPS for p, slug, _, _ in items}
ASSETS = {"flow.svg", "comparison-example.html", "wireframe-example.html",
          "promoted-example.html"}

CSS = """
:root{--ink:#15202E;--ink2:#55606F;--ink3:#8A94A3;--page:#fff;--sunken:#F5F7FA;
--line:#E2E7EE;--accent:#2F6FED;--new:#7B5BD6;--gen:#0E7C53;--run:#B2541A;
--font:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,system-ui,sans-serif;
--mono:ui-monospace,SFMono-Regular,Menlo,monospace}
*{box-sizing:border-box}html,body{margin:0;height:100%}
body{background:var(--page);color:var(--ink);font:16px/1.65 var(--font);display:flex}

/* ---- the Slipstream rail ----
   Matches the catalogue's own sidebar: white, navy, the same tokens. It was
   invented dark here, which made the pack feel like a different product.
   Collapsed it keeps a 48px sliver so it never disappears entirely, with the
   toggle centred above the list in both states. */
#sl{width:236px;flex:none;background:#FFFFFF;border-right:1px solid #DDE3ED;
height:100vh;overflow-y:auto;overflow-x:hidden;display:flex;flex-direction:column;
transition:width .16s ease}
body.sl-collapsed #sl{width:48px}
.sl-toggle-row{display:flex;justify-content:center;padding:12px 0 10px;flex:none}
#slToggle{width:30px;height:30px;border:1px solid #DDE3ED;background:#fff;
border-radius:8px;cursor:pointer;color:#6B7C96;font-size:14px;line-height:1;
display:flex;align-items:center;justify-content:center;flex:none}
#slToggle:hover{background:#F4F6FA;color:#092D5E;border-color:#C3CDDD}
.sl-body{min-width:236px}
body.sl-collapsed .sl-body{display:none}
.sl-brand{padding:0 18px 14px;border-bottom:1px solid #DDE3ED;margin-bottom:10px}
.sl-brand b{display:block;font:700 17px/1.2 var(--display,inherit);color:#092D5E;
letter-spacing:-.01em}
.sl-brand span{font:400 11.5px/1.5 var(--font);color:#6B7C96;display:block;margin-top:2px}
#sl h3{font:650 10.5px/1 var(--font);letter-spacing:.1em;text-transform:uppercase;
color:#8A94A3;margin:16px 18px 6px}
#sl a{display:block;padding:6px 18px;color:#0A1E3C;text-decoration:none;
font:400 13.5px/1.45 var(--font)}
#sl a:hover{background:#F4F6FA}
#sl a.home{color:#2A67FF;font-weight:600;padding-top:0}

/* ---- the pack's own rail ---- */
nav.docs{width:270px;flex:none;background:var(--sunken);border-right:1px solid var(--line);
height:100vh;overflow-y:auto;padding:14px 0 40px}
.railtop{display:flex;align-items:center;gap:8px;padding:0 14px 12px;margin-bottom:6px;
border-bottom:1px solid var(--line)}
#slToggle{flex:none;width:28px;height:28px;border:1px solid var(--line);background:#fff;
border-radius:7px;cursor:pointer;color:var(--ink2);font-size:13px;line-height:1;
display:flex;align-items:center;justify-content:center}
#slToggle:hover{background:#EAEFF6;color:var(--ink)}
.railtop b{font-size:13px}
.railtop span{font-size:11px;color:var(--ink3);display:block;font-weight:400}
nav.docs h2{font-size:11px;letter-spacing:.09em;text-transform:uppercase;color:var(--ink3);
margin:18px 20px 6px;font-weight:650}
nav.docs a{display:block;padding:6px 20px;color:var(--ink2);text-decoration:none;font-size:14px;
border-left:2px solid transparent}
nav.docs a:hover{background:#EAEFF6;color:var(--ink)}
nav.docs a.on{border-left-color:var(--accent);color:var(--ink);font-weight:600;background:#E8EFFC}
.tag{font-size:9.5px;font-weight:700;letter-spacing:.05em;padding:1px 5px;border-radius:3px;
margin-left:6px;vertical-align:1px}
.t-new{background:#EEE8FD;color:var(--new)}.t-gen{background:#DFF3E9;color:var(--gen)}
.t-run{background:#FBE8DA;color:var(--run)}

main{flex:1;min-width:0;height:100vh;overflow-y:auto;padding:0 0 120px}
.inner{max-width:820px;margin:0 auto;padding:30px 32px}
.crumb{position:sticky;top:0;z-index:6;background:rgba(255,255,255,.97);
border-bottom:1px solid var(--line);padding:11px 32px;display:flex;
align-items:center;gap:8px;font:400 13px/1.4 var(--font);color:var(--ink3)}
.crumb a{color:var(--ink2);text-decoration:none}
.crumb a:hover{color:var(--accent);text-decoration:underline}
.crumb .sep{color:#C3CDDD}
.crumb .here{color:var(--ink);font-weight:600}
.crumb .gh{margin-left:auto;display:inline-flex;align-items:center;gap:6px;
border:1px solid var(--line);border-radius:8px;padding:5px 11px;color:var(--ink2);
font-size:12.5px;text-decoration:none;white-space:nowrap}
.crumb .gh:hover{background:var(--sunken);color:var(--ink);text-decoration:none}
.crumb .gh svg{width:14px;height:14px}
.filehead{position:sticky;top:43px;background:rgba(255,255,255,.96);
border-bottom:1px solid var(--line);padding:11px 32px;z-index:5;
font:600 12.5px/1.4 var(--mono);color:var(--ink2)}
.filehead i{font-style:normal;color:var(--ink3);font-weight:400}
section{scroll-margin-top:90px;border-bottom:1px solid var(--line)}
section:last-child{border-bottom:0}
.lead-in{padding:34px 32px 10px;max-width:820px;margin:0 auto}
.lead-in h1{font-size:29px;margin:0 0 8px;letter-spacing:-.02em}
.lead-in p{color:var(--ink2);margin:0 0 6px}
.md h1{font-size:29px;line-height:1.2;letter-spacing:-.02em;margin:.2em 0 .5em}
.md h2{font-size:21px;letter-spacing:-.01em;margin:1.9em 0 .5em;padding-bottom:.25em;
border-bottom:1px solid var(--line)}
.md h3{font-size:17px;margin:1.6em 0 .4em}.md h4{font-size:15px;margin:1.4em 0 .3em}
.md p{margin:.75em 0;color:#242E3C}.md ul,.md ol{padding-left:1.35em;margin:.7em 0}
.md li{margin:.3em 0}
.md code{background:#EFF2F6;padding:1.5px 6px;border-radius:4px;font:.855em var(--mono);
color:#1F3C73}
.md pre{background:#132033;color:#DCE6F5;padding:15px 18px;border-radius:9px;overflow-x:auto;
font:13px/1.6 var(--mono);margin:1em 0}
.md pre code{background:none;color:inherit;padding:0;font-size:inherit}
.md table{border-collapse:collapse;width:100%;margin:1.1em 0;font-size:14.5px;display:block;
overflow-x:auto}
.md th,.md td{border:1px solid var(--line);padding:8px 11px;text-align:left;vertical-align:top}
.md th{background:var(--sunken);font-size:12px;text-transform:uppercase;letter-spacing:.06em;
color:var(--ink3);font-weight:650;white-space:nowrap}
.md tr:nth-child(even) td{background:#FBFCFE}
.md blockquote{margin:1.1em 0;padding:.6em 1.1em;border-left:3px solid var(--accent);
background:#F4F8FF;color:#24405E;border-radius:0 6px 6px 0}
.md blockquote p{margin:.35em 0}.md a{color:var(--accent)}
.md hr{border:0;border-top:1px solid var(--line);margin:2em 0}.md strong{font-weight:650}
.md img{width:100%;height:auto;display:block;border:1px solid var(--line);border-radius:8px;
background:#fff}
.seealso{background:#FFF8EE;border:1px solid #F0DCBC;border-radius:9px;padding:12px 16px;
font-size:14px;margin:0 0 4px}
.seealso a{color:#9A5A12;font-weight:600}
@media(max-width:900px){nav.docs,#sl{display:none}body.sl-open #sl{display:none}}
"""

JS = """
(function(){
  var b=document.body, t=document.getElementById('slToggle'), K='slipstream-pack-rail';
  function paint(){ var open=!b.classList.contains('sl-collapsed');
    t.textContent = open ? '\\u2039' : '\\u203a';
    t.title = open ? 'Collapse the Slipstream rail' : 'Expand the Slipstream rail';
    t.setAttribute('aria-expanded', open ? 'true' : 'false'); }
  /* Collapsed by default: the pack's own rail is what you came for. The sliver
     keeps the way back visible instead of hiding it behind a memory. */
  b.classList.add('sl-collapsed');
  try{ if(localStorage.getItem(K)==='1') b.classList.remove('sl-collapsed'); }catch(e){}
  paint();
  t.addEventListener('click', function(){
    b.classList.toggle('sl-collapsed'); paint();
    try{ localStorage.setItem(K, b.classList.contains('sl-collapsed')?'0':'1'); }catch(e){}
  });

  var here=document.getElementById('crumbHere');
  var links={}, secs=[].slice.call(document.querySelectorAll('section[id]'));
  secs.forEach(function(s){ var a=document.querySelector('nav.docs a[href="#'+s.id+'"]');
    if(a) links[s.id]=a; });
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){ if(!e.isIntersecting) return;
      for(var k in links) links[k].classList.remove('on');
      var a=links[e.target.id];
      if(a){ a.classList.add('on');
        if(here) here.textContent = a.textContent.replace(/(new|gen|run)$/,'').trim(); }
    });
  },{rootMargin:'-12% 0px -78% 0px'});
  secs.forEach(function(s){ io.observe(s); });
})();
"""


def _link(m):
    """A cross-reference, resolved once: in-pack links become anchors."""
    stem, ext = m.group(1), m.group(2)
    if ext == "md":
        slug = SLUGS.get(stem + ".md")
        return 'href="#%s"' % slug if slug else 'href="../docs/%s.md"' % stem
    return 'href="../docs/%s.%s"' % (stem, ext)


def slipstream_rail():
    """Generated from the seed, so the rail cannot drift from the catalogue."""
    seed = json.loads((ROOT / "source" / "data-seed.json").read_text(encoding="utf-8"))
    by_flow = {}
    for s in seed["screens"]:
        by_flow.setdefault(s["flowId"], []).append(s)   # flowId, not flow
    for v in by_flow.values():
        v.sort(key=lambda x: x.get("order", 0))
    h = ['<aside id="sl">'
         '<div class="sl-toggle-row">'
         '<button id="slToggle" aria-label="Expand or collapse the Slipstream rail">'
         '</button></div>'
         '<div class="sl-body"><div class="sl-brand"><b>Slipstream</b>'
         '<span>Start where the last person finished.</span></div>'
         '<a class="home" href="../index.html">← The catalogue</a>']
    for f in sorted(seed["flows"], key=lambda x: x.get("order", 0)):
        scr = by_flow.get(f["id"], [])
        if not scr:
            continue
        h.append("<h3>%s</h3>" % f["name"])
        for s in scr:
            h.append('<a href="../screens/%s.html">%s</a>' % (s["id"], s["name"]))
    if sum(len(v) for v in by_flow.values()) != len(seed["screens"]):
        sys.exit("rail lost screens: check the flowId join")
    h.append('<h3>Also</h3><a href="../index.html">Components</a>'
             '<a href="../index.html">Foundations</a><a href="../index.html">Learn</a>')
    h.append("</div></aside>")
    return "".join(h)


def build():
    OUT.mkdir(exist_ok=True)
    rail, body = [], []
    for name, items in GROUPS:
        rail.append("<h2>%s</h2>" % name)
        for src, slug, label, tag in items:
            if not src.exists():
                sys.exit("missing: %s" % src)
            rail.append('<a href="#%s">%s%s</a>' % (
                slug, label,
                '<span class="tag t-%s">%s</span>' % (tag, tag) if tag else ""))
            html = md(src.read_text(encoding="utf-8"))
            html = re.sub(r'href="([A-Za-z0-9._-]+)\.(md|html|svg)"', _link, html)
            html = re.sub(r'src="([a-z0-9.-]+\.svg)"', r'src="../docs/\1"', html)
            rel = src.relative_to(ROOT).as_posix()
            body.append(
                '<section id="%s"><div class="filehead">%s <i>&mdash; %s</i></div>'
                '<div class="inner md">%s</div></section>' % (slug, rel, label, html))

    page = (
        '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<title>The pack — Slipstream</title>\n<style>%s</style>\n</head>\n<body>\n'
        '%s\n<nav class="docs"><div class="railtop">'
        '<button id="slToggle" aria-label="Show or hide the Slipstream rail"></button>'
        '<b>The pack<span>%d documents</span></b></div>%s</nav>\n'
        '<main>'
        '<div class="crumb"><a href="../index.html">Slipstream</a>'
        '<span class="sep">›</span><span class="here" id="crumbHere">The pack</span>'
        '<a class="gh" href="https://github.com/yashparashar-meesho/Valmo-captain-panel-SoT/tree/main/docs" target="_blank" rel="noopener">'
        '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-3.16 19.49c.5.09.68-.22.68-.48v-1.7C6.73 19.91 6.14 18 6.14 18a2.7 2.7 0 0 0-1.13-1.49c-.92-.63.07-.62.07-.62a2.14 2.14 0 0 1 1.56 1.05 2.17 2.17 0 0 0 2.96.85 2.18 2.18 0 0 1 .65-1.37c-2.23-.25-4.57-1.11-4.57-4.95a3.88 3.88 0 0 1 1.03-2.69 3.6 3.6 0 0 1 .1-2.65s.84-.27 2.75 1.03a9.4 9.4 0 0 1 5 0c1.91-1.3 2.75-1.03 2.75-1.03a3.6 3.6 0 0 1 .1 2.65 3.87 3.87 0 0 1 1.03 2.69c0 3.85-2.34 4.7-4.57 4.95a2.43 2.43 0 0 1 .7 1.89v2.8c0 .27.18.58.69.48A10 10 0 0 0 12 2z"/></svg>'
        'All files on GitHub</a></div>'
        '<div class="lead-in"><h1>The pack</h1>'
        '<p>Everything the design method reads on every run — the same documents a '
        'person can read. Generated from <code>docs/</code>; edit the markdown there, '
        'never this page. Every file is in ''<a href="https://github.com/yashparashar-meesho/Valmo-captain-panel-SoT/tree/main/docs" target="_blank" rel="noopener">the docs folder on GitHub</a> ''if you want to read or download the originals.</p>'
        '<p class="seealso">The worked run ends in a comparison sheet: '
        '<a href="run/shapes.html">see the five shapes drawn</a>.</p></div>'
        '%s</main>\n<script>%s</script>\n</body>\n</html>\n'
        % (CSS, slipstream_rail(), len(SLUGS), "".join(rail), "".join(body), JS))

    shapes = (RUN / "shapes.html").read_text(encoding="utf-8")
    written = {"index.html": page, "run/shapes.html": shapes}
    stale = [n for n, h in written.items()
             if not (OUT / n).exists() or (OUT / n).read_text(encoding="utf-8") != h]

    if "--check" in sys.argv:
        if stale:
            sys.exit("pack/ is stale: %s\nRun: python3 scripts/build_pack_pages.py"
                     % ", ".join(sorted(stale)))
        print("pack/ is current: %d documents on one page" % len(SLUGS))
        return
    for n, h in written.items():
        t = OUT / n
        t.parent.mkdir(parents=True, exist_ok=True)
        t.write_text(h, encoding="utf-8")
    # the per-document pages this replaced
    for old in OUT.glob("*.html"):
        if old.name != "index.html":
            old.unlink()
    for old in (OUT / "run").glob("*.html"):
        if old.name != "shapes.html":
            old.unlink()
    print("Wrote pack/index.html: %d documents, %d stale" % (len(SLUGS), len(stale)))


build()
