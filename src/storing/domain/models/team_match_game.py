from dataclasses import dataclass
from enum import Enum
from typing import Optional

class HelmetColor(Enum):
    RED = 'red'
    BLUE = 'blue'
    WHITE = 'white'
    YELLOW = 'yellow'

HOME_TEAM_HELMETS = [HelmetColor.RED, HelmetColor.BLUE]
GUEST_TEAM_HELMETS = [HelmetColor.WHITE, HelmetColor.YELLOW]

class Score(Enum):
    THREE = 3
    TWO = 2
    ONE = 1
    ZERO = 0

@dataclass(unsafe_hash=True)
class RiderScore:
    score: Optional[Score]
    helmet_color: HelmetColor
    warning: bool
    defect: bool
    fall: bool
    exclusion: bool
    rider_number: int


@dataclass
class RiderScores:
    rider_a: Optional[RiderScore] = None
    rider_b: Optional[RiderScore] = None
    rider_c: Optional[RiderScore] = None
    rider_d: Optional[RiderScore] = None


class Heat:
    possible_scores = sorted([s.value for s in list(Score)], reverse=True)

    def __init__(
        self, heat_number: int,
        attempt_number: int,
        finished: bool = False,
        winner_time: float = None,
    ):
        self.heat_number = heat_number
        self.attempt_number = attempt_number
        self.finished = finished
        self.winner_time = winner_time
        self.rider_scores: dict[str, Optional[RiderScore]] = dict()

    def __eq__(self, other):
        if not isinstance(other, Heat):
            return False
        return (
            self.heat_number == other.heat_number
            and self.attempt_number == other.attempt_number
        )

    def __gt__(self, other):
        return self.heat_number > other.heat_number or (
            self.heat_number == other.heat_number
            and self.attempt_number > other.attempt_number
        )

    def __hash__(self):
        return hash((self.heat_number, self.attempt_number))

    def save_result(self, rider_scores: RiderScores):
        if not self.is_correct_scores(rider_scores):
            raise Exception('Incorrect scores')
        if not self.rider_scores:
            self.rider_scores['a'] = rider_scores.rider_a
            self.rider_scores['b'] = rider_scores.rider_b
            self.rider_scores['c'] = rider_scores.rider_c
            self.rider_scores['d'] = rider_scores.rider_d
        else:
            if self.rider_scores['a'] != rider_scores.rider_a:
                self.rider_scores['a'] = rider_scores.rider_a
            if self.rider_scores['b'] != rider_scores.rider_b:
                self.rider_scores['b'] = rider_scores.rider_b
            if self.rider_scores['c'] != rider_scores.rider_c:
                self.rider_scores['c'] = rider_scores.rider_c
            if self.rider_scores['d'] != rider_scores.rider_d:
                self.rider_scores['d'] = rider_scores.rider_d

    def is_correct_scores(self, rider_scores: RiderScores):
        scores = [
            s.score.value
            for s in rider_scores.__dict__.values()
            if s is not None and s.score is not None
        ]
        helmets = [
            s.helmet_color.value
            for s in rider_scores.__dict__.values()
            if s is not None and s.score is not None
        ]
        return len(scores) == len(set(scores)) \
            and set(scores) == set(self.possible_scores[:len(scores)]) \
            and len(scores) == len(set(helmets))


@dataclass(unsafe_hash=True)
class TeamCompositionRider:
    id_league_team_rider: int
    rider_number: int


class TeamMatchGame:
    def __init__(self, id_team_match: int):
        self.id_team_match = id_team_match
        self.home_team_composition: set[TeamCompositionRider] = set()
        self.guest_team_composition: set[TeamCompositionRider] = set()
        self.heats: set[Heat] = set()

    def add_teams_compositions(
        self,
        home_team_composition: list[TeamCompositionRider],
        guest_team_composition: list[TeamCompositionRider],
    ):
        if self.can_add_home_composition(home_team_composition):
            self.home_team_composition.update(home_team_composition)
        else:
            raise Exception('Invalid composition')
        if self.can_add_guest_composition(guest_team_composition):
            self.guest_team_composition.update(guest_team_composition)
        else:
            raise Exception('Invalid composition')

    def can_add_home_composition(self, composition: list[TeamCompositionRider]):
        return len(composition) <= 8 and len(
            [rider for rider in composition if not 9 <= rider.rider_number <= 16]
        ) == 0 and len(composition) == len(set([r.rider_number for r in composition]))

    def can_add_guest_composition(self, composition: list[TeamCompositionRider]):
        return len(composition) <= 8 and len(
            [rider for rider in composition if not 1 <= rider.rider_number <= 8]
        ) == 0 and len(composition) == len(set([r.rider_number for r in composition]))

    def finish_heat_attempt(self, heat: Heat, rider_scores: RiderScores):
        if not self.are_valid_riders(rider_scores):
            raise Exception('Invalid riders')
        if heat in self.heats:
            heat = next(h for h in self.heats if h == heat)
            heat.save_result(rider_scores)
        elif self.can_add_heat(heat):
            self.heats.add(heat)
            heat.save_result(rider_scores)
        else:
            raise Exception('More than 15 heats already')

    def are_valid_riders(self, riders: RiderScores):
        home_rider_numbers = [r.rider_number for r in self.home_team_composition]
        guest_rider_numbers = [r.rider_number for r in self.guest_team_composition]
        for rider in riders.__dict__.values():
            if rider.rider_number not in home_rider_numbers \
                and rider.rider_number not in guest_rider_numbers:
                return False
            if rider.rider_number in home_rider_numbers \
                and rider.helmet_color not in HOME_TEAM_HELMETS:
                return False
            elif rider.rider_number in guest_rider_numbers \
                and rider.helmet_color not in GUEST_TEAM_HELMETS:
                return False
        return True

    def can_add_heat(self, heat: Heat):
        if not heat.finished:
            return True
        return len([h for h in self.heats if h.finished]) < 15

    @property
    def home_team_scores(self):
        scores = 0
        for heat in self.heats:
            if heat.finished:
                for rider in heat.rider_scores.values():
                    if rider and rider.score and rider.helmet_color in HOME_TEAM_HELMETS:
                        scores += rider.score.value
        return scores

    @property
    def guest_team_scores(self):
        scores = 0
        for heat in self.heats:
            if heat.finished:
                for rider in heat.rider_scores.values():
                    if rider and rider.score and rider.helmet_color in GUEST_TEAM_HELMETS:
                        scores += rider.score.value
        return scores
