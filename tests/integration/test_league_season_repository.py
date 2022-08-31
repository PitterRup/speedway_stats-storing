import pytest

from storing.adapters.repositories import league_season_repository as repository
from storing.domain.models import league_season as model

pytestmark = pytest.mark.usefixtures("mappers")

def test_add_season(sqlite_session_factory):
    # given
    session = sqlite_session_factory()
    repo = repository.SqlAlchemyLeagueSeasonRepository(session)
    sponsor = model.LeagueSponsor('PGE Ekstraliga')
    season = model.LeagueSeason(2008, 1, sponsor)

    # when
    repo.add(season)

    # then
    ret_season = repo.get(2008)
    assert ret_season == season
    assert ret_season.sponsor == sponsor

def test_add_team_to_league_season(sqlite_session_factory):
    # given
    session = sqlite_session_factory()
    repo = repository.SqlAlchemyLeagueSeasonRepository(session)
    season = model.LeagueSeason(2008, 1, model.LeagueSponsor('PGE Ekstraliga'))
    team_sponsor = model.TeamSponsor('EWinner Apator Toruń')
    team = model.LeagueTeam(1, team_sponsor)

    # when
    season.add_team(team)
    season.add_rider_to_team(1, 1)
    repo.add(season)

    # then
    ret_season = repo.get(2008)
    assert ret_season == season
    assert list(ret_season.teams)[0] == team
    assert list(ret_season.teams)[0].sponsor == team_sponsor

def test_add_match_to_league_season(sqlite_session_factory):
    # given
    session = sqlite_session_factory()
    repo = repository.SqlAlchemyLeagueSeasonRepository(session)
    season = model.LeagueSeason(2008, 1, model.LeagueSponsor('PGE Ekstraliga'))
    home_team = model.LeagueTeam(1, model.TeamSponsor('EWinner Apator Toruń'))
    guest_team = model.LeagueTeam(2, model.TeamSponsor('EWinner Apator Toruń'))
    season.add_team(home_team)
    season.add_team(guest_team)
    repo.add(season)
    match = model.TeamMatch(1, 2, 1)

    # when
    season.add_match(match)

    # then
    ret_season = repo.get(2008)
    assert list(ret_season.matches)[0] == match
