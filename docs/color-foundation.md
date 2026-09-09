# Color: the palette, and how every rule reaches it

**This file is the stored reference.** Build against the tokens here; do not sample
colours off the live panel ad hoc.

Read off Crystal (`crystal.meeshosupplyassets.com` → Foundation / Colors) and the
Valmo Blue sheet, and reconciled against the live captain panel on **2026-09-10**.

---

## 1. How it works

Identical in shape to the type library. One block in `flow-ledger.html`'s kit CSS
declares every colour as a `--vp<Name>` token. Nothing else in the codebase may name
a raw colour.

Two layers, on purpose:

- **Palette** — 41 colours. What the colour *is* (`--vpGreyLight01: #E6EBF2`).
- **Semantic aliases** — what a colour is *for*, pointing at a palette entry
  (`--vpBorder: var(--vpGreyLight01)`). Rules reference these, so re-pointing a role
  is a one-line change and the palette stays the single source.

## 2. The palette — 43 colours

**From Crystal (32)** — reproduced exactly: `white` `black`; `greyLight01/02`
`gainsboro` `santasGray` `greyMid01/02` `greyDark01/02`; `redBg` `redBorder`
`blushPink` `redAction`; `orangeBg` `orangeBorder` `orangeAction`; `greenBg`
`greenBorder` `greenAction` `emeraldGreen`; `yellowBg` `paleAmber` `yellowBorder`
`yellowAction` `amberBrown`; `pinkBg` `pinkBorder` `pinkAction`; `graphPrimary`
`graphSecondary` `graphTertiary`.

**Crystal's four blue shades are deliberately excluded.** `blueBg #EDEAFF`,
`blueBorder #CCC3FF`, `blueAction #3C29B7` and `blueDarkBg #30228A` are *purple*.
Valmo does not use them; Valmo Blue stands in their place.

**Valmo Blue (6)**

| Token | Hex | |
|---|---|---|
| `valmoPrimaryDark` | `#092D5E` | brand — links, primary buttons, active tab text |
| `valmoBlue` | `#2A67FF` | |
| `valmoBlueT1` | `#6E9DEE` | (also Crystal's `graphPrimary`) |
| `valmoBlue2` | `#C5D7FF` | the 4px bar on the selected nav row |
| `valmoBlueT2` | `#C7DCFF` | |
| `valmoBlueBg` | `#E3EDFF` | |

**Valmo-only (3)** — live uses these and neither palette carries them:

| Token | Hex | Covers |
|---|---|---|
| `valmoNavy` | `#072042` | the sidebar rail — darker than PrimaryDark |
| `valmoPageBg` | `#EAEAF2` | the page ground behind every panel |
| `valmoBlueT3` | `#DDE7FE` | segmented-control active fill |
| `valmoNavyMid` | `#0D2B52` | map side-panel toggle |
| `valmoGreenDeep` | `#1A7D3A` | positive metric hint |


## 2a. Navigation — its own category

The rail is a separate colour world: white type and pale tints on navy, where the rest
of the panel is dark type on white. It is called out as its own group so it reads as
the exception it is, and **the nav component draws from nothing else**.

Every value measured off live's sidebar:

| Token | Resolves to | Role |
|---|---|---|
| `navBg` | `valmoNavy #072042` | the rail |
| `navText` | `white` | nav rows, account name, Log Out |
| `navTextDim` | `greyLight01 #E6EBF2` | BEU pill text, "Captain Panel" |
| `navAvatarBg` | `greyLight01 #E6EBF2` | avatar disc |
| `navPillBorder` | `white` | 1px ring on the BEU pill |
| `navActiveBar` | `valmoBlue2 #C5D7FF` | 4px selected edge |
| `navActiveBg` | `#C5D7FF` @ 20% | selected row fill |
| `navDivider` | `#C3C9D4` @ 20% | every rule in the rail |

**On measuring the two alpha tints.** Live states them in `oklab`. Converting the
*opaque* oklab gives the exact hex (`#C5D7FF`, `#C3C9D4`); reading the composited
pixel back off a canvas does not, because at 20% opacity the premultiplied 8-bit
value quantises — it reports `#C3D7FF` / `#C3C8D2`. Our rail reads back with those
same two values, i.e. identical to live through an identical path. Trust the opaque
conversion, not the composited readback.

## 3. Two exemptions

By the same reasoning that keeps glyphs out of the type library:

- **Artwork (11)** — fills that colour a drawn mark, not an interface surface:
  `.vp-shipdot` and its `.diff-dc` / `.outside` / `.rto` variants, `.vp-shiptri`,
  `.vp-legend-tri`, `.vp-maparea`, `.vp-mapbase`, `.vp-dcpin`, `.vp-mapattrib`,
  `.vp-mapzoom`. The map screens' inline SVG marker fills are exempt for the same
  reason — they are illustration pulled from live, and rewriting them would make the
  assets diverge from the originals.
- **Alpha (11)** — shadows, scrims and translucent overlays. CSS cannot feed a
  `var()` into `rgba()`, so these stay literal; where one is a palette colour at a set
  opacity the comment says which.

## 4. What the audit changed

Before: 15 tokens, but **27 distinct raw colour literals across 52 uses** in the kit
bypassed them, and nothing checked. After: **0** raw colours outside the two
exemptions — in the kit, in every component's markup, and on every rendered screen.

Component markup was carrying colour too: the map legend keys set their swatch
colour inline, and three panels set `background:#fff` inline. The legend keys now use
`.vp-legend-dot.outside / .rto / .diff-dc`, and the panels use `var(--vpSurface)`, so
no component declares a colour of its own.

Snapped to the nearest palette entry (ΔE in CIE Lab, all imperceptible at these sizes):

| Was | Now | ΔE |
|---|---|---|
| `#fdecec` inline alert | `redBg #FFEEED` | 0.8 |
| `#fbefe0` peach | `orangeBg #FFEDDE` | 2.2 |
| `#e8ebf7` date-picker range | `valmoPageBg #EAEAF2` | 2.3 |
| `#eef4fd` empty-state card | `greyLight02 #F2F5FA` | 2.3 |

The two visible snaps were **reverted** and added to the palette instead, as
`valmoNavyMid` and `valmoGreenDeep` — a 5.8 and a 16.2 ΔE shift is a colour change,
not a rounding.

Dropped as unused: `--vpNavyActive #16345c`, `--vpPink #ec4899` (0 references each).

**One real bug found.** The selected nav row was `#DDE7FE` at 20%. Live is
`#C5D7FF` at 20% — its `oklab(0.878738 -0.0039801 -0.0586712 / 0.2)` converts to
exactly Valmo Blue 2. Fixed.

## 5. Live confirms the palette

Two values measured off live land exactly on it, which is the strongest evidence the
palette is the right one:

- selected nav row → `#C5D7FF` @ 20% = **valmoBlue2**
- sidebar dividers → `#C3C9D4` @ 20% = **greyMid01**

Live's page ground `#EAEAF2`, rail `#072042`, brand `#092D5E` and segment fill
`#DDE7FE` were all measured directly and are carried verbatim.
