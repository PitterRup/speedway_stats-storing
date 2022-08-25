from random import choice
from typing import Optional

from storing.domain.model import TeamMatchGame, RiderScores, RiderScore, HelmetColor, Score

def random_team_match_game() -> TeamMatchGame:
    return TeamMatchGame(1)

def random_rider_scores(rider_numbers: int = 4) -> RiderScores:
    rider_types = ['rider_a', 'rider_b', 'rider_c', 'rider_d']
    scores = sorted(list(Score), key=lambda s: s.value, reverse=True)
    riders = {
        rider_types[i]: random_rider_score(scores[i])
        for i in range(rider_numbers)
    }
    return RiderScores(**riders)

def random_rider_score(score: Optional[Score] = None) -> RiderScore:
    return RiderScore(
        score=choice(list(Score)) if score is None else score,
        helmet_color=choice(list(HelmetColor)),
        waring=False,
        defect=False,
        fall=False,
        exclusion=False,
        composition_rider_id=1,
    )
