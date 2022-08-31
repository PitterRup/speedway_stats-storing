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


class AbstractTeamsGroupUnitOfWork(AbstractUnitOfWork[model.TeamsGroup]):
    teams_groups: base_repository.AbstractRepository

    def _get_seen_objects(self) -> set[model.TeamsGroup]:
        return self.teams_groups.seen
