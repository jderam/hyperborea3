import json
import random  # noqa: F401
from typing import Dict, List

from hyperborea.chargen import (
    ac_to_aac,
    apply_spells_per_day_bonus,
    calculate_ac,
    class_id_to_name,
    class_name_to_id,
    get_alignment,
    get_attr,
    get_class_abilities,
    get_class_level_data,
    get_combat_matrix,
    get_deity,
    get_gender,
    get_hd,
    get_level,
    get_race,
    get_race_id,
    get_save_bonuses,
    get_spells,
    get_starting_armour,
    get_starting_gear,
    get_starting_money,
    get_starting_shield,
    get_starting_weapons_melee,
    get_starting_weapons_missile,
    get_thief_skills,
    get_turn_undead_matrix,
    get_xp_bonus,
    get_xp_to_next,
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
        self.xp_to_next: int = get_xp_to_next(self.class_id, self.level)
        self.xp_bonus: bool = get_xp_bonus(self.class_id, self.attr)

        self.alignment = get_alignment(self.class_id)
        self.deity = get_deity(self.alignment["short_name"])
        self.race_id = get_race_id()
        self.race = get_race(self.race_id)
        self.gender = get_gender()

        self.hd = get_hd(self.class_id, self.level)
        self.hp = roll_hit_points(
            self.class_id,
            self.level,
            self.attr["cn"]["hp_adj"],
        )
        cl_data = get_class_level_data(self.class_id, self.level)
        self.fa = cl_data["fa"]
        self.ca = cl_data["ca"]
        self.ta = cl_data["ta"]
        self.sv = cl_data["sv"]

        self.sv_bonus = get_save_bonuses(self.class_id)

        self.combat_matrix = get_combat_matrix(self.fa)

        self.name = ""

        self.armour = get_starting_armour(self.class_id)
        self.shield = get_starting_shield(self.class_id)

        self.ac = calculate_ac(
            self.armour["ac"],
            self.shield["def_mod"] if self.shield is not None else 0,
            self.attr["dx"]["def_adj"],
        )
        self.aac = ac_to_aac(self.ac)

        self.weapons_melee = get_starting_weapons_melee(self.class_id)
        self.weapons_missile = get_starting_weapons_missile(self.class_id)
        # fill out weapon details
        self.equipment = get_starting_gear(self.class_id)
        self.money = get_starting_money()

        self.thief_skills = get_thief_skills(
            self.class_id,
            self.level,
            self.attr["dx"]["score"],
            self.attr["in"]["score"],
            self.attr["ws"]["score"],
        )

        self.turn_undead_matrix = get_turn_undead_matrix(
            self.ta,
            self.attr["ch"]["turn_adj"],
        )

        # TODO: Make a wrapper function for all the functions needed
        # to get final spell list (familiar, etc.)
        self.spells = apply_spells_per_day_bonus(
            spells=get_spells(self.class_id, self.level, self.ca),
            bonus_spells_in=self.attr["in"]["bonus_spells"],
            bonus_spells_ws=self.attr["ws"]["bonus_spells"],
        )

        self.class_abilities = get_class_abilities(self.class_id, self.level)
        self.apply_class_ability_funcs(self.class_abilities)

        self.cleanup()

    def apply_class_ability_funcs(self, class_abilities: List[Dict]) -> None:
        """"""

        def extraordinary(stats: List[str]):
            for stat in stats:
                self.attr[stat]["feat"] += 8

        def gain_familiar():
            pass

        def improve_attack_rate():
            pass

        def improve_mv(mv: int):
            pass

        def mastery(weapon_ids: List[int]):
            pass

        def monk_ac_bonus(level: int):
            pass

        def monk_empty_hand(level: int):
            pass

        def monk_run(level: int):
            pass

        def priest_specialized_faith(alignment: str, level: int):
            pass

        def runegraving(level: int):
            pass

        def skilful_defender(level: int):
            pass

        upd_functions = [
            x["upd_function"] for x in class_abilities if x["upd_function"] is not None
        ]
        for uf in upd_functions:
            eval(uf)

        return

    def cleanup(self):
        for a in self.class_abilities:
            del a["upd_function"]

    def to_dict(self):
        char_dict = self.__dict__
        return char_dict

    def to_json(self):
        char_json = json.dumps(self.__dict__)
        return char_json


if __name__ == "__main__":
    from pprint import pprint

    pc = PlayerCharacter(subclasses=True)
    pprint(pc.to_dict())
