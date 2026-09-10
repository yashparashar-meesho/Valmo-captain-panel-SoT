# Spacing: the scale, the six roles, and how every rule reaches them

**This file is the stored reference.** Build against the tokens here.

Read from Figma — *`<temp>` Claude feeding · spacing*, section "Final Palate - 16 Jan
(After WS)" — on **2026-09-10**. The Figma explains the roles with a mobile screen;
the roles are layout concepts, so they apply unchanged to the desktop panel.

---

## 1. How it works

Two layers, the same shape as the colour foundation:

- **Scale** — what a distance *is*. A 4px step ladder, plus negatives for deliberate
  pull-ins and overlaps: `--vpSpace0` … `--vpSpace40`, `--vpSpaceN4` … `--vpSpaceN16`.
- **Semantic** — what a distance is *for*. Six roles, each pointing at a scale step:
  `--vpSpacingVerPad12: var(--vpSpace12)`.

Rules reference the semantic tokens only. Nothing outside this block may write a raw
pixel distance in `padding`, `margin` or `gap`.

## 2. The six roles

Straight from the Figma:

| Role | Means |
|---|---|
| `margin` | screen edge to content — the page's outer gutter |
| `inline` | between items sitting side by side, in a row |
| `stack` | between items stacked one above the other |
| `verPad` | inside a container, top and bottom |
| `horPad` | inside a container, left and right |
| `secGap` | between whole sections, where a divider usually sits |

A shorthand is split by role: `padding: A B` is `verPad A` + `horPad B`;
`margin: A B` is `stack A` + `inline B`. `gap` is `stack` in a column and `inline` in
a row, read off the rule's own `flex-direction`.

Figma publishes only certain steps per role — `margin` has just 00 and 16, `horPad`
has no 00 — and a role only offers what it publishes.

## 3. Valmo additions, and why they exist

**The live panel does not sit on a 4px grid.** Auditing the kit found **213 spacing
declarations, of which 83 (39%) land between Figma's steps** — and they land there
because they were measured off live:

| Live measurement | Why that exact number |
|---|---|
| `.vp-navitem` padding `14px 20px` | makes the nav row exactly 48px |
| `.vp-btn` padding `7px 16px` | 7 + 20 line-height + 7 + 2 borders = live's 36px button |
| `.vp-sidebar-footer .vp-navitem` padding `22px 20px` | live's 65px footer block |
| `.vp-subtabbar .vp-tab` padding `10px 0 8px` | live's 38px tab bar |

Snapping those to the 4px grid would have undone the pixel parity this catalog exists
for. So the ladder is **extended** rather than enforced — the same call already made
for typography (9 Valmo styles on top of Crystal's 19) and colour (5 Valmo colours on
top of Crystal's palette).

**15 Valmo steps:** 1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 18, 22, 30 px.
They are labelled as Valmo in the Foundations → Spacing view, so it stays obvious
which distances the design system sanctions and which the live panel simply uses.

Totals: **30 scale steps, 76 semantic tokens.**

## 4. Coverage (verified)

- **213 of 213** spacing declarations in the kit route through the foundation.
- **0** raw pixel distances remain in any `padding`, `margin` or `gap`.
- Components draw from the same tokens as the screens — the kit is one stylesheet.

## 5. The mapping changed nothing on screen

The point of the exercise was tokens, not a redesign. Re-checking every geometry
previously established against live — **34 of 34 measurements unchanged**: header
bands (52 / 109 / 44), content gutter 266, nav row 48, footer blocks 65 and 68,
button 36, breadcrumb row 49, payment panel 418, stat bar 70, breakup card 50,
footer bar 72, Service Area tab bar 38 and side panel 352×1034.

A note for anyone re-running this: an unterminated comment in the generated token
block silently swallowed the whole Valmo scale, every `var()` referencing it became
invalid, and padding collapsed to 0 — the page still *looked* plausible. Balance
`/*` and `*/`, and assert that no `var(--vpSpac…)` is referenced without a matching
definition.
