from datetime import date
import pytest

from storing.domain.models.base import Rider, RidersGroup, Team, TeamsGroup


@pytest.mark.parametrize('name, expected_team_name', [
    ('MOTOR Lublin', 'Lublin'),
])
def test_recognizing_teams(name, expected_team_name):
    # given
    teams = TeamsGroup('speedway')
    teams.teams.add(Team('Lublin'))
    teams.teams.add(Team('Wrocław'))

    # when
    team = teams.recognize(name)

    # then
    assert team is not None
    assert team.name == expected_team_name


def test_recognize_team_can_not_find_more_than_one_team():
    # given
    teams = TeamsGroup('speedway')
    teams.teams.add(Team('Lublin'))
    teams.teams.add(Team('Wrocław'))

    # when
    with pytest.raises(Exception):
        teams.recognize('Lublin Wrocław')


@pytest.mark.parametrize('name, expected_rider_name', [
    ('Bartosz Zmarzlik', 'Bartosz Zmarzlik'),
])
def test_recognizing_riders(name, expected_rider_name):
    # given
    riders = RidersGroup('speedway')
    riders.riders.add(Rider('Bartosz Zmarzlik', date(1993, 1, 1)))
    riders.riders.add(Rider('Paweł Zmarzlik', date(1993, 1, 1)))
    riders.riders.add(Rider('Maciej Janowski', date(1993, 1, 1)))

    # when
    rider = riders.recognize(name)

    # then
    assert rider is not None
    assert rider.name == expected_rider_name


def test_recognize_rider_can_not_find_more_than_one_rider():
    # given
    riders = RidersGroup('speedway')
    riders.riders.add(Rider('Lublin', date(1993, 1, 1)))
    riders.riders.add(Rider('Wrocław', date(1993, 1, 1)))

    # when
    with pytest.raises(Exception):
        riders.recognize('Lublin Wrocław')
