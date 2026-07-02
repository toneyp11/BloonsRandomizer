# tests/test_randomizer.py
"""Unit tests for the pure randomizer logic (no GUI required)."""
import pytest

import BloonsRandomizer as b


@pytest.fixture(autouse=True)
def default_config():
    """Reset the module-level config globals to known values before each test."""
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


# --- camo detection guarantee ----------------------------------------------

def test_tower_has_camo_uses_rolled_paths():
    dart = next(t for t in b.towerPools["Primary"] if t["name"] == "Dart Monkey")
    # Enhanced Eyesight is path 3 tier 2: camo only when bottom path >= 2
    assert b.towerHasCamo(dart, [5, 2, 0]) is False   # bottom path unbought
    assert b.towerHasCamo(dart, [5, 0, 2]) is True     # bottom path at tier 2
    assert b.towerHasCamo(dart, [2, 0, 5]) is True     # bottom path at tier 5


def test_tower_has_camo_innate():
    ninja = next(t for t in b.towerPools["Magic"] if t["name"] == "Ninja Monkey")
    assert b.towerHasCamo(ninja, [0, 2, 5]) is True    # innate, any spread


def test_generated_sets_always_have_camo():
    b.waterBan = False
    b.heroEnabled = True
    b.numPrimary = b.numMilitary = b.numMagic = b.numSupport = 1
    for _ in range(300):
        towers = b.createList()
        assert any(t.camo for t in towers)


def test_only_innate_heroes_satisfy_camo():
    # a generated hero counts for camo only if it detects camo from level 1
    innate = {"Ezili", "Sauda", "Psi", "Silas"}
    for _ in range(300):
        h = b.hero()
        assert h.camo == (h.name in innate)


def test_impossible_camo_config_does_not_hang():
    # no towers and no hero -> empty set; must return without looping forever
    b.heroEnabled = False
    b.numPrimary = b.numMilitary = b.numMagic = b.numSupport = 0
    assert b.createList() == []


# --- distinct fifth tiers --------------------------------------------------

def _main_index(tower):
    return tower.paths.index(b.mainUpgrades)


def test_two_duplicates_get_distinct_fifth_tiers():
    towers = [b.Tower("Dart Monkey", False, [5, 2, 0]),
              b.Tower("Dart Monkey", False, [5, 0, 2])]
    b.enforceDistinctFifthTiers(towers)
    assert _main_index(towers[0]) != _main_index(towers[1])


def test_three_duplicates_use_all_three_paths():
    towers = [b.Tower("Dart Monkey", False, [5, 2, 0]) for _ in range(3)]
    b.enforceDistinctFifthTiers(towers)
    assert sorted(_main_index(t) for t in towers) == [0, 1, 2]


def test_four_duplicates_allowed_with_max_distinctness():
    towers = [b.Tower("Dart Monkey", False, [5, 2, 0]) for _ in range(4)]
    b.enforceDistinctFifthTiers(towers)  # must not raise
    # only three paths exist, so four copies cover all three (one repeat)
    assert len(set(_main_index(t) for t in towers)) == 3


def test_distinct_towers_are_untouched():
    dart = b.Tower("Dart Monkey", False, [5, 2, 0])
    ninja = b.Tower("Ninja Monkey", False, [0, 2, 5])
    b.enforceDistinctFifthTiers([dart, ninja])
    assert dart.paths == [5, 2, 0]
    assert ninja.paths == [0, 2, 5]


def test_generated_duplicates_have_distinct_fifth_tiers():
    b.heroEnabled = False
    b.waterBan = False
    b.numPrimary = b.numMilitary = b.numMagic = b.numSupport = 5
    for _ in range(200):
        groups = {}
        for tower in b.createList():
            groups.setdefault(tower.name, []).append(tower)
        for name, group in groups.items():
            mains = [_main_index(t) for t in group]
            # distinct while the 3 paths allow it, then repeats are permitted
            assert len(set(mains)) == min(len(group), 3), (name, mains)


def test_check_conditions_rejects_water_when_banned():
    b.waterBan = True
    water_tower = b.Tower("Monkey Sub", True, [5, 2, 0])
    assert b.checkConditions([water_tower]) is False


def test_check_conditions_allows_water_when_not_banned():
    b.waterBan = False
    water_tower = b.Tower("Monkey Sub", True, [5, 2, 0])
    water_tower.camo = True  # satisfy the always-on camo guarantee in isolation
    assert b.checkConditions([water_tower]) is True


# --- Tower -----------------------------------------------------------------

def test_tower_str_format():
    assert str(b.Tower("Dart Monkey", False, [5, 2, 0])) == "Dart Monkey (5, 2, 0)"


def test_hero_str_has_no_path():
    assert str(b.Tower("Quincy", False, None, isHero=True)) == "Quincy"


def test_camo_marker_on_tower():
    tower = b.Tower("Dartling Gunner", False, [0, 5, 2])
    tower.camo = True
    assert str(tower) == "Dartling Gunner (0, 5, 2) [Camo]"


def test_camo_marker_on_hero():
    hero = b.Tower("Ezili", False, None, isHero=True)
    hero.camo = True
    assert str(hero) == "Ezili [Camo]"


def test_no_camo_marker_when_not_detected():
    assert "[Camo]" not in str(b.Tower("Bomb Shooter", False, [5, 2, 0]))


def test_generated_heroes_display_without_path():
    for _ in range(200):
        text = str(b.hero())
        assert "(" not in text, text


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


def test_single_type_config_yields_only_that_type():
    # the effect the "Primary Only" preset configures: 4 primary, 0 of the rest
    b.heroEnabled = False
    b.numPrimary, b.numMilitary, b.numMagic, b.numSupport = 4, 0, 0, 0
    primary_names = {t["name"] for t in b.towerPools["Primary"]}
    for _ in range(100):
        towers = b.createList()
        assert len(towers) == 4
        assert all(t.name in primary_names for t in towers)


def test_generated_towers_come_from_data():
    b.heroEnabled = False
    b.numPrimary = b.numMilitary = b.numMagic = b.numSupport = 1
    valid = {t["name"] for pool in b.towerPools.values() for t in pool}
    for _ in range(200):
        for tower in b.createList():
            assert tower.name in valid
