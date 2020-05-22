from functools import singledispatchmethod
from typing import cast, List

from injector import inject
from returns.result import safe

from dev_droga_courses.shared.service import (
    Command, CommandHandler, Event, Result,
)
from .cmd import DefineMonthlyPlan
from .exce import AlreadyExists
from .individual import IndividualPlan
from .repository import IndividualPlanRepository


class CommandHandlerService(CommandHandler):
    @inject
    def __init__(self, repository: IndividualPlanRepository) -> None:
        self._repository = repository

    @safe
    def __call__(self, command: Command) -> Result:
        return cast(Result, self._handle(command))

    @singledispatchmethod
    def _handle(self, command: Command) -> List[Event]:
        raise NotImplementedError

    @_handle.register(DefineMonthlyPlan)
    def _define_monthly_plan(self, command: DefineMonthlyPlan) -> List[Event]:
        if self._repository.find(command.name):
            raise AlreadyExists(command.name)

        plan = IndividualPlan.createMonthly(
            command.name, command.monthlyFee, command.pauses,
        )
        self._repository.save(plan)
        return []
