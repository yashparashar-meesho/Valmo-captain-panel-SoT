#!/usr/bin/env python3
"""Render the docs/ pack as readable pages on the site, under pack/.

    python3 scripts/build_pack_pages.py            # -> pack/*.html
    python3 scripts/build_pack_pages.py --check    # fail if stale (CI)

GENERATED. Never hand-edit pack/*.html - edit the markdown in docs/ and run
this. The pack is the source; these pages are a reading surface for people who
do not want to read raw markdown on GitHub. A second copy of a fact drifts,
so nothing here is written by hand.

Links between documents are rewritten from .md to .html. The three worked
examples and flow.svg are already HTML or SVG and are linked, not converted.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from md_to_html import md  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUT = ROOT / "pack"

# order, title, blurb - mirrors docs/README.md's own grouping
GROUPS = [
    ("Start here", [
        ("panel-principles", "Who the captain is", "The person and the product, and what the live panel already gets wrong."),
        ("design-method", "The design method", "How a problem becomes a page. Four sections, one gate."),
        ("never-do-this", "Never do this", "Every line cost someone real time at least once."),
    ]),
    ("Building a page", [
        ("page-framework", "Page framework", "What a page is made of."),
        ("layout-rules", "Layout rules", "How wide, how tall, what scrolls."),
        ("section-rules", "Section rules", "A new section, or bake it into one that exists."),
    ]),
    ("What already exists", [
        ("pages", "Pages", "Every screen built so far, and what it is for. Generated."),
        ("components", "Components", "The component inventory. Generated."),
    ]),
    ("Foundations", [
        ("color-foundation", "Colour", "Which colour, and the token for it."),
        ("spacing-foundation", "Spacing", "Which spacing token."),
        ("typography-audit", "Typography", "Which type style."),
        ("fidelity-checklist", "Fidelity checklist", "Does it match live?"),
    ]),
]
# the worked run - source markdown lives in examples/capacity-cut/
RUN = ROOT / "examples" / "capacity-cut"
RUN_OUT = OUT / "run"
RUN_PAGES = [
    ("BRIEF", "The brief", "The problem pinned down: constraints, success tests, and the seven situations."),
    ("APPROACHES", "The DRD", "Five approaches on the axes, each with the captain's journey and the case for it."),
]

EXTRAS = [
    ("../docs/flow.svg", "The method diagram", "The four sections at a glance."),
    ("../docs/comparison-example.html", "A comparison sheet", "Five approaches drawn as schematics. The worked standard."),
    ("../docs/wireframe-example.html", "A wireframe", "Grey only, on the real skeleton."),
    ("../docs/promoted-example.html", "A promoted design", "Crystal colour, real components."),
]

CSS = """
*{box-sizing:border-box}
:root{--ink:#1A1A1F;--mute:#6B6B76;--line:#E6E6EC;--bg:#F4F4F7;--card:#fff;--acc:#2F6BFF}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.65 -apple-system,BlinkMacSystemFont,
 "Segoe UI",Roboto,sans-serif;-webkit-font-smoothing:antialiased}
.bar{background:var(--card);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:5}
.bar .in{max-width:860px;margin:0 auto;padding:13px 24px;display:flex;gap:12px;align-items:baseline;
 flex-wrap:wrap}
