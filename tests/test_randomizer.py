# tests/test_randomizer.py
"""Unit tests for the pure randomizer logic (no GUI required)."""
import pytest

import BloonsRandomizer as b


@pytest.fixture(autouse=True)
def default_config():
    """Reset the module-level config globals to known values before each test."""
    b.players = 1
    b.waterBan = False
    b.heroEnabled = True
    b.numPrimary = 1
    b.numMilitary = 1
    b.numMagic = 1
    b.numSupport = 1
    yield


# --- parseTowerCount -------------------------------------------------------

@pytest.mark.parametrize("value,expected", [
    ("0", 0),
    ("5", 5),
    ("3", 3),
])
def test_parse_tower_count_valid(value, expected):
    assert b.parseTowerCount(value) == expected


@pytest.mark.parametrize("value", ["-1", "6", "abc", "", "2.5"])
def test_parse_tower_count_invalid(value):
    assert b.parseTowerCount(value) == -1


# --- genPaths --------------------------------------------------------------

def test_gen_paths_has_one_main_one_cross_one_zero():
    """Every generated path set is exactly one main, one cross, one unused."""
    for _ in range(200):
        paths = b.genPaths()
        assert sorted(paths) == [0, b.crossUpgrades, b.mainUpgrades]


# --- genTowerFromCategory --------------------------------------------------

def test_gen_tower_from_category_sets_water_from_data():
    # Military contains water towers (Sub/Buccaneer) and land towers; over many
    # rolls the water flag must always match what the data says for that tower.
    water_by_name = {t["name"]: t["water"] for t in b.towerPools["Military"]}
    for _ in range(200):
        tower = b.genTowerFromCategory("Military")
        assert tower.water == water_by_name[tower.name]


def test_gen_tower_from_category_uses_valid_paths():
    tower = b.genTowerFromCategory("Primary")
    assert sorted(tower.paths) == [0, b.crossUpgrades, b.mainUpgrades]


# --- generateMonkeyList ----------------------------------------------------

def test_monkey_list_respects_counts_and_hero():
    b.heroEnabled = True
    b.numPrimary, b.numMilitary, b.numMagic, b.numSupport = 2, 1, 0, 3
    monkeys = b.generateMonkeyList()
    # 1 hero + 2 + 1 + 0 + 3
    assert len(monkeys) == 7


def test_monkey_list_without_hero():
    b.heroEnabled = False
    b.numPrimary = b.numMilitary = b.numMagic = b.numSupport = 1
    assert len(b.generateMonkeyList()) == 4


# --- water ban -------------------------------------------------------------

def test_water_ban_excludes_water_towers():
    b.waterBan = True
    b.numPrimary = b.numMilitary = b.numMagic = b.numSupport = 5
    for _ in range(50):
        towers = b.createList()
        assert all(not t.water for t in towers)


def test_check_conditions_rejects_water_when_banned():
    b.waterBan = True
    water_tower = b.Tower("Monkey Sub", True, [5, 2, 0])
    assert b.checkConditions([water_tower]) is False


def test_check_conditions_allows_water_when_not_banned():
    b.waterBan = False
    water_tower = b.Tower("Monkey Sub", True, [5, 2, 0])
    assert b.checkConditions([water_tower]) is True


# --- Tower -----------------------------------------------------------------

def test_tower_str_format():
    assert str(b.Tower("Dart Monkey", False, [5, 2, 0])) == "Dart Monkey (5, 2, 0)"


# --- data-driven rosters ---------------------------------------------------

def test_tower_pools_loaded_from_data():
    assert set(b.towerPools) == {"Primary", "Military", "Magic", "Support", "Hero"}
    tower_names = {t["name"] for cat in ("Primary", "Military", "Magic", "Support")
                   for t in b.towerPools[cat]}
    assert len(tower_names) == 25
    # Desperado (a newer Primary) is present now that rosters come from data
    assert "Desperado" in {t["name"] for t in b.towerPools["Primary"]}


def test_heroes_loaded_from_data():
    hero_names = {h["name"] for h in b.towerPools["Hero"]}
    assert len(hero_names) == 18
    # Newer heroes are present now that the roster comes from data
    assert {"Dan D'Monke", "Silas"} <= hero_names


def test_hero_generation_draws_from_data():
    valid = {h["name"] for h in b.towerPools["Hero"]}
    for _ in range(200):
        assert b.hero().name in valid


def test_generated_towers_come_from_data():
    b.heroEnabled = False
    b.numPrimary = b.numMilitary = b.numMagic = b.numSupport = 1
    valid = {t["name"] for pool in b.towerPools.values() for t in pool}
    for _ in range(200):
        for tower in b.createList():
            assert tower.name in valid
