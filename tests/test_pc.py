from hyperborea.player_character import PlayerCharacter


def test_pc():
    # stress test on building a bunch of characters
    for i in range(10000):
        pc = PlayerCharacter()
        assert pc.attr["st"]["score"] in range(3, 19)
        assert pc.attr["dx"]["score"] in range(3, 19)
        assert pc.attr["cn"]["score"] in range(3, 19)
        assert pc.attr["in"]["score"] in range(3, 19)
        assert pc.attr["ws"]["score"] in range(3, 19)
        assert pc.attr["ch"]["score"] in range(3, 19)
        assert pc.level in range(1, 13)
