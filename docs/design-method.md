# The design method

How a problem becomes a page. Four sections, **one** blocking gate.

This file is the instruction set behind the `slipstream` skill. Reading it is
enough to run the method by hand; the skill just removes the fetching.

![The four sections, their gates, and where the one blocking stop is](flow.svg)

## Reading the diagram

The four sections run left to right. Each one ends in a **gate** — the amber
box — and nothing moves right until that gate is answered. The arrows carry
meaning:

| | |
|---|---|
| **green →** | the gate passed; go on |
| **red ↰** | the gate failed; go back to the top of this section and re-run |
| **green dashed, underneath** | the finished module becomes catalogue, which makes the next Section 0 better |

### Section 0 — Locate · *what already exists*

| step | what happens |
|---|---|
| **Match the KRD to the catalogue** | Read `pages.md` and `components.md` and find what this problem touches. **Nothing is fetched** — no screens, no icons, no fonts. They may belong to a page that is about to be ruled out. |
| **Report, do not ask yet** | The problem as you read it, what it touches, the conventions that bind the work, and what already exists to reuse. **No gate here** — Section 0 flows straight into Section 1. |
| | **Where it lives is not decided here.** That is one of the things the five approaches differ on, so it belongs in the DRD. |

### Section 1 — Diverge · *what we could do*

| step | what happens |
|---|---|
| **Interrogate the gaps** | Ask only what the KRD left out *and* Section 0 could not answer. Never re-ask what the catalogue already knows. |
| **Write the DRD** | Five genuinely different approaches — what each does, what it costs, what it rules out, and **where each one would live**. Rendered as a page and opened in the browser, never handed over as a raw `.md`. The open questions ask where it should live, with a recommendation. |
| **🔒 The DRD is approved** | **The one hard stop.** Not *shared*, not *sent* — approved, in words. Nothing is fetched and nothing is built until it is. No converging before this either: shapes are compared on screen, not as sentences. |

### Section 2 — Shape · *what it looks like*

| step | what happens |
|---|---|
| **Fetch — once, here** | One batched pass: the screen, only the icons it references, the three fonts, `kit.css`, and any vendor script its markup links. |
| **Comparison sheet** | All five approaches as small schematics on one page, each beside what it does, costs and rules out. Schematic on purpose — the question is *which shape*, not *is this spacing right*. **Never skipped because the DRD named a favourite**: liking an approach in prose is not the same as seeing it. |
| **🔒 Pick one or two** | The losers go to the Idea Wall. **There is no greyed full-size stage after this** — once a shape is chosen, the next useful artefact is the design itself. |

### Section 3 — Promote · *make it real*

| step | what happens |
|---|---|
| **Every new block becomes a component** | Built in Crystal tokens, named, and listed back for approval. Colour returns here, and not before. |
| **Two promoted → one page** | A small `V1 / V2` switcher above the panel. Comparing means flicking between them in the same spot; separate links lose the alignment. |
| **PR 1, then PR 2** | Components first, on their own, so nothing depends on something not yet upstream. Then the module, wired into every screen's rail. |

### The loop underneath

The shipped module is now in the catalogue, so the next Section 0 starts from
a better map. That is the whole point of the dashed line — and it only keeps
working while promoting stays cheap. The moment it becomes a chore, the
catalogue starts going stale and Section 0 starts lying.


---

## Section 0 — Locate

**Automatic. No human input, no gate, nothing fetched.**

> Section 0 is reading. The pack is all you need — no screen files, no icons,
> no fonts, no stylesheet. Those come in **one batched pass** later, once the
> DRD has been approved. Fetching early spends the user's time on files that
> may belong to a page they are about to rule out.

Before anything is designed, establish what already exists. Skipping this is
how approaches get invented in a vacuum and the final UI lands off-spec.

1. Read [panel-principles.md](panel-principles.md) **first** — who the captain
   is, and the panel's standing failures. Several entries there contradict
   assumptions a page is easy to build on: the panel is an **end-of-day** tool,
   not one open while the work happens; **WhatsApp is the competitor**; there
   is **no homepage**, so nothing can assume where they arrived from.
2. Read [pages.md](pages.md) and [components.md](components.md).
3. Match the KRD against them.
4. Report, without asking anything yet: **the problem as you read it**, the
   modules and screens it touches, the conventions that will bind the work,
   and what already exists that can be reused.

> **The prerequisite: understand the problem properly first.** This is not a
> step, it is the ground everything else stands on. A misread problem produces
> a correct-looking DRD, five careful approaches and a finished design that
> solves the wrong thing — and nothing downstream will catch it, because every
> later stage inherits the misreading. If the KRD is thin, the right move is
> to go back to it, not to proceed carefully.

