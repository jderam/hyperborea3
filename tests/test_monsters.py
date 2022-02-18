from hyperborea3.monsters import get_all_monsters
from hyperborea3.valid_data import VALID_MONSTER_IDS


def test_get_all_monsters():
    monsters = get_all_monsters()
    assert [x["monster_id"] for x in monsters] == VALID_MONSTER_IDS
