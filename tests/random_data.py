from random import choice
from typing import Optional
from storing.domain.models.league_season import LeagueSeason, LeagueTeam, TeamSponsor, LeagueSponsor

from storing.domain.models.team_match_game import (
    TeamCompositionRider, TeamMatchGame, RiderScores,
    RiderScore, HelmetColor, Score, HOME_TEAM_HELMETS
)

def random_team_match_game() -> TeamMatchGame:
    match = TeamMatchGame(1, 1, 2)
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
    scores = [Score(3), Score(2), Score(1), Score(0)]
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
    warning: bool = False,
    defect: bool = False,
    fall: bool = False,
    exclusion: bool = False,
) -> RiderScore:
    return RiderScore(
        score=score,
        helmet_color=choice(list(HelmetColor)) if helmet_color is None else helmet_color,
        warning=warning,
        defect=defect,
        fall=fall,
        exclusion=exclusion,
        rider_number=1 if rider_number is None else rider_number,
    )

def random_league_team(id_team):
    return LeagueTeam(
        id_team=id_team,
        sponsor=TeamSponsor(full_name='team', titular=True),
    )

def random_league_season(year: int = None):
    return LeagueSeason(
        year=year or 2022,
        id_league=1,
        sponsor=LeagueSponsor(full_name='sponsor', titular=True)
    )
