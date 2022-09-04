import threading
import time
from datetime import date

import pytest

from storing.domain.models import base as model
from storing.service_layer import unit_of_work

pytestmark = pytest.mark.usefixtures("mappers")

def retrieve_teams_group_and_save_team(
    uow: unit_of_work.SqlAlchemyTeamsGroupUnitOfWork,
    team_group: str = 'Speedway',
    team_name: str = 'Lublin'
):
    teams_group = uow.teams_groups.get(team_group)
    team = model.Team(team_name)
    teams_group.add(team)


def retrieve_riders_group_and_save_team(
    uow: unit_of_work.SqlAlchemyRidersGroupUnitOfWork,
    rider_group: str = 'Speedway',
    rider_name: str = 'Zmarzlik'
):
    riders_group = uow.riders_groups.get(rider_group)
    rider = model.Rider(rider_name, date(1993, 1, 1))
    riders_group.add(rider)


@pytest.mark.parametrize('uow_factory, init_sql, check_sql, exp_name, operation', [
    (
        unit_of_work.SqlAlchemyTeamsGroupUnitOfWork,
        "insert into teams_groups values (1, 'Speedway', 0)",
        "select name from teams where name = 'Lublin'",
        'Lublin',
        retrieve_teams_group_and_save_team,
    ),
    (
        unit_of_work.SqlAlchemyRidersGroupUnitOfWork,
        "insert into riders_groups values (1, 'Speedway', 0)",
        "select name from riders where name = 'Zmarzlik'",
        'Zmarzlik',
        retrieve_riders_group_and_save_team,
    ),
])
def test_uow_can_retrieve_a_team_group_and_save_team(
    sqlite_session_factory, uow_factory, init_sql, check_sql, exp_name, operation
):
    # given
    session = sqlite_session_factory()
    session.execute(init_sql)
    session.commit()
    uow = uow_factory(sqlite_session_factory)

    # when
    with uow:
        operation(uow)
        uow.commit()

    # then
    [[added_name]] = session.execute(check_sql)
    assert added_name == exp_name


def add_teams_group(uow: unit_of_work.SqlAlchemyTeamsGroupUnitOfWork):
    teams_group = model.TeamsGroup('Speedway')
    uow.teams_groups.add(teams_group)


def add_riders_group(uow: unit_of_work.SqlAlchemyRidersGroupUnitOfWork):
    riders_group = model.RidersGroup('Speedway')
    uow.riders_groups.add(riders_group)


@pytest.mark.parametrize('uow_factory, check_sql, operation', [
    (
        unit_of_work.SqlAlchemyTeamsGroupUnitOfWork,
        'select * from teams_groups',
        add_teams_group,
    ),
    (
        unit_of_work.SqlAlchemyRidersGroupUnitOfWork,
        'select * from riders_groups',
        add_riders_group,
    ),
])
def test_rolls_back_uncommited_work_by_default(
    sqlite_session_factory, uow_factory, check_sql, operation
):
    # given
    uow = uow_factory(sqlite_session_factory)

    # when
    with uow:
        operation(uow)

    # then
    new_session = sqlite_session_factory()
    assert len(list(new_session.execute(check_sql))) == 0


@pytest.mark.parametrize('uow_factory, check_sql, operation', [
    (
        unit_of_work.SqlAlchemyTeamsGroupUnitOfWork,
        'select * from teams_groups',
        add_teams_group,
    ),
    (
        unit_of_work.SqlAlchemyRidersGroupUnitOfWork,
        'select * from riders_groups',
        add_riders_group,
    ),
])
def test_rolls_back_on_error(sqlite_session_factory, uow_factory, check_sql, operation):
    # given
    uow = uow_factory(sqlite_session_factory)

    class MyException(Exception):
        pass

    # when
    with pytest.raises(MyException):
        with uow:
            operation(uow)
            raise MyException()

    # then
    new_session = sqlite_session_factory()
    assert len(list(new_session.execute(check_sql))) == 0


def try_to_add_team(name, group_name, exceptions, session_factory):
    try:
        with unit_of_work.SqlAlchemyTeamsGroupUnitOfWork(session_factory) as uow:
            retrieve_teams_group_and_save_team(uow, group_name, name)
            time.sleep(0.2)
            uow.commit()
    except Exception as err:  # pylint: disable=broad-except
        exceptions.append(err)


def try_to_add_rider(name, group_name, exceptions, session_factory):
    try:
        with unit_of_work.SqlAlchemyRidersGroupUnitOfWork(session_factory) as uow:
            retrieve_riders_group_and_save_team(uow, group_name, name)
            time.sleep(0.2)
            uow.commit()
    except Exception as err:  # pylint: disable=broad-except
        exceptions.append(err)


@pytest.mark.parametrize('init_sql, check_sql, try_to_do_1, args_1, try_to_do_2, args_2', [
    (
        "insert into teams_groups values (1, 'Speedway', 0)",
        "SELECT version_number FROM teams_groups WHERE name='Speedway'",
        try_to_add_team, ('Lublin', 'Speedway'),
        try_to_add_team, ('Wrocław', 'Speedway'),
    ),
    (
        "insert into riders_groups values (1, 'Speedway', 0)",
        "SELECT version_number FROM riders_groups WHERE name='Speedway'",
        try_to_add_rider, ('Zmarzlik', 'Speedway'),
        try_to_add_rider, ('Janowski', 'Speedway'),
    ),
])
def test_concurrent_updates_to_version_are_not_allowed(
    postgres_session_factory, init_sql, check_sql,
    try_to_do_1, args_1,
    try_to_do_2, args_2,
):
    # given
    session = postgres_session_factory()
    session.execute(init_sql)
    session.commit()

    exceptions: list[Exception] = []

    # when
    _try_to_do_1 = lambda: try_to_do_1(  # pylint: disable=unnecessary-lambda-assignment
        *args_1, exceptions, postgres_session_factory
    )
    _try_to_do_2 = lambda: try_to_do_2(  # pylint: disable=unnecessary-lambda-assignment
        *args_2, exceptions, postgres_session_factory
    )
    thread1 = threading.Thread(target=_try_to_do_1)
    thread2 = threading.Thread(target=_try_to_do_2)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    # then
    [[version]] = session.execute(check_sql)
    assert version == 1
    assert len(exceptions) == 1
    exception = exceptions[0]
    assert "could not serialize access due to concurrent update" in str(exception)
