# The design method

How a problem becomes a page. Four sections, **one** blocking gate.

This file is the instruction set behind the `slipstream` skill. Reading it is
enough to run the method by hand; the skill just removes the fetching.

```
KRD → [0] LOCATE → [1] DIVERGE → [2] SHAPE → [3] PROMOTE → Final UI
                                                               │
                              every shipped module ◄───────────┘
                              makes the next LOCATE smarter
```

---

## Section 0 — Locate

**Automatic. No human input except a confirmation.**

Before anything is designed, establish what already exists. Skipping this is
how approaches get invented in a vacuum and the final UI lands off-spec.

1. Read [pages.md](pages.md) and [components.md](components.md).
2. Match the KRD against them.
3. Produce candidates — **and candidates are shapes of change, not only
   screens.** Walk all four, in this order, and say why each is in or out:

   | # | shape | looks like |
   |---|---|---|
   | 1 | extend a section on an existing screen | a field, a column, a state |
   | 2 | a new section on an existing screen | its own heading and data scope |
   | 3 | **a new screen inside an existing module** | **a tab — `tabs` already exists and two modules use it** |
   | 4 | a new module | nothing in the rail fits |

4. Name the conventions that will bind this work: the framework, the layout
   rules, the relevant foundations.

**Gate — confirm the target.** Seconds, not a review. "Yes, that one," or
"no, it's X." If wrong, re-run with the correction.

> Never present a single confident answer. One option invites acceptance of a
> wrong one; several invite a decision.

> **Shape 3 is the one that gets missed.** It was missed on the very first
> real run. Two traps cause it, and both are easy to fall into again:
>
> - **Reading a screen's `notHere` as the module's.** `notHere` is scoped to
>   **one screen**. "DC Capacity does not show per-pilot detail" excludes it
>   from *that screen*, and says nothing about a second screen in the same
>   module. A new tab is a new screen, so the exclusion never applied to it.
> - **Reading the module's current shape instead of the catalogue's patterns.**
>   A module having no tabs today is not evidence against a tab. Check
>   [components.md](components.md) for what is available, not the target page
>   for what it happens to use.

## Section 1 — Diverge

**You drive. The DRD is required; waiting for approval of it is not.**

> **"Does not block" means do not wait for sign-off. It does not mean skip.**
> On the first real run the DRD was never written, and the chosen approach was
> compared against nothing on paper — including the option that had been
> missed. Section 2 does not start until the DRD file exists.

1. **Interrogate the gaps** — ask only what the KRD left out *and* Section 0
   could not answer. Do not re-ask what the catalogue already knows.
2. **Write the DRD.** A document a PM can read on its own, not a chat
   transcript. For each approach: what it does, what it costs, what it rules out.
3. **As many approaches as are genuinely distinct.** If there are two, say two.
   A fixed count produces three real ideas and two to pad.
4. **Converge to one or two** before shaping anything.

> **Approach ≠ IA.** Diverge here on *what we do about the problem* — surface it
> on an existing screen, give it a dedicated page, make it a notification.
> Structure comes next. Diverging on both axes at once gives fifteen options
> that are really three, and nobody can review that.

**Write the DRD to a file** — `DRD.md` beside the work — and share it. Then
keep going: comments fold into Section 2 as they arrive. Two blocking gates
turns this into a multi-day loop, and cycle time is what kills design methods.

So the rule has two halves, and they are easy to confuse:

| | |
|---|---|
| **required** | the DRD exists as a written artefact before Section 2 starts |
| **not required** | anyone approving it before Section 2 starts |

## Section 2 — Shape

**You drive. This is where the real gate is.**

For each surviving approach:

1. **IA outline first** — header, then sections in order, then what is in each.
   Check it against [section-rules.md](section-rules.md) before building.
2. **Build the wireframe in HTML**, on the standard skeleton
   ([page-framework.md](page-framework.md)).
   - Where the catalogue has the pattern → **use the real component**.
   - Where it does not → **a grey box with a label**.
3. **Invent freely in grey.** The catalogue decides how something is *rendered*,
   never whether it is *allowed*. A method that only permits existing
   components cannot produce a new idea.
4. **Publish for review** — a branch gives a preview link; full-page screenshots
   go to the Figma gallery, named `<branch>-<approach>` so any frame traces back
   to the wireframe that made it.

**Gate — reviewers pick one.** The only gate that stops work. Changes loop back
to that wireframe.

Losing wireframes go to the **Idea Wall** (`log-exploration`): logged, never
reviewed, allowed to go stale. Dead ends are the reason the wall exists.

## Section 3 — Promote

**This half already works — it is the loop that shipped PRs #42 → #43 → #44.**

1. **Every grey box becomes a real component.** Built properly in Crystal
   tokens, named, and **listed back to you for approval** — so additions to the
   library are a decision, not something discovered later.
2. **PR 1 — the components**, on their own. The library gets them first, so
   nothing depends on something that is not upstream yet.
3. **PR 2 — the module**, wired into every screen's rail.
4. Regenerate: `build_docs.py`, `export_to_github.py`, `check_v2_sync.py`.

The shipped module is now part of the catalogue, so the next Section 0 is
better than this one. **That is the feedback loop** — and it only stays healthy
if promoting is cheap. The moment it becomes a chore, the catalogue starts
decaying.

---

## Where each gate actually is

| section | gate | cost |
|---|---|---|
| 0 Locate | confirm the target | seconds |
| 1 Diverge | *none* — shared, non-blocking | — |
| 2 Shape | **reviewers pick a wireframe** | the real one |
| 3 Promote | approve new components | minutes |

## What this method assumes you have read

[page-framework.md](page-framework.md) · [layout-rules.md](layout-rules.md) ·
[section-rules.md](section-rules.md) · [never-do-this.md](never-do-this.md) ·
the three foundations · [fidelity-checklist.md](fidelity-checklist.md)

The `slipstream` skill fetches all of these before Section 0.
