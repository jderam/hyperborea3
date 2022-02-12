from pathlib import Path
import json
from hyperborea3.chargen import get_level, get_xp_to_next
from hyperborea3.player_character import PlayerCharacter
from hyperborea3.valid_data import VALID_CLASS_ID_MAP


def generate_sample_pcs():
    root_dir = f"{Path(__file__).parent.parent}/hyperborea3/sample_data/PlayerCharacter"
    print(f"{root_dir=}")
    for class_id, class_name in VALID_CLASS_ID_MAP.items():
        xp = 0
        xp_to_next = 1
        while xp_to_next:
            level = get_level(class_id, xp)
            print(f"Generating {class_name=} {level=}")
            xp_to_next = get_xp_to_next(class_id, level)

            file_name = f"{class_name.replace(' ', '_')}_{str(level).zfill(2)}.json"
            out_path = f"{root_dir}/{file_name}"
            pc_json = PlayerCharacter(class_id=class_id, xp=xp).to_dict()
            print(f"writing file {out_path=}")
            with open(out_path, "w") as f:
                f.write(json.dumps(pc_json, indent=4))
            xp = xp_to_next


if __name__ == "__main__":
    generate_sample_pcs()
