import pytest
import random
from hyperborea3.player_character import PlayerCharacter
from hyperborea3.valid_data import (
    VALID_ABILITY_SCORES,
    VALID_ALIGMENTS_SHORT,
    VALID_CA,
    VALID_DENOMINATIONS,
    VALID_DICE_METHODS,
    VALID_FA,
    VALID_GENDERS,
    VALID_GP,
    VALID_LEVELS,
    VALID_RACE_IDS,
    VALID_SAVES,
    VALID_TA,
)


@pytest.mark.repeat(5000)
def test_pc():
    # stress test on building a bunch of characters
    pc = PlayerCharacter(xp=random.randint(1, 1000) * 1000)
    assert pc.attr["st"]["score"] in VALID_ABILITY_SCORES
    assert pc.attr["dx"]["score"] in VALID_ABILITY_SCORES
    assert pc.attr["cn"]["score"] in VALID_ABILITY_SCORES
    assert pc.attr["in"]["score"] in VALID_ABILITY_SCORES
    assert pc.attr["ws"]["score"] in VALID_ABILITY_SCORES
    assert pc.attr["ch"]["score"] in VALID_ABILITY_SCORES
    assert pc.level in VALID_LEVELS
    assert pc.race_id in VALID_RACE_IDS
    assert pc.gender in VALID_GENDERS
    assert pc.alignment["short_name"] in VALID_ALIGMENTS_SHORT
    assert pc.method in VALID_DICE_METHODS
    assert pc.fa in VALID_FA
    assert pc.ca in VALID_CA
    assert pc.ta in VALID_TA
    assert pc.sv in VALID_SAVES
    assert len(pc.equipment) > 0
    for k in VALID_DENOMINATIONS:
        if k == "gp":
            assert pc.money[k] in VALID_GP
        else:
            assert pc.money[k] == 0
    if pc.ca == 0:
        assert pc.spells is None
