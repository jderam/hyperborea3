import pytest

from hyperborea3.spells import (
    get_all_spells,
    get_spell,
)
from hyperborea3.valid_data import (
    VALID_SPELL_IDS,
)


def test_get_spell():
    for spell_id in VALID_SPELL_IDS:
        spell_data = get_spell(spell_id)
        assert spell_data["spell_id"] == spell_id
        assert spell_data["reversible"] in [None, True, False]


def test_get_invalid_spell():
    invalid_spell_id = max(VALID_SPELL_IDS) + 1
    with pytest.raises(ValueError) as exc_info:
        get_spell(invalid_spell_id)
    assert exc_info.type is ValueError
    assert exc_info.value.args[0] == f"spell_id={invalid_spell_id} is invalid."


def test_get_all_spells():
    spells = get_all_spells()
    assert [x["spell_id"] for x in spells] == VALID_SPELL_IDS
    for spell in spells:
        assert spell["reversible"] in [None, True, False]
