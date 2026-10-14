#!/usr/bin/env python3
"""Render the docs/ pack as a fragment the Slipstream app loads: pack/content.html.

    python3 scripts/build_pack_pages.py            # -> pack/content.html
    python3 scripts/build_pack_pages.py --check    # fail if stale (CI)

GENERATED. Never hand-edit pack/content.html - edit the markdown in docs/
(or examples/capacity-cut/) and run this. The markdown is the source; a second
copy of a fact drifts.

This is a FRAGMENT, not a page. It is fetched by the Slipstream app and shown
as a view inside it, so the pack sits under the catalogue's real navigation
rather than a lookalike built beside it. An earlier version of this script
rendered its own shell and its own imitation of the rail - which is how the
pack ended up looking like a different product.

One scroll, every document a section, with a doc rail down the left: the shape
people actually read a reference in.
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
    ("Demo Run \u2014 Please check", [
        (RUN / "BRIEF.md", "run-brief", "1 \u00b7 The brief", "run"),
        (RUN / "APPROACHES.md", "run-approaches", "2 \u00b7 The DRD", "run"),
        (None, "run-shapes", "3 \u00b7 The wireframes", "run"),
    ]),
]
SLUGS = {p.name: slug for _, items in GROUPS for p, slug, _, _ in items if p}
ASSETS = {"flow.svg", "comparison-example.html", "wireframe-example.html",
          "promoted-example.html"}

CSS = """
<style>
.packv{display:flex;min-height:0;height:100%;--pl:#E2E7EE;--pm:#55606F;--p3:#8A94A3;
--pa:#2F6FED;--pmono:ui-monospace,SFMono-Regular,Menlo,monospace}
.packv-rail{width:258px;flex:none;background:#F5F7FA;border-right:1px solid var(--pl);
overflow-y:auto;padding:14px 0 40px}
.packv-rail h4{font:650 11px/1 var(--ui);letter-spacing:.09em;text-transform:uppercase;
color:var(--p3);margin:16px 20px 6px}
.packv-rail h4:first-child{margin-top:0}
.packv-rail a{display:block;padding:6px 20px;color:var(--pm);text-decoration:none;
font:400 14px/1.45 var(--ui);border-left:2px solid transparent}
.packv-rail a:hover{background:#EAEFF6;color:var(--ink)}
.packv-rail a.on{border-left-color:var(--pa);color:var(--ink);font-weight:600;background:#E8EFFC}
.packv-tag{font:700 9.5px/1 var(--ui);letter-spacing:.05em;padding:2px 5px;border-radius:3px;
margin-left:6px;vertical-align:1px}
.t-new{background:#EEE8FD;color:#7B5BD6}.t-gen{background:#DFF3E9;color:#0E7C53}
.t-run{background:#FBE8DA;color:#B2541A}
.packv-body{flex:1;min-width:0;overflow-y:auto;padding:0 0 110px;background:#fff}
.packv-lead{padding:30px 32px 10px;max-width:820px;margin:0 auto}
.packv-lead h1{font:650 29px/1.2 var(--display,var(--ui));margin:0 0 8px;color:var(--navy);
letter-spacing:-.02em}
.packv-lead p{color:var(--pm);margin:0 0 6px;font:400 14.5px/1.7 var(--ui)}
.packv-see{background:#FFF8EE;border:1px solid #F0DCBC;border-radius:9px;padding:11px 15px;
font:400 13.5px/1.6 var(--ui);margin:10px 0 0}
.packv-see a{color:#9A5A12;font-weight:600}
.packv sect{display:block;scroll-margin-top:0;border-bottom:1px solid var(--pl)}
.packv-file{position:sticky;top:0;background:rgba(255,255,255,.96);
border-bottom:1px solid var(--pl);padding:10px 32px;z-index:4;
font:600 12.5px/1.4 var(--pmono);color:var(--pm)}
.packv-file i{font-style:normal;color:var(--p3);font-weight:400}
.packv-in{max-width:820px;margin:0 auto;padding:28px 32px}
.packv-in h1{font:650 28px/1.2 var(--display,var(--ui));letter-spacing:-.02em;margin:.2em 0 .5em;
color:var(--navy)}
.packv-in h2{font:650 21px/1.3 var(--ui);margin:1.9em 0 .5em;padding-bottom:.25em;
border-bottom:1px solid var(--pl);color:var(--navy)}
.packv-in h3{font:650 17px/1.4 var(--ui);margin:1.6em 0 .4em}
.packv-in h4{font:650 15px/1.4 var(--ui);margin:1.4em 0 .3em}
.packv-in p,.packv-in li{font:400 15px/1.65 var(--ui);color:#242E3C}
.packv-in ul,.packv-in ol{padding-left:1.35em;margin:.7em 0}
.packv-in li{margin:.3em 0}
.packv-in code{background:#EFF2F6;padding:1.5px 6px;border-radius:4px;
font:.855em var(--pmono);color:#1F3C73}
.packv-in pre{background:#132033;color:#DCE6F5;padding:15px 18px;border-radius:9px;
overflow-x:auto;font:13px/1.6 var(--pmono);margin:1em 0;white-space:pre-wrap;
overflow-wrap:anywhere}
.packv-in pre code{background:none;color:inherit;padding:0;font-size:inherit}
.packv-in table{border-collapse:collapse;width:100%;margin:1.1em 0;font-size:14.5px;
display:block;overflow-x:auto}
.packv-in th,.packv-in td{border:1px solid var(--pl);padding:8px 11px;text-align:left;
vertical-align:top}
.packv-in th{background:#F5F7FA;font:650 12px/1.4 var(--ui);text-transform:uppercase;
letter-spacing:.06em;color:var(--p3);white-space:nowrap}
.packv-in tr:nth-child(even) td{background:#FBFCFE}
.packv-in blockquote{margin:1.1em 0;padding:.6em 1.1em;border-left:3px solid var(--pa);
background:#F4F8FF;color:#24405E;border-radius:0 6px 6px 0}
.packv-in blockquote p{margin:.35em 0}
.packv-in a{color:var(--pa)}
.packv-in hr{border:0;border-top:1px solid var(--pl);margin:2em 0}
.packv-in strong{font-weight:650}
.packv-in img{width:100%;height:auto;display:block;border:1px solid var(--pl);
border-radius:8px;background:#fff}
.packv-btn{display:inline-flex;align-items:center;gap:7px;background:#092D5E;color:#fff;
text-decoration:none;font:650 13.5px/1 var(--ui);padding:10px 16px;border-radius:9px;
margin:0 8px 8px 0}
.packv-btn:hover{background:#0B3A79;color:#fff}
.packv-btn.ghost{background:#fff;color:#092D5E;border:1px solid #C3CDDD}
.packv-btn.ghost:hover{background:#F5F7FA}
.packv-frame{width:100%;height:560px;border:1px solid var(--pl);border-radius:10px;
background:#fff;display:block;margin:4px 0 10px}
.packv-note{font:400 13px/1.6 var(--ui);color:var(--p3);margin:6px 0 0}
.packv-selfrun{margin:28px 0 0;padding:20px 22px;border:1px solid #DCE5F5;border-radius:12px;
background:linear-gradient(180deg,#F7F9FE 0%,#F1F5FC 100%)}
.packv-selfrun h3{margin:0 0 10px;font:650 17px/1.3 var(--ui);color:#092D5E}
.packv-selfrun ol{margin:0 0 14px;padding-left:20px}
.packv-selfrun li{margin:.4em 0}
.packv-dl{margin:0;display:flex;flex-wrap:wrap}
.packv-fig{margin:0 0 22px;padding:0;cursor:zoom-in}
.packv-fig img{width:100%;height:auto;display:block;border:1px solid var(--pl);
border-radius:10px;background:#fff}
.packv-fig figcaption{font:400 12.5px/1.6 var(--ui);color:var(--p3);text-align:center;
margin-top:7px}
.packv-zoom{position:fixed;inset:0;z-index:90;background:rgba(10,30,60,.82);
display:flex;flex-direction:column;padding:18px;cursor:zoom-out}
.packv-zoom img{flex:1;min-height:0;width:100%;object-fit:contain}
.packv-zoom .x{align-self:flex-end;background:#fff;border:0;border-radius:8px;
font:650 13px/1 var(--ui);padding:9px 14px;cursor:pointer;margin-bottom:12px;color:#0A1E3C}
@media(max-width:900px){.packv-rail{display:none}}
</style>
"""

GH = ("https://github.com/yashparashar-meesho/"
      "Valmo-captain-panel-SoT/tree/main/docs")


def _link(m):
    """A cross-reference, resolved once: in-pack links become anchors."""
    stem, ext = m.group(1), m.group(2)
    if ext == "md":
        slug = SLUGS.get(stem + ".md")
        return 'href="#pack-%s"' % slug if slug else 'href="%s/%s.md"' % (GH, stem)
    return 'href="docs/%s.%s"' % (stem, ext)


DRD_MD = "examples/capacity-cut/APPROACHES.md"
BRIEF_MD = "examples/capacity-cut/BRIEF.md"

# The wireframes are a page, not a document, so the step shows the real thing
# rather than describing it. Someone judging the method needs to see what it
# produced, and a link alone gets skipped.
WIREFRAME_SECTION = (
    '<sect id="pack-run-shapes">'
    '<div class="packv-file">examples/capacity-cut/shapes.html '
    '<i>&mdash; 3 \u00b7 The wireframes</i></div>'
    '<div class="packv-in">'
    '<h1>The wireframes</h1>'
    '<p>Step 3. All five approaches drawn as schematics on one page, each beside '
    'the captain\u2019s journey and the situations it can show. This is where a '
    'shape chosen from a paragraph either survives being looked at or does not.</p>'
    '<p><a class="packv-btn" href="pack/run/shapes.html" target="_blank" '
    'rel="noopener">Open full size \u2197</a></p>'
    '<iframe class="packv-frame" src="pack/run/shapes.html" loading="lazy" '
    'title="The five approaches drawn as schematics"></iframe>'
    '<p class="packv-note">The final design is deliberately not here. Every step '
    'up to it is, so the method can be judged on its working rather than its '
    'result.</p>'
    '</div></sect>')

# What to do to run one yourself, attached to the DRD because that is the
# artefact people will want to copy the shape of.
SELF_RUN = (
    '<div class="packv-selfrun">'
    '<h3>Run one yourself</h3>'
    '<ol>'
    '<li><b>Install the skill</b> \u2014 one line, in <a href="?view=learn">Start now</a>. '
    'It needs Claude Code and nothing else.</li>'
    '<li><b>Describe the problem</b> in a new chat, or paste a KRD. Not a command, '
    'just the problem \u2014 <i>\u201cCaptains have no way to see which of their pilots '
    'are idle right now.\u201d</i></li>'
    '<li><b>Answer what it asks.</b> It separates questions about the KRD from '
    'decisions that are yours. Everything you answer goes back into the brief and '
    'the DRD.</li>'
    '<li><b>Approve the DRD before anything is built.</b> That gate is the whole '
    'method; the documents above are what it hands you.</li>'
    '</ol>'
    '<p class="packv-dl">'
    '<a class="packv-btn" href="%s" download>\u2193 Download this DRD (.md)</a>'
    '<a class="packv-btn ghost" href="%s" download>\u2193 Download the brief (.md)</a>'
    '</p>'
    '<p class="packv-note">Markdown, as produced. Open them beside your own run to '
    'see the shape each step should take.</p>'
    '</div>' % (DRD_MD, BRIEF_MD))


def inject_diagram(html):
    """The method diagram, where the index explains what each file answers.

    It is the same drawing design-method.md carries. Repeating it here is not
    duplication - it is generated from the same file - and it is the one thing
    that makes the list of documents read as a sequence rather than a shelf.
    """
    fig = ('<figure class="packv-fig" data-zoom="docs/flow.svg">'
           '<img src="docs/flow.svg" alt="The four sections of the method, '
           'their gates, and where the one blocking stop is">'
           '<figcaption>The method, end to end. Tap to open it full size.</figcaption>'
           '</figure>')
    marker = "<h2>Which file answers which question</h2>"
    return html.replace(marker, fig + marker, 1) if marker in html else fig + html


def build():
    OUT.mkdir(exist_ok=True)
    rail, body = [], []
    for name, items in GROUPS:
        rail.append("<h4>%s</h4>" % name)
        for src, slug, label, tag in items:
            rail.append('<a href="#pack-%s" data-pack="%s">%s%s</a>' % (
                slug, slug, label,
                '<span class="packv-tag t-%s">%s</span>' % (tag, tag) if tag else ""))
            if src is None:                       # the wireframe sheet, not markdown
                body.append(WIREFRAME_SECTION)
                continue
            if not src.exists():
                sys.exit("missing: %s" % src)
            html = md(src.read_text(encoding="utf-8"))
            html = re.sub(r'href="([A-Za-z0-9._-]+)\.(md|html|svg)"', _link, html)
            html = re.sub(r'src="([a-z0-9.-]+\.svg)"', r'src="docs/\1"', html)
            if slug == "readme":
                html = inject_diagram(html)
            if slug == "run-approaches":
                html += SELF_RUN
            body.append(
                '<sect id="pack-%s"><div class="packv-file">%s <i>&mdash; %s</i></div>'
                '<div class="packv-in">%s</div></sect>'
                % (slug, src.relative_to(ROOT).as_posix(), label, html))

    frag = (CSS +
        '<div class="packv">'
        '<nav class="packv-rail">%s</nav>'
        '<div class="packv-body">'
        '<div class="packv-lead"><h1>The pack</h1>'
        '<p>Everything the design method reads on every run \u2014 the same documents '
        'a person can read. Generated from <code>docs/</code>; edit the markdown '
        'there, never this page. Every file is in '
        '<a href="%s" target="_blank" rel="noopener">the docs folder on GitHub</a> '
        'if you want to read or download the originals.</p>'
        '<p class="packv-see">The worked run ends in a comparison sheet: '
        '<a href="pack/run/shapes.html" target="_blank" rel="noopener">'
        'see the five shapes drawn</a>.</p></div>'
        '%s</div></div>' % ("".join(rail), GH, "".join(body)))

    shapes = (RUN / "shapes.html").read_text(encoding="utf-8")
    written = {"content.html": frag, "run/shapes.html": shapes}
    stale = [n for n, h in written.items()
             if not (OUT / n).exists() or (OUT / n).read_text(encoding="utf-8") != h]

    if "--check" in sys.argv:
        if stale:
            sys.exit("pack/ is stale: %s\nRun: python3 scripts/build_pack_pages.py"
                     % ", ".join(sorted(stale)))
        print("pack/ is current: %d documents" % len(SLUGS))
        return
    for n, h in written.items():
        t = OUT / n
        t.parent.mkdir(parents=True, exist_ok=True)
        t.write_text(h, encoding="utf-8")
    # the standalone page this replaced - one source of truth, not two
    old = OUT / "index.html"
    if old.exists():
        old.unlink()
    print("Wrote pack/content.html: %d documents, %d stale" % (len(SLUGS), len(stale)))


build()
