from dataclasses import dataclass
from typing import NewType, Optional

from storing.domain.models.aggregate import AggregateRoot


Year = NewType('Year', int)


@dataclass
class TeamSponsor:
    full_name: str
    titular: bool = True


@dataclass(unsafe_hash=True)
class LeagueTeamRider:
    id_rider: int


class LeagueTeam:
    def __init__(self, id_team: int, sponsor: TeamSponsor):
        self.id_team: int  = id_team
        self.sponsor: TeamSponsor = sponsor
        self.riders: set[LeagueTeamRider] = set()

    def add_rider(self, id_rider: int):
        self.riders.add(LeagueTeamRider(id_rider))


@dataclass
class TeamMatch:
    id_home_team: int
    id_guest_team: int
    match_round: int
    match_round_description: Optional[str] = None

    def __hash__(self):
        return hash((self.match_round, self.id_home_team, self.id_guest_team))


@dataclass
class LeagueSponsor:
    full_name: str
    titular: bool = True


class LeagueSeason(AggregateRoot):
    def __init__(self, year: int, id_league: int, sponsor: LeagueSponsor):
        super().__init__()
        self.year: int = year
        self.id_league: int = id_league
        self.sponsor: LeagueSponsor = sponsor
        self.teams: set[LeagueTeam] = set()
        self.matches: set[TeamMatch] = set()

    def add_team(self, team: LeagueTeam):
        if len(self.teams) == 8:
            raise Exception('Can not add more teams')
        self.teams.add(team)

    def add_match(self, match: TeamMatch):
        if self.can_add_match(match):
            self.matches.add(match)
        else:
            raise Exception('Invalid match')

    def can_add_match(self, match: TeamMatch):
        teams = [team.id_team for team in self.teams]
        if match.id_home_team not in teams:
            return False
        if match.id_guest_team not in teams:
            return False
        return True

    def add_rider_to_team(self, id_rider: int, id_team: int):
        team = next(t for t in self.teams if t.id_team == id_team)
        if not team:
            raise Exception('Invalid id_team')
        if self.can_add_rider_to_team(id_rider, id_team):
            team.add_rider(id_rider)
        else:
            raise Exception('Rider exists in other team')

    def can_add_rider_to_team(self, id_rider: int, id_team: int):
        for team in self.teams:
            if team.id_team != id_team and len(
                [id_rider for r in team.riders if r.id_rider == id_rider]
            ) > 0:
                return False
        return True
