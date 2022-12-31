import pytest
import random

from hyperborea3.chargen import roll_dice, roll_stats


def test_3d6():
    results = [roll_dice(3, 6) for i in range(10000)]
    assert min(results) == 3
    assert max(results) == 18
    assert 10.4 <= sum(results) / len(results) <= 10.6


@pytest.mark.repeat(1000)
def test_reroll():
    result = roll_dice(1, 6, reroll=[1])
    assert 2 <= result <= 6


def test_reroll_exception():
    with pytest.raises(AssertionError):
        roll_dice(1, 6, reroll=[1, 2, 3, 4, 5, 6])


@pytest.mark.repeat(1000)
def test_dice_method5():
    attr = roll_stats(method=5, class_id=random.randint(1, 4))
    for stat in attr:
        assert 8 <= attr[stat]["score"] <= 18
