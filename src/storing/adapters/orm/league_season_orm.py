import logging

from sqlalchemy import Column, ForeignKey, Integer, MetaData, Table, Unicode, Boolean
from sqlalchemy.orm import mapper, relationship

from storing.domain.models import league_season as model

log = logging.getLogger(__name__)

metadata = MetaData()

team_sponsors = Table(
    "team_sponsors",
    metadata,
    Column("id_team_sponsor", Integer, primary_key=True, autoincrement=True),
    Column("id_league_team", ForeignKey('league_teams.id_league_team'), nullable=False),
    Column("full_name", Unicode(255), nullable=False),
    Column("titular", Boolean, nullable=False),
)

league_team_riders = Table(
    "league_team_riders",
    metadata,
    Column("id_league_team_rider", Integer, primary_key=True, autoincrement=True),
    Column("id_league_team", ForeignKey('league_teams.id_league_team'), nullable=False),
    Column("id_rider", Integer, nullable=False),
)

league_teams = Table(
    "league_teams",
    metadata,
    Column("id_league_team", Integer, primary_key=True, autoincrement=True),
    Column("id_league_season", ForeignKey('league_seasons.id_league_season'), nullable=False),
    Column("id_team", Integer, nullable=False),
)

team_matches = Table(
    "team_matches",
    metadata,
    Column("id_team_match", Integer, primary_key=True, autoincrement=True),
    Column("id_league_season", ForeignKey('league_seasons.id_league_season'), nullable=False),
    Column("match_round", Integer, nullable=False),
    Column("match_round_description", Unicode(255)),
    Column("id_home_team", Integer, nullable=False),
    Column("id_guest_team", Integer, nullable=False),
)

league_sponsors = Table(
    "league_sponsors",
    metadata,
    Column("id_team_sponsor", Integer, primary_key=True, autoincrement=True),
    Column("id_league_season", ForeignKey('league_seasons.id_league_season'), nullable=False),
    Column("full_name", Unicode(255), nullable=False),
    Column("titular", Boolean, nullable=False),
)

league_seasons = Table(
    "league_seasons",
    metadata,
    Column("id_league_season", Integer, primary_key=True, autoincrement=True),
    Column("id_league", Integer, nullable=False),
    Column("year", Integer, nullable=False),
)

def start_mappers():
    log.info("Starting mappers")
    team_sponsors_mapper = mapper(
        model.TeamSponsor,
        team_sponsors,
    )
    league_team_riders_mapper = mapper(
        model.LeagueTeamRider,
        league_team_riders,
    )
    league_teams_mapper = mapper(
        model.LeagueTeam,
        league_teams,
        properties={
            'riders': relationship(league_team_riders_mapper, collection_class=set),
            'sponsor': relationship(team_sponsors_mapper, uselist=False),
        },
    )
    team_matches_mapper = mapper(
        model.TeamMatch,
        team_matches,
    )
    league_sponsors_mapper = mapper(
        model.LeagueSponsor,
        league_sponsors
    )
    mapper(
        model.LeagueSeason,
        league_seasons,
        properties={
            'sponsor': relationship(league_sponsors_mapper, uselist=False),
            'teams': relationship(league_teams_mapper, collection_class=set),
            'matches': relationship(team_matches_mapper, collection_class=set),
        }
    )
