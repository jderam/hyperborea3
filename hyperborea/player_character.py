import json
from typing import List
from hyperborea.chargen import (
    ac_to_aac,
    calculate_ac,
    class_id_to_name,
    class_name_to_id,
    get_attr,
    get_starting_armour,
    get_starting_shield,
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
            self.class_id = select_random_class(self.attr)
            self.class_name = class_id_to_name(self.class_id)
        
        self.xp: int = int(xp)
        self.level: int = 0

        self.hd = 0
        self.hp = 0
        self.name = ""
        self.race_id = 0
        self.race_name = ""

        

        self.fa = 0
        self.ca = 0
        self.ta = 0
        self.sv = {
            "save": 0,
            "bonuses": {
                "death": 0,
                "transformation": 0,
                "device": 0,
                "avoidance": 0,
                "sorcery": 0,
            },
        }
        
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

        # get scores

        # get mods

        # get qualifying classes

        # get class

        # calculate level

        # get alignment

        # get st bonuses

        # get allowed armour, shields, weapons

        # get starting equip

        # calculate ac

        # fill out weapon details

        # calculate hp

    def to_dict(self):
        char_dict = self.__dict__
        return char_dict

    def to_json(self):
        char_json = json.dumps(self.__dict__)
        return char_json

if __name__ == "__main__":
    pc = PlayerCharacter()
    print(pc.to_dict())
