import inspect
from typing import Callable

from storing.adapters.orm import base_orm, league_season_orm, team_match_game_orm
from storing.service_layer import handlers, messagebus, unit_of_work


def bootstrap(
    uow: unit_of_work.AbstractUnitOfWork,
    publish: Callable,
    start_orm: bool = True,
) -> messagebus.MessageBus:

    if start_orm:
        base_orm.start_mappers()
        league_season_orm.start_mappers()
        team_match_game_orm.start_mappers()

    dependencies = {"uow": uow, "publish": publish}
    injected_event_handlers = {
        event_type: [
            inject_dependencies(handler, dependencies)
            for handler in event_handlers
        ]
        for event_type, event_handlers in handlers.EVENT_HANDLERS.items()
    }
    injected_command_handlers = {
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in handlers.COMMAND_HANDLERS.items()
    }

    return messagebus.MessageBus(
        uow=uow,
        event_handlers=injected_event_handlers,
        command_handlers=injected_command_handlers,
    )


def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency
        for name, dependency in dependencies.items()
        if name in params
    }
    return lambda message: handler(message, **deps)  # pylint: disable=unnecessary-lambda
