import json
import logging
import random  # noqa: F401
from typing import Any, Dict, List, Optional
from uuid import uuid4

from hyperborea3 import __version__ as HYPERBOREA3_VERSION
from hyperborea3.chargen import (
    ac_to_aac,
    apply_spells_per_day_bonus,
    calculate_ac,
    class_id_to_name,
    get_age,
    get_alignment,
    get_attr,
    get_class_abilities,
    get_class_level_data,
    get_combat_matrix,
    get_complexion,
    get_deity,
    get_eye_colour,
    get_favoured_weapons,
    get_gender,
    get_hair_colour,
    get_hd,
    get_height_and_weight,
    get_languages,
    get_level,
    get_next_atk_rate,
    get_priest_abilities,
    get_race,
    get_race_id,
    get_random_familiar,
    get_save_bonuses,
    get_secondary_skill,
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
    roll_dice,
    roll_hit_points,
    select_random_class,
)
from hyperborea3.namegen import generate_name
from hyperborea3.valid_data import (
    VALID_AC_TYPES,
    VALID_CLASS_IDS,
    VALID_DICE_METHODS,
    VALID_SUBCLASS_PARAMS,
)

logger = logging.getLogger(__name__)


class PlayerCharacter:
    def __init__(
        self,
        method: int = 3,
        class_id: int = 0,
        subclasses: int = 2,
        xp: int = 0,
        ac_type: str = "descending",
    ):
        # validations
        assert method in VALID_DICE_METHODS
        assert class_id in [0] + VALID_CLASS_IDS
        assert subclasses in VALID_SUBCLASS_PARAMS
        assert ac_type in VALID_AC_TYPES

        self.app_version = HYPERBOREA3_VERSION
        self.character_id: str = uuid4().hex

        # Always use Method VI if a specific class is chosen
        if class_id != 0:
            self.method: int = 6
            self.class_id = class_id
            self.class_name = class_id_to_name(self.class_id)
            self.attr = get_attr(
                method=self.method,
                class_id=self.class_id,
            )
        else:
            self.method = method
            self.attr = get_attr(
                method=self.method,
                class_id=class_id,
            )
            self.class_id = select_random_class(self.attr, subclasses)
            self.class_name = class_id_to_name(self.class_id)

        self.xp: int = int(xp)
        self.level: int = get_level(self.class_id, self.xp)
        self.xp_to_next: Optional[int] = get_xp_to_next(self.class_id, self.level)
        self.xp_bonus: bool = get_xp_bonus(self.class_id, self.attr)

        # Background
        self.race_id: int = get_race_id()
        self.race: str = get_race(self.race_id)
        self.gender: str = get_gender()
        self.name: str = generate_name(self.race_id, self.gender)
        self.age: int = get_age(self.race_id)
        height, weight = get_height_and_weight(self.race_id, self.gender)
        self.height: str = height
        self.weight: str = weight
        self.eye_colour: str = get_eye_colour(self.race_id, self.gender)
        self.hair_colour: str = get_hair_colour(self.race_id, self.gender)
        self.complexion: str = get_complexion(self.race_id, self.gender)
        self.alignment: Dict[str, Any] = get_alignment(self.class_id)
        self.languages: List[str] = get_languages(self.attr["in"]["lang"])
        self.deity: Dict[str, Any] = get_deity(self.alignment["short_name"])
        self.secondary_skill: str = get_secondary_skill()

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

        if ac_type == "descending":
            self.combat_matrix = get_combat_matrix(self.fa)
        self.armour = get_starting_armour(self.class_id)
        self.shield = get_starting_shield(self.class_id)

        self.ac = calculate_ac(
            self.armour["ac"],
            self.shield["def_mod"] if self.shield is not None else 0,
            self.attr["dx"]["def_adj"],
        )
        self.mv = self.armour["mv"]

        self.weapons_melee = get_starting_weapons_melee(self.class_id)
        self.weapons_missile = get_starting_weapons_missile(self.class_id)
        self.update_weapons_atk_dmg()
        self.equipment = get_starting_gear(self.class_id)
        self.money = get_starting_money()
        self.favoured_weapons = get_favoured_weapons(self.class_id)

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

        if ac_type == "ascending":
            self.ascending_ac()

        self.sort_class_abilities()
        self.cleanup()

    def update_weapons_atk_dmg(self):
        for w in self.weapons_melee:
            # w["melee_atk"] += self.fa
            w["melee_atk"] += self.attr["st"]["atk_mod"]
            w["dmg_adj"] += self.attr["st"]["dmg_adj"]
            if w["hurlable"]:
                # w["hurled_atk"] += self.fa
                w["hurled_atk"] += self.attr["dx"]["atk_mod"]
        for w in self.weapons_missile:
            # w["missile_atk"] += self.fa
            w["missile_atk"] += self.attr["dx"]["atk_mod"]
            if w["hurled"]:
                w["dmg_adj"] += self.attr["st"]["dmg_adj"]

    def apply_class_ability_funcs(self, class_abilities: List[Dict[str, Any]]) -> None:
        """"""

        def extraordinary(stats: List[str]):
            for stat in stats:
                self.attr[stat]["feat"] += 8

        def gain_familiar():
            animal = get_random_familiar()
            hp = roll_dice(1, 3) + 1
            self.hp += hp
            if self.class_id == 2:
                school = "mag"
            elif self.class_id == 16:
                school = "wch"
            else:
                ValueError(
                    "Only expecting Magician (2) or Witch (16). "
                    f"Got {self.class_id=}"
                )
            if self.spells is not None:
                for spd_lvl in self.spells[school]["spells_per_day"].keys():
                    if self.spells[school]["spells_per_day"][spd_lvl] > 0:
                        self.spells[school]["spells_per_day"][spd_lvl] += 1
            for cls_abl in self.class_abilities:
                if cls_abl["ability_title"] == "Familiar":
                    cls_abl["brief_desc"] += f". [{animal}, {hp} hp]"

        def improve_attack_rate():
            for w in self.weapons_melee:
                w["atk_rate"] = get_next_atk_rate(w["atk_rate"])

        def improve_mv(mv: int):
            self.mv = mv

        def mastery(weapon_ids: List[int]):
            for w in self.weapons_melee:
                if w["weapon_id"] in weapon_ids:
                    w["mastery"] = True
                    w["atk_rate"] = get_next_atk_rate(w["atk_rate"])
                    w["melee_atk"] += 1
                    w["dmg_adj"] += 1
                    if w["hurlable"]:
                        w["hurled_rof"] = get_next_atk_rate(w["hurled_rof"])
                        w["hurled_atk"] += 1

            for w in self.weapons_missile:
                if w["weapon_id"] in weapon_ids:
                    w["mastery"] = True
                    w["missile_atk"] += 1
                    w["dmg_adj"] += 1
                    # Long Bow and Short Bow
                    if w["weapon_id"] in [209, 211]:
                        # advance once for levels 1-6
                        w["rof"] = get_next_atk_rate(w["rof"])
                        # advance again for levels 7-12
                        if self.level >= 7:
                            w["rof"] = get_next_atk_rate(w["rof"])
                    # Light Crossbow
                    elif w["weapon_id"] == 214:
                        # only advance for levels 7-12
                        if self.level >= 7:
                            w["rof"] = get_next_atk_rate(w["rof"])
                    else:
                        raise ValueError(
                            "Only expecting mastery for missile weapons 209/211/214, "
                            f"not weapon_id={w['weapon_id']}"
                        )

        def monk_ac_bonus(level: int):
            ac_bonus = (level + 1) // 2
            self.ac -= ac_bonus
            for cls_abl in self.class_abilities:
                if cls_abl["ability_title"] == "Defensive Ability":
                    cls_abl["brief_desc"] += f" (+{ac_bonus})"

        def monk_empty_hand(level: int):
            empty_hand_dice = (level + 2) // 3
            empty_hand_damage = f"{empty_hand_dice}d4"
            for w in self.weapons_melee:
                if w["weapon_id"] == 104:
                    w["atk_rate"] = "2/1"
                    w["damage"] = f"{empty_hand_damage}+1"
                    if self.level >= 5:
                        w["melee_atk"] += 1
            for cls_abl in self.class_abilities:
                if cls_abl["ability_title"] == "Empty Hand":
                    cls_abl["brief_desc"] += f" ({empty_hand_damage} damage)"

        def monk_run(level: int):
            self.mv = 50
            if level >= 7:
                self.mv = 60

        def priest_specialized_faith(deity_id: int, level: int):
            ability_name = f"Specialized Faith ({self.deity['deity_name']})"
            priest_abilities = get_priest_abilities(deity_id, level)
            for p in priest_abilities:
                self.class_abilities.append(
                    {
                        "class_id": self.class_id,
                        "level": p["level"],
                        "ability_title": ability_name,
                        "brief_desc": p["ability_desc"],
                        "ability_desc": None,
                        "upd_function": None,
                    }
                )
            self.class_abilities = [
                x
                for x in self.class_abilities
                if x["ability_title"] != "Specialized Faith"
            ]

        def runegraving(level: int):
            pass

        def skilful_defender(level: int):
            ac_bonus = 1
            if level >= 7:
                ac_bonus = 2
            self.ac -= ac_bonus
            for cls_abl in self.class_abilities:
                if cls_abl["ability_title"] == "Skilful Defender":
                    cls_abl["brief_desc"] += f" (+{ac_bonus})"

        upd_functions = [
            x["upd_function"] for x in class_abilities if x["upd_function"] is not None
        ]
        for uf in upd_functions:
            eval(uf)

        return

    def ascending_ac(self):
        self.armour["ac"] = ac_to_aac(self.armour["ac"])
        self.ac = ac_to_aac(self.ac)
        for w in self.weapons_melee:
            w["melee_atk"] += self.fa
            if w["hurlable"]:
                w["hurled_atk"] += self.fa
        for w in self.weapons_missile:
            w["missile_atk"] += self.fa

    def sort_class_abilities(self):
        self.class_abilities = sorted(
            self.class_abilities, key=lambda x: (x["level"], x["ability_title"])
        )

    def cleanup(self):
        for a in self.class_abilities:
            del a["upd_function"]

    def to_dict(self):
        char_dict = self.__dict__
        return char_dict

    def to_json(self, indent=None):
        char_json = json.dumps(self.__dict__, indent=indent)
        return char_json


if __name__ == "__main__":
    from pprint import pprint

    pc = PlayerCharacter()
    pprint(pc.to_dict())
