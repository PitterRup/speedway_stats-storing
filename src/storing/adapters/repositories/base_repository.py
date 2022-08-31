from storing.adapters.repositories.abstract_repository import (
    AbstractRepository, AbstractSqlAlchemyRepository
)
from storing.domain.models import base as model


class AbstractTeamsGroupRepository(AbstractRepository[model.TeamsGroup, str]):
    pass


class SqlAlchemyTeamsGroupRepository(AbstractSqlAlchemyRepository, AbstractTeamsGroupRepository):

    def _get(self, ident: str):
        return self.session.query(model.TeamsGroup).filter_by(name=ident).first()


class AbstractRidersGroupRepository(AbstractRepository[model.RidersGroup, str]):
    pass


class SqlAlchemyRidersGroupRepository(AbstractSqlAlchemyRepository, AbstractRidersGroupRepository):

    def _get(self, ident: str):
        return self.session.query(model.RidersGroup).filter_by(name=ident).first()
