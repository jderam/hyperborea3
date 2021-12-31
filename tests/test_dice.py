import hyperborea.chargen as cg


def test_3d6():
    results = [cg.roll_dice(3, 6) for i in range(10000)]
    assert min(results) == 3
    assert max(results) == 18
    assert 10.4 <= sum(results) / len(results) <= 10.6
