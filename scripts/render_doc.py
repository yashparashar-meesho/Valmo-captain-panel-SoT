#!/usr/bin/env python3
"""Render a markdown document as a readable page, serve it, and open it.

The DRD is written for a person to read and approve. Handing over a raw .md
is handing over the source of a document, not the document - it reads badly
and it makes approving it feel like reviewing a diff.

    python3 scripts/render_doc.py DRD.md            # render, serve, open
    python3 scripts/render_doc.py DRD.md --no-open  # render and serve only
    python3 scripts/render_doc.py DRD.md --html-only

Keeps the .md as the source: edit it and re-run. The page is standalone, so
it also works if you just double-click the HTML.
"""
import re
import subprocess
import sys
import webbrowser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from md_to_html import md  # noqa: E402

CSS = """
:root{--ink:#15202E;--ink2:#4E5A6B;--ink3:#8A94A3;--page:#FBFCFD;--surface:#fff;
--line:#E3E8EF;--accent:#2F6FED;--ok:#13874B;--warn:#B4541E;
--font:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,system-ui,sans-serif;
--mono:ui-monospace,SFMono-Regular,Menlo,monospace}
*{box-sizing:border-box}
body{margin:0;background:var(--page);color:var(--ink);font:17px/1.7 var(--font);
padding-block:0 120px}
.bar{position:sticky;top:0;z-index:5;background:rgba(251,252,253,.93);
backdrop-filter:blur(8px);border-bottom:1px solid var(--line);padding:13px 0}
.bar .in{max-width:760px;margin:0 auto;padding:0 28px;display:flex;align-items:center;
justify-content:space-between;gap:16px}
.bar .n{font:600 13px/1 var(--mono);color:var(--ink2)}
.bar .t{font:600 12px/1 var(--font);color:var(--ok);background:#E4F5EC;
border:1px solid #BFE6D2;border-radius:99px;padding:5px 11px}
main{max-width:760px;margin:0 auto;padding:16px 28px}
h1{font-size:34px;line-height:1.15;letter-spacing:-.022em;margin:.5em 0 .35em;text-wrap:balance}
h2{font-size:23px;letter-spacing:-.012em;margin:2em 0 .5em;padding-bottom:.28em;
border-bottom:1px solid var(--line)}
h3{font-size:18.5px;margin:1.7em 0 .35em}
h4{font-size:16px;margin:1.4em 0 .3em;color:var(--ink2)}
p{margin:.8em 0}
ul,ol{padding-left:1.4em;margin:.75em 0}li{margin:.38em 0}
code{background:#EEF1F6;padding:1.5px 6px;border-radius:4px;font:.84em var(--mono);color:#1F3C73}
pre{background:#121E2F;color:#DDE7F6;padding:16px 19px;border-radius:10px;overflow-x:auto;
font:13.5px/1.65 var(--mono);margin:1.1em 0}
pre code{background:none;color:inherit;padding:0;font-size:inherit}
table{border-collapse:collapse;width:100%;margin:1.2em 0;font-size:15px;display:block;
overflow-x:auto}
th,td{border:1px solid var(--line);padding:9px 12px;text-align:left;vertical-align:top}
th{background:#F2F5F9;font-size:11.5px;text-transform:uppercase;letter-spacing:.07em;
color:var(--ink3);font-weight:650;white-space:nowrap}
tr:nth-child(even) td{background:#FCFDFE}
blockquote{margin:1.2em 0;padding:.7em 1.2em;border-left:3px solid var(--accent);
background:#F3F8FF;color:#22405F;border-radius:0 7px 7px 0}
blockquote p{margin:.4em 0}
a{color:var(--accent)}
hr{border:0;border-top:1px solid var(--line);margin:2.2em 0}
strong{font-weight:650}
@media(max-width:700px){body{font-size:16px}main,.bar .in{padding-left:16px;padding-right:16px}}
"""


def render(src: Path) -> Path:
    text = src.read_text(encoding="utf-8")
    title = next((m.group(1).strip()
                  for m in re.finditer(r"^#\s+(.+)$", text, re.M)), src.stem)
    out = src.with_suffix(".html")
    out.write_text(
        "<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        "<title>%s</title>\n<style>%s</style>\n</head>\n<body>\n"
        "<div class=\"bar\"><div class=\"in\"><span class=\"n\">%s</span>"
        "<span class=\"t\">for review — say if it is good to go</span></div></div>\n"
        "<main>%s</main>\n</body>\n</html>\n"
        % (title, CSS, src.name, md(text)), encoding="utf-8")
    return out


def free_port(start=8300):
    import socket
    for p in range(start, start + 200):
        with socket.socket() as s:
            if s.connect_ex(("127.0.0.1", p)) != 0:
                return p
    raise SystemExit("no free port")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    if not args:
        sys.exit(__doc__)
    src = Path(args[0]).resolve()
    if not src.exists():
        sys.exit("no such file: %s" % src)

    out = render(src)
    print("rendered -> %s" % out)
    if "--html-only" in flags:
        return

    port = free_port()
    subprocess.Popen([sys.executable, "-m", "http.server", str(port)],
                     cwd=str(out.parent),
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    url = "http://localhost:%d/%s" % (port, out.name)

    # never hand over a link before it answers - one was given out once for a
    # server that never started, because the port was taken
    import time
    import urllib.request
    for _ in range(40):
        try:
            if urllib.request.urlopen(url, timeout=1).status == 200:
                break
        except Exception:
            time.sleep(0.15)
    else:
        sys.exit("served on %d but the page never returned 200" % port)

    print("serving  %s" % url)
    if "--no-open" not in flags:
        webbrowser.open(url)
        print("opened in your browser")


if __name__ == "__main__":
    main()
