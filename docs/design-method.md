# The design method

How a problem becomes a page. Four sections, **one** blocking gate.

This file is the instruction set behind the `slipstream` skill. Reading it is
enough to run the method by hand; the skill just removes the fetching.

![The four sections, their gates, and where the one blocking stop is](flow.svg)

---

## Section 0 — Locate

**Automatic. No human input except a confirmation. Fetches nothing.**

> Section 0 is reading and discussion. The pack is all you need — no screen
> files, no icons, no fonts, no stylesheet. Those come in **one batched pass**
> later, once the DRD has been approved and there is something to build
> against. Fetching early spends the user's time on files that may belong to
> a screen they are about to rule out.

Before anything is designed, establish what already exists. Skipping this is
how approaches get invented in a vacuum and the final UI lands off-spec.

1. Read [pages.md](pages.md) and [components.md](components.md).
2. Match the KRD against them.
3. Decide **where it can live**. Once the problem is understood, there are only
   ever two answers, and the first has three placements inside it. Ask the
   module question first — it is the bigger decision, and it bounds the rest.

   **1 — In an existing module.** Name which one, and why that one.

   | | placement | looks like | precedent |
   |---|---|---|---|
   | 1a | a new section on an existing page | its own heading and its own data scope | every module |
   | 1b | a tab or sub-tab | a sibling view of the same subject | `tabs` in Pilot Management and Growth Dashboard; sub-tabs in Service Area |
   | 1c | inside a nested page of that module | a drill-down that already exists | `payment-details` under Captain Payments |

   **2 — A new module in the rail.** Only when nothing in the rail owns the
   subject. Expensive: it has to earn a permanent slot, which usually means
   someone opens it as part of a routine.

   Use [section-rules.md](section-rules.md) to choose between 1a and the
   others — *own heading plus own data scope* is the test.

4. Name the conventions that will bind this work: the framework, the layout
   rules, the relevant foundations.

**Gate — confirm the target.** Seconds, not a review. "Yes, that one," or
"no, it's X." If wrong, re-run with the correction.

4. **Recommend one**, and say why — then ask. Showing four options and no
   opinion pushes the decision back to the person who asked you to make it.
   Showing one option invites acceptance of a wrong one. Show all four, mark
   which are out and why, and name the one you would pick.

> **1b and 1c are the ones that get missed.** 1b was missed on the very first
> real run. Two traps cause it, and both are easy to fall into again:
>
> - **Reading a screen's `notHere` as the module's.** `notHere` is scoped to
>   **one screen**. "DC Capacity does not show per-pilot detail" excludes it
>   from *that screen*, and says nothing about a tab, a sub-tab or a nested
>   page in the same module. Those are different screens; the exclusion never
>   reached them.
> - **Reading the module's current shape instead of the catalogue's patterns.**
>   A module having no tabs today is not evidence against a tab. Check
>   [components.md](components.md) for what is available, not the target page
>   for what it happens to use.

## Section 1 — Diverge

**You drive. The DRD is a blocking gate: nothing is built until it is approved.**

> This was non-blocking in the first version, to protect cycle time. After a
> real run it was changed: the DRD was skipped, wireframes were built against
> nothing written down, and an approach nobody had considered turned out to be
> the right one. **The gate is worth the day.**

1. **Interrogate the gaps** — ask only what the KRD left out *and* Section 0
   could not answer. Do not re-ask what the catalogue already knows.
2. **Write the DRD** — `DRD.md` as the source, then render it to a page and
   **open it in the browser**:

   ```bash
   python3 scripts/render_doc.py DRD.md
   ```

   Handing over a raw `.md` hands over the *source* of a document, not the
   document. It reads badly, and approving it feels like reviewing a diff.

3. **Five approaches.** Genuinely different ways to solve the problem, not one
   idea in five costumes. For each: what it does, what it costs, what it rules
   out. If two collapse into the same thing, say so and find another — do not
   quietly ship four.

4. **Do not converge yet.** Converging here is what makes the whole exercise
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
does, what it costs, and what it rules out. Build it with the `wfc-` classes
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

**Gate — the reviewer picks one or two.** Then build the real thing. There is
no greyed full-size stage in between: once a shape is chosen, the next useful
artefact is the design, and a full-size wireframe of a decided shape is a
drawing of work already understood.

Losing approaches go to the **Idea Wall** (`log-exploration`): logged, never
reviewed, allowed to go stale. Dead ends are the reason the wall exists.

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
