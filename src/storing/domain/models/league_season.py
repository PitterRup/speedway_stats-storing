from dataclasses import dataclass


@dataclass
class TeamSponsor:
    titular: bool
    full_name: str


class LeagueTeam:
    def __init__(self, id_team: int, sponsor: TeamSponsor, id_stadium: int):
        self.id_team: int  = id_team
        self.sponsor: TeamSponsor = sponsor
        self.id_stadium: int = id_stadium
        self.riders: set[int] = set()

    def add_rider(self, id_rider: int):
        self.riders.add(id_rider)


@dataclass
class TeamMatch:
    match_round: int
    match_round_description: str
    home_team_id: int
    guest_team_id: int

    def __hash__(self):
        return hash((self.match_round, self.home_team_id, self.guest_team_id))


class LeagueSeason:
    def __init__(self, year: int, id_league: int):
        self.year: int = year
        self.id_league: int = id_league
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
        if match.home_team_id not in teams:
            return False
        if match.guest_team_id not in teams:
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
            if team.id_team != id_team and id_rider in team.riders:
                return False
        return True
