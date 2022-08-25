import pytest

from tests.random_data import random_rider_score, random_rider_scores
from storing.domain.model import Heat, RiderScores, Score


def test_heat_can_contain_less_than_4_riders():
    # given
    heat = Heat(heat_number=1, attempt_number=1, finished=True)

    # when
    heat.save_result(random_rider_scores())

    # then
    assert list(heat.rider_scores.keys()) == ['a', 'b', 'c', 'd']

    # when
    heat.save_result(random_rider_scores(rider_numbers=3))

    # then
    assert list(heat.rider_scores.keys()) == ['a', 'b', 'c', 'd']


def test_riders_received_unique_scores():
    # given
    heat = Heat(heat_number=1, attempt_number=1, finished=True)

    # when
    with pytest.raises(Exception):
        heat.save_result(RiderScores(
            rider_a=random_rider_score(score=Score.ONE),
            rider_b=random_rider_score(score=Score.ONE),
            rider_c=random_rider_score(score=Score.ONE),
            rider_d=random_rider_score(score=Score.ONE),
        ))


def test_riders_received_most_scores_as_it_possible():
        # given
    heat = Heat(heat_number=1, attempt_number=1, finished=True)

    # when
    heat.save_result(RiderScores(
        rider_a=random_rider_score(score=Score.THREE),
        rider_b=random_rider_score(score=Score.TWO),
        rider_c=None,
        rider_d=random_rider_score(score=Score.ONE),
    ))

    with pytest.raises(Exception):
        heat.save_result(RiderScores(
            rider_a=random_rider_score(score=Score.TWO),
            rider_b=random_rider_score(score=Score.ONE),
            rider_c=random_rider_score(score=Score.ZERO),
            rider_d=None
        ))
