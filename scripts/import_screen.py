#!/usr/bin/env python3
"""Fold an edited screen page back into the source, then rebuild the site.

The artefact a designer actually works on is a rendered screens/<id>.html - it is
what "Copy screen" hands them and what they open in a browser. The source of truth
is that same markup living as a JSON string in source/data-seed.json. This script
is the bridge, so nobody has to hand-paste HTML into JSON.

    python3 scripts/import_screen.py screens/payment-details.html

It extracts the page's body, turns the icon <img src> back into data-icon keys,
writes it into source/data-seed.json and the copy embedded in flow-ledger.html,
re-runs the export, and then proves the round trip: the screen it just wrote must
re-export byte-identically to the file you handed it.

Run it before committing. Commit the source change and the regenerated output
together - CI checks that they agree, and the Vercel preview only shows your
change if the generated files are in the PR.
"""
import base64
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE = ROOT / "source"
SEED = SOURCE / "data-seed.json"
LEDGERS = [SOURCE / "flow-ledger.html"]
TAG = '<script id="seed-data" type="application/json">'


def die(msg):
    sys.exit("import_screen: " + msg)


def extract_body(page, path):
    """Everything between <body> and the scripts the export appends."""
    i = page.find("<body>")
    if i == -1:
        die("%s has no <body> - is it an exported screen page?" % path)
    i += len("<body>")
    j = page.find("<script", i)
    if j == -1:
        j = page.find("</body>", i)
    if j == -1:
        die("%s has no closing </body>" % path)
    return page[i:j].strip()


def to_icon_keys(body, icons):
    """src="../assets/icons/<key>.<ext>"  ->  data-icon="<key>"

    The export maps the other way; the file stem is the key verbatim. An icon the
    catalog does not know about is a hard error rather than a silent pass-through,
    because it would export as an <img> with no src.
    """
    unknown = []

    def repl(m):
        key = Path(m.group(1)).stem
        if key not in icons:
            unknown.append(m.group(1))
        return 'data-icon="%s"' % key

    out = re.sub(r'src="\.\./assets/icons/([^"]+)"', repl, body)
    if unknown:
        die("these icons are not in the catalog: %s\n"
            "            add them to source/data-seed.json's icons map first"
            % ", ".join(sorted(set(unknown))))
    return out


def write_seed(data):
    text = json.dumps(data, indent=2, ensure_ascii=False)
    SEED.write_text(text, encoding="utf-8")
    blob = json.dumps(data, ensure_ascii=False, indent=2)
    if "</script>" in blob or "<script" in blob:
        die("the seed contains a literal script tag, which would close the "
            "seed-data element and break every page that embeds it")
    for p in LEDGERS:
        if not p.exists():
            continue
        s = p.read_text(encoding="utf-8")
        a = s.find(TAG)
        if a == -1:
            die("%s has no seed-data element" % p.name)
        a += len(TAG)
        b = s.find("</script>", a)
        p.write_text(s[:a] + "\n" + blob + "\n" + s[b:], encoding="utf-8")


def main():
    if len(sys.argv) < 2:
        die("usage: import_screen.py <screens/….html> [more…]")

    data = json.loads(SEED.read_text(encoding="utf-8"))
    icons = data.get("icons", {})
    by_id = {s["id"]: s for s in data["screens"]}

    changed = []
    for arg in sys.argv[1:]:
        path = Path(arg)
        if not path.exists():
            die("%s does not exist" % path)
        sid = path.stem
        if sid not in by_id:
            die("no screen with id %r in the catalog (known: %s)"
                % (sid, ", ".join(sorted(by_id))))
        body = to_icon_keys(extract_body(path.read_text(encoding="utf-8"), path), icons)
        if body == by_id[sid]["code"]:
            print("  %-30s unchanged" % sid)
            continue
        old = len(by_id[sid]["code"])
        by_id[sid]["code"] = body
        changed.append(sid)
        print("  %-30s updated (%d -> %d chars)" % (sid, old, len(body)))

    if not changed:
        print("Nothing to import.")
        return

    write_seed(data)
    print("Wrote source/data-seed.json and the embedded copies.")

    r = subprocess.run([sys.executable, str(HERE / "export_to_github.py")],
                       capture_output=True, text=True)
    if r.returncode:
        die("the export failed after import:\n" + (r.stderr or r.stdout))
    print(r.stdout.strip().splitlines()[0])

    # Round trip: what we just wrote must re-export to exactly what we were given.
    for sid in changed:
        produced = (ROOT / "screens" / (sid + ".html")).read_text(encoding="utf-8")
        given = Path([a for a in sys.argv[1:] if Path(a).stem == sid][0]).read_text(encoding="utf-8")
        if extract_body(produced, "generated") != extract_body(given, "given"):
            die("round trip failed for %s: the re-exported page does not match the "
                "file you gave me. Nothing was lost - source/ has your markup - but "
                "the export is not reproducing it, so investigate before committing." % sid)
    print("Round trip verified for: " + ", ".join(changed))
    print("\nCommit source/ and the regenerated files together, then open a PR.")


if __name__ == "__main__":
    main()
