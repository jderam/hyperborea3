from pathlib import Path
from hyperborea.chargen import (
    DB,
    ac_to_aac,
    calculate_ac,
    get_alignment,
    get_attr_mod,
    get_class_level_data,
    get_class_list,
    get_hd,
    get_level,
    get_starting_armour,
    get_starting_shield,
    roll_hit_points,
)


def test_db():
    assert Path(DB).is_file()


def test_get_class_list():
    class_list = get_class_list(subclasses=True)
    assert len(class_list) == 33
    class_list = get_class_list(subclasses=False)
    assert len(class_list) == 4


def test_get_level():
    for class_id in range(1, 34):
        for xp in range(0, 1000000, 1000):
            level = get_level(class_id, xp)
            assert level in range(1, 13)


def test_get_class_level_data():
    for class_id in range(1, 34):
        for level in range(1, 13):
            cl_data = get_class_level_data(class_id, level)
            assert cl_data["fa"] in range(0, 13)
            assert cl_data["ca"] in range(0, 13)
            assert cl_data["ta"] in range(0, 13)
            assert cl_data["sv"] in range(11, 17)


def test_get_hd():
    for class_id in range(1, 34):
        for level in range(1, 13):
            hd = get_hd(class_id, level)
            qty = hd.split("d")[0]
            # number of dice in 1-9
            assert int(qty) in range(1, 10)
            part2 = hd.split("d")[1].split("+")
            assert len(part2) in [1, 2]
            # die size in d4, d6, d8, d10, d12
            assert int(part2[0]) in [4, 6, 8, 10, 12]
            if len(part2) == 2:
                # +hp in 1,2,3; 2,4,6; 3,6,9; 4,8,12
                assert int(part2[1]) in [1, 2, 3, 4, 6, 8, 9, 12]


def test_roll_hit_points():
    max_possible_hp = (10 * 12) + (12 * 3)  # Barbarian
    for class_id in range(1, 34):
        for level in range(1, 13):
            for cn_score in range(3, 19):
                mods = get_attr_mod("cn", cn_score)
                hp_adj = mods["hp_adj"]
                hp = roll_hit_points(class_id, level, hp_adj)
                assert level <= hp <= max_possible_hp


def test_starting_armour():
    for class_id in range(1, 34):
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
            "description",
        ]


def test_starting_shield():
    for class_id in range(1, 34):
        shield = get_starting_shield(class_id)
        assert shield is None or list(shield.keys()) == [
            "shield_id",
            "shield_type",
            "def_mod",
            "cost",
            "weight",
        ]


def test_calculate_ac():
    for class_id in range(1, 34):
        armour = get_starting_armour(class_id)
        shield = get_starting_shield(class_id)
        shield_def_mod = shield["def_mod"] if shield is not None else 0
        for dx_score in range(3, 19):
            dx_mod = get_attr_mod("dx", dx_score)
            ac = calculate_ac(
                armour["ac"],
                shield_def_mod,
                dx_mod["def_adj"],
            )
            # all AC values for starting characters should be 1 to 11 (level 1)
            # This may need updating after we include higher-level PCs,
            #   depending on if they have any abilities that improve AC
            assert ac in range(
                1, 12
            ), f"""invalid ac:
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


def test_alignment():
    for class_id in range(1, 34):
        alignment = get_alignment(class_id)
        if class_id in [1, 2, 3, 7, 8, 11, 13, 18, 19]:
            allowed_alignments = ["CE", "CG", "LE", "LG", "N"]
        elif class_id in [4, 24, 25, 26, 31]:
            allowed_alignments = ["CE", "CG", "LE", "N"]
        elif class_id == 10:
            allowed_alignments = ["CG", "LG", "N"]
        elif class_id in [14, 22, 30]:
            allowed_alignments = ["CE", "LE", "N"]
        elif class_id in [15, 16, 21, 23, 29, 32]:
            allowed_alignments = ["CE", "CG", "N"]
        elif class_id in [12, 28]:
            allowed_alignments = ["LE", "LG", "N"]
        elif class_id in [5, 6, 20]:
            allowed_alignments = ["CE", "CG"]
        elif class_id == 33:
            allowed_alignments = ["LE", "N"]
        elif class_id == 9:
            allowed_alignments = ["LG"]
        elif class_id == 27:
            allowed_alignments = ["LE"]
        elif class_id == 17:
            allowed_alignments = ["N"]
        else:
            raise ValueError(f"Unexpected class_id: {class_id}")

        assert (
            alignment["short_name"] in allowed_alignments
        ), f"""
            Unexpected alignment '{alignment}' not in
            allowed values {allowed_alignments}
        """
