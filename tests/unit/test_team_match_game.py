import pytest

from tests.random_data import random_rider_scores, random_team_match_game
from storing.domain.model import Heat, TeamCompositionRider


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

    # when
    home_team.append(TeamCompositionRider(id_league_team_rider=1000, rider_number=17))
    match.add_teams_compositions(home_team, guest_team)

    # then
    assert len(match.home_team_composition) == 8
    assert len(match.guest_team_composition) == 8


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
    match.add_teams_compositions(home_team, guest_team)

    # then
    assert len(match.home_team_composition) == 0
    assert len(match.guest_team_composition) == 8


def test_guest_composition_rider_number_are_from_1_to_8():
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
    match.add_teams_compositions(home_team, guest_team)

    # then
    assert len(match.home_team_composition) == 8
    assert len(match.guest_team_composition) == 0

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
    match.add_teams_compositions(home_team, guest_team)

    # then
    assert len(match.home_team_composition) == 0
    assert len(match.guest_team_composition) == 0
