from datetime import date
import pytest

from storing.adapters.repositories import base_repository
from storing.domain.models import base as model

pytestmark = pytest.mark.usefixtures("mappers")


def test_add_teams_group(sqlite_session_factory):
    # given
    session = sqlite_session_factory()
    repo = base_repository.SqlAlchemyTeamsGroupRepository(session)
    grp = model.TeamsGroup('Speedway')
    grp.teams.add(model.Team('Lublin'))

    # when
    repo.add(grp)

    # then
    assert repo.get('Speedway') == grp


def test_add_riders_group(sqlite_session_factory):
    # given
    session = sqlite_session_factory()
    repo = base_repository.SqlAlchemyRidersGroupRepository(session)
    grp = model.RidersGroup('Speedway')
    grp.riders.add(model.Rider('Bartosz Zmarzlik', date(1993, 1, 1)))

    # when
    repo.add(grp)

    # then
    assert repo.get('Speedway') == grp
