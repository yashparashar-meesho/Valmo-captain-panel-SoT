#!/usr/bin/env python3
"""
Regenerate the Valmo-captain-panel-SoT GitHub mirror from data-seed.json.

Run this after editing flows/screens/components (data-seed.json is the source of
truth for this export; flow-ledger.html itself is only used to pull the current
kit.css and its own JS/shell for building index.html).

Usage:
    python3 scripts/export_to_github.py [output_dir]

    output_dir defaults to the repo root, which is also the deployed site.

Everything under source/ is authored; everything else at the root is generated.
After it finishes:
    git add -A && git commit -m "..." && git push

Design note — real files, not inline base64:
Every screen/component/index page references icons via a real, separate file
under assets/icons/ instead of embedding base64 text. Two reasons:
  1. These files are always opened through a local server (never raw file://
     double-click) per the pull-command instructions, so relative/absolute
     path references work fine — there's no need to inline for that.
  2. A repo full of ~100KB base64 blobs is slow to review in a PR, slow for
     the org's TruffleHog pre-commit secret scanner (long base64 text produces
     many false-positive "candidate secret" matches, each individually
     verified over the network), and just plain hard to read. Real small
     binary icon files avoid all of that and keep diffs meaningful.
"""
import json
import re
import sys
import base64
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
# Source and site live in the same repo now, so a contributor can change a screen
# and open a PR against the thing that actually drives the site. Inputs are under
# source/; everything else at the root is generated and should never be hand-edited.
SOURCE = PROJECT_ROOT / "source"
SEED_PATH = SOURCE / "data-seed.json"
FLOW_LEDGER_HTML = SOURCE / "flow-ledger.html"

EXT_MAP = {"image/svg+xml": "svg", "image/png": "png", "image/jpeg": "jpg"}

NAV_SCRIPT = """<script>
document.querySelectorAll("[data-goto]").forEach(function (el) {
  el.style.cursor = "pointer";
});
document.addEventListener("click", function (e) {
  var el = e.target.closest("[data-goto]");
  if (el) location.href = el.getAttribute("data-goto") + ".html";
});
/* These pages must be served over http://, not double-clicked open. On file:// Chrome
   refuses to load assets reached via ../ , so the map raster and every icon come up
   blank with no explanation. Rather than let that happen silently, say so on the page
   and give the exact command to fix it. */
if (location.protocol === "file:") {
  var b = document.createElement("div");
  b.setAttribute("style", [
    "position:fixed", "top:0", "left:0", "right:0", "z-index:99999",
    "background:#fdecec", "border-bottom:1px solid #f0b7b4", "color:#7a1c17",
    "font:500 13px/1.5 Inter,system-ui,sans-serif", "padding:10px 16px", "text-align:center"
  ].join(";"));
  b.innerHTML = "This page is open from a file, so the map and icons cannot load. " +
    "Serve the folder instead \\u2014 run <code style=\\"background:#fff;padding:1px 5px;" +
    "border-radius:3px;\\">python3 -m http.server 8000</code> in the folder that contains " +
    "<code style=\\"background:#fff;padding:1px 5px;border-radius:3px;\\">screens/</code>, " +
    "then open <code style=\\"background:#fff;padding:1px 5px;border-radius:3px;\\">" +
    "http://localhost:8000/screens/</code> and pick this file.";
  document.body.appendChild(b);
  document.body.style.paddingTop = "44px";
}
</script>"""

# Screens and components deliberately load NOTHING from the network. Mier B02 ships
# in assets/fonts and the kit carries a metrics-matched "Mier Fallback", so there is
# nothing left for a Google Fonts link to do except block first paint when the network
# is slow, proxied or absent. These pages now render fully offline.
FONTS = "<!-- no external fonts: Mier B02 is local, with a metric-matched fallback -->"

# Nothing here needs JS to render - the markup is static and the accordions are real
# <details> elements. This only stops a missing image from leaving a broken-image
# glyph in the layout: the box keeps its reserved size, so nothing shifts.
ROBUST_SCRIPT = """<script>
document.addEventListener("error", function (e) {
  var el = e.target;
  if (el && el.tagName === "IMG") { el.style.visibility = "hidden"; }
}, true);
</script>"""


