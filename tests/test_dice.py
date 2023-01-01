import pytest
import random

from hyperborea3.chargen import (
    roll_dice,
    roll_ndn_drop_lowest,
    roll_ndn_drop_highest,
    roll_stats,
)

AVG_4D6_DROP_LOWEST = 12.2446
AVG_4D6_DROP_HIGHEST = 8.7554
TOLERANCE = 0.1


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


def test_ndn_drop_lowest():
    sample = [roll_ndn_drop_lowest(4, 6, 1) for _ in range(10000)]
    average = sum(sample) / len(sample)
    assert (
        (AVG_4D6_DROP_LOWEST - TOLERANCE)
        <= average
        <= (AVG_4D6_DROP_LOWEST + TOLERANCE)
    )


def test_ndn_drop_highest():
    sample = [roll_ndn_drop_highest(4, 6, 1) for _ in range(10000)]
    average = sum(sample) / len(sample)
    assert (
        (AVG_4D6_DROP_HIGHEST - TOLERANCE)
        <= average
        <= (AVG_4D6_DROP_HIGHEST + TOLERANCE)
    )


@pytest.mark.repeat(1000)
def test_dice_method5():
    attr = roll_stats(method=5, class_id=random.randint(1, 4))
    for stat in attr:
        assert 8 <= attr[stat]["score"] <= 18
