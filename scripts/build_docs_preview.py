#!/usr/bin/env python3
"""Render docs/*.md into one self-contained review page.

No CDN, no fetch, no server required - the markdown is converted here and
baked into the HTML. The first version of this page pulled marked.js from a
CDN and fetched each file at runtime; with no network it reported every
section as "could not load". A review tool that needs the internet to show
files that are sitting on disk is the wrong shape.

    python3 scripts/build_docs_preview.py      # -> docs-preview.html

The output is a throwaway review artefact, not part of the pack. It is
deliberately untracked.
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUT = ROOT / "docs-preview.html"

GROUPS = [
    ("Start here", [
        ("README.md", "Index of the pack", "new"),
        ("design-method.md", "The four-section flow", "new"),
    ]),
    ("Rules — please read closely", [
        ("page-framework.md", "What a page is made of", "new"),
        ("layout-rules.md", "Rail, header, work area, scroll", "new"),
        ("section-rules.md", "New section vs bake in", "new"),
        ("never-do-this.md", "Things not to do", "new"),
    ]),
    ("Inventory", [
        ("pages.md", "All 11 screens", "gen"),
        ("components.md", "All 53 components", "gen"),
    ]),
    ("Existing foundations", [
        ("color-foundation.md", "43 colours", ""),
        ("spacing-foundation.md", "Scale and six roles", ""),
        ("typography-audit.md", "28 styles", ""),
        ("fidelity-checklist.md", "Matching live", ""),
    ]),
]


# ---------------------------------------------------------------- inline ----
def inline(s):
    """Inline markdown -> HTML. Code spans are extracted first so nothing
    inside them is treated as markup."""
    spans = []

    def stash(m):
        spans.append(m.group(1))
        return "\x00%d\x00" % (len(spans) - 1)

    s = re.sub(r"`([^`]+)`", stash, s)
    s = html.escape(s, quote=False)
    s = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img alt="\1" src="\2">', s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", s)
    s = re.sub(r"(?<![\w_])_([^_\n]+)_(?![\w_])", r"<em>\1</em>", s)
    s = re.sub(r"\x00(\d+)\x00",
               lambda m: "<code>%s</code>" % html.escape(spans[int(m.group(1))], quote=False), s)
    return s


def cells(row):
    row = row.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|"):
        row = row[:-1]
    # a escaped pipe inside a cell is content, not a separator
    parts, buf = [], ""
    i = 0
    while i < len(row):
        if row[i] == "\\" and i + 1 < len(row) and row[i + 1] == "|":
            buf += "|"
            i += 2
        elif row[i] == "|":
            parts.append(buf)
            buf = ""
            i += 1
        else:
            buf += row[i]
            i += 1
    parts.append(buf)
    return [p.strip() for p in parts]


# ----------------------------------------------------------------- block ----
def md(text):
    lines = text.split("\n")
    out, i = [], 0
    while i < len(lines):
        ln = lines[i]

        if ln.startswith("```"):                                   # fenced code
            i += 1
            buf = []
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i]); i += 1
            i += 1
            out.append("<pre><code>%s</code></pre>" % html.escape("\n".join(buf), quote=False))
            continue

        if ln.strip().startswith("<!--"):                          # comment
            while i < len(lines) and "-->" not in lines[i]:
                i += 1
            i += 1
            continue

        m = re.match(r"(#{1,6})\s+(.*)", ln)                       # heading
        if m:
            lv = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (lv, inline(m.group(2)), lv))
            i += 1
            continue

        if re.match(r"^\s*([-*_])\s*\1\s*\1[\s\-*_]*$", ln):       # hr
            out.append("<hr>"); i += 1; continue

        if ln.lstrip().startswith("|") and i + 1 < len(lines) \
           and re.match(r"^\s*\|?[\s:\-|]+\|[\s:\-|]*$", lines[i + 1]):
            head = cells(ln)
            i += 2
            body = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                body.append(cells(lines[i])); i += 1
            t = ["<table><thead><tr>"]
            t += ["<th>%s</th>" % inline(h) for h in head]
            t.append("</tr></thead><tbody>")
            for r in body:
                r = (r + [""] * len(head))[:len(head)]
                t.append("<tr>" + "".join("<td>%s</td>" % inline(c) for c in r) + "</tr>")
            t.append("</tbody></table>")
            out.append("".join(t))
            continue

        if ln.lstrip().startswith(">"):                            # blockquote
            buf = []
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                buf.append(re.sub(r"^\s*>\s?", "", lines[i])); i += 1
            out.append("<blockquote>%s</blockquote>" % md("\n".join(buf)))
            continue

        m = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)", ln)          # list
        if m:
            ordered = not m.group(2) in "-*+"
            tag = "ol" if ordered else "ul"
            items, base = [], len(m.group(1))
            while i < len(lines):
                mm = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)", lines[i])
                if mm and len(mm.group(1)) == base:
                    items.append([mm.group(3)]); i += 1
                elif items and lines[i].strip() and lines[i].startswith(" " * (base + 1)):
                    items[-1].append(lines[i].strip()); i += 1
                else:
                    break
            out.append("<%s>%s</%s>" % (
                tag, "".join("<li>%s</li>" % inline(" ".join(it)) for it in items), tag))
            continue

        if not ln.strip():                                         # blank
            i += 1
            continue

        buf = []                                                   # paragraph
        while i < len(lines) and lines[i].strip() \
                and not re.match(r"^(#{1,6}\s|```|\s*\||\s*>)", lines[i]) \
                and not re.match(r"^(\s*)([-*+]|\d+[.)])\s+", lines[i]):
            buf.append(lines[i].strip()); i += 1
        if buf:
            out.append("<p>%s</p>" % inline(" ".join(buf)))
    return "\n".join(out)


CSS = """
:root{--ink:#15202E;--ink2:#55606F;--ink3:#8A94A3;--page:#fff;--sunken:#F5F7FA;
--line:#E2E7EE;--accent:#2F6FED;--new:#7B5BD6;--gen:#0E7C53;
--font:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,system-ui,sans-serif;
--mono:ui-monospace,SFMono-Regular,Menlo,monospace}
*{box-sizing:border-box}html,body{margin:0;height:100%}
body{background:var(--page);color:var(--ink);font:16px/1.65 var(--font);display:flex}
nav{width:270px;flex:none;background:var(--sunken);border-right:1px solid var(--line);
height:100vh;overflow-y:auto;padding:22px 0 40px}
nav h2{font-size:12px;letter-spacing:.09em;text-transform:uppercase;color:var(--ink3);
margin:20px 20px 8px;font-weight:650}nav h2:first-child{margin-top:0}
nav a{display:block;padding:6px 20px;color:var(--ink2);text-decoration:none;font-size:14px;
border-left:2px solid transparent}
nav a:hover{background:#EAEFF6;color:var(--ink)}
nav a.on{border-left-color:var(--accent);color:var(--ink);font-weight:600;background:#E8EFFC}
.tag{font-size:10px;font-weight:700;letter-spacing:.05em;padding:1px 5px;border-radius:3px;
margin-left:6px;vertical-align:1px}
.t-new{background:#EEE8FD;color:var(--new)}.t-gen{background:#DFF3E9;color:var(--gen)}
main{flex:1;min-width:0;height:100vh;overflow-y:auto;padding:0 0 120px}
.inner{max-width:820px;margin:0 auto;padding:36px 32px}
.filehead{position:sticky;top:0;background:rgba(255,255,255,.95);border-bottom:1px solid var(--line);
padding:12px 32px;z-index:5;font:600 13px/1.4 var(--mono);color:var(--ink2)}
section{scroll-margin-top:50px;border-bottom:1px solid var(--line)}section:last-child{border-bottom:0}
.md h1{font-size:30px;line-height:1.2;letter-spacing:-.02em;margin:.2em 0 .5em}
.md h2{font-size:21px;letter-spacing:-.01em;margin:1.9em 0 .5em;padding-bottom:.25em;
border-bottom:1px solid var(--line)}
.md h3{font-size:17px;margin:1.6em 0 .4em}.md h4{font-size:15px;margin:1.4em 0 .3em}
.md p{margin:.75em 0;color:#242E3C}.md ul,.md ol{padding-left:1.35em;margin:.7em 0}
.md li{margin:.3em 0}
.md code{background:#EFF2F6;padding:1.5px 6px;border-radius:4px;font:.855em var(--mono);color:#1F3C73}
.md pre{background:#132033;color:#DCE6F5;padding:15px 18px;border-radius:9px;overflow-x:auto;
font:13px/1.6 var(--mono);margin:1em 0}
.md pre code{background:none;color:inherit;padding:0;font-size:inherit}
.md table{border-collapse:collapse;width:100%;margin:1.1em 0;font-size:14.5px;display:block;overflow-x:auto}
.md th,.md td{border:1px solid var(--line);padding:8px 11px;text-align:left;vertical-align:top}
.md th{background:var(--sunken);font-size:12px;text-transform:uppercase;letter-spacing:.06em;
color:var(--ink3);font-weight:650;white-space:nowrap}
.md tr:nth-child(even) td{background:#FBFCFE}
.md blockquote{margin:1.1em 0;padding:.6em 1.1em;border-left:3px solid var(--accent);
background:#F4F8FF;color:#24405E;border-radius:0 6px 6px 0}
.md blockquote p{margin:.35em 0}.md a{color:var(--accent)}
.md hr{border:0;border-top:1px solid var(--line);margin:2em 0}.md strong{font-weight:650}
.note{background:#FFF6EC;border:1px solid #F0D4B4;color:#7A4312;border-radius:8px;
padding:11px 15px;font-size:14px;margin:0 0 26px}
@media(max-width:900px){nav{display:none}}

/* ---------------- comment mode ---------------- */
#bar{position:fixed;right:18px;bottom:18px;z-index:60;display:flex;gap:8px;align-items:center;
background:#fff;border:1px solid var(--line);border-radius:11px;padding:7px;
box-shadow:0 6px 24px rgba(16,32,56,.14)}
#bar button{font:600 13px/1 var(--font);border-radius:7px;padding:9px 13px;cursor:pointer;
border:1px solid var(--line);background:#fff;color:var(--ink)}
#bar button:hover{background:var(--sunken)}
#bar #tgl.on{background:#2F6FED;border-color:#2F6FED;color:#fff}
#bar #send{background:#13874B;border-color:#13874B;color:#fff}
#bar #send:disabled{opacity:.45;cursor:not-allowed}
#cnt{font:600 12px/1 var(--font);color:var(--ink2);padding:0 4px}
body.cmt .md p,body.cmt .md li,body.cmt .md h1,body.cmt .md h2,body.cmt .md h3,
body.cmt .md h4,body.cmt .md blockquote,body.cmt .md pre,body.cmt .md tr{cursor:crosshair}
body.cmt .md p:hover,body.cmt .md li:hover,body.cmt .md h1:hover,body.cmt .md h2:hover,
body.cmt .md h3:hover,body.cmt .md h4:hover,body.cmt .md blockquote:hover,
body.cmt .md pre:hover,body.cmt .md tr:hover{outline:2px solid #9DC0FA;outline-offset:3px;
border-radius:3px;background:#F3F8FF}
[data-has]{border-left:3px solid #E9A13B!important;padding-left:10px!important;
background:#FFFBF3!important;position:relative}
[data-has]::after{content:"\\1F4AC";position:absolute;left:-26px;top:1px;font-size:13px}
#pop{position:absolute;z-index:70;width:330px;background:#fff;border:1px solid var(--line);
border-radius:11px;box-shadow:0 10px 34px rgba(16,32,56,.2);padding:12px}
#pop .src{font:12px/1.45 var(--font);color:var(--ink3);margin-bottom:8px;max-height:56px;
overflow:hidden;border-left:2px solid var(--line);padding-left:8px}
#pop textarea{width:100%;min-height:84px;border:1px solid var(--line);border-radius:7px;
padding:8px 10px;font:14px/1.5 var(--font);resize:vertical;color:var(--ink)}
#pop .row{display:flex;gap:7px;margin-top:9px}
#pop button{font:600 13px/1 var(--font);border-radius:7px;padding:8px 12px;cursor:pointer;
border:1px solid var(--line);background:#fff}
#pop .save{background:#2F6FED;border-color:#2F6FED;color:#fff}
#pop .del{margin-left:auto;color:#C0392B;border-color:#F0C8C2}
#drawer{position:fixed;right:0;top:0;bottom:0;width:390px;background:#fff;z-index:65;
border-left:1px solid var(--line);box-shadow:-8px 0 30px rgba(16,32,56,.12);
display:none;flex-direction:column}
#drawer.open{display:flex}
#drawer header{padding:15px 18px;border-bottom:1px solid var(--line);display:flex;
align-items:center;justify-content:space-between;font:650 15px/1 var(--font)}
#drawer header button{border:0;background:none;font-size:20px;cursor:pointer;color:var(--ink2)}
#list{flex:1;overflow-y:auto;padding:10px 14px 24px}
.ci{border:1px solid var(--line);border-radius:9px;padding:10px 12px;margin-bottom:10px;cursor:pointer}
.ci:hover{background:var(--sunken)}
.ci .f{font:600 11px/1 var(--mono);color:#2F6FED;text-transform:none}
.ci .s{font:12px/1.45 var(--font);color:var(--ink3);margin:5px 0 6px;
display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.ci .n{font:14px/1.5 var(--font);color:var(--ink);white-space:pre-wrap}
#empty{color:var(--ink3);font-size:14px;padding:16px 4px}
#toast{position:fixed;left:50%;transform:translateX(-50%);bottom:26px;z-index:90;
background:#15202E;color:#fff;padding:11px 18px;border-radius:9px;font:14px/1 var(--font);
display:none}
"""

JS = r"""
var obs=new IntersectionObserver(function(es){es.forEach(function(e){
var a=document.getElementById('nav-'+e.target.id);
if(a&&e.isIntersecting){var c=document.querySelectorAll('nav a.on');
for(var i=0;i<c.length;i++)c[i].classList.remove('on');a.classList.add('on');}});},
{rootMargin:'-10% 0px -80% 0px'});
var s=document.querySelectorAll('section');for(var i=0;i<s.length;i++)obs.observe(s[i]);

/* ------------------------------------------------ comment mode ---------- */
var KEY='slipstream-review-comments', SEL='p,li,h1,h2,h3,h4,blockquote,pre,tr';
var C={};
try{C=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){C={}}
function save(){try{localStorage.setItem(KEY,JSON.stringify(C))}catch(e){}}

/* A stable address per block: which file, and the nth block of that tag in it.
   The snippet travels with the comment too, so a comment is still findable by
   eye if the docs shift under it. */
document.querySelectorAll('section').forEach(function(sec){
  var n={};
  sec.querySelectorAll(SEL).forEach(function(el){
    if(el.closest('pre')&&el.tagName!=='PRE')return;
    var t=el.tagName.toLowerCase(); n[t]=(n[t]||0)+1;
    el.dataset.cid=sec.id+'/'+t+n[t];
  });
});
function snip(el){return (el.innerText||'').replace(/\s+/g,' ').trim().slice(0,220)}
function fileOf(cid){return 'docs/'+cid.split('/')[0].replace(/-md$/,'.md')}

function paint(){
  document.querySelectorAll('[data-has]').forEach(function(e){e.removeAttribute('data-has')});
  Object.keys(C).forEach(function(cid){
    var el=document.querySelector('[data-cid="'+CSS.escape(cid)+'"]');
    if(el)el.setAttribute('data-has','1');
  });
  var k=Object.keys(C).length;
  document.getElementById('cnt').textContent=k+(k===1?' comment':' comments');
  document.getElementById('send').disabled=!k;
  var L=document.getElementById('list'); L.innerHTML='';
  if(!k){L.innerHTML='<div id="empty">No comments yet. Turn on comment mode, then click any '+
    'paragraph, heading, list item or table row.</div>';return;}
  Object.keys(C).forEach(function(cid){
    var c=C[cid], d=document.createElement('div'); d.className='ci';
    d.innerHTML='<div class="f"></div><div class="s"></div><div class="n"></div>';
    d.children[0].textContent=c.file; d.children[1].textContent=c.quote; d.children[2].textContent=c.note;
    d.onclick=function(){
      var el=document.querySelector('[data-cid="'+CSS.escape(cid)+'"]');
      if(el){el.scrollIntoView({block:'center'});open_(el);}
    };
    L.appendChild(d);
  });
}

var pop=null;
function close_(){if(pop){pop.remove();pop=null}}
function open_(el){
  close_();
  var cid=el.dataset.cid, cur=C[cid];
  pop=document.createElement('div'); pop.id='pop';
  pop.innerHTML='<div class="src"></div><textarea placeholder="What should change here?"></textarea>'+
    '<div class="row"><button class="save">Save</button><button class="cancel">Cancel</button>'+
    (cur?'<button class="del">Delete</button>':'')+'</div>';
  pop.querySelector('.src').textContent=snip(el);
  document.body.appendChild(pop);
  var r=el.getBoundingClientRect();
  pop.style.top=(window.scrollY+r.bottom+8)+'px';
  pop.style.left=Math.max(12,Math.min(r.left,window.innerWidth-350))+'px';
  var ta=pop.querySelector('textarea'); ta.value=cur?cur.note:''; ta.focus();
  pop.querySelector('.cancel').onclick=close_;
  if(cur)pop.querySelector('.del').onclick=function(){delete C[cid];save();paint();close_()};
  pop.querySelector('.save').onclick=function(){
    var v=ta.value.trim();
    if(v)C[cid]={file:fileOf(cid),anchor:cid,quote:snip(el),note:v,at:new Date().toISOString()};
    else delete C[cid];
    save();paint();close_();
  };
  ta.onkeydown=function(e){
    if(e.key==='Escape')close_();
    if((e.metaKey||e.ctrlKey)&&e.key==='Enter')pop.querySelector('.save').click();
  };
}

document.addEventListener('click',function(e){
  if(pop&&(pop===e.target||pop.contains(e.target)))return;
  if(!document.body.classList.contains('cmt')){close_();return}
  var el=e.target.closest(SEL);
  if(el&&el.dataset.cid&&el.closest('.md')){e.preventDefault();open_(el);}
  else close_();
});

function toast(m){var t=document.getElementById('toast');t.textContent=m;t.style.display='block';
  clearTimeout(t._h);t._h=setTimeout(function(){t.style.display='none'},3200)}

document.getElementById('tgl').onclick=function(){
  var on=document.body.classList.toggle('cmt');
  this.classList.toggle('on',on);
  this.textContent=on?'Comment mode: ON':'Comment mode';
  if(!on)close_();
};
document.getElementById('all').onclick=function(){
  document.getElementById('drawer').classList.toggle('open')};
document.getElementById('close').onclick=function(){
  document.getElementById('drawer').classList.remove('open')};

document.getElementById('send').onclick=function(){
  var out={sentAt:new Date().toISOString(),
           comments:Object.keys(C).map(function(k){return C[k]})};
  var btn=this; btn.disabled=true; btn.textContent='Sending…';
  fetch('/_comments',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify(out,null,1)})
  .then(function(r){return r.json()})
  .then(function(j){
    if(!j.ok)throw new Error(j.error||'rejected');
    btn.textContent='Sent ✓';
    toast(j.count+' comment(s) written to '+j.file+' — tell Claude they are ready.');
    setTimeout(function(){btn.textContent='Send to Claude';btn.disabled=false},2500);
  })
  .catch(function(err){
    btn.textContent='Send to Claude'; btn.disabled=false;
    var txt=JSON.stringify(out,null,1);
    navigator.clipboard.writeText(txt).then(function(){
      toast('Could not reach the server ('+err.message+') — copied to your clipboard instead.');
    },function(){
      var b=new Blob([txt],{type:'application/json'}), a=document.createElement('a');
      a.href=URL.createObjectURL(b); a.download='review-comments.json'; a.click();
      toast('Could not reach the server — downloaded the file instead.');
    });
  });
};
paint();
"""


def relink(rendered, included):
    """Point cross-references at the section on this page, not the raw file.

    The pack links between files the way markdown should - [pages.md](pages.md).
    On GitHub that renders the file. In this single-page review it would hand
    the browser a .md to download, so every link looked broken. Rewrite only
    the ones whose target is actually on the page; anything else is left alone.
    """
    def sub(m):
        target = m.group(1)
        frag = m.group(2) or ""
        return ('href="#%s"' % target.replace(".", "-")) if target in included \
            else m.group(0)
    return re.sub(r'href="([A-Za-z0-9._-]+\.md)(#[^"]*)?"', sub, rendered)


def main():
    nav, body, missing = [], [], []
    included = {fn for _, items in GROUPS for fn, _, _ in items}
    for group, items in GROUPS:
        nav.append("<h2>%s</h2>" % html.escape(group))
        for fn, desc, kind in items:
            sid = fn.replace(".", "-")
            tag = ('<span class="tag t-new">NEW</span>' if kind == "new" else
                   '<span class="tag t-gen">GEN</span>' if kind == "gen" else "")
            nav.append('<a id="nav-%s" href="#%s">%s%s</a>' % (sid, sid, fn[:-3], tag))
            p = DOCS / fn
            if not p.exists():
                missing.append(fn)
                rendered = "<p><b>Missing:</b> docs/%s</p>" % html.escape(fn)
            else:
                rendered = relink(md(p.read_text(encoding="utf-8")), included)
            body.append(
                '<section id="%s"><div class="filehead">docs/%s &nbsp;—&nbsp; %s</div>'
                '<div class="inner md">%s</div></section>'
                % (sid, html.escape(fn), html.escape(desc), rendered))

    page = ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            "<title>Slipstream pack — review</title>\n<style>%s</style>\n</head>\n<body>\n"
            "<nav>%s</nav>\n<main>\n<div class=\"inner\" style=\"padding-bottom:0\">"
            "<div class=\"note\"><b>Review copy.</b> Rendered from the real files in "
            "<code>docs/</code>. Purple = new this session · green = generated from the "
            "catalogue. Turn on <b>Comment mode</b> (bottom right), click any paragraph, "
            "heading, list item or table row to comment, then <b>Send to Claude</b>.</div>"
            "</div>\n%s\n</main>\n"
            "<div id=\"bar\"><button id=\"tgl\">Comment mode</button>"
            "<span id=\"cnt\">0 comments</span>"
            "<button id=\"all\">View all</button>"
            "<button id=\"send\" disabled>Send to Claude</button></div>\n"
            "<div id=\"drawer\"><header>Comments<button id=\"close\">×</button></header>"
            "<div id=\"list\"></div></div>\n<div id=\"toast\"></div>\n"
            "<script>%s<\\/script>\n</body>\n</html>\n"
            % (CSS, "\n".join(nav), "\n".join(body), JS)).replace("<\\/script>", "</" + "script>")

    OUT.write_text(page, encoding="utf-8")
    print("Wrote %s (%.0f KB) from %d files%s"
          % (OUT.name, len(page) / 1024, sum(len(i) for _, i in GROUPS),
             "; MISSING: " + ", ".join(missing) if missing else ""))


if __name__ == "__main__":
    main()
