# What I got wrong, and the check that catches it

Every entry here is a real mistake made while building this catalog, and the specific
check that would have caught it. Read this before starting a fidelity pass; run the
checks in §7 before saying a page is done.

---

## 1. Measuring live

**Never eyeball a comparison and call it superimposition.** The divider under the
sidebar's profile block went missing because "superimposition" meant a hand-picked
list of elements plus a look at a screenshot. Replace it with an exhaustive inventory
of *both* sides — walk every element, record geometry, type, colour, border, radius,
padding, opacity — and diff the two lists programmatically.

**Diff a component's inner elements, not just its bounding box.** The Pilot
Management banner's copy sat 20px left of live for a whole review cycle because the
check listed the banner and its illustration but never the heading, body lines or
button inside it. Everything on the list matched; the bug was in what was not listed.

**Walk the full DOM depth.** The segmented filter's outer stroke was missed because
the check only walked three levels and live's container sits at the fourth.

**Measure live before implementing, not after.** The card radius was assumed 4px and
is 8px. The footer blocks were assumed to reuse the 48px nav-row metrics and are 65
and 68. An inventory of the real values takes a minute and settles it.

**Read computed styles before destroying the iframe.** `CSSStyleDeclaration` is live;
once the frame is removed every value reads back empty.

**Do not trust `getComputedStyle` mid-transition.** It reported the chevron's rotation
as identity while the render was correct. For anything animated, check pixels.

**Alpha colours read back lossy.** A composited pixel at 20% opacity quantises: live's
`oklab(...)` divider reads as `#C3C8D2` off a canvas but converts to `#C3C9D4` when the
*opaque* oklab is converted. Convert the source value, don't sample the composite.

**Wait for the map before capturing.** Called out twice. Map screens need several
seconds; confirm tiles have actually painted before screenshotting.

**Don't guess a route.** `/captain/BEU/pilot-management` works, `/captain/BEU/service-area`
is a 403 while `/captain/service-area/...` is not. Navigate via the app's own nav.

**Retry live's failures before concluding.** The pilot table first rendered "having
trouble showing this data" — one Retry loaded it.

## 2. When live disagrees with the design system

Live does not sit on the 4px grid, and its type and colour wander off Crystal. The
standing decision is to **extend the library, never snap the clone**: 9 Valmo type
styles on Crystal's 19, 5 Valmo colours, 15 Valmo spacing steps. Snapping would undo
the pixel parity this catalog exists for. Label the additions so it stays obvious
which values the design system sanctions and which live merely uses.

Exemptions already agreed, so they don't get re-litigated:
- **glyphs** (`▾ ‹ › + − ✓ ⓘ`) sit outside the type library
- **artwork** (map pins, shipment dots, legend keys) and **alpha** (shadows, scrims)
  sit outside the palette
- the **hero banner** is exempt from the palette entirely — product may choose its
  own colours there, which is why its gradient is a literal

## 3. CSS traps in this codebase

**A typo'd token silently no-ops.** `var(--vpSpacingInline20)` did not exist, so the
whole `gap` declaration was dropped and the value fell back to `normal`. Now that
every distance routes through tokens this is the single most likely failure mode, and
it fails *invisibly*. Run the undefined-var check after every CSS change.

**An unterminated comment eats the rules after it.** One missing `*/` in a generated
token block swallowed the entire Valmo spacing scale; every padding collapsed to 0 and
the page still looked plausible.

**Inline styles in markup beat component CSS.** A `height:14px` capped the footer logo;
`width/height: fit-content` overrode the search field's metrics. When a component
refuses to take a value, grep the markup for an inline override.

**Check whether a class name is already taken.** `.vp-downloadbtn` already belonged to
the Service Area panel and was defined later in the sheet, so it quietly won.

**Specificity beats intent.** `.vp-pageheader h3` (class+element) outranks a bare
`.vp-heading1`, which is why the type utilities are scoped `.vp-scope .vp-<name>`.

**Non-scaling strokes are already in screen pixels.** Scaling `stroke-width` by 3.6
when porting SVG to Leaflet made every outline 4x too heavy.

**Clipped geometry shows its seams once the view moves.** Polygons clipped to a fixed
viewport look fine on a static raster and become a hard rectangle on a pannable map.

## 4. Generated edits

**Balance the counts after any scripted rewrite.** A dropped `</div>` nested the whole
Service Area panel inside a hidden layer and made it vanish; the naive check was fooled
by a nested element's own closing tag. Count `<div>`/`</div>` and `/*`/`*/` on the
output, and assert.

**Keep both copies of the seed in step.** `data-seed.json` and the blob embedded in
`flow-ledger.html` must be written together — updating one and then reading the other
silently reverted three icons.

## 5. Refactor hygiene

**Delete what a change orphans.** `.vp-pageheader` and `.vp-sa-title` survived as dead
code after the page band replaced them; `page-header` survived as a component no screen
used, with the wrong title size, sitting next to its replacement.

**Fix the metadata too.** Screens kept naming a retired component in their
`components` lists. That metadata is what the catalog and any agent reading
`manifest.json` go by, so a stale name there is worse than a stale file.

**The export only writes.** It now prunes screens, components and icons the catalog no
longer has, and fails if an `<img>` would ship without a `src` — added after a retired
component's page lingered and after component markup referencing icons by key exported
with no `src` at all.

## 6. Git and process

**Squash-merging a stacked PR deletes its base branch and auto-closes the child**, and
a closed PR's base cannot be retargeted. Merge the base, rebase the child onto `main`,
then merge — or use a merge commit.

**Verify on the deployed build, not just locally.** Serving locally proves the export;
only the deployed URL proves what people will open.

**Don't scan a JS application with an HTML-shaped regex.** The ledger deliberately
writes `'<' + '/script>'`, sets `src` at runtime, and has `/*` inside strings — all of
which trip naive structural checks. Verify functionally instead.

## 7. The checks to run before calling a page done

1. Inventory live and ours exhaustively, including every component's **inner**
   elements, and diff programmatically.
2. Superimpose live's real measured boxes over the rendered page.
3. `var()` audit: every `var(--vp…)` referenced is defined. **After** the last CSS edit.
4. Structure: `<div>`/`</div>` and `/*`/`*/` balance on every exported page.
5. No raw `px` in any `padding`/`margin`/`gap`; no colour outside the palette; no type
   outside the library — except the documented exemptions.
6. Every image loads; no `<img>` without a `src`.
7. All 34 pages render with no console errors.
8. Re-verify on the deployed URL after merging.
