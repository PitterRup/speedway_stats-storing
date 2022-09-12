from dataclasses import dataclass


class Event:
    pass


@dataclass
class RecognizedMultipleTeams(Event):
    recognizing_team_name: str


@dataclass
class NotRecognizedTeam(Event):
    recognizing_team_name: str


@dataclass
class RecognizedTeam(Event):
    recognizing_team_name: str
    id_team: int


@dataclass
class RecognizedMultipleRiders(Event):
    recognizing_rider_name: str


@dataclass
class NotRecognizedRider(Event):
    recognizing_rider_name: str


@dataclass
class RecognizedRider(Event):
    recognizing_rider_name: str
    id_rider: int
