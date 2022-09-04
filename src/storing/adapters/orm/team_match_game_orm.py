import logging

from sqlalchemy import (
    Boolean, Column, Enum, ForeignKey, Integer, MetaData, Numeric, Table, Unicode, and_, event
)
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.orm.collections import attribute_mapped_collection

from storing.domain.models import team_match_game as model


log = logging.getLogger(__name__)

metadata = MetaData()

team_match_game_heat_riders = Table(
    "team_match_game_heat_riders",
    metadata,
    Column("id_team_match_game_heat_rider", Integer, primary_key=True, autoincrement=True),
    Column("rider_number", Integer, nullable=False),
    Column("score", Integer, nullable=False),
    Column("helmet_color", Enum(model.HelmetColor), nullable=False),
    Column("warning", Boolean, nullable=False),
    Column("defect", Boolean, nullable=False),
    Column("fall", Boolean, nullable=False),
    Column("exclusion", Boolean, nullable=False),
)

team_match_game_heat_rider_int = Table(
    "team_match_game_heat_rider_int",
    metadata,
    Column("id_team_match_heat_rider_int", Integer, primary_key=True, autoincrement=True),
    Column(
        "id_team_match_game_heat",
        ForeignKey("team_match_game_heats.id_team_match_game_heat"),
        nullable=False,
    ),
    Column(
        "id_team_match_game_heat_rider",
        ForeignKey("team_match_game_heat_riders.id_team_match_game_heat_rider"),
        nullable=False,
    ),
    Column("rider_type", Unicode(1))
)

team_match_game_heats = Table(
    "team_match_game_heats",
    metadata,
    Column("id_team_match_game_heat", Integer, primary_key=True, autoincrement=True),
    Column("id_team_match_game", ForeignKey("team_match_games.id_team_match_game"), nullable=False),
    Column("heat_number", Integer, nullable=False),
    Column("attempt_number", Integer, nullable=False),
    Column("finished", Boolean, nullable=False),
    Column("winner_time", Numeric(3, 3)),
)

team_match_game_compositions = Table(
    "team_match_game_compositions",
    metadata,
    Column("id_team_match_game_composition", Integer, primary_key=True, autoincrement=True),
    Column("id_team_match_game", ForeignKey("team_match_games.id_team_match_game"), nullable=False),
    Column("id_league_team", Integer, nullable=False),
    Column("id_league_team_rider", Integer, nullable=False),
    Column("rider_number", Integer, nullable=False),
)

team_match_games = Table(
    "team_match_games",
    metadata,
    Column("id_team_match_game", Integer, primary_key=True, autoincrement=True),
    Column("id_team_match", Integer, nullable=False),
    Column("id_home_league_team", Integer, nullable=False),
    Column("id_guest_league_team", Integer, nullable=False),
)

def start_mappers():
    log.info("Starting mappers")
    team_match_game_heat_riders_mapper = mapper(
        model.RiderScore,
        team_match_game_heat_riders
    )
    team_match_game_heats_mapper = mapper(
        model.Heat,
        team_match_game_heats,
        properties={
            "rider_scores": relationship(
                team_match_game_heat_riders_mapper,
                collection_class=attribute_mapped_collection("rider_type"),
                secondary=team_match_game_heat_rider_int,
            ),
        },
    )
    team_match_game_compositions_mapper = mapper(
        model.TeamCompositionRider,
        team_match_game_compositions,
    )
    mapper(
        model.TeamMatchGame,
        team_match_games,
        properties={
            "home_team_composition": relationship(
                team_match_game_compositions_mapper,
                collection_class=set,
                primaryjoin=and_(
                    team_match_games.c.id_team_match_game == team_match_game_compositions.c.id_team_match_game,  # pylint: disable=line-too-long
                    team_match_games.c.id_home_league_team == team_match_game_compositions.c.id_league_team,  # pylint: disable=line-too-long
                ),
                foreign_keys=[
                    team_match_game_compositions.c.id_team_match_game,
                    team_match_game_compositions.c.id_league_team,
                ]
            ),
            "guest_team_composition": relationship(
                team_match_game_compositions_mapper,
                collection_class=set,
                primaryjoin=and_(
                    team_match_games.c.id_team_match_game == team_match_game_compositions.c.id_team_match_game,  # pylint: disable=line-too-long
                    team_match_games.c.id_guest_league_team == team_match_game_compositions.c.id_league_team,  # pylint: disable=line-too-long
                ),
                foreign_keys=[
                    team_match_game_compositions.c.id_team_match_game,
                    team_match_game_compositions.c.id_league_team,
                ]
            ),
            "heats": relationship(team_match_game_heats_mapper, collection_class=set),
        }
    )

@event.listens_for(model.TeamMatchGame, "load")
def receive_load(game, _):
    game.events = []
