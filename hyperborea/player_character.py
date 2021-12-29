import json
from typing import List
from chargen import (
    class_name_to_id,
    get_attr,
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
            method = 6
            self.class_id = class_name_to_id(selected_class)
        self.method: int = method
        
        # Convert selected_class to class_id
        self.class_id = None
        
        self.name = ""
        
        self.class_name = ""
        self.race_id = 0
        self.race_name = ""
        self.xp: int = xp
        self.level: int = 0
        self.attr = get_attr(
            method=method,
            class_id=class_name_to_id(selected_class),
        )
        self.hp = 0
        self.ac = 0
        self.aac = 0
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
        self.mv = 0
        self.armour = []
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
