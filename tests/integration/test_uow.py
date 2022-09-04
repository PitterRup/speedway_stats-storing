import threading
import time
import pytest

from storing.domain.models import base as model
from storing.service_layer import unit_of_work

pytestmark = pytest.mark.usefixtures("mappers")


def test_uow_can_retrieve_a_team_group_and_save_team(sqlite_session_factory):
    # given
    session = sqlite_session_factory()
    session.execute("insert into teams_groups values (1, 'Speedway', 0)")
    session.commit()
    uow = unit_of_work.SqlAlchemyTeamsGroupUnitOfWork(sqlite_session_factory)

    # when
    with uow:
        teams_group = uow.teams_groups.get('Speedway')
        team = model.Team('Lublin')
        teams_group.teams.add(team)
        uow.commit()

    # then
    [[added_name]] = session.execute("select name from teams where name = 'Lublin'")
    assert added_name == 'Lublin'


def test_rolls_back_uncommited_work_by_default(sqlite_session_factory):
    # given
    uow = unit_of_work.SqlAlchemyTeamsGroupUnitOfWork(sqlite_session_factory)

    # when
    with uow:
        teams_group = model.TeamsGroup('Speedway')
        uow.teams_groups.add(teams_group)

    # then
    new_session = sqlite_session_factory()
    assert len(list(new_session.execute('select * from teams_groups'))) == 0


def test_rolls_back_on_error(sqlite_session_factory):
    # given
    uow = unit_of_work.SqlAlchemyTeamsGroupUnitOfWork(sqlite_session_factory)

    class MyException(Exception):
        pass

    # when
    with pytest.raises(MyException):
        with uow:
            teams_group = model.TeamsGroup('Speedway')
            uow.teams_groups.add(teams_group)
            raise MyException()

    # then
    new_session = sqlite_session_factory()
    assert len(list(new_session.execute('select * from teams_groups'))) == 0


def try_to_add_team(name, group_name, exceptions, session_factory):
    team = model.Team(name)
    try:
        with unit_of_work.SqlAlchemyTeamsGroupUnitOfWork(session_factory) as uow:
            teams = uow.teams_groups.get(group_name)
            teams.add(team)
            time.sleep(0.2)
            uow.commit()
    except Exception as err:  # pylint: disable=broad-except
        exceptions.append(err)


def test_concurrent_updates_to_version_are_not_allowed(postgres_session_factory):
    # given
    session = postgres_session_factory()
    session.execute("insert into teams_groups values (1, 'Speedway')")
    session.commit()

    exceptions: list[Exception] = []

    # when
    try_to_add_team1 = lambda: try_to_add_team(  # pylint: disable=unnecessary-lambda-assignment
        'Lublin', 'Speedway', exceptions, postgres_session_factory
    )
    try_to_add_team2 = lambda: try_to_add_team(  # pylint: disable=unnecessary-lambda-assignment
        'Wrocław', 'Speedway', exceptions, postgres_session_factory
    )
    thread1 = threading.Thread(target=try_to_add_team1)
    thread2 = threading.Thread(target=try_to_add_team2)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    # then
    [[version]] = session.execute(
        "SELECT version_number FROM teams_groups WHERE name=:name",
        dict(name='Speedway'),
    )
    assert version == 1
    assert len(exceptions) == 1
    exception = exceptions[0]
    assert "could not serialize access due to concurrent update" in str(exception)
