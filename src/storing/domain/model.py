from dataclasses import dataclass
from enum import Enum

class HelmetColor(Enum):
    RED = 'red'
    BLUE = 'blue'
    WHITE = 'white'
    YELLOW = 'yellow'


class Score(Enum):
    THREE = 3
    TWO = 2
    ONE = 1
    ZERO = 0

@dataclass
class RiderScore:
    score: Score
    helmet_color: HelmetColor
    waring: bool
    defect: bool
    fall: bool
    exclusion: bool


@dataclass
class RiderScores:
    rider_a: RiderScore
    rider_b: RiderScore
    rider_c: RiderScore
    rider_d: RiderScore


class Heat:
    def __init__(self, heat_number: int, attempt_number: int, finished: bool = False, winner_time: float = None):
        self.heat_number = heat_number
        self.attempt_number = attempt_number
        self.finished = finished
        self.winner_time = winner_time
        self.rider_scores = dict()  # dict[str, RiderScore]

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


class TeamMatchGame:
    def __init__(self):
        self.heats = set()  # Set[Heat]

    def finish_heat(self, heat: Heat, rider_scores: RiderScores):
        if heat in self.heats:
            heat = next(h for h in self.heats if h == heat)
            heat.save_result(rider_scores)
        elif not heat.finished or self.can_add_heat(heat):
            self.heats.add(heat)
        else:
            raise Exception('More than 15 heats already')
        heat.save_result(rider_scores)                    

    def can_add_heat(self, heat: Heat):        
        return len([h for h in self.heats if h.finished]) < 15
            