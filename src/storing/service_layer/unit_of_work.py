import abc
from typing import Generator, TypeVar, Generic

from storing.adapters.repositories import base_repository
from storing.domain.models import base as model

M = TypeVar('M')

class AbstractUnitOfWork(abc.ABC, Generic[M]):

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    def collect_new_events(self) -> Generator[M, None, None]:
        for obj in self._get_seen_objects():
            while obj.events:
                yield obj.events.pop(0)

    @abc.abstractmethod
    def _get_seen_objects(self) -> set[model.TeamsGroup]:
        raise NotImplementedError

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()  # pylint: disable=attribute-defined-outside-init
        self._enter()
        return super().__enter__()

    @abc.abstractmethod
    def _enter(self):
        raise NotImplementedError

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


class AbstractTeamsGroupUnitOfWork(AbstractUnitOfWork[model.TeamsGroup]):
    teams_groups: base_repository.AbstractTeamsGroupRepository

    def _get_seen_objects(self) -> set[model.TeamsGroup]:
        return self.teams_groups.seen


class SqlAlchemyTeamsGroupUnitOfWork(AbstractTeamsGroupUnitOfWork, SqlAlchemyUnitOfWork):
    def _enter(self):
        self.teams_groups = base_repository.SqlAlchemyTeamsGroupRepository(self.session)


class AbstractRidersGroupUnitOfWork(AbstractUnitOfWork[model.RidersGroup]):
    riders_groups: base_repository.AbstractRidersGroupRepository

    def _get_seen_objects(self) -> set[model.TeamsGroup]:
        return self.riders_groups.seen


class SqlAlchemyRidersGroupUnitOfWork(AbstractRidersGroupUnitOfWork, SqlAlchemyUnitOfWork):
    def _enter(self):
        self.riders_groups = base_repository.SqlAlchemyRidersGroupRepository(self.session)
