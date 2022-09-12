from dataclasses import dataclass
from datetime import date

from storing.domain.models.aggregate import AggregateRoot
from storing.domain import events


@dataclass
class League:
    name: str


@dataclass
class Season:
    year: int


@dataclass(unsafe_hash=True)
class Team:
    name: str
    id_team: int = None


class TeamsGroup(AggregateRoot):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.teams: set[Team] = set()

    def add(self, team: Team):
        self.teams.add(team)
        self.version_number += 1

    def recognize(self, name: str):
        ret = []
        for team in self.teams:
            if team.name in name:
                ret.append(team)
        if len(ret) == 0:
            self.events.append(
                events.NotRecognizedTeam(recognizing_team_name=name)
            )
        elif len(ret) > 1:
            self.events.append(
                events.RecognizedMultipleTeams(recognizing_team_name=name)
            )
        else:
            self.events.append(
                events.RecognizedTeam(
                    recognizing_team_name=name,
                    id_team=ret[0].id_team,
                )
            )
            return ret[0]


@dataclass
class Stadium:
    name: str


@dataclass(unsafe_hash=True)
class Rider:
    name: str
    birthday: date
    id_rider: int = None


class RidersGroup(AggregateRoot):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.riders: set[Rider] = set()

    def add(self, rider: Rider):
        self.riders.add(rider)
        self.version_number += 1

    def recognize(self, name):
        ret = []
        for rider in self.riders:
            if rider.name == name:
                ret.append(rider)
        if len(ret) == 0:
            self.events.append(
                events.NotRecognizedRider(recognizing_rider_name=name)
            )
        elif len(ret) > 1:
            self.events.append(
                events.RecognizedMultipleRiders(recognizing_rider_name=name)
            )
        else:
            self.events.append(
                events.RecognizedRider(
                    recognizing_rider_name=name,
                    id_rider=ret[0].id_rider,
                )
            )
            return ret[0]


@dataclass
class Referee:
    name: str


@dataclass
class TrackCommisioner:
    name: str
