# CLAUDE.md

Guidance for working in this repo. Keep it short and current.

## What this is

A desktop tool that randomizes towers ("monkeys") in Bloons TD6 to create
challenge modes. Single-file Python app with a tkinter GUI. For each active
player it rolls a hero (optional) plus a configurable number of Primary,
Military, Magic, and Support towers, and assigns each a random upgrade-path
spread.

## Run it

```
python BloonsRandomizer.py
```

No install step, no third-party packages — the UI is stdlib `tkinter`.

## Test it

```
python -m pytest        # from the repo root
```

Tests live in `tests/` and cover the pure logic. Dev-only deps (just `pytest`)
are in `requirements-dev.txt`; install with `python -m pip install -r
requirements-dev.txt`. There are **no runtime dependencies** — see below.

## Verifying GUI changes without clicking

The logic is decoupled from the window, so you can drive the real widgets
headlessly (no blocking `mainloop`):

```python
import tkinter as tk, BloonsRandomizer as b
root = tk.Tk(); app = b.RandomizerApp(root); root.update()
app.playersVar.set('2'); app.on_generate(); root.update()
print(list(app.listboxes[0].get(0, tk.END)))
root.destroy()
```

Prefer this + `pytest` over launching the window. A quick real launch
(`python BloonsRandomizer.py`, confirm it opens) is a fine final check.

## Architecture (all in `BloonsRandomizer.py`)

Three layers:
1. **Config** — module-level globals (`players`, `waterBan`, `heroEnabled`,
   `numPrimary`/`numMilitary`/`numMagic`/`numSupport`, `mainUpgrades`,
   `crossUpgrades`). The UI writes these; the logic reads them.
2. **Pure logic** — `hero()`/`primary()`/`military()`/`magic()`/`support()`
   define the rosters and call `genTower()`; `genPaths()` rolls the upgrade
   spread; `generateMonkeyList()` + `checkConditions()` + `createList()`
   assemble a valid per-player list. `Tower` is the data class. These are the
   easily testable parts — add tests here when you change behavior.
3. **UI** — `RandomizerApp` (tkinter/`ttk`): a Settings tab and a Monkey
   Results tab with one listbox per player. `read_settings()` validates the
   inputs into the config globals; `on_generate()` repopulates the lists.

Path model: `genPaths()` returns `[a, b, c]` with exactly one entry set to
`mainUpgrades` (5), one to `crossUpgrades` (2), and one left 0 — the BTD6
two-path upgrade rule.

## Conventions

- **camelCase** for functions and variables (e.g. `parseTowerCount`,
  `heroEnabled`). This is deliberate and consistent across the file — match it;
  do **not** "fix" it to PEP8 snake_case. (New tkinter widget vars added in the
  rewrite also follow camelCase, e.g. `waterBanVar`.)
- The module docstring has a `Last Updated for Version NN` line. When you
  update rosters for a new BTD6 version, bump it.

## Updating for a new BTD6 version

Game content currently lives in two places:
- The roster lists inside `hero()`, `primary()`, `military()`, `magic()`,
  `support()` in `BloonsRandomizer.py` (each with a `water*` list). NOTE: this
  roster is stale — it targets ~v44 and is missing at least **Desperado** (a
  Primary). Prefer migrating the app to read `data/towers.json` (below) rather
  than maintaining these lists by hand.
- `data/towers.json` — the full, current dataset (see next section).

## Tower dataset (`data/towers.json`)

Single source of truth for every tower, upgrade, and cost. Structure:
`towers[]` each with `name`, `category` (Primary/Military/Magic/Support),
`water` (bool), `innateCamo` (bool), `baseCost`, `paragon` (`{name, cost}` or
null), and `paths[]` (3 paths x 5 `tiers[]`, each `{tier, name, cost, camo}`).

- **Costs** are Medium difficulty, excluding Monkey Knowledge/discounts.
- **`camo`** is True when the tower has permanent camo detection once that
  upgrade is owned (the granting upgrade and higher tiers on its path).
  **`innateCamo`** marks towers that detect camo with no upgrade (Ninja Monkey).
  Camo data comes from the wiki "Camo detection" page (v53.2); conditional,
  ability-only, paragon-only, and decamo-only sources are excluded. The
  granting upgrades are configured by name in `tools/fetch_towers.py`
  (`CAMO_GRANT` / `INNATE_CAMO`).
- **Sourcing:** names + costs come from the Blooncyclopedia (bloonswiki.com)
  MediaWiki Cargo tables, which are queryable via
  `api.php?action=cargoquery&tables=btd6_upgrades|btd6_paragons|btd6_towers`.
  The public HTML/`WebFetch` path is bot-blocked (402/403), but `curl` against
  `api.php` works. Costs were cross-checked against the blackeyefly calculator
  (`github.com/blackeyefly/blackeyefly.github.io`, `src/models/utils.ts`).
- `tests/test_towers_data.py` validates the file's shape (25 towers, 375
  upgrades, category counts, field types) — run it after any regeneration.
- The wiki data tracks the live game (~v54); when refreshing, re-query the
  Cargo tables rather than editing values by hand.

## Dependency policy

Runtime deps must stay at **zero** — stdlib only. Do not reintroduce
PySimpleGUI: its current release requires a license key and hangs on import,
which is why the app was previously stuck running from a prebuilt exe. If a
new capability seems to need a package, flag the tradeoff rather than adding it
silently.

## Don't commit

Build artifacts (`output/`, `*.exe`, `dist/`, `build/`) and `__pycache__/` are
gitignored. The old tracked `.exe` was removed on purpose — don't re-add it.
