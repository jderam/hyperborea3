from hyperborea3.chargen import get_spells


def test_level7_spells():
    spells = get_spells(10, 7, 1)
    assert spells is not None
    if spells is not None:
        assert list(spells["drd"].keys()) == ["spells_per_day", "spells_known"]
        assert list(spells["mag"].keys()) == ["spells_per_day", "spells_known"]