def extract_kit_css():
    html = FLOW_LEDGER_HTML.read_text(encoding="utf-8")
    marker = "/* ============ vp- component kit"
    idx = html.find(marker)
    if idx == -1:
        raise SystemExit("Couldn't find the vp- component kit marker in flow-ledger.html")
    end = html.find("</style>", idx)
    return html[idx:end]


def build_index_html(out_dir, data, manifest):
    """The Flow Ledger catalog, with a lean icons manifest (paths, not base64)
    spliced in so the deployed index.html stays small and reviewable."""
    html = FLOW_LEDGER_HTML.read_text(encoding="utf-8")
    start_tag = '<script id="seed-data" type="application/json">'
    end_tag = "</script>"
    i = html.find(start_tag)
    if i == -1:
        raise SystemExit("Couldn't find the seed-data script tag in flow-ledger.html")
    i += len(start_tag)
    j = html.find(end_tag, i)

    web_seed = dict(data)
    # expandIcons() in flow-ledger.html just does src="<value>" verbatim — it
    # doesn't care whether the value is a data URI or a path, so handing it a
    # relative path here is all that's needed to make it reference the real
    # files instead of embedding them.
    web_seed["icons"] = {key: f"assets/icons/{fname}" for key, fname in manifest.items()}

    new_html = html[:i] + json.dumps(web_seed) + html[j:]
    (out_dir / "index.html").write_text(new_html, encoding="utf-8")


