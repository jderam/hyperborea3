import json
from hyperborea.chargen import (
    ac_to_aac,
    calculate_ac,
    class_id_to_name,
    class_name_to_id,
    get_alignment,
    get_attr,
    get_class_level_data,
    get_hd,
    get_level,
    get_save_bonuses,
    get_starting_armour,
    get_starting_shield,
    roll_hit_points,
    select_random_class,
)


class PlayerCharacter:
    def __init__(
        self,
        method: int = 3,
        selected_class: str = "random",
        subclasses: bool = False,
        xp: int = 0,
    ):
        # Always use Method VI if a specific class is chosen
        if selected_class.lower() != "random":
            self.method = 6
            self.class_id = class_name_to_id(selected_class)
            self.class_name = class_id_to_name(self.class_id)
            self.attr = get_attr(
                method=self.method,
                class_id=self.class_id,
            )
        else:
            self.method: int = method
            self.attr = get_attr(
                method=self.method,
                class_id=0,
            )
            self.class_id = select_random_class(self.attr, subclasses)
            self.class_name = class_id_to_name(self.class_id)

        self.xp: int = int(xp)
        self.level: int = get_level(self.class_id, self.xp)

        self.alignment = get_alignment(self.class_id)

        self.hd = get_hd(self.class_id, self.level)
        self.hp = roll_hit_points(
            self.class_id,
            self.level,
            self.attr["cn"]["hp_adj"],
        )
        self.fa = get_class_level_data(self.class_id, self.level)["fa"]
        self.ca = get_class_level_data(self.class_id, self.level)["ca"]
        self.ta = get_class_level_data(self.class_id, self.level)["ta"]
        self.sv = get_class_level_data(self.class_id, self.level)["sv"]
        self.sv_bonus = get_save_bonuses(self.class_id)

        self.race_id = 0
        self.race_name = ""

        self.name = ""

        self.armour = get_starting_armour(self.class_id)
        self.shield = get_starting_shield(self.class_id)

        self.ac = calculate_ac(
            self.armour["ac"],
            self.shield["def_mod"] if self.shield is not None else 0,
            self.attr["dx"]["def_adj"],
        )
        self.aac = ac_to_aac(self.ac)

        self.weapons = []
        self.gear = []

        # calculate level

        # get allowed armour, shields, weapons

        # get starting equip

        # fill out weapon details

        # calculate hp

    def to_dict(self):
        char_dict = self.__dict__
        return char_dict

    def to_json(self):
        char_json = json.dumps(self.__dict__)
        return char_json
