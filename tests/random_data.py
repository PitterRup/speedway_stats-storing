from random import choice
from typing import Optional

from storing.domain.model import (
    TeamCompositionRider, TeamMatchGame, RiderScores,
    RiderScore, HelmetColor, Score, HOME_TEAM_HELMETS
)

def random_team_match_game() -> TeamMatchGame:
    match = TeamMatchGame(1)
    home_team = [
        TeamCompositionRider(id_league_team_rider=i + 100, rider_number=i)
        for i in range(9, 17)
    ]
    guest_team = [
        TeamCompositionRider(id_league_team_rider=i + 100, rider_number=i)
        for i in range(1, 9)
    ]
    match.add_teams_compositions(home_team, guest_team)
    return match

def random_rider_scores(rider_numbers: int = 4) -> RiderScores:
    rider_types = ['rider_a', 'rider_b', 'rider_c', 'rider_d']
    scores = sorted(list(Score), key=lambda s: s.value, reverse=True)
    helmets = list(HelmetColor)
    riders = {
        rider_types[i]: random_rider_score(
            scores[i],
            helmets[i],
            i + 1 + (8 if helmets[i] in HOME_TEAM_HELMETS else 0)
        )
        for i in range(rider_numbers)
    }
    return RiderScores(**riders)

def random_rider_score(
    score: Optional[Score] = None,
    helmet_color: Optional[HelmetColor] = None,
    rider_number: Optional[int] = None,
) -> RiderScore:
    return RiderScore(
        score=choice(list(Score)) if score is None else score,
        helmet_color=choice(list(HelmetColor)) if helmet_color is None else helmet_color,
        waring=False,
        defect=False,
        fall=False,
        exclusion=False,
        rider_number=1 if rider_number is None else rider_number,
    )
