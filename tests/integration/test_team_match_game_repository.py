import pytest

from storing.adapters.repositories import team_match_game_repository as repository
from storing.domain.models import team_match_game as model
from tests.random_data import random_rider_score

pytestmark = pytest.mark.usefixtures("mappers")

def test_add_team_match_game(sqlite_session_factory):
    # given
    session = sqlite_session_factory()
    repo = repository.SqlAlchemyTeamMatchGameRepository(session)
    game = model.TeamMatchGame(1, 1, 2)

    # when
    repo.add(game)

    # then
    ret_game = repo.get(1)
    assert ret_game == game

def test_add_team_compositions(sqlite_session_factory):
    # given
    session = sqlite_session_factory()
    repo = repository.SqlAlchemyTeamMatchGameRepository(session)
    game = model.TeamMatchGame(1, 1, 2)
    repo.add(game)
    rider_home = model.TeamCompositionRider(1, 10)
    rider_guest = model.TeamCompositionRider(2, 1)

    # when
    game.add_teams_compositions([rider_home], [rider_guest])

    # then
    ret_game = repo.get(1)
    assert ret_game == game
    assert len(ret_game.home_team_composition) == 1
    assert len(ret_game.guest_team_composition) == 1
    assert list(ret_game.home_team_composition)[0] == rider_home
    assert list(ret_game.guest_team_composition)[0] == rider_guest

def test_add_heat(sqlite_session_factory):
    # given
    session = sqlite_session_factory()
    repo = repository.SqlAlchemyTeamMatchGameRepository(session)
    game = model.TeamMatchGame(1, 1, 2)
    repo.add(game)
    rider_a = model.TeamCompositionRider(1, 10)
    rider_b = model.TeamCompositionRider(2, 1)
    rider_c = model.TeamCompositionRider(1, 11)
    rider_d = model.TeamCompositionRider(2, 2)
    game.add_teams_compositions([rider_a, rider_c], [rider_b, rider_d])
    heat = model.Heat(1, 1, True)
    rider_scores = model.RiderScores(
        rider_a=random_rider_score(
            model.Score(3), rider_number=10, helmet_color=model.HelmetColor.RED
        ),
        rider_b=random_rider_score(
            model.Score(2), rider_number=1, helmet_color=model.HelmetColor.WHITE
        ),
        rider_c=random_rider_score(
            model.Score(1), rider_number=11, helmet_color=model.HelmetColor.BLUE
        ),
        rider_d=random_rider_score(
            model.Score(0), rider_number=2, helmet_color=model.HelmetColor.YELLOW
        ),
    )

    # when
    game.finish_heat_attempt(heat, rider_scores)

    # then
    ret_game = repo.get(1)
    assert ret_game == game
    assert len(ret_game.heats) == 1
    assert list(ret_game.heats)[0] == heat
    ret_heat = list(ret_game.heats)[0]
    assert ret_heat.rider_scores['a'] == rider_scores.rider_a
    assert ret_heat.rider_scores['b'] == rider_scores.rider_b
    assert ret_heat.rider_scores['c'] == rider_scores.rider_c
    assert ret_heat.rider_scores['d'] == rider_scores.rider_d
