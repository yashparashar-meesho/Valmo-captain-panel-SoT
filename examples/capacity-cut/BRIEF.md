# Brief — Capacity Cut for Latent

**Step 1 of 4.** Nothing is designed yet and nothing has been fetched. This
exists so every later step can be checked against it by name.

## The problem, in one sentence

A Latent DC loses a fifth of its capacity for breaching any one of four
weekly metrics, and today finds out only after it has happened.

**The single decision the page must support:** *what do I do this week so I
am not cut — or so I get my capacity back?*

## What it touches

`dc-capacity` owns the number the cut acts on · `growth-dashboard` already
explains why orders moved and runs weekly, like the cut · `pilot-management`
owns the roster, and staffing is the only lever in the captain's own hands.

## Constraints

These come from the KRD. Every later step has to account for them **by name**.

| | constraint |
|---|---|
| **C1** | A breach of **any one** metric triggers a flat 20% cut. Cuts never stack within a week. |
| **C2** | Cuts continue weekly down to a floor of 100 orders. |
| **C3** | Reinstatement is +25% of the cut capacity — which restores it **in full** — and only when every metric is green. |
| **C4** | For Pilot Load, green means **a newly onboarded FE**, not a lower reading. A falling order count lowers the reading without anything improving. |
| **C5** | The captain **cannot turn this off**. Exceptions go through Control Tower only. |
| **C6** | The allowance tightens with maturity: new DCs under 5 weeks are exempt, stable 5pp, mature 2pp. |
| **C7** | Pilots receive no communication about this at all. |
| **C8** | **AMs are out of scope.** The KRD names them, but nothing is built for them here. Confirmed, not assumed. |

## Success test

The page is right if these are true of a real person using it. They are
checked again, line by line, against the built design in step 4.

| | the page is right if… |
|---|---|
| **T1** | a captain under a cut can say **which metric caused it**, without asking anyone |
| **T2** | a captain can say **exactly what has to happen** for capacity to come back — including that a lower Pilot Load reading is not enough (C4) |
| **T3** | a captain **not yet cut** can tell whether they are close to one |
| **T4** | a captain **cannot mistake this for a place to dispute** the cut (C5) |

## Situations

Produced by running the sweep — data, time, permission, lifecycle — against
the KRD. **The KRD describes only S3.** Every one of these has to be designed,
and each is walked against the finished page in step 4.

| | situation | where it came from |
|---|---|---|
| **S1** | never been cut, does not know this exists | lifecycle · before |
| **S2** | inside the allowance but close to it | data · exactly at the threshold |
| **S3** | first week under a cut | *the only one the KRD describes* |
| **S4** | third week running, already at the 100-order floor | lifecycle · during · C2 |
| **S5** | every metric green, but no new FE — so **not** recovering | C4 · the trap |
| **S6** | a new DC, under 5 weeks, exempt | C6 · excluded state |
| **S7** | the current week is shown to **yesterday** — one day behind, never incomplete | data · the current period |

## What the panel already tells us

From `panel-principles.md`, and each one changes something here:

- **The panels are merging** — design for a captain working here all day under
  operational pressure, not an end-of-day reporter.
- **`–` in an empty cell reads as a loading failure.** Captains see a bare
  dash and conclude the page is broken, not that there is genuinely nothing
  there. Our own `dc-capacity` does this today — the action bar shows `-`
  until a number is typed. Wherever a value is legitimately absent, say so in
  words.
- **Selected and unselected states are already reported as indistinguishable.**
  Anything tabbed has to do more than change font weight.
- **Recall is not available.** S1 has never seen this and will not have been
  trained. The page explains itself or it fails.
- **WhatsApp is the competitor.** If an AM can explain this faster in a
  message, the page has not earned its place.

## The gate — good to go?

This brief was shown and corrected before anything else was written. The three
answers below are what came back. **One of them removed an entire approach**,
which is the whole argument for asking here rather than after the DRD: at this
point it costs a sentence, and the same words arriving a stage later would have
invalidated five approaches already argued in full.

**Approved. IDs are frozen from here** — `C1`–`C8`, `T1`–`T4` and `S1`–`S7` are
referenced by name in everything that follows.

## Answered since the first draft

| | was open | answered |
|---|---|---|
| the cut's shape | daily or weekly? | **spread across the week, but not attributable to any single date.** So the figure is a weekly ceiling. Nothing may show a per-day cut. |
| what is cut | delivery, pickup, or both? | **capacity** — fewer orders arrive. Taken as the delivery number the page already commits; if pickup is cut too, that is a change, not a detail. |
| AMs | one page or two? | **neither — nothing is built for AMs here.** See C8. |

> **The AM answer removed an approach.** E existed because a scorecard is
> something a captain and an AM read together. With C8 settled there is no
> second reader, and E has no reason to exist. Four approaches, not five —
> the count follows the problem, and this is what that looks like in practice.

## Decided

| | answered |
|---|---|
| **where it lives** | **A + E.** A *Capacity Cut* tab in DC Capacity is the home; Growth Dashboard's capacity card is a door to it, as is the weekly notification. One home, many doors. |

## Still open

- Nothing blocking.
- **Watch S5.** Every metric green but no new FE, so not actually recovering.
  The approach that made this unavoidable (C, roster columns) was not chosen.
  A can say it; it has to say it well.
