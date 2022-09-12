from dataclasses import dataclass
from datetime import date


class Command:
    pass


@dataclass
class AddTeam(Command):
    team_group_name: str
    team_name: str


@dataclass
class RecognizeTeam(Command):
    team_group_name: str
    team_name: str


@dataclass
class AddRider(Command):
    rider_group_name: str
    rider_name: str
    birthday: date
