#!/usr/bin/env python3
"""Regenerate data/towers.json from the Blooncyclopedia (bloonswiki.com) Cargo API.

Usage:
    python tools/fetch_towers.py

Pulls base costs, upgrade names/costs, and paragon names/costs from the wiki's
structured Cargo tables and writes data/towers.json. Costs are Medium
difficulty, excluding Monkey Knowledge and discounts. The 'camo' field on each
upgrade is written as null (placeholder to be filled in later).

Only the standard library is used, keeping the project dependency-free.
"""
import json
import os
import urllib.parse
import urllib.request

API = "https://www.bloonswiki.com/api.php"
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "towers.json")

CATEGORY = {
    "Primary":  ["Dart Monkey", "Boomerang Monkey", "Bomb Shooter", "Tack Shooter",
                 "Ice Monkey", "Glue Gunner", "Desperado"],
    "Military": ["Sniper Monkey", "Monkey Sub", "Monkey Buccaneer", "Monkey Ace",
                 "Heli Pilot", "Mortar Monkey", "Dartling Gunner"],
    "Magic":    ["Wizard Monkey", "Super Monkey", "Ninja Monkey", "Alchemist",
                 "Druid", "Mermonkey"],
    "Support":  ["Banana Farm", "Spike Factory", "Monkey Village", "Engineer Monkey",
                 "Beast Handler"],
}
STANDARD = {name for names in CATEGORY.values() for name in names}
# Towers that can be placed on water (drives the app's "Ban Water Towers" option).
WATER = {"Monkey Sub", "Monkey Buccaneer", "Mermonkey", "Beast Handler"}

# Camo detection, from the wiki "Camo detection" page (BTD6 section, last updated
# v53.2). Each entry names the upgrade that grants the tower *permanent* camo
# detection; that upgrade and every higher tier on the same path get camo=true.
# Resolved by name at build time so a path/tier reshuffle can't silently misplace
# it. Conditional/ability-only and paragon-only sources are intentionally excluded
# (e.g. Boomerang Turbo Charge, Monkey Sub / Engineer paragons); "decamo" upgrades
# that strip camo but don't grant detection are also excluded.
CAMO_GRANT = {
    "Dart Monkey": "Enhanced Eyesight",
    "Ice Monkey": "Cold Snap",
    "Desperado": "Eagle Eye",
    "Sniper Monkey": "Night Vision Goggles",
    "Monkey Buccaneer": "Crow's Nest",
    "Monkey Ace": "Spy Plane",
    "Heli Pilot": "IFR",
    "Mortar Monkey": "Signal Flare",
    "Dartling Gunner": "Advanced Targeting",
    "Wizard Monkey": "Monkey Sense",
    "Super Monkey": "Ultravision",
    "Druid": "Ball Lightning",
    "Mermonkey": "Echosense Precision",
    "Monkey Village": "Radar Scanner",
    "Beast Handler": "Horned Owl",
}
# Towers that detect camo with no upgrade at all.
INNATE_CAMO = {"Ninja Monkey"}

# Heroes are pulled from the btd6_heroes table and added to the dataset with
# category "Hero" / isHero=True. They have levels rather than upgrade paths, so
# their "paths" list is empty and camo is expressed as a level, not per-upgrade.
# Heroes that can be placed on water (kept consistent with the water-placeable
# tower flag; Brickell requires water, Silas can use land or water).
WATER_HEROES = {"Admiral Brickell", "Silas"}
# Level at which a hero gains PERMANENT camo detection (1 = innate at level 1).
# From the wiki "Camo detection" page (v53.2). Item/ability-conditional sources
# (Geraldo's Genie Bottle, Corvus's Vision) are excluded, matching how tower
# conditionals are handled; heroes with no camo are simply absent here.
HERO_CAMO_LEVEL = {
    "Quincy": 5,
    "Captain Churchill": 6,
    "Etienne": 5,
    "Admiral Brickell": 7,
    "Ezili": 1,
    "Sauda": 1,
    "Psi": 1,
    "Silas": 1,
}


def apply_camo(name, paths):
    """Set the camo flag on every upgrade tier and return the tower innateCamo flag.

    camo=True means the tower has permanent camo detection once that upgrade is
    owned (the granting upgrade and higher tiers on its path). Raises if a
    configured granting upgrade name is not present in the tower's paths.
    """
    innate = name in INNATE_CAMO
    grant_name = CAMO_GRANT.get(name)
    grant_pos = None  # (path, tier) of the granting upgrade
    if grant_name:
        for path in paths:
            for upg in path["tiers"]:
                if upg["name"] == grant_name:
                    grant_pos = (path["path"], upg["tier"])
        if grant_pos is None:
            raise RuntimeError(f"{name}: camo-granting upgrade '{grant_name}' not found")

    for path in paths:
        for upg in path["tiers"]:
            camo = innate
            if grant_pos and path["path"] == grant_pos[0] and upg["tier"] >= grant_pos[1]:
                camo = True
            upg["camo"] = camo
    return innate


