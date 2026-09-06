# Valmo Captain Panel — Source of Truth

Pixel-faithful, offline mirror of the Valmo Partner captain panel screens tracked in the
Flow Ledger catalog. This repo exists so a fresh Claude Code session (or a human) can get
the exact real markup locally in seconds, with zero token cost — no fetching giant base64
blobs through a model's context, just a normal `git clone`.

**Meesho internal — private repo. Do not make public or share the clone URL outside the team.**

## Get it locally

```bash
git clone https://github.com/yashparashar-meesho/Valmo-captain-panel-SoT.git
```

Then open any file under `screens/` or `components/` directly — just double-click it, or drag
it into a browser tab. Every file is **fully self-contained**: fonts load from Google Fonts,
every icon is inlined as base64 right in the HTML, no external file references at all. No
build step, no local server, no path assumptions — it works exactly the same whether you open
it via `file://` (double-click) or serve it however you like.

## Layout

```
manifest.json        — flows, their screens (in order), and the component list
screens/<id>.html     — one real screen per file, exact markup, click-through navigation wired
components/<id>.html  — one component per file, for reuse in new work
assets/kit.css        — the shared stylesheet, kept here for reference (already inlined in every page)
assets/icons/         — every icon as a real .svg/.png file, kept here for reference/reuse
                        (already inlined as base64 in every screens/components page — nothing
                        reads from this folder to render)
```

Screens link to each other exactly like the real app: `data-goto` attributes on buttons,
back-arrows, and sidebar items navigate between the local screen files (`location.href =
"<id>.html"`).

## Staying in sync

This repo is a **generated mirror**, not the primary editing surface — keep editing
flows/screens/components in the Flow Ledger catalog itself (currently hosted on Vercel), then
re-run `scripts/export_to_github.py` and push whenever it changes. If something here looks
stale, the hosted catalog is the source of truth; ping whoever maintains this repo to refresh it.

## If you don't have git access here

The Flow Ledger catalog's "Copy pull command" / "Pull entire flow" buttons fall back to a
plain HTTP fetch of the hosted page itself (no special Claude access needed — curl, WebFetch,
anything works) and parse the flow/screen/component/icon data out of its embedded JSON. Slower
and heavier on tokens than `git clone`, but works for anyone with just a URL.
