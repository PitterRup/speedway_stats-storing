import pytest

from storing.domain.models.league_season import LeagueTeamRider, TeamMatch
from tests.random_data import random_league_season, random_league_team


def test_season_can_conatin_only_8_teams():
    # given
    season = random_league_season()

    # when
    for i in range(8):
        season.add_team(random_league_team(i))

    # then
    assert len(season.teams) == 8

    # when
    with pytest.raises(Exception):
        season.add_team(random_league_team(9))


def test_match_conatain_only_teams_from_league():
    # given
    season = random_league_season()
    season.add_team(random_league_team(1))
    season.add_team(random_league_team(2))

    # when
    season.add_match(TeamMatch(1, 2, 1))

    # then
    assert len(season.matches) == 1

    # when
    with pytest.raises(Exception):
        season.add_match(TeamMatch(3, 4, 1))

def test_rider_can_be_in_only_one_team():
    # given
    season = random_league_season()
    season.add_team(random_league_team(1))
    season.add_team(random_league_team(2))

    # when
    season.add_rider_to_team(id_rider=1, id_team=1)

    # then
    team = next(t for t in season.teams if t.id_team == 1)
    assert LeagueTeamRider(1) in team.riders

    # when
    with pytest.raises(Exception):
        season.add_rider_to_team(id_rider=1, id_team=2)
