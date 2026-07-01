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

Game content lives in the roster lists inside `hero()`, `primary()`,
`military()`, `magic()`, `support()`. Each also has a `water*` list marking
which entries are water-based (used by the "Ban Water Towers" option). Add new
towers/heroes to both the roster and, if applicable, its water list.

## Dependency policy

Runtime deps must stay at **zero** — stdlib only. Do not reintroduce
PySimpleGUI: its current release requires a license key and hangs on import,
which is why the app was previously stuck running from a prebuilt exe. If a
new capability seems to need a package, flag the tradeoff rather than adding it
silently.

## Don't commit

Build artifacts (`output/`, `*.exe`, `dist/`, `build/`) and `__pycache__/` are
gitignored. The old tracked `.exe` was removed on purpose — don't re-add it.
