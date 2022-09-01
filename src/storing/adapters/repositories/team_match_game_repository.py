from storing.adapters.repositories.abstract_repository import (
    AbstractRepository, AbstractSqlAlchemyRepository
)
from storing.domain.models import team_match_game as model

class AbstractTeamMatchGameRepository(AbstractRepository[model.TeamMatchGame, int]):
    pass


class SqlAlchemyTeamMatchGameRepository(
    AbstractSqlAlchemyRepository, AbstractTeamMatchGameRepository
):

    def _get(self, ident: int):
        return self.session.query(model.TeamMatchGame).filter_by(id_team_match_game=ident).first()
