---
name: slipstream
description: Design a page for the Valmo captain panel from a KRD, end to end — locate what already exists, diverge, wireframe, promote. Also the checker that verifies the Slipstream pack and its skills are working. Use this whenever someone states a problem, a KRD, a feature idea or a user need that touches the Valmo captain panel or anything in its domain — captains, pilots, DCs, delivery centres, service areas, AWBs, shipments, misrouting, rate cards, payments, settlements, capacity, onboarding or the partner app — EVEN IF they never say "design", "Slipstream", "Valmo" or "panel", and even if the message is only a sentence describing something captains cannot do today. Also use on "design X", "new module", "new screen", "new page", "start a design", "run slipstream", or any request to check that Slipstream is set up correctly. When in doubt and the subject is the captain panel, use it.
---

# Slipstream

Two jobs in one skill: **initiate** a design run, and **check** that everything
it depends on actually works. Run the check first, always — it costs one
command and prevents designing against a stale or missing rulebook.

> Every fetch here uses `--http1.1 --retry 3`. Without it, corporate networks
> intermittently return `curl: (16) Error in the HTTP2 framing layer`, which
> reads as a broken command when it is a transient network fault. A run that
> half-fetches the pack is worse than one that fails loudly.

**Repo:** `yashparashar-meesho/Valmo-captain-panel-SoT` (public — no auth
needed for reading)
**Raw base:** `https://raw.githubusercontent.com/yashparashar-meesho/Valmo-captain-panel-SoT/main`
**Catalogue site:** https://valmo-captain-panel-sot.vercel.app

---

## Part 1 — Check (run first, every time)

```bash
BASE=https://raw.githubusercontent.com/yashparashar-meesho/Valmo-captain-panel-SoT/main
for f in manifest.json docs/README.md docs/panel-principles.md docs/design-method.md \
         docs/page-framework.md docs/layout-rules.md docs/section-rules.md \
         docs/never-do-this.md docs/pages.md docs/components.md \
         docs/color-foundation.md docs/spacing-foundation.md \
         docs/typography-audit.md docs/fidelity-checklist.md docs/flow.svg \
         docs/comparison-example.html docs/wireframe-example.html \
         docs/promoted-example.html assets/wireframe.css \
         scripts/render_doc.py scripts/md_to_html.py; do
  printf '%-34s %s\n' "$f" "$(curl -s --http1.1 -o /dev/null -w '%{http_code}' $BASE/$f)"
done
```

**Then get the two scripts**, unless you are in a clone and already have them.
Every artefact step below runs `scripts/render_doc.py`, and the one-line
install gave you only this file:

```bash
mkdir -p scripts
for f in render_doc.py md_to_html.py; do
  curl -fsSL --http1.1 --retry 3 -o scripts/$f $BASE/scripts/$f
done
```

`render_doc.py` imports `md_to_html.py` from beside it, so fetching one without
the other fails with `ModuleNotFoundError`. Get both.

Everything must be `200`. A `404` means the pack moved or was renamed — stop
and say so rather than designing without it.

Also confirm, and report in one line:

- **`log-exploration` — optional, and not shipped.** It parks losing
  approaches on the Idea Wall. It is deliberately not published, so it will
  normally be absent. **Do not report that as a problem** — say nothing unless
  the user asks to log something, and then explain it is not installed.
  Everything else in the method works without it.
- **Working in a clone?** If the user has the repo locally, prefer local files
  and run `python3 scripts/check_v2_sync.py` and
  `python3 scripts/build_docs.py --check`. Both must pass. If `build_docs`
  reports stale, the inventory you are about to read is out of date — regenerate
  before trusting it.

**Read `docs/panel-principles.md` first.** It is the only file describing the
person and the product rather than how to build a page, and it contradicts
several comfortable assumptions: the panels are **merging into this one**, so
design for a captain working here **all day under operational pressure**, not
the end-of-day reporter they are today · **speed is a feature**, 3–5 tabs per
task today · **read-only is the root of the adoption problem** ·
**WhatsApp is the competitor** and is winning · there is **no homepage** · a `–` in an empty cell reads as a loading failure ·
selected and unselected states are known to be indistinguishable · payments
lag a week. Its **eight principles are the UX checks** on the finished design,
answered with an argument each, never a tick.

