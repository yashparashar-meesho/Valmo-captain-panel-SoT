#!/usr/bin/env python3
"""Serve the repo for review, and accept comments back from docs-preview.html.

`python3 -m http.server` only does GET, so the review page had no way to hand
anything back - comments would have to be copied out by hand. This adds one
endpoint:

    POST /_comments   body: the comment list as JSON
                      -> writes review-comments.json at the repo root

which Claude can then read directly. Everything else behaves exactly like the
plain static server.

    python3 scripts/review_server.py [port]      # default 8777
"""
import json
import sys
from datetime import datetime
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "review-comments.json"
MAX = 2 * 1024 * 1024


class Handler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path.rstrip("/") != "/_comments":
            self.send_error(404)
            return
        count = 0
        try:
            n = int(self.headers.get("Content-Length") or 0)
            if n <= 0 or n > MAX:
                raise ValueError("body is %d bytes" % n)
            payload = json.loads(self.rfile.read(n).decode("utf-8"))
            if not isinstance(payload, dict) or "comments" not in payload:
                raise ValueError("expected an object with a 'comments' key")
            payload["receivedAt"] = datetime.now().astimezone().isoformat(timespec="seconds")
            OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
            count = len(payload.get("comments") or [])
            body = json.dumps({"ok": True, "count": count, "file": OUT.name}).encode()
            self.send_response(200)
        except Exception as e:                       # noqa: BLE001 - report, never crash the review
            body = json.dumps({"ok": False, "error": str(e)}).encode()
            self.send_response(400)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        print("  -> %s (%d comment(s))" % (OUT.name, count))

    def end_headers(self):
        # the review page is edited and rebuilt constantly; a cached copy is
        # always the wrong one, and chasing it with ?v=N by hand got old fast
        self.send_header("Cache-Control", "no-store, must-revalidate")
        super().end_headers()

    def log_message(self, fmt, *args):
        if "_comments" in (args[0] if args else ""):
            super().log_message(fmt, *args)


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8777
    srv = ThreadingHTTPServer(("127.0.0.1", port),
                              partial(Handler, directory=str(ROOT)))
    print("Review server on http://localhost:%d" % port)
    print("  page     http://localhost:%d/docs-preview.html" % port)
    print("  comments POST /_comments -> %s" % OUT)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")


if __name__ == "__main__":
    main()
