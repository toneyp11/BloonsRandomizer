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
EXPECTED_UPGRADES = 375  # 25 towers x 3 paths x 5 tiers


@pytest.fixture(scope="module")
def data():
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)


def test_tower_count(data):
    assert len(data["towers"]) == EXPECTED_TOWERS


def test_category_counts(data):
    counts = {}
    for tower in data["towers"]:
        counts[tower["category"]] = counts.get(tower["category"], 0) + 1
    assert counts == EXPECTED_CATEGORY_COUNTS


def test_tower_names_unique(data):
    names = [t["name"] for t in data["towers"]]
    assert len(names) == len(set(names))


def test_base_costs_positive(data):
    for tower in data["towers"]:
        assert isinstance(tower["baseCost"], int)
        assert tower["baseCost"] > 0, tower["name"]


def test_every_tower_has_three_full_paths(data):
    for tower in data["towers"]:
        paths = tower["paths"]
        assert [p["path"] for p in paths] == [1, 2, 3], tower["name"]
        for path in paths:
            assert [u["tier"] for u in path["tiers"]] == [1, 2, 3, 4, 5], \
                f"{tower['name']} path {path['path']}"


def test_total_upgrade_count(data):
    total = sum(len(p["tiers"]) for t in data["towers"] for p in t["paths"])
    assert total == EXPECTED_UPGRADES


def test_upgrade_fields(data):
    for tower in data["towers"]:
        for path in tower["paths"]:
            for upg in path["tiers"]:
                assert isinstance(upg["name"], str) and upg["name"], tower["name"]
                assert isinstance(upg["cost"], int) and upg["cost"] >= 0, tower["name"]
                # camo is a deliberate placeholder for now
                assert "camo" in upg, tower["name"]


def test_paragons_well_formed(data):
    for tower in data["towers"]:
        paragon = tower["paragon"]
        if paragon is None:
            continue
        assert isinstance(paragon["name"], str) and paragon["name"]
        assert isinstance(paragon["cost"], int) and paragon["cost"] > 0


def test_water_flags_are_bool(data):
    for tower in data["towers"]:
        assert isinstance(tower["water"], bool)
