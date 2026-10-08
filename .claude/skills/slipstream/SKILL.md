---
name: slipstream
description: Design a page for the Valmo captain panel from a KRD, end to end — locate what already exists, diverge, wireframe, promote. Also the checker that verifies the Slipstream pack and its skills are working. Use this whenever someone states a problem, a KRD, a feature idea or a user need that touches the Valmo captain panel or anything in its domain — captains, pilots, DCs, delivery centres, service areas, AWBs, shipments, misrouting, rate cards, payments, settlements, capacity, onboarding or the partner app — EVEN IF they never say "design", "Slipstream", "Valmo" or "panel", and even if the message is only a sentence describing something captains cannot do today. Also use on "design X", "new module", "new screen", "new page", "start a design", "run slipstream", or any request to check that Slipstream is set up correctly. When in doubt and the subject is the captain panel, use it.
---

# Slipstream

Two jobs in one skill: **initiate** a design run, and **check** that everything
it depends on actually works. Run the check first, always — it costs one
command and prevents designing against a stale or missing rulebook.

**Repo:** `yashparashar-meesho/Valmo-captain-panel-SoT` (public — no auth
needed for reading)
**Raw base:** `https://raw.githubusercontent.com/yashparashar-meesho/Valmo-captain-panel-SoT/main`
**Catalogue site:** https://valmo-captain-panel-sot.vercel.app

---

## Part 1 — Check (run first, every time)

```bash
BASE=https://raw.githubusercontent.com/yashparashar-meesho/Valmo-captain-panel-SoT/main
for f in manifest.json docs/README.md docs/design-method.md docs/page-framework.md \
         docs/layout-rules.md docs/section-rules.md docs/never-do-this.md \
         docs/pages.md docs/components.md docs/color-foundation.md \
         docs/spacing-foundation.md docs/typography-audit.md docs/fidelity-checklist.md; do
  printf '%-34s %s\n' "$f" "$(curl -s -o /dev/null -w '%{http_code}' $BASE/$f)"
done
```

Everything must be `200`. A `404` means the pack moved or was renamed — stop
and say so rather than designing without it.

Also confirm, and report in one line:

- **`log-exploration` skill present?** Needed in Section 2 to park losing
  wireframes. If missing, say so — the run can continue, the wall entry cannot.
- **Working in a clone?** If the user has the repo locally, prefer local files
  and run `python3 scripts/check_v2_sync.py` and
  `python3 scripts/build_docs.py --check`. Both must pass. If `build_docs`
  reports stale, the inventory you are about to read is out of date — regenerate
  before trusting it.

Then **read the pack** — at minimum `design-method.md`, `pages.md`,
`components.md`, `page-framework.md`, `section-rules.md`, `never-do-this.md`.
Do not skim. These replace the codebase.

---

## Part 2 — Initiate

Follow `docs/design-method.md`. It is the authority; the notes below are only
what the skill adds.

### Section 0 — Locate

Match the KRD against `pages.md` and `components.md`. Report:

```
TARGET CANDIDATES
  1. <screen-id>  — <why this one>
  2. <screen-id>  — <why this one>
  3. none of these — a new page, because <why>

CONVENTIONS THAT BIND THIS WORK
  <the framework, the layout rules, the foundations that apply>

WHAT ALREADY EXISTS THAT YOU CAN REUSE
  <components from the inventory that this problem will need>
```

Then **ask the user to confirm the target**. Never pick one silently. Never
present only one candidate.

### Once a target is confirmed — fetch it directly

No website, no clicking. The repo is public, so:

```bash
BASE=https://raw.githubusercontent.com/yashparashar-meesho/Valmo-captain-panel-SoT/main
D=<folder>          # ask the user where, with AskUserQuestion
mkdir -p $D/screens $D/assets/icons $D/assets/fonts $D/assets/vendor

curl -s $BASE/screens/<id>.html -o $D/screens/<id>.html
curl -s $BASE/assets/kit.css    -o $D/assets/kit.css
for f in Mier_B02-Book.woff2 Mier_B02-Demi.woff2 Mier_B02-Bold.woff2; do
  curl -s $BASE/assets/fonts/$f -o $D/assets/fonts/$f; done
# only the icons this screen references
for i in $(grep -o 'assets/icons/[A-Za-z0-9_.-]*' $D/screens/<id>.html \
           | sed 's|assets/icons/||' | sort -u); do
  curl -s $BASE/assets/icons/$i -o $D/assets/icons/$i; done
```

**Behaviour files.** Some screens link a script in `assets/vendor/`. Read
`VENDOR_RULES` in `source/flow-ledger.html` (or just grep the fetched screen
for `assets/vendor/`) and fetch what it references. A missing one 404s silently
— the page renders perfectly and its inputs do nothing.

Serve it (`python3 -m http.server 8080`) and give the user the link. **Never
preview it yourself through a built-in browser tool** — those commonly render a
file outside their project directory as a static snapshot with no JavaScript,
which silently breaks click-through while looking fine.

### Sections 1–3

Per `design-method.md`. The things most often got wrong:

- **Section 1** diverges on *approach*, not structure. Do not produce a fixed
  number of approaches.
- **Section 2** uses real components where the catalogue has them and **grey
  boxes where it does not**. Grey boxes are the point — never narrow an idea to
  fit the existing library.
- **Section 3** turns every grey box into a real Crystal component, **lists them
  back to the user for approval**, and ships them in their own PR *before* the
  module.

---

## Part 3 — Check again, before promoting

Before opening any PR, verify and report each line as pass or fail:

| check | how |
|---|---|
| layout rules hold | rail 250 never scrolls · header sticky ≥52 · grey work area · 16px gutter · first section 16px below header · scrollbars visible |
| section count | 1 or 2, never 3 (`section-rules.md`) |
| heading levels | `h3` page title, `h4` section title, nothing else |
| no forbidden patterns | re-read `never-do-this.md` and name anything you did |
| tokens only | no raw hex, px type or ad-hoc spacing — and any deliberate deviation is written down, not silent |
| source edited, not output | `source/flow-ledger.html` + `source/data-seed.json`, never `kit.css` / `index.html` / `screens/*` |
| generators run | `build_docs.py`, `export_to_github.py` |
| sync check passes | `check_v2_sync.py` exits 0 |
| components first | new components in their own PR, merged before the module PR |

Report failures plainly. **Do not report a check as passed without running it.**

---

## Keeping the pack honest

When the user corrects something, the correction belongs **in a file**, not in
this conversation and not in an assistant's memory:

| kind of correction | goes in |
|---|---|
| a measurement or match-to-live mistake | `docs/fidelity-checklist.md` |
| something that should never be done again | `docs/never-do-this.md` |
| a structural or layout rule | `docs/layout-rules.md` / `docs/section-rules.md` |
| a new component | the catalogue, then `build_docs.py` |

Offer to write it before the session ends. A correction that stays in a chat
reaches one person once; the same correction in the pack reaches everyone who
ever pulls a screen.
