from typing import Type, Callable

from storing.domain import commands, events
from storing.domain.models import base
from storing.service_layer import unit_of_work


def add_team(
    cmd: commands.AddTeam,
    uow: unit_of_work.AbstractTeamsGroupUnitOfWork,
):
    with uow:
        teams = uow.teams_groups.get(cmd.team_group_name)
        if teams is None:
            teams = base.TeamsGroup(cmd.team_group_name)
            uow.teams_groups.add(teams)
        teams.add(base.Team(cmd.team_name))
        uow.commit()


def recognize_team(
    cmd: commands.AddTeam,
    uow: unit_of_work.AbstractTeamsGroupUnitOfWork,
):
    with uow:
        teams = uow.teams_groups.get(cmd.team_group_name)
        teams.recognize(cmd.team_name)
        uow.commit()


def publish_recognized_team_event(
    event: events.Event,
    publish: Callable,
):
    publish("team_recognized", event)


def add_rider(
    cmd: commands.AddRider,
    uow: unit_of_work.AbstractRidersGroupUnitOfWork,
):
    with uow:
        riders = uow.riders_groups.get(cmd.rider_group_name)
        if riders is None:
            riders = base.RidersGroup(cmd.rider_group_name)
            uow.riders_groups.add(riders)
        riders.add(base.Rider(cmd.rider_name, cmd.birthday))
        uow.commit()


EVENT_HANDLERS: dict[Type[events.Event], Callable] = {
    events.RecognizedTeam: [publish_recognized_team_event],
}

COMMAND_HANDLERS: dict[Type[commands.Command], Callable] = {
    commands.AddTeam: add_team,
    commands.RecognizeTeam: recognize_team,
    commands.AddRider: add_rider,
}
