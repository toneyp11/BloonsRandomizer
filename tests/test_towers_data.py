# tests/test_towers_data.py
"""Structural validation for data/towers.json.

These tests guard the shape and internal consistency of the dataset, not the
exact cost values (those come from the wiki and change with game patches).
"""
import json
import os

import pytest

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "towers.json")

EXPECTED_CATEGORY_COUNTS = {"Primary": 7, "Military": 7, "Magic": 6, "Support": 5}
EXPECTED_TOWERS = 25
EXPECTED_HEROES = 18
EXPECTED_UPGRADES = 375  # 25 towers x 3 paths x 5 tiers


@pytest.fixture(scope="module")
def data():
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def towers(data):
    """Non-hero entries."""
    return [t for t in data["towers"] if not t["isHero"]]


@pytest.fixture(scope="module")
def heroes(data):
    return [t for t in data["towers"] if t["isHero"]]


# --- shared ----------------------------------------------------------------

def test_all_names_unique(data):
    names = [t["name"] for t in data["towers"]]
    assert len(names) == len(set(names))


def test_is_hero_is_bool(data):
    for entry in data["towers"]:
        assert isinstance(entry["isHero"], bool), entry["name"]


def test_water_and_camo_flags_are_bool(data):
    for entry in data["towers"]:
        assert isinstance(entry["water"], bool), entry["name"]
        assert isinstance(entry["innateCamo"], bool), entry["name"]


def test_base_costs_positive(data):
    for entry in data["towers"]:
        assert isinstance(entry["baseCost"], int)
        assert entry["baseCost"] > 0, entry["name"]


# --- towers ----------------------------------------------------------------

def test_tower_count(towers):
    assert len(towers) == EXPECTED_TOWERS


def test_category_counts(towers):
    counts = {}
    for tower in towers:
        counts[tower["category"]] = counts.get(tower["category"], 0) + 1
    assert counts == EXPECTED_CATEGORY_COUNTS


def test_every_tower_has_three_full_paths(towers):
    for tower in towers:
        paths = tower["paths"]
        assert [p["path"] for p in paths] == [1, 2, 3], tower["name"]
        for path in paths:
            assert [u["tier"] for u in path["tiers"]] == [1, 2, 3, 4, 5], \
                f"{tower['name']} path {path['path']}"


def test_total_upgrade_count(towers):
    total = sum(len(p["tiers"]) for t in towers for p in t["paths"])
    assert total == EXPECTED_UPGRADES


def test_upgrade_fields(towers):
    for tower in towers:
        for path in tower["paths"]:
            for upg in path["tiers"]:
                assert isinstance(upg["name"], str) and upg["name"], tower["name"]
                assert isinstance(upg["cost"], int) and upg["cost"] >= 0, tower["name"]
                assert isinstance(upg["camo"], bool), tower["name"]


def test_camo_persists_up_each_path(towers):
    """Once an upgrade grants camo, higher tiers on the same path keep it."""
    for tower in towers:
        for path in tower["paths"]:
            seen_camo = False
            for upg in path["tiers"]:
                if upg["camo"]:
                    seen_camo = True
                elif seen_camo:
                    raise AssertionError(
                        f"{tower['name']} path {path['path']} loses camo after gaining it")


def test_known_camo_anchors(towers):
    """Spot-check a few known camo facts against the wiki."""
    by_name = {t["name"]: t for t in towers}
    # Ninja detects camo innately
    assert by_name["Ninja Monkey"]["innateCamo"] is True
    # Dart Monkey gains camo at Enhanced Eyesight (path 3, tier 2)
    dart_p3 = by_name["Dart Monkey"]["paths"][2]["tiers"]
    assert dart_p3[0]["camo"] is False   # tier 1
    assert dart_p3[1]["camo"] is True    # tier 2 (Enhanced Eyesight)
    # Bomb Shooter never detects camo
    bomb = by_name["Bomb Shooter"]
    assert bomb["innateCamo"] is False
    assert not any(u["camo"] for p in bomb["paths"] for u in p["tiers"])


def test_paragons_well_formed(towers):
    for tower in towers:
        paragon = tower["paragon"]
        if paragon is None:
            continue
        assert isinstance(paragon["name"], str) and paragon["name"]
        assert isinstance(paragon["cost"], int) and paragon["cost"] > 0


# --- heroes ----------------------------------------------------------------

def test_hero_count(heroes):
    assert len(heroes) == EXPECTED_HEROES


def test_heroes_have_hero_category(heroes):
    for hero in heroes:
        assert hero["category"] == "Hero", hero["name"]


def test_heroes_have_no_paths_or_paragon(heroes):
    for hero in heroes:
        assert hero["paths"] == [], hero["name"]
        assert hero["paragon"] is None, hero["name"]


def test_hero_camo_level(heroes):
    for hero in heroes:
        level = hero["camoLevel"]
        assert level is None or (isinstance(level, int) and 1 <= level <= 20), hero["name"]
        # innateCamo is exactly "detects camo from level 1"
        assert hero["innateCamo"] == (level == 1), hero["name"]


def test_known_hero_anchors(heroes):
    by_name = {h["name"]: h for h in heroes}
    # New heroes are present
    assert "Dan D'Monke" in by_name
    assert "Silas" in by_name
    # Silas is water-placeable and detects camo innately
    assert by_name["Silas"]["water"] is True
    assert by_name["Silas"]["innateCamo"] is True
    # Quincy gains permanent camo at level 5
    assert by_name["Quincy"]["camoLevel"] == 5
    # Admiral Brickell requires water
    assert by_name["Admiral Brickell"]["water"] is True
