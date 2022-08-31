import logging

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Numeric,
    Table,
    MetaData,
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import mapper, relationship

from storing.domain.models import base

log = logging.getLogger(__name__)

metadata = MetaData()

leagues = Table(
    "leagues",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255)),
)

seasons = Table(
    "seasons",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("year", Numeric(4, 0)),
)

teams_groups = Table(
    "teams_groups",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255)),
)

teams = Table(
    "teams",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("id_team_group", ForeignKey('teams_groups.id'), nullable=False),
    Column("name", String(255)),
)

stadiums = Table(
    "stadiums",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255)),
)


riders_groups = Table(
    "riders_groups",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255)),
)


riders = Table(
    "riders",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("id_rider_group", ForeignKey('riders_groups.id'), nullable=False),
    Column("name", String(255)),
    Column("birthday", DateTime),
)

referees = Table(
    "referees",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255)),
)

track_commisioners = Table(
    "track_commisioners",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255)),
)

def start_mappers():
    log.info("Starting mappers")
    mapper(
        base.League,
        leagues
    )
    mapper(
        base.Season,
        seasons
    )
    teams_mapper = mapper(
        base.Team,
        teams
    )
    mapper(
        base.TeamsGroup,
        teams_groups,
        properties={'teams': relationship(teams_mapper, collection_class=set)}
    )
    mapper(
        base.Stadium,
        stadiums
    )
    riders_mapper = mapper(
        base.Rider,
        riders
    )
    mapper(
        base.RidersGroup,
        riders_groups,
        properties={'riders': relationship(riders_mapper, collection_class=set)}
    )
    mapper(
        base.Referee,
        referees
    )
    mapper(
        base.TrackCommisioner,
        track_commisioners
    )
