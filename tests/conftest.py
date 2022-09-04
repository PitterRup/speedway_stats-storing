import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers, close_all_sessions
from tenacity import retry, stop_after_delay

from storing import config
from storing.adapters.orm import base_orm, league_season_orm, team_match_game_orm

@pytest.fixture
def in_memory_sqlite_db():
    engine = create_engine("sqlite:///:memory:")
    base_orm.metadata.create_all(engine)
    league_season_orm.metadata.create_all(engine)
    team_match_game_orm.metadata.create_all(engine)
    yield engine
    base_orm.metadata.drop_all(engine)
    league_season_orm.metadata.drop_all(engine)
    team_match_game_orm.metadata.drop_all(engine)


@pytest.fixture
def sqlite_session_factory(in_memory_sqlite_db):  # pylint: disable=redefined-outer-name
    yield sessionmaker(bind=in_memory_sqlite_db)


@retry(stop=stop_after_delay(10))
def wait_for_postgres_to_come_up(engine):
    return engine.connect()


@pytest.fixture(scope="session")
def postgres_db():
    engine = create_engine(config.get_postgres_uri(), isolation_level="SERIALIZABLE")
    wait_for_postgres_to_come_up(engine)
    base_orm.metadata.create_all(engine)
    league_season_orm.metadata.create_all(engine)
    team_match_game_orm.metadata.create_all(engine)
    yield engine
    close_all_sessions()
    base_orm.metadata.drop_all(engine)
    league_season_orm.metadata.drop_all(engine)
    team_match_game_orm.metadata.drop_all(engine)


@pytest.fixture
def postgres_session_factory(postgres_db):  # pylint: disable=redefined-outer-name
    yield sessionmaker(bind=postgres_db)    


@pytest.fixture
def postgres_session(postgres_session_factory):  # pylint: disable=redefined-outer-name
    return postgres_session_factory()


@pytest.fixture
def mappers():
    base_orm.start_mappers()
    league_season_orm.start_mappers()
    team_match_game_orm.start_mappers()
    try:
        yield
    finally:
        clear_mappers()
