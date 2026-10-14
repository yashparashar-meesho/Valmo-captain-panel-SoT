# The captain, and the panel's standing problems

From the *Captain Panel — Increasing Trust, Comprehension and Adoption*
workshop. This is the only file in the pack that describes **the person and
the product**, rather than how to build a page. Read it in the brief, before
anything else — most of it changes design decisions, and several entries
contradict assumptions a page can easily be built on.

---

## Who the captain is

A **seasoned logistics partner running a small-to-medium delivery centre**.
Not an office worker. Their day is physical, interrupted, and spent across
several tools — most of which are not this panel.

| when | what they are doing | the tool they reach for |
|---|---|---|
| early morning | sorting shipments, assigning pilots | Log10, physical sorting, **WhatsApp** |
| mid-day | tracking RVP pickups, watching OOR | OpsTech, **WhatsApp** |
| evening | cash collection, reconciliation | Excel / register, Log10, **WhatsApp** |
| end of day | reporting, manpower planning | **Captain Panel**, Libra, AM calls |

### That table is today. Design for where it is going.

**The panels are merging.** Log10, OpsTech and the ERP panel are being pulled
into the Captain Panel, and daily operations move onto it. So the table above
describes a captain who is being replaced by a different one: not someone who
visits at the end of the day to report, but **someone working inside the panel
all day, under operational pressure**.

Design for that captain. Concretely, it means:

- **A page may assume the captain is in the panel while the work happens.**
  Time-critical things can live here. They could not before.
- **Speed is a feature.** The work is scanning, manifesting, closing DRS,
  handling exceptions, reconciling — high volume, repeated, under time
  pressure. Captains already cross 3–5 tabs for a single task. Every extra
  step is paid many times a day.
- **Read-only is not enough.** *"Most things are read only"* is named as the
  root of the adoption problem. A page that only displays has to say why it is
  not simply a report.
- **The panel is becoming the place of record.** As operations move onto it,
  a number that disagrees with another surface is not a cosmetic bug.

### Two things that do not change with the merge

**WhatsApp is the competitor, and it is winning.** *"WhatsApp pe AM ko message
karna faster hai."* A page justifies itself by beating a message to a human.
"We put it on the panel" is not a solution on its own — and merging the panels
raises that bar rather than removing it.

**The captain is busy and interrupted.** *"I'm usually busy in operations — I
miss the training sessions."* Nothing can assume prior training, a tutorial
seen once, or a term explained elsewhere. **Recall is not available**, and an
all-day tool under pressure makes that more true, not less.

---

## The eight principles

From the Loadshare panel UX audit. Use them as the UX checks on a finished
design — each one answered with an argument, not a tick.

| | principle | the question to answer |
|---|---|---|
| 1 | **Efficiency** | How many steps and tabs does the task take? Captains cross 3–5 tabs per task today. |
| 2 | **Proactive communication** | Does it tell them *before* the problem, or after? Deadlines and capacity limits are invisible today until an action is blocked. |
| 3 | **Guidance** | Is help at the point of need, or somewhere else? |
| 4 | **Transparency** | Is system state visible — what happened, what is happening, what will? |
| 5 | **Actionability** | Can they fix it from here, and is the next step obvious? |
| 6 | **Consistency** | Same word, same placement, same pattern as the rest of the panel. |
| 7 | **Intuitiveness** | Can it be recognised at a glance, without reading? |
| 8 | **Error prevention** | Are inputs validated early? Is there a fallback when the system fails? |

---

## Known failures — never ship these again

Every one of these was found in the live panel. They are not hypothetical.

### Copy and terminology

- **Use the captain's word, not the system's.** They say *OFD* and *OOR*; the
  panel says *Open Orders*. They say *DC*; other surfaces say *Hub*.
- *"Capacity Limit"* and *"DO Compliance"* are **not understood**. Neither is
  *"prevent"* in *"days left to prevent loss"*.
- *"Loss marked"* reads as *already processed*. It is not.
- The same thing must be called the same thing on Atlas, the panel, Log10 and
  in offline comms. Inconsistency across surfaces is itself a trust problem.

### Components

- **An empty cell shown as `–` reads as a loading failure.** Design the empty
  state; never leave a dash standing in for one.
- **Selected and unselected states are not distinguishable.** This has been
  reported from the live panel, so a tab strip or toggle that only changes
  weight is not enough.
- The **info `i` icon is too small** to be seen or hit.
- **Hover-only actions are not discoverable.** Anything hover-revealed is,
  in practice, missing.
- **Do not mix pagination and infinite scroll.** Pick one, panel-wide.
- Horizontal scroll is hard to use — Loss Management is the example. Avoid it;
  if unavoidable, make it obvious.
- **Informational and actionable elements are not visually separated.** If a
  captain cannot tell what they can press, they press nothing.

### Structure

- **There is no homepage.** The panel has no starting point, so no page can
  assume the captain arrived from anywhere in particular.
- **No hierarchy or grouping in navigation**, and no framework for adding new
  features — which is why every new module makes the rail worse.
- **Nudges and flags compete.** Several modules each shout; nothing says which
  is urgent. A new flag needs a reason to outrank the others, and a sunset.

### Trust and data

- **Payments lag by a week; some data by 8–10 hours.** A number without a
  timestamp will be mistrusted, and rightly.
- **Loadshare and the panel disagree** on volume and payments. If a figure
  exists elsewhere, say which source this one is.
- **Most of the panel is read-only**, which is the root of the adoption
  problem. A page that only displays has to justify why it is not a report.

---

## The communication rule

> **If it's not on the panel, it's not official.**

The panel is the intended single source of truth. Critical updates land here
first; WhatsApp and AMs are reminder channels that point back, never
replacements. A design that assumes an AM will explain it has already failed.

---

## What is changing, and must not be designed against

- **Typography is moving from Mier B02 to DM Sans.** The catalogue is still
  Mier and is correct today. Do not pre-empt the change; do not add anything
  that depends on Mier's specific metrics.
- **The colour palette is being revised** for contrast and accessibility —
  the current primary blue sits too close to dark grey.
- **Mobile web is coming.** Captains are already using the panel on phones
  with no mobile experience at all. A desktop-only layout is a known gap, not
  a safe assumption.

> These are directional and dated. If a design turns on one of them, ask —
> do not assume this file is current.
