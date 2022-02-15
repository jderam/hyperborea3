import pytest

from hyperborea3.spells import (
    get_spell,
)
from hyperborea3.valid_data import (
    VALID_SPELL_IDS,
)


def test_get_spells():
    for spell_id in VALID_SPELL_IDS:
        spell_data = get_spell(spell_id)
        assert spell_data["spell_id"] == spell_id


def test_get_invalid_spell():
    invalid_spell_id = max(VALID_SPELL_IDS) + 1
    with pytest.raises(ValueError) as exc_info:
        get_spell(invalid_spell_id)
    assert exc_info.type is ValueError
    assert exc_info.value.args[0] == f"spell_id={invalid_spell_id} is invalid."
