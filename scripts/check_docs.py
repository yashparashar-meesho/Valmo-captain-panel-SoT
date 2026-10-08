#!/usr/bin/env python3
"""The docs pack has to stay true, or it is worse than having none.

A rulebook that is quietly wrong is more dangerous than a missing one: people
follow it. Prose cannot keep itself honest, so these are the checks that can:

  1. every file the index names exists
  2. every relative markdown link resolves
  3. the generated inventories are current
  4. every flow and screen carries UX context
  5. the skill does not reference a file that is not there

Check 5 is the one that matters most in the field. The skill fetches the pack
from a URL, and a missing file there is a 404 in someone else's session, long
after the rename that caused it.

    python3 scripts/check_docs.py
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SKILL = ROOT / ".claude" / "skills" / "slipstream" / "SKILL.md"
SEED = ROOT / "source" / "data-seed.json"

problems = []
notes = []


def main():
    if not DOCS.is_dir():
        sys.exit("no docs/ directory")
    on_disk = {p.name for p in DOCS.glob("*.md")}

    # 1 + 2 ------------------------------------------------- links resolve --
    linked = set()
    for md in sorted(DOCS.glob("*.md")):
        for m in re.finditer(r"\[[^\]]+\]\(([^)#]+\.md)(#[^)]*)?\)", md.read_text(encoding="utf-8")):
            target = m.group(1)
            linked.add(Path(target).name)
            if not (md.parent / target).exists():
                problems.append("%s links to %s, which does not exist" % (md.name, target))

    orphans = on_disk - linked - {"README.md"}
    if orphans:
        notes.append("not linked from anywhere in the pack: %s" % ", ".join(sorted(orphans)))

    index = (DOCS / "README.md")
    if not index.exists():
        problems.append("docs/README.md is missing - the pack has no index")
    else:
        named = {Path(m.group(1)).name
                 for m in re.finditer(r"\[[^\]]+\]\(([^)#]+\.md)", index.read_text(encoding="utf-8"))}
        for f in sorted(on_disk - named - {"README.md"}):
            problems.append("docs/%s exists but README.md does not list it - "
                            "a file nobody is pointed at will not be read" % f)

    # 3 ------------------------------------------------- generated are current --
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "build_docs.py"), "--check"],
                       capture_output=True, text=True, cwd=str(ROOT))
    if r.returncode != 0:
        problems.append((r.stdout + r.stderr).strip() or "build_docs.py --check failed")

    # 4 -------------------------------------------------------- UX coverage --
    seed = json.loads(SEED.read_text(encoding="utf-8"))
    for kind in ("flows", "screens"):
        missing = [x["id"] for x in seed[kind] if not (x.get("ux") or {}).get("decision"
                   if kind == "screens" else "who")]
        if missing:
            notes.append("%s with no UX context yet: %s"
                         % (kind, ", ".join(missing)))

    # 5 ------------------------------------------- the skill's file list is real --
    if not SKILL.exists():
        notes.append("no slipstream skill at .claude/skills/slipstream/SKILL.md")
    else:
        text = SKILL.read_text(encoding="utf-8")
        referenced = sorted({m.group(1) for m in re.finditer(r"docs/([a-z0-9-]+\.md)", text)})
        for f in referenced:
            if f not in on_disk:
                problems.append("the slipstream skill fetches docs/%s, which does not exist. "
                                "That is a 404 in someone else's session." % f)
        uncovered = sorted(on_disk - set(referenced) - {"README.md"})
        if uncovered:
            notes.append("in docs/ but never fetched by the skill: %s" % ", ".join(uncovered))

    # ------------------------------------------------------------- report --
    for n in notes:
        print("NOTE: " + n)
    if problems:
        print("\nDOCS PACK IS BROKEN:")
        for p in problems:
            print("  - " + p)
        sys.exit(1)
    print("Docs pack is consistent: %d files, all links resolve, inventories current, "
          "skill references all exist." % len(on_disk))


if __name__ == "__main__":
    main()