> **Do not decide where it lives here.** Where a thing goes is one of the
> things the five approaches *differ on* — settling it before they exist
> collapses the design space to whatever seemed obvious first, and the DRD
> then diverges inside a box nobody argued for. It belongs in the DRD, and
> the question belongs in the DRD's open questions.


## Section 1 — Diverge

**You drive. The DRD is a blocking gate: nothing is built until it is approved.**

> This was non-blocking in the first version, to protect cycle time. After a
> real run it was changed: the DRD was skipped, wireframes were built against
> nothing written down, and an approach nobody had considered turned out to be
> the right one. **The gate is worth the day.**

1. **Interrogate the gaps** — ask only what the KRD left out *and* Section 0
   could not answer. Do not re-ask what the catalogue already knows.

   > **A question about the KRD is about what the KRD does not say. A question
   > about the design is yours to decide and state.** Mixing them makes the
   > reader adjudicate your design choices as though they were facts. Order
   > questions by how much design they change, and always say what you will do
   > if they go unanswered.

2. **Sweep for the cases the KRD did not mention.** A KRD describes the happy
   path almost every time. The edge cases are not missing because they do not
   matter — they are missing because nobody thought of them, and that includes
   you unless you work from a list:

   | generator | ask |
   |---|---|
   | **data** | missing · zero · stale · exactly one · thousands · *exactly at the threshold* |
   | **time** | the first ever · mid-transition · after a long absence · the current, incomplete period |
   | **permission** | the user cannot act · a different role is looking |
   | **lifecycle** | before · during · after · reverted |

   Run it and the capacity-cut KRD immediately gives up: *exactly at 2pp* ·
   *a new DC that is exempt* · *already at the 100-order floor* · *every metric
   green but no new FE* · *this week's data incomplete*. **The KRD covers none
   of them.** Each one becomes either a constraint or a success test, and each
   one has to appear as a situation in the shapes.
3. **Write the DRD** — `DRD.md` as the source, then render it to a page and
   **open it in the browser**:

   ```bash
   python3 scripts/render_doc.py DRD.md
   ```

   Handing over a raw `.md` hands over the *source* of a document, not the
   document. It reads badly, and approving it feels like reviewing a diff.

4. **As many approaches as the problem actually has.** Not five for the sake
   of five. For each: what it does, what it costs, what it rules out, and
   **where it would live**.

   ### What makes approaches genuinely different

   **Placement is the entry axis, not the design axis.** Five approaches that
   differ only on *where it goes* are one axis explored five times. Inside any
   placement the real choices are:

   | axis | the span |
   |---|---|
   | **what is shown** | everything · only the exception · only the action |
   | **who acts** | the user alone · the user with someone else · the system acts and informs |
   | **when it is surfaced** | always · on the event · at the moment of the decision |
   | **how it is framed** | status · warning · instruction · score |
   | **depth** | summary only · item level · both |

   Place each approach on these axes and show the table. A set where four
   approaches sit on the same point is visibly thin — which is the whole
   purpose of writing it down.

   > **The discriminator.** Two approaches are the same if switching from one
   > to the other **does not change what the user does**. If their behaviour
   > is identical, it is a variant, not an approach. Same look, different
   > behaviour: two approaches. Different look, same behaviour: one.

   ### How many

   The count follows the problem. **If the honest answer is two, write two** —
   and say why there are only two. Padding to five produces three real ideas
   and two costumes, and the costumes waste the reader's attention in exactly
   the place it is most needed.

   **If they cluster, stop and ask.** When three approaches turn out to be the
   same idea in different clothes, say so, name the real fork underneath them,
   and ask which side of it to explore. A clustered set is not a failure to
   report — it usually means the problem has one obvious shape and a single
   real question, and naming that question is worth more than five options.

5. **Ask where it should live in the DRD's open questions**, with your
   recommendation and the one reason that decides it. By then the approaches
   are on the page, so the question gets answered against something real
   instead of in the abstract.

### Where it can live

There are only ever two answers, and the first has three placements inside it.
**Every approach in the DRD names its own placement** — that is part of what
makes the approaches different from one another.

> **The prerequisite: understand the problem properly first.** This is not
> a step, it is the ground everything else stands on. A misread problem
> produces a correct-looking DRD, five careful approaches and a finished
> design that solves the wrong thing — and nothing downstream will catch
> it, because every later stage inherits the misreading. If the KRD is
> thin, the right move is to go back to it, not to proceed carefully.

**1 — In an existing module.** Name which one, and why that one. The three
placements are a **ladder, not a menu**: each rung costs more than the one
below it, so take the lowest rung that genuinely serves the problem.

> **Before proposing any new surface at all, ask whether a control removes
> the need for one.** A date dropdown, a filter, a toggle or a sort on what
> is already there will often do the whole job. *"Show me last week"* is a
> date control, not a screen. A new tab or page proposed where a filter
> would have done is work nobody needed, in a place nobody will look.

