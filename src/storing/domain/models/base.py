from dataclasses import dataclass
from datetime import date

from storing.domain.models.aggregate import AggregateRoot


@dataclass
class League:
    name: str


@dataclass
class Season:
    year: int


@dataclass(unsafe_hash=True)
class Team:
    name: str


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
            raise Exception('Not found')
        if len(ret) > 1:
            raise Exception('Found more than one team')
        return ret[0]


@dataclass
class Stadium:
    name: str


@dataclass(unsafe_hash=True)
class Rider:
    name: str
    birthday: date


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
            raise Exception('Not found')
        if len(ret) > 1:
            raise Exception('Found more than one rider')
        return ret[0]


@dataclass
class Referee:
    name: str


@dataclass
class TrackCommisioner:
    name: str
