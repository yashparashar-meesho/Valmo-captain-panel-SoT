# Typography: the library, and the live-panel audit behind it

**This file is the stored reference. Do not re-measure the live panel** — build against
the numbers here. Re-audit only if the live panel is redesigned or Crystal changes.

Measured on the live captain panel (`partner-app.valmo.in`, BEU — no VPN needed) and on
Crystal (`crystal.meeshosupplyassets.com` → Foundation / Typography) on **2026-09-10**.

---

## 1. Naming rule

Category follows the **weight**, not the usage:

| Mier face | CSS weight | Category |
|---|---|---|
| Book | 400 | `Body…` |
| Demi | 600 | `ButtonText…` |
| Bold | 700 | `ButtonText…` |

`Display…` is its own category and keeps its own names. Valmo-only additions carry a
`Valmo` suffix (or a descriptive name) so it is obvious they are not from Crystal.

## 2. The library — 28 styles

Defined once in `flow-ledger.html`'s kit CSS as `--vp<Name>` tokens plus `.vp-<name>`
classes. Nothing else in the codebase may declare `font-family` / `font-size` /
`font-weight` / `line-height`.

### From Crystal (19, reproduced exactly)

| Style | Face | px/lh | Style | Face | px/lh |
|---|---|---|---|---|---|
| Display1 | Bold 600 | 28/36 | Body1 | Book 400 | 15/20 |
| Heading1 | Bold 700 | 21/28 | Body2 | Book 400 | 13/20 |
| Heading2 | Bold 700 | 19/24 | Body3 | Book 400 | 12/16 |
| Heading3 | Bold 700 | 17/24 | Body4 | Book 400 | 11/16 |
| Heading4 | Bold 700 | 15/20 | Body5 | Book 400 | 10/16 |
| Heading5 / 6 | Demi 600 | 13/20 | Body6 | Book 400 | 9/12 ᵁᶜ |
| Heading7 | Demi 600 | 12/16 | ButtonText1 | Demi 600 | 15/20 |
| Heading8 | Demi 600 | 11/16 † | ButtonText2 | Demi 600 | 13/20 |
| | | | ButtonText3 | Demi 600 | 12/16 |
| | | | ButtonText4 | Demi 600 | 11/16 ᵁᶜ |

ᵁᶜ uppercase. Heading5 = Heading6 = ButtonText2 (identical in Crystal).
† Crystal ships Heading8 as 11/**28** — a 2.5× line-height, evidently a slip. Corrected
to 11/16 to match the other 11px styles.

### Valmo additions (9) — live patterns Crystal does not cover

| Style | Face | px/lh | Covers |
|---|---|---|---|
| Display2Valmo | Bold 700 | 28/**28** ‡ | hero figures (`+₹39,099.50`) |
| Display3Banner | Demi 600 | 21/28 | Growth Dashboard figures |
| Display3BannerValue | Book 400 | 21/28 | Growth Dashboard running text |
| Body17Valmo | Book 400 | 17/24 | stat-summary figures (Payments, Loss Mgmt) |
| Body14Valmo | Book 400 | 14/20 | table cells |
| ButtonText14DemiValmo | Demi 600 | 14/20 | table column headers, "Sort by:" |
| ButtonText14BoldValmo | Bold 700 | 14/20 | table action links, banner headings |
| ButtonText13BoldValmo | Bold 700 | 13/20 | small bold — links, compact labels |
| Body14TightValmo | Book 400 | 14/**16** | breadcrumbs |

‡ Live renders the hero stat at 28/**20**. We use 28/28 deliberately: 20px is smaller
than the glyph size and risks clipping numerals, and Display1's 36px adds unwanted
leading to a standalone figure.

**On Body14TightValmo.** The coverage audit below matched on size + effective weight
only, so it never surfaced a *line-height* gap: live sets breadcrumbs at 14px on a 16px
line, where `Body14Valmo` (table cells) uses 20px. Added 2026-09-10 while matching the
payment-details page, where the 4px difference moved the whole header band.

### Weight 500 is a no-op — do not add it

The live panel writes `font-weight: 500` in many places, but registers Mier at only
w400 / w600 / w700. The same string measures **220.35px at both 400 and 500** (600 →
220.98, 700 → 221.43), so 500 already falls back to Book. Treat live's 500 as 400.

### Glyph exemption

Eight kit rules size a **symbol**, not language, and are deliberately outside the
library: `.vp-select .chev`, `.vp-collapse-head .chev`, `.vp-mapzoom span`,
`.vp-panel-toggle`, `.vp-cbx.on::after`, `.vp-info-dot`, `.vp-dp-nav .arw`, and
`.vp-pagination .pg.arrow` (24px, sized to live's 40x40 arrow cells).
A text style would be the wrong tool for `▾ ‹ › + − ✓ ⓘ`.

---

## 3. Live-panel coverage (stored measurement)

Element-weighted across **1,463 rendered text elements**, all 8 module landing pages.
"Covered" = the element's size + effective weight exists in the library.

### Before the 14px family was added — 84.6%

| Module | Elements | Covered | % |
|---|---|---|---|
| Growth Dashboard | 79 | 79 | 100% |
| Cash Pendency | 47 | 47 | 100% |
| Loss Management | 53 | 52 | 98.1% |
| DC Capacity | 34 | 33 | 97.1% |
| Service Area | 33 | 31 | 93.9% |
| Pilot Rate Card | 1009 | 907 | 89.9% |
| Pilot Management | 112 | 48 | 42.9% |
| Payments | 96 | 40 | 41.7% |
| **Total** | **1463** | **1237** | **84.6%** |

The two low scores were entirely the 14px table cluster.

### After adding the 14px family — 99.0%

| Remaining gap | Elements | Share of all live text |
|---|---|---|
| 16/600 (pagination) | 8 | 0.5% |
| 16/700 (primary buttons) | 3 | 0.2% |
| 12/700 (a "Recommended" chip) | 2 | 0.1% |
| 25/400 (one Loss Mgmt banner) | 1 | 0.1% |
| **Total uncovered** | **14** | **1.0%** |

Those 14 are left uncovered on purpose: 16px maps to 15px (same weight), and the
25/400 banner and 12/700 chip were explicitly de-scoped.

### Per-module notes

- **Cash Pendency** and **Service Area → Misrouted Shipment** were already 100% Crystal-clean before any additions.
- **Pilot Rate Card** is the heaviest page (1009 text elements) and the worst offender pre-additions: 13/700 ×221 and 14/400 ×91.
- **Page titles** are consistently Heading1 (21/700/28) in every module.
- `Valmo Support` is not a route — it opens support, so there is no landing page to audit.

## 4. Two live behaviours worth remembering

- **Active sub-tabs are not bolder.** In Service Area all three tabs are 15px Book; the
  active one is marked by **colour only** (`#092d5e` vs `#272829`). Our clone had been
  bolding it to 700 — fixed.
- **Tables are 14px throughout**, not 15px: cells 14/400, headers 14/600, action links
  14/700. This is the single biggest typographic fact about the panel.

## 5. Clone compliance (verified)

All 7 screens, 462 rendered text nodes: **462/462 in Mier B02**, zero raw
`font-size`/`font-weight` declarations in screens or components, and the only values
outside the library are the 2 map zoom glyphs (`+` / `−`) per map screen.