> **Depth costs visibility, and that is a real trade — say it out loud.**
> A nested page is seen by whoever goes looking for it. If you recommend
> 1c, name that cost in the same breath: *"this fits here, but it will be
> seen less because it sits inside."*
>
> **It is a cost to state, never grounds to rule a placement out** — not
> even when the problem itself is one of awareness. If the placement is the
> best fit and everyone agrees the visibility is enough for what is being
> built, it ships. The method's job is to put the trade in front of the
> person deciding, not to decide for them by quietly removing an option.

| | placement | when it is right |
|---|---|---|
| **1a** | **on the existing page** — stack another section vertically, *or* extend a section already there, horizontally or vertically (a column, a field, a state) | it fits on that page |
| **1b** | **a tab or sub-tab** | it does **not** fit on that page — adding to or removing from it stops making sense — but it belongs to the same subject, so a tab lets the module hold both |
| **1c** | **inside a nested page the module already has** | it belongs to one item's detail, not to the module's main view |

> **When two modules both seem to own it.** This is common — pilot
> productivity touches capacity *and* the roster. It is not a reason to
> reach for a new module, and it is never a reason to build the thing twice.
>
> 1. **Pick the module where it makes more sense to live.** That is its
>    home, and it is built once, there.
> 2. **At the other touchpoint, add a door** — an entry point, or a line
>    explaining the new thing and linking to it. That keeps the two subjects
>    correlated and sends traffic to the home.
> 3. **Never build the same thing in both places.** Two homes means two
>    things to maintain and, before long, two versions of the truth.
> 4. **If you genuinely cannot pick, say so and ask** — and give your
>    reasoning for each side, not just the question. A decision made with
>    the reasoning in the open is one the next person can learn from; a bare
>    "which one?" teaches nobody anything.

**2 — A new module in the rail.** Only when no module owns the subject.
Expensive: it has to earn a permanent slot, which usually means someone
opens it as part of a routine.

> **A module having no tabs today is not an argument against a tab.** Any
> module can take one — the component exists, and which modules happen to
> use it now says nothing about which may. The same goes for sub-tabs and
> nested pages. Judge by whether the thing fits the page, never by the
> page's current furniture.

Within 1a, [section-rules.md](section-rules.md) decides *new section* from
*extend what is there* — **own heading plus own data scope** is the test.

**Worked example — "show the capacity cut history, last five weeks".**
Both of the obvious answers are wrong, and for the same reason.

| reading | answer it suggests | why it is wrong |
|---|---|---|
| it is about the whole DC, not one item | a tab | if the ask is only *show the weeks*, a section on the page already there carries it — or it goes at the top of the first section. A tab buys nothing. |
| you would reach it from the "cut this week" card | a nested page | if the overview has a date control, clicking any week already shows that week. The page is not needed at all. |

The answer is **1a**, and the thing that decides it is the size of the
problem, not the shape of the navigation. Both wrong answers come from
reaching for a new surface before asking whether the existing one could
carry it.


6. **Do not converge yet.** Converging here is what makes the whole exercise
   theatre: the shapes are compared as sentences, when the thing that actually
   decides it is seeing them laid out.

> **Approach ≠ IA.** Diverge here on *what we do about the problem* — surface it
> on an existing screen, give it a dedicated page, make it a notification.
> Structure comes next. Diverging on both axes at once gives fifteen options
> that are really three, and nobody can review that.

**Gate — the DRD is approved.** Hard stop. Not "shared", not "sent" —
approved, in words, by the person who asked for the work. Revise and re-render
until they say it is good to go.

Only then does anything get fetched or built.

## Section 2 — Shape

**Starts only after the DRD is approved.** This is where the real gate is.

**Fetch once, here.** One batched pass for everything the build needs — the
screen, only the icons it references, the three fonts, `kit.css`, and any
vendor script its markup links. Not before, not drip-fed.

**All five approaches on one page**, each a small schematic beside what it
does, what it costs, and what it rules out.

> **Never skip this sheet because the DRD already drew a favourite.** Liking
> an approach in the DRD is liking a *paragraph*. That is the thing this whole
> method exists to avoid — Section 1 says not to converge precisely because
> shapes argued as sentences lose to shapes seen side by side. A preference
> stated from prose is provisional until it has been looked at.
>
> Build the sheet, show it, and let the preference survive or change. The user
> may still say *"skip it, build A and B"* — that is their call to make out
> loud. It is never yours to make on their behalf by reading ahead.

