from datetime import date
from typing import Type

from storing import bootstrap
from storing.adapters.repositories import base_repository
from storing.domain import commands, events
from storing.service_layer import unit_of_work


class FakeTeamsGroupsRepository(base_repository.AbstractTeamsGroupRepository):
    def __init__(self, teams_group):
        super().__init__()
        self._teams_group = set(teams_group)

    def _add(self, obj):
        self._teams_group.add(obj)

    def _get(self, ident):
        return next((g for g in self._teams_group if g.name == ident), None)


class FakeRidersGroupsRepository(base_repository.AbstractRidersGroupRepository):
    def __init__(self, teams_group):
        super().__init__()
        self._riders_groups = set(teams_group)

    def _add(self, obj):
        self._riders_groups.add(obj)

    def _get(self, ident):
        return next((g for g in self._riders_groups if g.name == ident), None)


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self):
        self.committed = False

    def _commit(self):
        self.committed = True

    def rollback(self):
        pass


class FakeTeamsGroupUnitOfWork(FakeUnitOfWork, unit_of_work.AbstractTeamsGroupUnitOfWork):
    def __init__(self):
        self.teams_groups = FakeTeamsGroupsRepository([])
        super().__init__()


class FakeRidersGroupUnitOfWork(FakeUnitOfWork, unit_of_work.AbstractRidersGroupUnitOfWork):
    def __init__(self):
        self.riders_groups = FakeRidersGroupsRepository([])
        super().__init__()


def bootstrap_teams_groups_test_app(published_events: list[tuple[str, Type[events.Event]]] = None):
    def fake_publish(*args):
        if published_events is not None:
            published_events.append(args)

    return bootstrap.bootstrap(
        start_orm=False,
        uow=FakeTeamsGroupUnitOfWork(),
        publish=fake_publish,
    )


def bootstrap_riders_groups_test_app(published_events: list[tuple[str, Type[events.Event]]] = None):
    def fake_publish(*args):
        if published_events is not None:
            published_events.append(args)
            
    return bootstrap.bootstrap(
        start_orm=False,
        uow=FakeRidersGroupUnitOfWork(),
        publish=fake_publish,
    )



class TestAddTeam:
    def test_for_new_teams_group(self):
        bus = bootstrap_teams_groups_test_app()
        bus.handle(commands.AddTeam('Speedway', 'Lublin'))
        assert bus.uow.teams_groups.get("Speedway") is not None
        assert bus.uow.committed

    def test_for_existing_teams_group(self):
        bus = bootstrap_teams_groups_test_app()
        bus.handle(commands.AddTeam('Speedway', 'Lublin'))
        bus.handle(commands.AddTeam('Speedway', 'Wrocław'))
        assert "Wrocław" in [
            t.name for t in bus.uow.teams_groups.get("Speedway").teams
        ]


class TestRecognizeTeam:
    def test_publish_event_when_recognized(self):
        published_events = []
        bus = bootstrap_teams_groups_test_app(published_events)
        bus.handle(commands.AddTeam('Speedway', 'Lublin'))
        bus.handle(commands.RecognizeTeam('Speedway', 'Lublin'))
        assert published_events[-1] == ('team_recognized', events.RecognizedTeam('Lublin', None))


class TestAddRider:
    def test_for_new_riders_group(self):
        bus = bootstrap_riders_groups_test_app()
        bus.handle(commands.AddRider('Speedway', 'Bartosz Zmarzlik', date(1993, 1, 1)))
        assert bus.uow.riders_groups.get("Speedway") is not None
        assert bus.uow.committed

    def test_for_existing_riders_group(self):
        bus = bootstrap_riders_groups_test_app()
        bus.handle(commands.AddRider('Speedway', 'Bartosz Zmarzlik', date(1993, 1, 1)))
        bus.handle(commands.AddRider('Speedway', 'Paweł Zmarzlik', date(1993, 1, 1)))
        assert "Paweł Zmarzlik" in [
            t.name for t in bus.uow.riders_groups.get("Speedway").riders
        ]
