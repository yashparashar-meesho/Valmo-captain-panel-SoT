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
import re
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

    # A screen's code is markup. Behaviour is vendored under assets/vendor and pulled
    # in per screen by the exporter and the ledger, the way sa-map.js and
    # dc-capacity.js are — one home to fix it in, and a seed that stays reviewable.
    # This also keeps a literal "</script>" out of the seed, which rides inside a
    # <script> element and would be closed early by one. That surfaces as an
    # unterminated-JSON error two checks up, which says nothing about the real cause.
    # Small inline handlers (onclick=) are long-standing here and are not covered.
    scripted = [s["id"] for s in seed["screens"] if "<script" in s.get("code", "")]
    if scripted:
        problems.append(
            "these screens carry a <script> in their code: %s. Move the behaviour to "
            "source/assets/vendor/<name>.js and have the exporter and "
            "screenIframeDoc() pull it in when the screen needs it."
            % ", ".join(scripted))

    # VENDOR_RULES names the behaviour files a screen's markup pulls in. A name in
    # that table with no file behind it 404s in the browser with nothing on screen to
    # say so - the page renders perfectly and its inputs never respond. Cheap to check
    # here, invisible everywhere else.
    m = re.search(r"var VENDOR_RULES = (\[.*?\]);", LIVE.read_text(encoding="utf-8"), re.S)
    if not m:
        problems.append("flow-ledger.html no longer has a VENDOR_RULES table; the exporter "
                        "reads it out of that file and will fail.")
    else:
        for r in json.loads(m.group(1)):
            for f in r["head"] + r["tail"]:
                if not (SOURCE / "assets" / "vendor" / f).exists():
                    problems.append("VENDOR_RULES names %s, but source/assets/vendor/%s "
                                    "does not exist." % (f, f))

    # Every module in the rail must be reachable from every screen. The rail is
    # copied into each screen's markup, so adding a module means editing eleven
    # files - DC Capacity shipped wired on its own screen only, and from anywhere
    # else the new module simply did not exist. Rather than hardcode the module
    # list here, compare the screens against each other: a rail entry that is a
    # link on one screen and dead on another is the bug, whatever the module.
    NAV = re.compile(r'<div class="vp-navitem[^"]*"(?P<goto>\s+data-goto="[^"]*")?[^>]*>'
                     r'.*?<span class="lbl">(?P<label>[^<]*)</span>', re.S)
    linked, dead = set(), {}
    for s in seed["screens"]:
        for m in NAV.finditer(s.get("code", "")):
            label = m.group("label").strip()
            if m.group("goto"):
                linked.add(label)
            else:
                dead.setdefault(label, []).append(s["id"])
    for label in sorted(linked & set(dead)):
        problems.append(
            "the rail item %r links to a module on some screens but is dead on: %s. "
            "Every module we have built has to be reachable from every screen - "
            "someone in fullscreen cannot go back to switch. Add data-goto to the "
            "<div class=\"vp-navitem\"> for it there too."
            % (label, ", ".join(dead[label])))

    # versions.json is the one generated file git history feeds rather than
    # source/, so the reproducible-export check cannot police it. It froze once
    # already - three merges went by with the catalogue still reporting five
    # versions - so say plainly when it is behind. Not fatal: during a pull
    # request it is *always* behind by that branch's own commits, and the
    # post-merge workflow is what brings it current.
    try:
        import subprocess
        vj = json.loads((ROOT / "versions.json").read_text(encoding="utf-8"))
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(ROOT),
                              capture_output=True, text=True).stdout.strip()
        if head and vj.get("head") and not head.startswith(vj["head"]):
            # Count only commits that changed something versions.json records.
            # It can never contain the hash of the commit that writes it, so a
            # plain HEAD comparison reports "1 behind" forever - and a warning
            # that always fires is one people stop reading.
            missed = subprocess.run(
                ["git", "rev-list", "--count", vj["head"] + "..HEAD",
                 "--", "source/flow-ledger.html", "screens"],
                cwd=str(ROOT), capture_output=True, text=True).stdout.strip()
            if missed and missed != "0":
                print("NOTE: versions.json is missing %s commit(s) that changed "
                      "the ledger or a screen. Run scripts/build_versions.py, or "
                      "let the versions workflow do it after the merge." % missed)
    except Exception:
        pass

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
