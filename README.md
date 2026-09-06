# Valmo Captain Panel — Source of Truth

Pixel-faithful, offline mirror of the Valmo Partner captain panel screens tracked in the
[Flow Ledger artifact](https://claude.ai/code/artifact/4178d4f0-99d6-4541-a6b5-5ea666ffaaeb).
This repo exists so a fresh Claude Code session (or a human) can get the exact real markup
locally in seconds, with zero token cost — no fetching giant base64 blobs through a model's
context, just a normal `git clone`.

**Meesho internal — private repo. Do not make public or share the clone URL outside the team.**

## Get it locally

```bash
git clone https://github.com/yashparashar-meesho/Valmo-captain-panel-SoT.git
```

Then open any file under `screens/` or `components/` directly in a browser — everything is
self-contained (fonts load from Google Fonts, icons are real local `.svg`/`.png` files next to
the HTML, no build step, no server required, though a local server works too if you prefer).

## Layout

```
manifest.json        — flows, their screens (in order), and the component list
screens/<id>.html     — one real screen per file, exact markup, click-through navigation wired
components/<id>.html  — one component per file, for reuse in new work
assets/kit.css        — the shared stylesheet every screen and component uses
assets/icons/         — every icon as a real .svg/.png file (no inline base64 anywhere)
```

Screens link to each other exactly like the real app and the Flow Ledger artifact: `data-goto`
attributes on buttons/back-arrows/sidebar items navigate between the local screen files.

## Staying in sync

This repo is a **generated mirror** of the Flow Ledger artifact, not the primary editing
surface — keep editing flows/screens/components in the artifact itself, then re-run the export
+ push whenever it changes. If something here looks stale, the artifact is the source of truth;
ping whoever maintains this repo to refresh it.

## If you don't have git access here

The Flow Ledger artifact's "Copy pull command" / "Pull entire flow" buttons fall back to
fetching directly from the artifact's own database via the Artifact tool if this repo isn't
reachable — slower and heavier on tokens, but works without git.
