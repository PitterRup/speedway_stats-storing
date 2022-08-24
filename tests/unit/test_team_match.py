import pytest

from tests.random_data import random_rider_scores
from storing.domain.model import TeamMatchGame, Heat


def test_match_cannot_contain_more_than_15_finished_heats():
    # given
    match = TeamMatchGame()

    # when
    for i in range(1, 16):
        match.finish_heat(
            Heat(heat_number=i, attempt_number=1, finished=True),
            random_rider_scores(),
        )

    # then
    with pytest.raises(Exception):
        match.finish_heat(
            Heat(heat_number=16, attempt_number=1, finished=True),
            random_rider_scores(),
        )

    assert len(match.heats) == 15


def test_match_can_conatain_more_than_15_unfinished_heats():
    # given
    match = TeamMatchGame()

    # when
    for i in range(1, 16):
        match.finish_heat(
            Heat(heat_number=i, attempt_number=1, finished=True),
            random_rider_scores(),
        )

    match.finish_heat(
        Heat(heat_number=16, attempt_number=1, finished=False),
        random_rider_scores(),
    )

    assert len(match.heats) == 16