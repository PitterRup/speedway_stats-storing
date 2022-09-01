import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from storing.adapters.orm import base_orm, league_season_orm, team_match_game_orm

@pytest.fixture
def in_memory_sqlite_db():
    engine = create_engine("sqlite:///:memory:")
    base_orm.metadata.create_all(engine)
    league_season_orm.metadata.create_all(engine)
    team_match_game_orm.metadata.create_all(engine)
    return engine


@pytest.fixture
def sqlite_session_factory(in_memory_sqlite_db):  # pylint: disable=redefined-outer-name
    yield sessionmaker(bind=in_memory_sqlite_db)


@pytest.fixture
def mappers():
    base_orm.start_mappers()
    league_season_orm.start_mappers()
    team_match_game_orm.start_mappers()
    yield
    clear_mappers()
