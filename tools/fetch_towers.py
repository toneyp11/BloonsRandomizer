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
            towers.append({
                "name": name, "category": category, "water": name in WATER,
                "baseCost": base_cost.get(name), "paragon": paragon.get(name),
                "paths": paths,
            })

    if problems:
        raise RuntimeError("Data problems:\n  " + "\n  ".join(problems))

    return {
        "meta": {
            "game": "Bloons TD 6",
            "description": "Every tower with all upgrade paths, names, and costs.",
            "costBasis": "Medium difficulty; excludes Monkey Knowledge and all discounts.",
            "source": "Blooncyclopedia (bloonswiki.com) Cargo tables btd6_towers / btd6_upgrades / btd6_paragons.",
            "camoNote": "The 'camo' field is a placeholder (null) for whether the upgrade grants camo detection.",
        },
        "categories": list(CATEGORY),
        "towers": towers,
    }


def main():
    data = build()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    upgrades = sum(len(p["tiers"]) for t in data["towers"] for p in t["paths"])
    print(f"Wrote {os.path.relpath(OUT)}: {len(data['towers'])} towers, "
          f"{upgrades} upgrades, {sum(1 for t in data['towers'] if t['paragon'])} paragons.")


if __name__ == "__main__":
    main()