> **Never skip this sheet because the DRD already drew a favourite.** Liking
> an approach in the DRD is liking a *paragraph*. That is the thing this whole
> method exists to avoid — Section 1 says not to converge precisely because
> shapes argued as sentences lose to shapes seen side by side. A preference
> stated from prose is provisional until it has been looked at.
>
> Build the sheet, show it, and let the preference survive or change. The user
> may still say "skip it, build A and B" — that is their call to make out
> loud. It is never yours to make on their behalf by reading ahead. Build it with the `wfc-` classes
in `assets/wireframe.css`; [comparison-example.html](comparison-example.html)
is the standard.

1. **IA outline first** — header, then sections in order, then what is in each.
   Check it against [section-rules.md](section-rules.md) before drawing.
2. **Schematic, on purpose.** The question here is *which shape*, not *is this
   spacing right*. Five full-size pages is too much scrolling to compare, and
   the rationale ends up nowhere near the shape it belongs to.
3. **Invent freely.** The catalogue never limits what can be proposed. A method
   that only permits existing components cannot produce a new idea. Mark which
   blocks are new — those are the component backlog.

4. **The schematic is a contract with the design that follows.** It must name
   the same blocks, in the same order, as the thing eventually built. If the
   design needs a block the schematic never showed, that is a change worth
   surfacing — not something to add quietly. A reviewer who picked a shape
   should recognise it when the design arrives; if they have to ask *"which
   wireframe became this?"*, the schematic was decoration.

5. **Draw navigation as navigation.** Tabs are a row with the active one
   underlined (`wfc-tabs`), never a row of equal bordered boxes — that reads
   as a button group and shows nothing about which view you are on. Use
   `wfc-steps` for a progression, never for navigation.

**Gate — the reviewer picks one or two.** Then build the real thing. There is
no greyed full-size stage in between: once a shape is chosen, the next useful
artefact is the design, and a full-size wireframe of a decided shape is a
drawing of work already understood.

Losing approaches go to the **Idea Wall** (`log-exploration`): logged, never
reviewed, allowed to go stale. Dead ends are the reason the wall exists.

### Checking the design as UX, not only as UI

The layout checks are syntactic and will all pass on a page nobody can use.
Answer the **eight principles** in [panel-principles.md](panel-principles.md)
with an argument each, and walk **every situation** the edge sweep produced —
narrate the captain in that situation, step by step, ending either in *they
succeed* or *here is where they stall*. A stall is a finding.

Phrase it adversarially. *"Is the hierarchy right?"* grades itself. *"A
captain opens this at 7am, has never seen it, and is already under a cut —
what do they get wrong?"* has an answer.

## Section 3 — Promote

**This half already works — it is the loop that shipped PRs #42 → #43 → #44.**

1. **Every new block becomes a real component.** Built properly in Crystal
   tokens, named, and **listed back to you for approval** — so additions to the
   library are a decision, not something discovered later.

2. **More than one approach promoted → one page, not several links.** Put each
   version in a `.vsw-pane` behind a small switcher pinned above the panel
   (`.vsw` in `assets/wireframe.css`, plus `assets/review-switch.js`):

   ```html
   <div class="vsw"><span class="vsw-k">Version</span>
     <button data-v="v1" data-title="Capacity Cuts tab" class="on">V1</button>
     <button data-v="v2" data-title="Columns in the roster">V2</button>
     <span class="vsw-t">Capacity Cuts tab</span></div>
   <div class="vsw-pane" id="v1"> …the whole panel UI… </div>
   <div class="vsw-pane" id="v2" hidden> … </div>
   <script src="../assets/review-switch.js"></script>
   ```

   Comparing two designs means flicking between them **in the same spot**. Two
   tabs lose the alignment, and with it most of the comparison. Keys `1`–`9`
   and the arrows switch; the version is kept in the URL so a link can point
   at one.
3. **PR 1 — the components**, on their own. The library gets them first, so
   nothing depends on something that is not upstream yet.
4. **PR 2 — the module**, wired into every screen's rail.
5. Regenerate: `build_docs.py`, `export_to_github.py`, `check_v2_sync.py`.

The shipped module is now part of the catalogue, so the next Section 0 is
better than this one. **That is the feedback loop** — and it only stays healthy
if promoting is cheap. The moment it becomes a chore, the catalogue starts
decaying.

---

## Where each gate actually is

| section | gate | blocking? |
|---|---|---|
| 0 Locate | confirm the target | yes, but seconds |
| 1 Diverge | **the DRD is approved** | **yes — nothing is fetched or built until it is** |
| 2 Shape | **reviewers pick one or two approaches** | yes |
| 3 Promote | approve the new components | yes, minutes |

## What this method assumes you have read

[page-framework.md](page-framework.md) · [layout-rules.md](layout-rules.md) ·
[section-rules.md](section-rules.md) · [never-do-this.md](never-do-this.md) ·
the three foundations · [fidelity-checklist.md](fidelity-checklist.md)

The `slipstream` skill fetches all of these before Section 0.
