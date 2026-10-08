# Universal layout rules

From the *Guide for Slipstream* frame in the Figma spacing file (node `28:13356`).
These hold for **every** module, not per screen. Until now they survived only as
comments inside `flow-ledger.html`'s stylesheet — which meant a new page could
only be built correctly by someone who had read the CSS.

The structure these rules apply to is in [page-framework.md](page-framework.md).

---

## Rail

- **250px, fixed.** Height follows the screen.
- **Never scrolls vertically.** `overflow: hidden`, always.
- 250 is our Crystal component's width, not the 224 the Figma guide draws.
  The guide is wrong here and the component is right — this was confirmed and
  is not up for re-deciding.

## Header

- **Fixed to the top.** Everything in the work area scrolls under it
  (`position: sticky; top: 0`).
- **52px minimum**, and it grows when its contents need more. The Figma guide
  draws 60 on a 1056 work area; 52 is the measured live value and wins.
- Padding `12px 16px`. It spans the full work area, cancelling the gutter with
  a negative inline margin, so the band runs edge to edge.

## Work area

- **Always grey.** Universally, every module.
- **16px side gutter**, 16px at the bottom, **0 at the top** — the header
  provides the top edge.
- **The first section sits 16px below the header.**
- The work area is the scroll container, not the document.

## Sections

1. **Each has a background colour.** White unless something else is specified.
2. **16px padding on all sides**, for everything inside.
3. **8px radius.**
4. **16px between stacked sections.**
5. A section **may scroll independently** of the page, vertically or
   horizontally.

## Scrollbars

**Whenever a section or the page can scroll, the scrollbar is visible by
default.** Nobody should have to guess that something scrolls. This is why the
work area uses `overflow-y: scroll` rather than `auto` — a gutter that appears
and disappears also shifts the layout by its own width.

The one place this does not apply is the map (below).

## Tabs directly under the header

A tab strip immediately beneath the header **does not take the 16px gap**. The
two bands meet on a 1px divider. Same for a sub-tab bar. Tabs always carry a
white ground of their own rather than borrowing the work area's grey.

## The map exemption

Service Area's three screens bypass the gutter entirely and run the map edge to
edge, and the map's own scroll is panning, not scrolling — so the always-visible
scrollbar rule does not apply to it either.

This is the only exemption. It is deliberate. Do not "fix" it.

## Applying these to an existing screen

These rules were applied retroactively to every live-equivalent screen, with
Service Area exempted. If you find a screen that disagrees with this file, the
screen is wrong — but check [deliberate differences](fidelity-checklist.md)
first, because a few mismatches with live are intentional.