Then **read the pack** — at minimum `design-method.md`, `pages.md`,
`components.md`, `page-framework.md`, `section-rules.md`, `never-do-this.md`.
Do not skim. These replace the codebase.

---

## Part 2 — Initiate

Follow `docs/design-method.md`. It is the authority; the notes below are only
what the skill adds.

### Section 0 — Locate

Read the pack and match the KRD against `pages.md` and `components.md`. Then
**run the edge-case sweep** — data · time · permission · lifecycle — because a
KRD describes the happy path almost every time, and write `BRIEF.md`:

```
THE PROBLEM AS I READ IT
  <in your own words — if this is wrong, everything after it is wrong>

WHAT IT TOUCHES
  <every module and screen the problem reaches, and why each is relevant —
   name them all, including ones you expect to rule out, or they vanish>

CONSTRAINTS            C1, C2, …   the rules the design cannot break
SUCCESS TESTS          T1, T2, …   what a person must be able to do
SITUATIONS             S1, S2, …   every case the sweep found

OPEN QUESTIONS
  <what only they can answer, and what you will assume if they do not>
```

**Nothing else goes in the brief.** You read the conventions and the component
inventory in the step before this and you will need them in Section 2 — but
they are build material. The brief is read by someone deciding whether you have
understood their problem, and anything that is not that is in the way. A brief
that cannot be read and corrected in a few minutes gets skimmed, and a skimmed
brief is approved without being checked.

Render it and open it, then **ask whether it is good to go:**

```bash
python3 scripts/render_doc.py BRIEF.md
```

### Open every artefact you make

```bash
python3 scripts/render_doc.py BRIEF.md        # markdown → a readable page
python3 scripts/render_doc.py BRIEF.md --html-only   # render only, no server
python3 scripts/render_doc.py shapes.html     # already a page → served as-is
```

The brief, the DRD, the comparison sheet and the design are each rendered,
served and **opened in the browser** as soon as they exist — Chrome where it
exists, the default browser otherwise. **Those four, and nothing else.** The
component list and the checks are read alongside the design: render them, link
them, do not open them.

Each of the four in its own tab, because a run is read by comparing its
artefacts. But the same artefact never opens twice — re-render it after a
correction and the script says *already open, reload that tab*. All the
documents in one directory share one server.

If a browser cannot be opened at all, say so and give the URL.

### The brief gate — blocking

**Nothing in Section 1 starts until they say the brief is good to go.** Not
"shared", not "sent" — answered.

This is the cheapest correction in the method. A misread problem produces a
correct-looking DRD, five careful approaches and a finished design that solves
the wrong thing, and nothing downstream catches it. In the capacity-cut run the
brief came back with three corrections, and one of them removed an entire
approach — had it arrived after the DRD, five approaches would already have
been argued against the wrong problem.

**IDs freeze at this gate.** Before it, renumber freely. After it, `C4` and
`T2` are referenced by name everywhere: mark withdrawn items withdrawn, and
give new facts new numbers.

**Where it lives is not decided here.** It is one of the things the five
approaches differ on; settling it now collapses the design space to whatever
seemed obvious first. It belongs in the DRD, with the question in the DRD's
open questions.

### Section 0 fetches nothing

The pack is all Section 0 needs. No screen files, no icons, no fonts, no
stylesheet — those may belong to a screen the user is about to rule out. One
batched fetch happens later, after the DRD is approved.

### Section 1 — the DRD, and a hard stop

Write `DRD.md` with **as many genuinely different approaches as the problem
has** — usually around five, never padded to five (what each does, what it
costs, what it rules out). Then render and open it:

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

curl -s --http1.1 $BASE/screens/<id>.html -o $D/screens/<id>.html
curl -s --http1.1 $BASE/assets/kit.css    -o $D/assets/kit.css
for f in Mier_B02-Book.woff2 Mier_B02-Demi.woff2 Mier_B02-Bold.woff2; do
  curl -s --http1.1 $BASE/assets/fonts/$f -o $D/assets/fonts/$f; done