def cargo(tables, fields, order_by, where=None):
    """Run a Cargo query and return the list of row dicts."""
    params = {
        "action": "cargoquery", "format": "json", "limit": "500",
        "tables": tables, "fields": fields, "order_by": order_by,
    }
    if where:
        params["where"] = where
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (BloonsRandomizer data fetch)"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    if "error" in payload:
        raise RuntimeError(payload["error"].get("info", "cargo query failed"))
    return [row["title"] for row in payload.get("cargoquery", [])]


def build():
    base_rows = cargo("btd6_towers", "name,cost", "name")
    upg_rows = cargo("btd6_upgrades", "tower,path,tier,name,cost", "tower,path,tier", where="unused=0")
    par_rows = cargo("btd6_paragons", "tower,name,cost", "tower")

    base_cost = {r["name"]: int(r["cost"]) for r in base_rows
                 if r.get("name") in STANDARD and r.get("cost") not in (None, "")}

    upg = {}
    for r in upg_rows:
        name = r.get("tower")
        if name not in STANDARD:
            continue
        upg.setdefault(name, {}).setdefault(int(r["path"]), {})[int(r["tier"])] = \
            {"name": r["name"], "cost": int(r["cost"])}

    paragon = {r["tower"]: {"name": r["name"], "cost": int(r["cost"])}
               for r in par_rows if r.get("tower") in STANDARD}

    towers, problems = [], []
    for category, names in CATEGORY.items():
        for name in names:
            if name not in base_cost:
                problems.append(f"{name}: missing base cost")
            paths = []
            for p in (1, 2, 3):
                tiers = []
                for tier in (1, 2, 3, 4, 5):
                    cell = upg.get(name, {}).get(p, {}).get(tier)
                    if cell is None:
                        problems.append(f"{name}: missing path {p} tier {tier}")
                        continue
                    tiers.append({"tier": tier, "name": cell["name"],
                                  "cost": cell["cost"], "camo": None})
                paths.append({"path": p, "tiers": tiers})
            innate = apply_camo(name, paths)
            towers.append({
                "name": name, "category": category, "isHero": False,
                "water": name in WATER, "innateCamo": innate,
                "baseCost": base_cost.get(name), "paragon": paragon.get(name),
                "paths": paths,
            })

    # Heroes: levels instead of upgrade paths, so no paths/paragon.
    hero_rows = cargo("btd6_heroes", "name,cost", "name")
    for r in hero_rows:
        name = r.get("name")
        if r.get("cost") in (None, ""):
            problems.append(f"{name}: missing hero cost")
        camo_level = HERO_CAMO_LEVEL.get(name)
        towers.append({
            "name": name, "category": "Hero", "isHero": True,
            "water": name in WATER_HEROES, "innateCamo": camo_level == 1,
            "camoLevel": camo_level,
            "baseCost": int(r["cost"]) if r.get("cost") not in (None, "") else None,
            "paragon": None,
            "paths": [],
        })

    if problems:
        raise RuntimeError("Data problems:\n  " + "\n  ".join(problems))

    return {
        "meta": {
            "game": "Bloons TD 6",
            "description": "Every tower with all upgrade paths, names, and costs, plus heroes.",
            "costBasis": "Medium difficulty; excludes Monkey Knowledge and all discounts.",
            "source": "Blooncyclopedia (bloonswiki.com) Cargo tables btd6_towers / btd6_upgrades / btd6_paragons / btd6_heroes.",
            "heroNote": "Entries with isHero=True are heroes (category 'Hero'). Heroes level up rather than take upgrade paths, so 'paths' is empty and 'paragon' is null. 'camoLevel' is the level at which the hero gains permanent camo detection (null if none/conditional); 'innateCamo' is True when that level is 1.",
            "camoNote": "Per-upgrade 'camo' is True when the tower has permanent camo detection once that upgrade is owned (granting upgrade and higher tiers on its path). 'innateCamo' marks towers that detect camo with no upgrade (Ninja Monkey). Source: wiki 'Camo detection' page, BTD6 section (v53.2). Excludes conditional/ability-only, paragon-only, and decamo-only sources.",
        },
        "categories": list(CATEGORY) + ["Hero"],
        "towers": towers,
    }


def main():
    data = build()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    upgrades = sum(len(p["tiers"]) for t in data["towers"] for p in t["paths"])
    heroes = sum(1 for t in data["towers"] if t["isHero"])
    print(f"Wrote {os.path.relpath(OUT)}: {len(data['towers']) - heroes} towers, "
          f"{heroes} heroes, {upgrades} upgrades, "
          f"{sum(1 for t in data['towers'] if t['paragon'])} paragons.")


if __name__ == "__main__":
    main()
