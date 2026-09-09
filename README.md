# Valmo Captain Panel — Source of Truth

Pixel-faithful mirror of the Valmo Partner captain panel screens tracked in the Flow Ledger
catalog. This repo exists so a fresh Claude Code session (or a human) can get the exact real
markup in seconds, at a cost that scales with what's actually asked for — not with how big
this repo grows.

**Public repo.** Contains real pilot names, phone numbers, and transaction IDs from the
source catalog — left public as a deliberate call so the Flow Ledger catalog works for anyone
regardless of Claude plan or team, without needing repo access to be granted per person.

## Get one screen, one flow, or a component

Don't `git clone` this repo — it pulls every screen and component every time, regardless of
what you actually need, and that cost only grows as more flows get added. Instead fetch just
the file(s) you want:

```bash
curl -s https://raw.githubusercontent.com/yashparashar-meesho/Valmo-captain-panel-SoT/main/screens/<id>.html -o screens/<id>.html
```

Then grep that file for its `assets/icons/<file>` references and fetch just those the same
way into `assets/icons/`. The Flow Ledger catalog's "Copy current screen" / "Copy Entire
flow" / component-pull buttons already generate the exact commands for this — that's the
easiest way to drive it end to end (folder prompt, fetch, local server, link to open).

Every `screens/*.html` and `components/*.html` file references its stylesheet inline but its
icons via a relative `../assets/icons/<file>` path, so pulled files need to sit under a
`screens/` or `components/` folder next to a sibling `assets/icons/` folder — mirror the
repo's own layout locally and it works exactly the same as here.

## Serve it, don't double-click it

**These pages must be opened over `http://`, not as a `file://` double-click.** Chrome refuses
to load assets reached via `../` from a file URL, so the icons — and on the Service Area screens
the whole map raster — come up blank. From the folder that contains `screens/`:

```bash
python3 -m http.server 8000
# then open http://localhost:8000/screens/<id>.html
```

Every page detects this itself: opened from a file it shows a banner at the top explaining the
problem and giving that command, so nobody has to guess why the map is empty.

## What's interactive

The screens are static HTML with inline handlers — no build step, no JS libraries, no runtime
fetches — so behaviour is identical wherever they're served. On the Service Area screens the
map-layer checkboxes really do show and hide their marker groups, the Area Update History rows
switch the boundary version, and the date-range picker opens as an overlay and lets you pick a
range. Data itself is a fixed snapshot, not live: counts and dates stay put, and the Download
AWB Details button is deliberately inert.

## Typography

All type comes from one place: the **Foundations / Typography** block at the top of
`assets/kit.css`. It ships Mier B02 (the panel's real typeface, three faces under
`assets/fonts/`) plus the 19 Crystal type styles and 8 Valmo-only additions the live panel
needs, as `--vp<Name>` tokens and matching `.vp-scope .vp-<name>` classes.

Nothing outside that block may declare `font-family`, `font-size`, `font-weight` or
`line-height` — components and screens pick a style instead. `docs/typography-audit.md` is the
stored measurement behind the library (what live actually uses, per module, and why each
addition exists); build against those numbers rather than re-measuring the live panel.

Browse the styles in the catalog under **Foundations**.

## Degrading well

These pages are meant to survive bad conditions — a partial pull, a blocked CDN, no
network at all.

**Screens and components request nothing from the network.** Mier B02 ships in
`assets/fonts/`, so there is no webfont link to block first paint. Open a screen on a
plane and it renders exactly as it does online.

**A missing font costs a typeface, not a layout.** The kit defines a `Mier Fallback`
face — Arial (or a metric-compatible clone) scaled to Mier's advance widths. Measured
against Mier, plain `system-ui` sets 8.9–13.4% wide, which is enough to overflow a
table row or push a page title into its action button. With the fallback that drift
drops to about 3%, and vertical rhythm does not move at all, because every type style
carries an explicit line-height.

**A missing image leaves a gap, not a broken layout.** Pull a screen without its
icons and each `<img>` is hidden while keeping its reserved box, so rows keep their
height and the map area keeps its size and background. Text is unaffected.

**Opened as a file instead of served**, every page says so in a banner and gives the
command to fix it, rather than silently showing a blank map.

The catalog (`index.html`) is the one page that still uses a webfont, for its own
chrome. It loads non-render-blocking, so a slow or unreachable Google Fonts delays
nothing — the page paints in the fallback stack and upgrades if the font arrives.

## Layout

```
manifest.json        — flows, their screens (in order), and the component list
screens/<id>.html     — one real screen per file, exact markup, click-through navigation wired
components/<id>.html  — one component per file, for reuse in new work
assets/kit.css        — the shared stylesheet, kept here for reference (already inlined in every page)
assets/fonts/         — Mier B02 (Book/Demi/Bold) as real .woff2 files
docs/typography-audit.md — the live-panel type measurement the library is built from
assets/icons/         — every icon as a real .svg/.png file, referenced by relative path from
                        screens/ and components/ pages
```

Screens link to each other exactly like the real app: `data-goto` attributes on buttons,
back-arrows, and sidebar items navigate between the local screen files (`location.href =
"<id>.html"`).

## Staying in sync

This repo is a **generated mirror**, not the primary editing surface — keep editing
flows/screens/components in the Flow Ledger catalog itself (hosted on Vercel), then re-run
`scripts/export_to_github.py` and push whenever it changes. If something here looks stale,
the hosted catalog is the source of truth; ping whoever maintains this repo to refresh it.

## If you don't have git/gh access here

The Flow Ledger catalog's pull buttons fall back to a plain HTTP fetch of the hosted page
itself (no special Claude access needed — curl, WebFetch, anything works) and parse the
flow/screen/component/icon data out of its embedded JSON. Slower and heavier on tokens than
fetching files directly from this repo, but works for anyone with just a URL.
