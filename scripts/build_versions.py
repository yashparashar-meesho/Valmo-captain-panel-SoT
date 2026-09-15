#!/usr/bin/env python3
"""Build versions.json — the per-screen and per-flow history the ledger shows.

Why this is baked at build time rather than read from the GitHub API at runtime:
the unauthenticated API allows 60 requests an hour per IP, and answering "what
are this screen's versions" needs one call per commit to diff the content. One
screen would exhaust the budget. Baking it also means the history keeps working
offline and after the repo goes private again.

What counts as a version. Not every commit that touched the file: every screen
inlines the sidebar, so a nav change rewrites all seven, and until recently they
inlined the kit too. A commit is a version of a screen only if it changed that
screen's own content region — everything from <div class="vp-content onward.
Measured on real history, that drops a little over half the entries.

    python3 scripts/build_versions.py [--since <sha>]

--since sets the cutoff. The base-setup phase rewrote everything repeatedly and
those entries say nothing about a screen's design; pass the commit where the base
settled and history starts there.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEED = ROOT / "source" / "data-seed.json"
OUT = ROOT / "versions.json"


def git(*args):
    r = subprocess.run(["git", "-C", str(ROOT)] + list(args),
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit("git %s failed:\n%s" % (" ".join(args), r.stderr.strip()))
    return r.stdout


def scope_of(sha):
    """How wide was this commit? A change that touched one screen is about that
    screen; one that touched every screen is a sweep - the sidebar, a foundation,
    the export. Both are real history, but they are not the same kind of entry,
    and a reader deserves to be told which they are looking at."""
    files = git("show", "--name-only", "--format=", sha).split()
    n = len([f for f in files if f.startswith("screens/")])
    if n <= 1:
        return "screen"
    if n <= 3:
        return "module"
    return "sweep"


def content_of(blob):
    """The screen's own content, without the chrome every screen shares."""
    i = blob.rfind("</style>")
    if i == -1:
        i = blob.find("<body>")
    body = blob[i:] if i > -1 else blob
    m = re.search(r'<div class="vp-content.*', body, re.S)
    content = m.group(0) if m else body
    # Stop before the scripts the exporter appends to every page - the image
    # fallback, the navigation handler, and on map screens the Leaflet tag.
    # They are shared boilerplate, so a change to them touches all seven files
    # at once; counting that as a change to each screen is how a history fills
    # up with commits that never altered the screen you are looking at, which
    # is the thing this file exists to avoid. Screen markup may not contain a
    # script tag (the seed forbids it), so the first one is always the
    # exporter's.
    j = content.find("<script")
    return content[:j] if j > -1 else content


def history_for(path, since=None):
    rng = ("%s..HEAD" % since) if since else "HEAD"
    log = git("log", "--format=%H\x1f%cI\x1f%s", rng, "--", path).strip()
    if not log:
        return []
    rows = [l.split("\x1f") for l in log.splitlines()]
    out, prev = [], None
    for sha, date, subject in reversed(rows):          # oldest first
        try:
            blob = git("show", "%s:%s" % (sha, path))
        except SystemExit:
            continue
        cur = content_of(blob)
        if cur != prev:
            out.append({"sha": sha, "short": sha[:7], "date": date[:10],
                        "subject": subject, "scope": scope_of(sha)})
        prev = cur
    out.reverse()                                       # newest first
    return out


def ledger_history():
    """The catalog's own evolution — commits that changed the ledger UI itself.

    The file was called flow-ledger-v2.html while it was being designed and became
    flow-ledger.html when it was promoted, so --follow is what keeps the two halves
    of the story joined up. Nothing is stored: an old index.html is self-contained,
    so the ledger fetches it from git and runs it in a frame.
    """
    log = git("log", "--follow", "--format=%H\x1f%cI\x1f%s",
              "--", "source/flow-ledger.html").strip()
    if not log:
        return []
    out = []
    for line in log.splitlines():
        sha, date, subject = line.split("\x1f")
        out.append({"sha": sha, "short": sha[:7], "date": date[:10], "subject": subject})
    return out


def main():
    since = None
    if "--since" in sys.argv:
        since = sys.argv[sys.argv.index("--since") + 1]

    seed = json.loads(SEED.read_text(encoding="utf-8"))
    screens, flows = {}, {}

    for s in seed["screens"]:
        path = "screens/%s.html" % s["id"]
        screens[s["id"]] = history_for(path, since)

    for f in seed["flows"]:
        ids = [s["id"] for s in seed["screens"] if s["flowId"] == f["id"]]
        seen = {}
        for sid in ids:
            for v in screens[sid]:
                seen.setdefault(v["sha"], v)
        flows[f["id"]] = sorted(seen.values(), key=lambda v: v["date"], reverse=True)

    ledger = ledger_history()

    head = git("rev-parse", "HEAD").strip()
    OUT.write_text(json.dumps(
        {"head": head[:7], "since": since, "screens": screens, "flows": flows,
         "ledger": ledger},
        indent=2), encoding="utf-8")

    print("versions.json written (cutoff: %s)\n" % (since or "none — full history"))
    for sid, vs in screens.items():
        print("  %-30s %2d versions" % (sid, len(vs)))
    print()
    for fid, vs in flows.items():
        print("  %-30s %2d versions" % (fid + " (flow)", len(vs)))
    print()
    print("  %-30s %2d versions" % ("the ledger itself", len(ledger)))


if __name__ == "__main__":
    main()