def main():
    out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else PROJECT_ROOT
    (out_dir / "assets" / "icons").mkdir(parents=True, exist_ok=True)
    (out_dir / "screens").mkdir(parents=True, exist_ok=True)
    (out_dir / "components").mkdir(parents=True, exist_ok=True)

    data = json.loads(SEED_PATH.read_text(encoding="utf-8"))
    icons = data.get("icons", {})
    screens = data["screens"]
    components = data["components"]

    kit_css = extract_kit_css()
    # kit.css sits in assets/, so fonts are one level nearer from there
    (out_dir / "assets" / "kit.css").write_text(
        kit_css.replace('url("assets/fonts/', 'url("fonts/'), encoding="utf-8")

    # Mier B02 ships as real font files, same as the icons - no base64 in the repo
    (out_dir / "assets" / "fonts").mkdir(parents=True, exist_ok=True)
    fonts_src = SOURCE / "assets" / "fonts"
    n_fonts = 0
    for f in sorted(fonts_src.glob("*.woff2")):
        (out_dir / "assets" / "fonts" / f.name).write_bytes(f.read_bytes())
        n_fonts += 1
    if not n_fonts:
        raise SystemExit("no fonts found in %s - the typography library needs them" % fonts_src)

    # Leaflet, vendored so the map screens need no CDN
    (out_dir / "assets" / "vendor").mkdir(parents=True, exist_ok=True)
    vendor_src = SOURCE / "assets" / "vendor"
    n_vendor = 0
    for f in sorted(vendor_src.glob("*")):
        if f.is_file():
            (out_dir / "assets" / "vendor" / f.name).write_bytes(f.read_bytes())
            n_vendor += 1

    # Every screen and component links assets/kit.css rather than inlining a copy.
    # Inlining made each page self-contained, but it also meant a one-line change to
    # a shared token rewrote all 34 pages: ~2MB of duplicated CSS in the repo, diffs
    # 36 files wide for a single rule, and a file history where half the commits
    # touching a screen never changed that screen. One sheet fixes all three. The
    # font URLs inside kit.css are already relative to assets/, which is where the
    # sheet lives, so they resolve unchanged from any depth.

    manifest = {}
    for key, uri in icons.items():
        header, b64 = uri.split(",", 1)
        mime = header.split(";")[0].replace("data:", "")
        ext = EXT_MAP.get(mime, "bin")
        raw = base64.b64decode(b64)
        fname = f"{key}.{ext}"
        (out_dir / "assets" / "icons" / fname).write_bytes(raw)
        manifest[key] = fname

    def expand_screen_code(code):
        def repl(m):
            fname = manifest.get(m.group(1))
            return f'src="../assets/icons/{fname}"' if fname else m.group(0)
        return re.sub(r'data-icon="([^"]+)"', repl, code)

    def expand_component_html(html):
        def repl(m):
            uri = m.group(1)
            for key, v in icons.items():
                if v == uri:
                    fname = manifest.get(key)
                    if fname:
                        return f'src="../assets/icons/{fname}"'
            return m.group(0)
        html = re.sub(r'src="(data:image/[a-zA-Z+]+;base64,[A-Za-z0-9+/=]+)"', repl, html)
        # Components may reference an icon the same way screens do, by key. Without
        # this those <img>s exported with no src at all and rendered broken.
        return expand_screen_code(html)

    def screen_page(screen):
        body = expand_screen_code(screen["code"])
        # Only the map screens pay for Leaflet, and it is served from assets/vendor so
        # the library itself needs no CDN. Tiles do need the network; when they cannot
        # be reached the baked raster underneath stays visible.
        maps = ""
        if 'class="vp-maparea"' in body:
            maps = ('<link rel="stylesheet" href="../assets/vendor/leaflet.css">\n'
                    '<script src="../assets/vendor/leaflet.js"></script>')
        return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>{screen['name']} — Valmo Partner</title>
{FONTS}
{maps}
<style>body{{margin:0;background:#eaeaf2;}}[data-goto]{{cursor:pointer;}}</style>
<link rel="stylesheet" href="../assets/kit.css">
</head>
<body>
{body}
{ROBUST_SCRIPT}
{NAV_SCRIPT}
{'<script src="../assets/vendor/sa-map.js"></script>' if maps else ''}
</body>
</html>
"""

    def component_page(comp):
        body = expand_component_html(comp["html"])
        return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>{comp['name']} — Valmo Partner component</title>
{FONTS}
<style>body{{margin:0;padding:24px;background:#eaeaf2;}}</style>
<link rel="stylesheet" href="../assets/kit.css">
</head>
<body>
<div class="vp-scope">
{body}
</div>
{ROBUST_SCRIPT}
</body>
</html>
"""

    for s in screens:
        (out_dir / "screens" / f"{s['id']}.html").write_text(screen_page(s), encoding="utf-8")
    for c in components:
        page = component_page(c)
        stray = re.findall(r'<img(?![^>]*\ssrc=)[^>]*>', page)
        if stray:
            raise SystemExit(
                "component %s exports an <img> with no src: %s" % (c["id"], stray[:2]))
        (out_dir / "components" / f"{c['id']}.html").write_text(page, encoding="utf-8")

    # Prune what the catalog no longer has. Without this the export only ever adds:
    # rename or retire a screen/component/icon and its old file stays behind forever,
    # so the repo accumulates ghosts that still look like real source of truth.
    def prune(subdir, keep):
        removed = []
        for f in sorted((out_dir / subdir).glob("*")):
            if f.is_file() and f.name not in keep:
                f.unlink()
                removed.append(f.name)
        return removed

    stale = (
        prune("screens", {f"{s['id']}.html" for s in screens})
        + prune("components", {f"{c['id']}.html" for c in components})
        + prune("assets/icons", set(manifest.values()))
    )
    if stale:
        print("Pruned %d file(s) no longer in the catalog: %s" % (len(stale), ", ".join(stale)))

    build_index_html(out_dir, data, manifest)

    flows = data["flows"]
    repo_manifest = {
        "flows": [
            {
                "id": f["id"],
                "name": f["name"],
                "description": f.get("description", ""),
                "screens": [
                    {"id": s["id"], "name": s["name"], "order": s.get("order", 0)}
                    for s in sorted(
                        [s for s in screens if s["flowId"] == f["id"]],
                        key=lambda s: s.get("order", 0),
                    )
                ],
            }
            for f in flows
        ],
        "components": [c["id"] for c in components],
    }
    (out_dir / "manifest.json").write_text(json.dumps(repo_manifest, indent=2), encoding="utf-8")

    print(f"Exported {n_vendor} vendor files, {len(screens)} screens, {len(components)} components, {len(manifest)} icons, {n_fonts} fonts, index.html -> {out_dir}")
    print("Next: cd", out_dir, "&& git add -A && git commit -m 'Sync from Flow Ledger' && git push")


if __name__ == "__main__":
    main()
