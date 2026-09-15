#!/usr/bin/env python3
"""The live ledger and data-seed.json must agree.

(The filename is historical: it once compared two ledgers while v2 was being
designed. v2 is now the only ledger — the name stays because
.github/workflows/verify.yml calls it by name.)

source/flow-ledger.html carries a copy of the catalog embedded in its seed-data
element, so the file still opens by double-click. That copy and source/data-seed.json
have to be written together — when they drifted once before, three icons silently
reverted and nothing noticed until the pages were opened. This is the guard.

    python3 scripts/check_v2_sync.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "source"
SEED = SOURCE / "data-seed.json"
LIVE = SOURCE / "flow-ledger.html"
TAG = '<script id="seed-data" type="application/json">'


def embedded(path):
    s = path.read_text(encoding="utf-8")
    a = s.find(TAG)
    if a == -1:
        sys.exit("%s: no seed-data element" % path.name)
    a += len(TAG)
    return s[a:s.find("</script>", a)]


def main():
    problems = []

    try:
        seed = json.loads(SEED.read_text(encoding="utf-8"))
    except ValueError as e:
        sys.exit("source/data-seed.json does not parse: %s" % e)

    blob = embedded(LIVE)
    try:
        inline = json.loads(blob)
    except ValueError as e:
        sys.exit("the seed embedded in flow-ledger.html does not parse: %s" % e)

    if inline != seed:
        problems.append(
            "flow-ledger.html's embedded catalog differs from data-seed.json — "
            "they must be written together. scripts/import_screen.py does this for you.")

    if any("css" in c for c in seed["components"]):
        problems.append(
            "a component carries its own copy of the kit again — that duplication was "
            "62%% of this file. The kit lives once, in flow-ledger.html's <style>.")

    if problems:
        print("SOURCE OUT OF SYNC:")
        for p in problems:
            print("  - " + p)
        sys.exit(1)

    print("Source is consistent: %d flows, %d screens, %d components, %d icons; "
          "the ledger's embedded copy matches data-seed.json."
          % (len(seed["flows"]), len(seed["screens"]),
             len(seed["components"]), len(seed["icons"])))


if __name__ == "__main__":
    main()