# only the icons this screen references
for i in $(grep -o 'assets/icons/[A-Za-z0-9_.-]*' $D/screens/<id>.html \
           | sed 's|assets/icons/||' | sort -u); do
  curl -s --http1.1 $BASE/assets/icons/$i -o $D/assets/icons/$i; done
```

**Behaviour files.** Some screens link a script in `assets/vendor/`. **Grep the
fetched screen for `assets/vendor/`** and fetch whatever it references — that
works from the public copies. (In a clone, `VENDOR_RULES` in
`source/flow-ledger.html` is the same list; the one-line install does not give
you that file.) A missing one 404s silently
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

### Whenever the user answers anything

**Update the brief and the DRD first, before doing anything else**, and show
the change as a diff — *what was open · what the answer is · what it changed.*
An answer in chat is not a decision until it is in the artefact: later steps
check against the brief, and the chat is gone next week.

**An answer often changes more than the question.** Say so when it does — in
the capacity-cut run *"ignore AMs"* removed an entire approach. **IDs freeze
once the brief is approved**: mark withdrawn items withdrawn, never delete or
renumber, because other documents reference `C4` and `T2` by name.

### Sections 1–3

Per `design-method.md`. The things most often got wrong:

- **Section 1 writes a `DRD.md`, always.** The method says the DRD does not
  block — that means *do not wait for sign-off*, not *skip it*. **Do not open
  an editor on a wireframe until `DRD.md` exists on disk.** On the first real
  run it was skipped, and the approach that was built had been compared
  against nothing written down, including an option that had been missed.
- **Derive the approaches from the brief; do not invent them.** The brief
  already named the modules (*what it touches*), the actors, and the moments
  (its *situations*). Those are the spans. Build candidates from them and
  prune — by the time you have imagined three you have anchored on the first.
- **Every module the brief named appears in the approach table, or is ruled
  out in a sentence.** Nothing from the brief may silently vanish.
- **Placement is one axis, not the excluded one.** Vary placement *and* what
  is shown · who acts · when surfaced · how framed · depth. Add a framing if
  the problem admits one the list does not have.
- **Two approaches are the same if switching between them does not change
  what the user does.**
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
- **Section 2 is grey, all of it.** Load `kit.css` then `assets/wireframe.css`
  and build the schematics with the `wfc-` classes — `comparison-example.html`
  is the standard for the sheet. A component the catalogue already has is drawn
  as that component, greyed. **Only** what it does *not* have becomes a
  labelled `.wf-box`, so the dashed boxes are an exact list of what has to be
  built. `wireframe-example.html` shows that grey vocabulary close up; it is a
  reference for *how grey works*, **not a stage to build** — there is no
  full-size wireframe step. A wireframe that looks finished turns review into
  proofreading instead of choosing; colour returns at promotion.
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
| source edited, not output **(clone)** | `source/flow-ledger.html` + `source/data-seed.json`, never `kit.css` / `index.html` / `screens/*` |
| generators run **(clone)** | `build_docs.py`, `export_to_github.py` |
| sync check passes **(clone)** | `check_v2_sync.py` exits 0 |
| components first **(clone)** | new components in their own PR, merged before the module PR |

**The four marked (clone) need write access to the repository.** Sections 0 to
2 run entirely from the public copies; Section 3 does not. Working without a
clone, report those four as *n/a — needs the repo*, never as passed, and hand
over the component list and the PR plan so someone with the repo can finish.
The other five checks, and every UX check below, run anywhere.

**The new components are listed back for approval as a rendered document** —
`COMPONENTS.md` through `render_doc.py`, like every other artefact — one entry
each: what it is, where it is used, and the existing component it was *not* an
extension of, with why.

**Then the UX checks**, which cannot be ticked and have to be written:

- the **eight principles** from `panel-principles.md`, one argument each
- a **walkthrough per situation** the edge sweep produced, in this shape:
  `SITUATION · THEY WANT · ARRIVING · steps · OUTCOME (succeeds | stalls at N
  because …)`. At least one where things have already gone wrong. A stall is
  a finding and ships as one, fixed or not.
- say plainly that a walkthrough written by the designer is self-assessment:
  it raises the floor, not the ceiling.

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
