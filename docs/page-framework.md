# The page framework

> You asked whether a framework is needed. There already is one — it just was
> not written down. Every one of the 11 screens is the same skeleton with
> different contents, and there is exactly one documented exemption.

## The skeleton

```
vp-shell                         the page. flex row, 100vh, never scrolls itself
├── vp-sidebar                   the rail. 250px, fixed, never scrolls
└── vp-content                   the work area. grey, scrolls, 16px side gutter
    ├── vp-pagebar               the header. sticky, min 52px, carries the h3
    ├── vp-tabs | vp-subtabbar    optional. sits flush under the header, 1px divider
    └── vp-panel                 the section. white, radius 8, 16px padding
        ├── section head (h4)    optional, may sit on a tinted strip
        └── content              cards, rows, tables, fields
```

`vp-shell`, `vp-sidebar`, `vp-content`, `vp-pagebar` and `vp-panel` each appear
**exactly 11 times across 11 screens** — once per page, no exceptions. That is
not a convention anyone has to remember; it is simply what a page is.

## Heading levels carry meaning

Measured across every screen, with no counter-examples:

| level | role | example |
|---|---|---|
| `h3` | page title, in the header band | `Payments`, `Growth Dashboard`, `DC Capacity` |
| `h4` | section title, inside a panel or on its strip | `Set Your DC Capacity`, `Your Order Summary` |

There is no `h1`, `h2`, `h5` or `h6` anywhere in the panel. Do not introduce
one — if content feels like it needs a third level, it is a card inside a
section, not a heading.

Two screens title the page with the **view** rather than the module
(`Payment Details (17 Aug – 23 Aug)`). That is correct when the page is a
drill-down: the rail already says which module you are in.

## How many sections a page has

Across all 11 screens: **one or two. Never three.**

That is a useful ceiling, not a hard law — but if a design wants four sections,
that is strong evidence the page is really two pages, or that three of them are
cards inside one section. Check [section-rules.md](section-rules.md) before
adding a third.

## The one exemption

**Service Area's three screens have no `vp-panel` at all.** The map is the work
area and runs edge to edge, with the 16px gutter deliberately bypassed
(`vp-content-flush`). A map boxed inside a padded white card is a worse map.

This is the only exemption, it is deliberate, and it is documented so nobody
"fixes" it. If a new page wants the same treatment, it needs the same
justification: the content *is* the canvas.

## Building order

Build in the order the skeleton nests. Starting from the content and working
outwards is how pages end up with the gutter, the header height or the
scroll container subtly wrong.

1. shell + rail (copy from any existing screen — it is identical on all 11)
2. header, with the `h3`
3. tabs, if the module has them
4. sections, top to bottom
5. contents of each section

## Where the rest lives

- measurements and behaviours → [layout-rules.md](layout-rules.md)
- when something earns its own section → [section-rules.md](section-rules.md)
- colour, spacing, type → the three foundation files
- what already exists → [pages.md](pages.md), [components.md](components.md)
