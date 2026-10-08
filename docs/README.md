# The Slipstream pack

Everything a person or an agent needs to design a page for the Valmo captain
panel correctly, without having read the codebase.

These files travel. The `slipstream` skill fetches them before it starts, and
the repo is public, so any of them can be read with a plain `curl` — no login:

```
https://raw.githubusercontent.com/yashparashar-meesho/Valmo-captain-panel-SoT/main/docs/<file>
```

## Which file answers which question

| question | file |
|---|---|
| How does a problem become a page? | [design-method.md](design-method.md) |
| What is a page made of? | [page-framework.md](page-framework.md) |
| How wide, how tall, what scrolls? | [layout-rules.md](layout-rules.md) |
| New section, or bake it in? | [section-rules.md](section-rules.md) |
| What will go wrong? | [never-do-this.md](never-do-this.md) |
| Has someone built this already? | [pages.md](pages.md) *(generated)* |
| Does this component exist? | [components.md](components.md) *(generated)* |
| Which colour? | [color-foundation.md](color-foundation.md) |
| Which spacing? | [spacing-foundation.md](spacing-foundation.md) |
| Which type style? | [typography-audit.md](typography-audit.md) |
| Does it match live? | [fidelity-checklist.md](fidelity-checklist.md) |

## Read in this order

**Designing something new** → `design-method.md`, then `pages.md` and
`components.md` to see what exists, then `page-framework.md` and
`section-rules.md` as you shape it.

**Matching an existing live screen** → `fidelity-checklist.md` first, then the
three foundations.

**Changing something shared** → `never-do-this.md` before you touch anything.

## Generated vs hand-written

`pages.md` and `components.md` are generated from `source/data-seed.json` by
`scripts/build_docs.py`. Hand-editing them is pointless — the next run
overwrites it. Everything else is hand-written and is the real source.

```bash
python3 scripts/build_docs.py          # regenerate
python3 scripts/build_docs.py --check  # fail if stale (CI runs this)
```

## Keeping this honest

This pack is only worth anything if it stays true. The rule:

> **When someone is corrected, the correction lands in a file — not in a
> chat, and not in an assistant's memory.**

A correction kept in a session reaches one person once. The same correction in
`never-do-this.md` or `fidelity-checklist.md` reaches everyone who ever pulls a
screen. `fidelity-checklist.md` is literally a correction log, and it is the
most valuable file here for exactly that reason.
