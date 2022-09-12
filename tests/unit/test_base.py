from datetime import date
import pytest

from storing.domain.models.base import Rider, RidersGroup, Team, TeamsGroup
from storing.domain import events


def test_add_team_increament_version_number():
    # given
    teams = TeamsGroup('speedway')
    team = Team('Lublin')

    # when
    assert teams.version_number == 0
    teams.add(team)

    # then
    assert teams.version_number == 1


@pytest.mark.parametrize('name, expected_team_name', [
    ('MOTOR Lublin', 'Lublin'),
])
def test_output_recognized_team(name, expected_team_name):
    # given
    teams = TeamsGroup('speedway')
    teams.add(Team('Lublin'))
    teams.add(Team('Wrocław'))

    # when
    team = teams.recognize(name)

    # then
    assert team is not None
    assert team.name == expected_team_name
    assert teams.events[-1] == events.RecognizedTeam(
        recognizing_team_name=name,
        id_team=team.id_team,
    )


def test_records_recognized_multiple_teams_event_when_recognize_team_find_more_than_one_team():
    # given
    teams = TeamsGroup('speedway')
    teams.add(Team('Lublin'))
    teams.add(Team('Wrocław'))

    # when
    team = teams.recognize('Lublin Wrocław')

    # then
    assert teams.events[-1] == events.RecognizedMultipleTeams(
        recognizing_team_name='Lublin Wrocław'
    )
    assert team is None


def test_records_not_recognized_team_event_when_recognize_team_not_find_team():
    # given
    teams = TeamsGroup('speedway')
    teams.add(Team('Lublin'))
    teams.add(Team('Wrocław'))

    # when
    team = teams.recognize('Częstochowa')

    # then
    assert teams.events[-1] == events.NotRecognizedTeam(
        recognizing_team_name='Częstochowa'
    )
    assert team is None


def test_add_rider_increament_version_number():
    # given
    riders = RidersGroup('speedway')
    rider = Rider('Lublin', date(1993, 1, 1))

    # when
    assert riders.version_number == 0
    riders.add(rider)

    # then
    assert riders.version_number == 1


@pytest.mark.parametrize('name, expected_rider_name', [
    ('Bartosz Zmarzlik', 'Bartosz Zmarzlik'),
])
def test_output_recognized_rider(name, expected_rider_name):
    # given
    riders = RidersGroup('speedway')
    riders.add(Rider('Bartosz Zmarzlik', date(1993, 1, 1)))
    riders.add(Rider('Paweł Zmarzlik', date(1993, 1, 1)))
    riders.add(Rider('Maciej Janowski', date(1993, 1, 1)))

    # when
    rider = riders.recognize(name)

    # then
    assert rider is not None
    assert rider.name == expected_rider_name
    assert riders.events[-1] == events.RecognizedRider(
        recognizing_rider_name=rider.name,
        id_rider=rider.id_rider,
    )


def test_records_not_recognized_rider_event_when_recognize_rider_not_find_team():
    # given
    riders = RidersGroup('speedway')
    riders.add(Rider('Bartosz Zmarzlik', date(1993, 1, 1)))

    # when
    rider = riders.recognize('Maciej Janowski')

    # then
    assert riders.events[-1] == events.NotRecognizedRider(
        recognizing_rider_name='Maciej Janowski'
    )
    assert rider is None
