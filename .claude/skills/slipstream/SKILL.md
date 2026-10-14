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

Read the pack, match the KRD against `pages.md` and `components.md`, and
**report — do not ask anything yet, and do not decide where it lives:**

```
THE PROBLEM AS I READ IT
  <in your own words — if this is wrong, everything after it is wrong>

WHAT IT TOUCHES
  <modules and screens from the catalogue, and why each is relevant>

CONVENTIONS THAT BIND THIS WORK
  <the framework, the layout rules, the foundations that apply>

WHAT ALREADY EXISTS THAT YOU CAN REUSE
  <components from the inventory this problem will need>
```

**Where it lives is not decided here.** It is one of the things the five
approaches differ on; settling it now collapses the design space to whatever
seemed obvious first. It belongs in the DRD, with the question in the DRD's
open questions.

### Section 0 fetches nothing

The pack is all Section 0 needs. No screen files, no icons, no fonts, no
stylesheet — those may belong to a screen the user is about to rule out. One
batched fetch happens later, after the DRD is approved.

### Section 1 — the DRD, and a hard stop

Write `DRD.md` with **five genuinely different approaches** (what each does,
what it costs, what it rules out), then render and open it:

```bash
python3 scripts/render_doc.py DRD.md
```

Never hand over the raw `.md`. **Then stop.** Nothing is fetched and nothing
is built until the user says the DRD is good to go. Revise and re-render until
they do.

### After the DRD is approved — fetch, in one pass

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

Serve it, and **check the port is free and the page returns 200 before you
send the link** — a link was once handed over for a server that never started
because the port was taken:

```bash
PORT=8080; while lsof -i :$PORT >/dev/null 2>&1; do PORT=$((PORT+1)); done
(cd $D && python3 -m http.server $PORT >/dev/null 2>&1 &) ; sleep 1
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:$PORT/screens/<id>.html
``` **Never
preview it yourself through a built-in browser tool** — those commonly render a
file outside their project directory as a static snapshot with no JavaScript,
which silently breaks click-through while looking fine.

### Sections 1–3

Per `design-method.md`. The things most often got wrong:

- **Section 1 writes a `DRD.md`, always.** The method says the DRD does not
  block — that means *do not wait for sign-off*, not *skip it*. **Do not open
  an editor on a wireframe until `DRD.md` exists on disk.** On the first real
  run it was skipped, and the approach that was built had been compared
  against nothing written down, including an option that had been missed.
- **Approaches differ on axes, not on placement.** Placement is how you get
  in; the design axes are *what is shown · who acts · when it is surfaced ·
  how it is framed · depth*. Put each approach on a table of those axes — a
  set clustered on one point is visibly thin. **Two approaches are the same
  if switching between them does not change what the user does.**
- **The count follows the problem.** Two real approaches beat five padded
  ones. If they cluster, name the real fork underneath and ask which side to
  explore rather than listing costumes.
- **Run the edge-case sweep in the brief** — data (missing · zero · stale ·
  one · thousands · exactly at the threshold) · time (first ever ·
  mid-transition · after absence · the current incomplete period) ·
  permission (cannot act · another role looking) · lifecycle (before · during
  · after · reverted). A KRD describes the happy path; the sweep is what finds
  the rest. Each case becomes a constraint or a test, and a situation in the
  shapes.
- **Section 2 wireframes are grey, all of them.** Load `kit.css` then
  `assets/wireframe.css`, put `wf` on the scope, and make every block a
  `.wf-box` whose label says what information goes there. Add `.exists` where
  the catalogue already has the pattern. A wireframe that looks finished turns
  review into proofreading instead of choosing — colour returns at promotion.
  Open `docs/wireframe-example.html` first — it is the standard, and guessing
  what "grey box" means is what produced near-final pages on the first run.
- **Never skip the comparison sheet because the DRD named a favourite.**
  Liking an approach in the DRD is liking a paragraph; the sheet is where
  shapes get compared as shapes. Build it and show it. The user may then say
  "skip it, build A and B" — their call, never yours to make by reading ahead.
- **The schematic is a contract with the design that follows.** Same blocks,
  same order. If a reviewer has to ask "which wireframe became this?", the
  comparison was decoration. A block the design needs but the schematic never
  showed is a change to surface, not to add quietly.
- **Draw tabs as tabs** — `wfc-tabs`, a row with the active one underlined.
  Never equal bordered boxes; that reads as a button group and hides which
  view is active.
- **Section 2 is the comparison sheet, and only that.** All five approaches as
  small schematics on one page, each beside what it does, costs and rules out
  (`wfc-` classes; `docs/comparison-example.html` is the standard). The
  reviewer picks one or two, and the next thing you build is **the real
  design** — there is no greyed full-size stage in between.
- **Two promoted designs ship as ONE page.** Each version in a `.vsw-pane`
  behind a small `V1 / V2` switcher pinned above the panel (`.vsw` in
  `assets/wireframe.css` + `assets/review-switch.js`;
  `docs/promoted-example.html` is the standard). Never several links —
  comparing means flicking between them in the same spot.
- **Status tints are the one exception to grey** — muted warn/bad/good where a
  state genuinely has to be told apart. Never brand colour.
- If a surviving approach has more than one sensible IA, say so and ask.
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
