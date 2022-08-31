from storing.adapters.repositories.abstract_repository import (
    AbstractRepository, AbstractSqlAlchemyRepository
)
from storing.domain.models import league_season as model

class AbstractLeagueSeasonRepository(AbstractRepository[model.LeagueSeason, model.Year]):
    pass


class SqlAlchemyLeagueSeasonRepository(
    AbstractSqlAlchemyRepository, AbstractLeagueSeasonRepository
):

    def _get(self, ident: model.Year):
        return self.session.query(model.LeagueSeason).filter_by(year=ident).first()
