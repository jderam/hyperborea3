from pathlib import Path
import pytest
from hyperborea.chargen import (
    DB,
    ac_to_aac,
    calculate_ac,
    get_attr_mod,
    get_starting_armour,
    get_starting_shield,
)



def test_db():
    assert Path(DB).is_file()

def test_starting_armour():
    for class_id in range(1,34):
        armour = get_starting_armour(class_id)
        assert list(armour.keys()) == [
            "armour_id",
            "armour_type",
            "ac",
            "dr",
            "weight_class",
            "mv",
            "cost",
            "weight",
            "description"
        ]

def test_starting_shield():
    for class_id in range(1,34):
        shield = get_starting_shield(class_id)
        assert shield is None or list(shield.keys()) == [
            "shield_id",
            "shield_type",
            "def_mod",
            "cost",
            "weight",
        ]
    

def test_calculate_ac():
    for class_id in range(1,34):
        armour = get_starting_armour(class_id)
        shield = get_starting_shield(class_id)
        shield_def_mod = shield["def_mod"] if shield is not None else 0
        for dx_score in range(3,19):
            dx_mod = get_attr_mod("dx", dx_score)
            ac = calculate_ac(
                armour["ac"],
                shield_def_mod,
                dx_mod["def_adj"],
            )
            # all AC values for starting characters should be 1 to 11 (level 1)
            # This may need updating after we include higher-level PCs,
            #   depending on if they have any abilities that improve AC
            assert ac in range(1,12), f"""invalid ac:
                class_id       = {class_id}
                armour_ac      = {armour["ac"]}
                shield_def_mod = {shield_def_mod}
                dx_score       = {dx_score}
                dx_def_adj     = {dx_mod["def_adj"]}
                ac             = {ac}
            """

def test_ac_to_aac():
    for ac in range(-10, 20):
        aac = ac_to_aac(ac)
        assert ac + aac == 19
