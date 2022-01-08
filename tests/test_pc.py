from hyperborea.player_character import PlayerCharacter
from valid_data import (
    VALID_ABILITY_SCORES,
    VALID_ALIGMENTS_SHORT,
    VALID_CA,
    VALID_DICE_METHODS,
    VALID_FA,
    VALID_GENDERS,
    VALID_LEVELS,
    VALID_RACE_IDS,
    VALID_SAVES,
    VALID_TA,
)


def test_pc():
    # stress test on building a bunch of characters
    for i in range(10000):
        pc = PlayerCharacter()
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
