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
    ("A worked run", [
        (RUN / "BRIEF.md", "run-brief", "The brief", "run"),
        (RUN / "APPROACHES.md", "run-approaches", "The DRD", "run"),
    ]),
]
SLUGS = {p.name: slug for _, items in GROUPS for p, slug, _, _ in items}
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
    return 'href="../docs/%s.%s"' % (stem, ext)


def build():
    OUT.mkdir(exist_ok=True)
    rail, body = [], []
    for name, items in GROUPS:
        rail.append("<h4>%s</h4>" % name)
        for src, slug, label, tag in items:
            if not src.exists():
                sys.exit("missing: %s" % src)
            rail.append('<a href="#pack-%s" data-pack="%s">%s%s</a>' % (
                slug, slug, label,
                '<span class="packv-tag t-%s">%s</span>' % (tag, tag) if tag else ""))
            html = md(src.read_text(encoding="utf-8"))
            html = re.sub(r'href="([A-Za-z0-9._-]+)\.(md|html|svg)"', _link, html)
            html = re.sub(r'src="([a-z0-9.-]+\.svg)"', r'src="../docs/\1"', html)
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
