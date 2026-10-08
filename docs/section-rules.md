# New section, or bake into an existing one?

The question that comes up on every new piece of work, and the one thing that
was written down nowhere. The rule below is **derived from the 11 screens
already built**, not invented — the worked examples are the evidence.

---

## The test

> **Own heading + own data scope → its own section.**
> **An attribute of data already on the page → bake it in.**

Both halves have to be true for a new section. A thing with a heading but no
independent data is a card. A thing with its own data but no heading is a row.

Ask it in this order:

1. **Could this section be reloaded on its own?** If its data comes from the
   same place as the section above it, it is not independent — bake it in.
2. **Does it need a title for the page to make sense?** If you would not give it
   an `h4`, it is not a section.
3. **Is this the third section?** No screen has three. See the ceiling below.

## Worked examples from what exists

| on screen | the thing | call | why |
|---|---|---|---|
| `payments-list` | hero stat + settlement table | **one section** | the table *is* the payments data; the stat summarises the same thing |
| `growth-dashboard` | Your Metrics / Your Order Summary | **two sections** | different date-scoped datasets, each with its own `h4` |
| `dc-capacity` | Set Your DC Capacity | **one section** | delivery and pickup are two cards inside it — same form, one save |
| `dc-capacity` | Forward Demand / Active Pilots | **baked in** | they are context for the capacity form, not their own subject |
| `dc-capacity` | the yellow notice | **baked in** | an annotation on the card it sits in |
| `dc-capacity` | the save bar | **neither** | a sticky action bar, part of the page chrome |
| `pilot-management-list` | the roster | **one section** | tabs switch views within it, not between sections |
| `service-area-*` | the map | **exemption** | the map is the work area — no panel at all |

The instructive pair is DC Capacity: *Delivery Capacity* and *Pickup Capacity*
look like they want to be two sections — two headings, two inputs, two
recommendations. They are **cards inside one section**, because one button
saves both. Shared fate means one section.

## If you bake in, follow the hierarchy

Baked-in content must sit in the section's existing order, not get appended
wherever it fits:

```
section head (h4) → context strip → the primary control or data → annotations
```

Dropping a new field below the save bar, or a new stat after the table, is the
failure mode this rule exists to prevent. Match the hierarchy of the section
you are joining — never something random.

## The ceiling

**One or two sections per page. Never three.**

Across all 11 screens there is no counter-example. If a design calls for a
third, one of these is true and worth deciding explicitly:

- it is really **two pages**, and the rail should carry both; or
- two of the three are **cards inside one section**; or
- you have found the genuine first exception — in which case say so out loud
  and add it here, so the next person inherits the reasoning.

## Things that are never sections

| | what it is instead |
|---|---|
| the yellow notice bar | an annotation inside a card |
| the sticky save bar | page chrome, outside the sections |
| the stat summary strip | context inside the section it describes |
| tabs / sub-tabs | navigation, sits under the header |
| a metric card | content inside a section |
