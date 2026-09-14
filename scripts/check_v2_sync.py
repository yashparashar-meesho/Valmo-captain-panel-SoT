#!/usr/bin/env python3
"""Guard against the two files drifting while v2 is being designed.

source/flow-ledger.html is canonical: export_to_github.py reads the vp- kit and
the seed blob out of it. flow-ledger-v2.html is a design copy of the *chrome* only — its
kit CSS and seed data must stay byte-identical, or we would be maintaining two
design systems without noticing.

Run before committing either file:
    python3 scripts/check_v2_sync.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
V1, V2 = ROOT / "source" / "flow-ledger.html", ROOT / "source" / "flow-ledger-v2.html"
TAG = '<script id="seed-data" type="application/json">'
MARK = "/* ============ vp- component kit"


def parts(path):
    s = path.read_text(encoding="utf-8")
    i = s.find(MARK)
    if i == -1:
        sys.exit("%s: no vp- kit marker" % path.name)
    kit = s[i:s.find("</style>", i)]
    a = s.find(TAG)
    if a == -1:
        sys.exit("%s: no seed blob" % path.name)
    a += len(TAG)
    return kit, s[a:s.find("</script>", a)]


if not V2.exists():
    print("source/flow-ledger-v2.html not present — nothing to check.")
    sys.exit(0)

k1, b1 = parts(V1)
k2, b2 = parts(V2)
bad = []
if k1 != k2:
    bad.append("the vp- kit CSS differs (%d vs %d bytes) — the design system must "
               "live in one place; edit source/flow-ledger.html and re-copy the block" % (len(k1), len(k2)))
if b1 != b2:
    bad.append("the seed blob differs — regenerate v2's blob from source/data-seed.json")
for name, blob in (("v1", b1), ("v2", b2)):
    try:
        json.loads(blob)
    except ValueError as e:
        bad.append("%s seed blob does not parse: %s" % (name, e))

if bad:
    print("v1/v2 OUT OF SYNC:")
    for b in bad:
        print("  - " + b)
    sys.exit(1)
print("v1 and v2 agree: kit %d bytes, seed %d bytes, both parse." % (len(k1), len(b1)))
