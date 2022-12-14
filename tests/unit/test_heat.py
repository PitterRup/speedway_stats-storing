import pytest

from tests.random_data import random_rider_score, random_rider_scores
from storing.domain.models.team_match_game import Heat, HelmetColor, RiderScores, Score


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
            rider_a=random_rider_score(Score(1), HelmetColor.BLUE),
            rider_b=random_rider_score(Score(1), HelmetColor.RED),
            rider_c=random_rider_score(Score(1), HelmetColor.WHITE),
            rider_d=random_rider_score(Score(1), HelmetColor.YELLOW),
        ))


def test_riders_have_unique_helmet_colors():
    # given
    heat = Heat(heat_number=1, attempt_number=1, finished=True)

    # when
    heat.save_result(RiderScores(
        rider_a=random_rider_score(Score(3), HelmetColor.BLUE),
        rider_b=random_rider_score(Score(2), HelmetColor.RED),
        rider_c=random_rider_score(Score(1), HelmetColor.WHITE),
        rider_d=random_rider_score(Score(0), HelmetColor.YELLOW),
    ))
    with pytest.raises(Exception):
        heat.save_result(RiderScores(
            rider_a=random_rider_score(Score(3), HelmetColor.BLUE),
            rider_b=random_rider_score(Score(2), HelmetColor.BLUE),
            rider_c=random_rider_score(Score(1), HelmetColor.BLUE),
            rider_d=random_rider_score(Score(0), HelmetColor.BLUE),
        ))


def test_riders_received_most_scores_as_possible():
    # given
    heat = Heat(heat_number=1, attempt_number=1, finished=True)

    # when
    heat.save_result(RiderScores(
        rider_a=random_rider_score(Score(3), HelmetColor.BLUE),
        rider_b=random_rider_score(Score(2), HelmetColor.RED),
        rider_c=None,
        rider_d=random_rider_score(Score(1), HelmetColor.WHITE),
    ))

    with pytest.raises(Exception):
        heat.save_result(RiderScores(
            rider_a=random_rider_score(Score(2), HelmetColor.BLUE),
            rider_b=random_rider_score(Score(1), HelmetColor.RED),
            rider_c=random_rider_score(Score(0), HelmetColor.WHITE),
            rider_d=None
        ))

def test_heat_attempt_not_finished_must_have_result_without_scores():
    # given
    heat = Heat(heat_number=1, attempt_number=1, finished=False)

    # when
    heat.save_result(
        RiderScores(
            rider_a=random_rider_score(None, HelmetColor.BLUE),
            rider_b=random_rider_score(None, HelmetColor.RED),
            rider_c=random_rider_score(None, HelmetColor.WHITE),
            rider_d=random_rider_score(None, HelmetColor.YELLOW, exclusion=True),
        )
    )
