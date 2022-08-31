import abc
from typing import Generic, TypeVar


M = TypeVar('M')
T = TypeVar('T')


class AbstractRepository(abc.ABC, Generic[M, T]):
    def __init__(self):
        self.seen = set()

    def add(self, obj: M):
        self._add(obj)
        self.seen.add(obj)

    def get(self, *args) -> M:
        obj = self._get(*args)
        if obj:
            self.seen.add(obj)
        return obj

    @abc.abstractmethod
    def _add(self, obj: M):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, ident: T) -> M:
        raise NotImplementedError


class AbstractSqlAlchemyRepository():
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, obj):
        self.session.add(obj)