.bar a{color:var(--acc);text-decoration:none;font-weight:600;font-size:13px}
.bar a:hover{text-decoration:underline}
.bar .n{font-weight:700;font-size:13px}
.bar .t{color:var(--mute);font-size:12px;margin-left:auto}
main{max-width:860px;margin:0 auto;padding:34px 24px 90px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:30px 34px}
h1{font-size:30px;line-height:1.2;margin:0 0 6px;letter-spacing:-.02em}
h2{font-size:21px;margin:2.1em 0 .5em;letter-spacing:-.01em}
h3{font-size:16px;margin:1.8em 0 .4em}
h4{font-size:14px;margin:1.5em 0 .3em;color:var(--mute)}
p,li{font-size:15px}
code{background:#F0F0F4;border-radius:4px;padding:1px 5px;font-size:13px;
 font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
pre{background:#1A1A1F;color:#E8E8EF;padding:14px 16px;border-radius:9px;overflow-x:auto}
pre code{background:none;color:inherit;padding:0}
table{border-collapse:collapse;width:100%;margin:1.1em 0;display:block;overflow-x:auto}
th,td{border-bottom:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top;
 font-size:14px}
th{color:var(--mute);font-weight:600;white-space:nowrap}
blockquote{margin:1.2em 0;padding:2px 0 2px 16px;border-left:3px solid var(--line);color:var(--mute)}
hr{border:0;border-top:1px solid var(--line);margin:2.2em 0}
a{color:var(--acc)}
strong{font-weight:650}
.lede{color:var(--mute);margin:0 0 26px;font-size:15px}
.grp{margin:0 0 30px}
.grp h2{font-size:12px;text-transform:uppercase;letter-spacing:.07em;color:var(--mute);
 margin:0 0 10px}
.rows{display:grid;gap:9px}
.row{display:block;background:var(--card);border:1px solid var(--line);border-radius:10px;
 padding:13px 16px;text-decoration:none;color:inherit}
.row:hover{border-color:#C9C9D4}
.row b{display:block;font-size:15px;margin-bottom:2px}
.row span{color:var(--mute);font-size:13.5px}
.nxt{display:flex;justify-content:space-between;gap:12px;margin-top:26px;font-size:13px}
@media(max-width:700px){body{font-size:16px}main,.bar .in{padding-left:16px;padding-right:16px}
 .card{padding:22px 18px}}
"""

ASSETS = {"flow.svg", "comparison-example.html", "wireframe-example.html",
          "promoted-example.html"}


def _link(m):
    """A cross-reference inside the pack, resolved exactly once."""
    stem, ext = m.group(1), m.group(2)
    if ext == "md":
        return 'href="%s.html"' % stem            # another page here
    return 'href="../docs/%s.%s"' % (stem, ext)   # a worked example or the svg


def shell(title, crumb, body, foot=""):
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<title>%s</title>\n<style>%s</style>\n</head>\n<body>\n'
            '<div class="bar"><div class="in">%s</div></div>\n'
            '<main>%s%s</main>\n</body>\n</html>\n'
            % (title, CSS, crumb, body, foot))

def build():
    OUT.mkdir(exist_ok=True)
    flat = [(s, t) for _, items in GROUPS for s, t, _ in items]
    written = {}

    for i, (slug, title) in enumerate(flat):
        src = DOCS / (slug + ".md")
        if not src.exists():
            sys.exit("missing: %s" % src)
        text = src.read_text(encoding="utf-8")
        body = md(text)
        # One pass, not two. Rewriting .md -> .html first and then redirecting
        # .html links at docs/ sent every cross-reference to a file that does
        # not exist, because the second rule matched what the first had just
        # written. Each link is now decided once.
        body = re.sub(r'href="([a-z0-9-]+)\.(md|html|svg)"', _link, body)
        nav = []
        if i:
            nav.append('<a href="%s.html">&larr; %s</a>' % (flat[i - 1][0], flat[i - 1][1]))
        else:
            nav.append("<span></span>")
        if i < len(flat) - 1:
            nav.append('<a href="%s.html">%s &rarr;</a>' % (flat[i + 1][0], flat[i + 1][1]))
        crumb = ('<a href="index.html">The pack</a><span class="n">%s</span>'
                 '<span class="t">generated from docs/%s.md</span>' % (title, slug))
        written[slug + ".html"] = shell(
            title + " — Slipstream", crumb,
            '<div class="card">%s</div>' % body,
            '<div class="nxt">%s</div>' % "".join(nav))

    rows = ""
    for name, items in GROUPS:
        rows += '<div class="grp"><h2>%s</h2><div class="rows">' % name
        for slug, title, blurb in items:
            rows += ('<a class="row" href="%s.html"><b>%s</b><span>%s</span></a>'
                     % (slug, title, blurb))
        rows += "</div></div>"
    rows += ('<div class="grp"><h2>A whole run</h2><div class="rows">'
             '<a class="row" href="run/index.html"><b>Capacity Cut for Latent</b>'
             '<span>Every artefact from one real pass of the method, in order.</span></a>'
             '</div></div>')
    rows += '<div class="grp"><h2>Worked examples</h2><div class="rows">'
    for href, title, blurb in EXTRAS:
        rows += '<a class="row" href="%s"><b>%s</b><span>%s</span></a>' % (href, title, blurb)
    rows += "</div></div>"

    written["index.html"] = shell(
        "The pack — Slipstream",
        '<a href="../index.html">Slipstream</a><span class="n">The pack</span>'
        '<span class="t">generated from docs/</span>',
        '<h1>The pack</h1><p class="lede">The documents the design method reads on every '
        'run — the same ones a person can read. Generated from <code>docs/</code>; '
        'edit the markdown there, never these pages.</p>' + rows)

    # --- the worked run -------------------------------------------------
    RUN_OUT.mkdir(parents=True, exist_ok=True)
    run_written = {}
    for j, (stem, title, blurb) in enumerate(RUN_PAGES):
        src = RUN / (stem + ".md")
        if not src.exists():
            sys.exit("missing: %s" % src)
        body = md(src.read_text(encoding="utf-8"))
        nav = []
        if j:
            nav.append('<a href="%s.html">&larr; %s</a>'
                       % (RUN_PAGES[j - 1][0].lower(), RUN_PAGES[j - 1][1]))
        else:
            nav.append('<a href="index.html">&larr; The run</a>')
        nxt = (RUN_PAGES[j + 1][0].lower(), RUN_PAGES[j + 1][1]) if j < len(RUN_PAGES) - 1 \
            else ("shapes", "The shapes")
        nav.append('<a href="%s.html">%s &rarr;</a>' % nxt)
        crumb = ('<a href="../index.html">The pack</a>'
                 '<a href="index.html">Capacity Cut</a><span class="n">%s</span>'
                 '<span class="t">as produced, not tidied afterwards</span>' % title)
        run_written["run/" + stem.lower() + ".html"] = shell(
            title + " \u2014 Capacity Cut", crumb,
            '<div class="card">%s</div>' % body,
            '<div class="nxt">%s</div>' % "".join(nav))

    steps = ""
    for stem, title, blurb in RUN_PAGES:
        steps += ('<a class="row" href="%s.html"><b>%s</b><span>%s</span></a>'
                  % (stem.lower(), title, blurb))
    steps += ('<a class="row" href="shapes.html"><b>The shapes</b><span>All five drawn '
              'as schematics, every shape marked against every situation.</span></a>')
    run_written["run/index.html"] = shell(
        "Capacity Cut for Latent \u2014 a worked run",
        '<a href="../index.html">The pack</a><span class="n">Capacity Cut for Latent</span>'
        '<span class="t">a whole run, in order</span>',
        '<h1>Capacity Cut for Latent</h1><p class="lede">Every artefact from one real pass '
        'of the design method, kept as it was produced rather than tidied afterwards. Read '
        'them in order \u2014 each is checked against the one before it, which is the point: '
        'an approach that contradicts the brief is caught because the brief was written '
        'down first.</p><div class="grp"><div class="rows">%s</div></div>' % steps)

    written.update(run_written)
    written["run/shapes.html"] = (RUN / "shapes.html").read_text(encoding="utf-8")

    stale = [n for n, html_ in written.items()
             if not (OUT / n).exists() or (OUT / n).read_text(encoding="utf-8") != html_]
    if "--check" in sys.argv:
        if stale:
            sys.exit("pack/ is stale: %s\nRun: python3 scripts/build_pack_pages.py"
                     % ", ".join(sorted(stale)))
        print("pack/ is current: %d pages" % len(written))
        return
    for n, html_ in written.items():
        t = OUT / n
        t.parent.mkdir(parents=True, exist_ok=True)
        t.write_text(html_, encoding="utf-8")
    print("Wrote %d pages to pack/ (%d stale)" % (len(written), len(stale)))

build()
