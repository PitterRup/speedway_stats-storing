import pytest

from tests.random_data import random_rider_score, random_rider_scores, random_team_match_game
from storing.domain.models.team_match_game import (
    Heat, HelmetColor, RiderScores, Score, TeamCompositionRider
)


def test_match_cannot_contain_more_than_15_finished_heats():
    # given
    match = random_team_match_game()

    # when
    for i in range(1, 16):
        match.finish_heat_attempt(
            Heat(heat_number=i, attempt_number=1, finished=True),
            random_rider_scores(),
        )

    # then
    with pytest.raises(Exception):
        match.finish_heat_attempt(
            Heat(heat_number=16, attempt_number=1, finished=True),
            random_rider_scores(),
        )

    assert len(match.heats) == 15


def test_match_can_conatain_more_than_15_unfinished_heats():
    # given
    match = random_team_match_game()

    # when
    for i in range(1, 16):
        match.finish_heat_attempt(
            Heat(heat_number=i, attempt_number=1, finished=True),
            random_rider_scores(),
        )

    match.finish_heat_attempt(
        Heat(heat_number=16, attempt_number=1, finished=False),
        random_rider_scores(),
    )

    assert len(match.heats) == 16


def test_composition_can_contain_8_riders():
    # given
    match = random_team_match_game()
    home_team = [
        TeamCompositionRider(id_league_team_rider=i + 100, rider_number=i)
        for i in range(9, 17)
    ]
    guest_team = [
        TeamCompositionRider(id_league_team_rider=i + 100, rider_number=i)
        for i in range(1, 9)
    ]

    # when
    match.add_teams_compositions(home_team, guest_team)

    # then
    assert len(match.home_team_composition) == 8
    assert len(match.guest_team_composition) == 8

    # given
    home_team.append(TeamCompositionRider(id_league_team_rider=1000, rider_number=17))

    # when
    with pytest.raises(Exception):
        match.add_teams_compositions(home_team, guest_team)


def test_home_composition_rider_numbers_are_from_9_to_16():
    # given
    match = random_team_match_game()
    home_team = [
        TeamCompositionRider(id_league_team_rider=i + 100, rider_number=i)
        for i in range(1, 9)
    ]
    guest_team = [
        TeamCompositionRider(id_league_team_rider=i + 100, rider_number=i)
        for i in range(1, 9)
    ]

    # when
    with pytest.raises(Exception):
        match.add_teams_compositions(home_team, guest_team)


def test_guest_composition_rider_numbers_are_from_1_to_8():
    # given
    match = random_team_match_game()
    home_team = [
        TeamCompositionRider(id_league_team_rider=i + 100, rider_number=i)
        for i in range(9, 17)
    ]
    guest_team = [
        TeamCompositionRider(id_league_team_rider=i + 100, rider_number=i)
        for i in range(9, 17)
    ]

    # when
    with pytest.raises(Exception):
        match.add_teams_compositions(home_team, guest_team)


def test_composition_rider_numbers_must_be_unique():
    # given
    match = random_team_match_game()
    home_team = [
        TeamCompositionRider(id_league_team_rider=i + 100, rider_number=9)
        for i in range(9, 17)
    ]
    guest_team = [
        TeamCompositionRider(id_league_team_rider=i + 100, rider_number=1)
        for i in range(1, 9)
    ]

    # when
    with pytest.raises(Exception):
        match.add_teams_compositions(home_team, guest_team)


def test_heat_contain_only_composition_riders():
    # given
    match = random_team_match_game()

    # when
    match.finish_heat_attempt(
        Heat(1, 1, True),
        RiderScores(
            rider_a=random_rider_score(Score.THREE, HelmetColor.BLUE, 9),
            rider_b=random_rider_score(Score.TWO, HelmetColor.RED, 10),
            rider_c=random_rider_score(Score.ONE, HelmetColor.WHITE, 1),
            rider_d=random_rider_score(Score.ZERO, HelmetColor.YELLOW, 2),
        ),
    )

    # then
    assert len(match.heats) == 1

    # when
    with pytest.raises(Exception):
        match.finish_heat_attempt(
            Heat(2, 1, True),
            RiderScores(
                rider_a=random_rider_score(Score.THREE, HelmetColor.BLUE, 22),
                rider_b=random_rider_score(Score.TWO, HelmetColor.RED, 23),
                rider_c=random_rider_score(Score.ONE, HelmetColor.WHITE, 24),
                rider_d=random_rider_score(Score.ZERO, HelmetColor.YELLOW, 25),
            ),
        )

def test_helmet_color_red_and_blue_are_home_team_and_other_are_guest():
    # given
    match = random_team_match_game()

    # when
    with pytest.raises(Exception):
        match.finish_heat_attempt(
            Heat(1, 1, True),
            RiderScores(
                rider_a=random_rider_score(Score.THREE, HelmetColor.BLUE, 1),
                rider_b=random_rider_score(Score.TWO, HelmetColor.RED, 2),
                rider_c=random_rider_score(Score.ONE, HelmetColor.WHITE, 9),
                rider_d=random_rider_score(Score.ZERO, HelmetColor.YELLOW, 10),
            ),
        )

def test_teams_scores():
    # given
    match = random_team_match_game()

    # when
    match.finish_heat_attempt(
        Heat(1, 1, True),
        RiderScores(
            rider_a=random_rider_score(Score.THREE, HelmetColor.BLUE, 10),
            rider_b=random_rider_score(Score.TWO, HelmetColor.RED, 9),
            rider_c=random_rider_score(Score.ONE, HelmetColor.WHITE, 1),
            rider_d=random_rider_score(Score.ZERO, HelmetColor.YELLOW, 2),
        ),
    )

    # then
    assert match.home_team_scores == 5
    assert match.guest_team_scores == 1

    # when
    match.finish_heat_attempt(
        Heat(2, 1, True),
        RiderScores(
            rider_a=random_rider_score(Score.ZERO, HelmetColor.BLUE, 9),
            rider_b=random_rider_score(Score.TWO, HelmetColor.RED, 10),
            rider_c=random_rider_score(Score.ONE, HelmetColor.WHITE, 1),
            rider_d=random_rider_score(Score.THREE, HelmetColor.YELLOW, 2),
        ),
    )

    # then
    assert match.home_team_scores == 7
    assert match.guest_team_scores == 5

    # when
    match.finish_heat_attempt(
        Heat(3, 1, False),
        RiderScores(
            rider_a=random_rider_score(None, HelmetColor.BLUE, 9, exclusion=True),
            rider_b=random_rider_score(None, HelmetColor.RED, 10),
            rider_c=random_rider_score(None, HelmetColor.WHITE, 1),
            rider_d=random_rider_score(None, HelmetColor.YELLOW, 2),
        ),
    )

    # then
    assert match.home_team_scores == 7
    assert match.guest_team_scores == 5
