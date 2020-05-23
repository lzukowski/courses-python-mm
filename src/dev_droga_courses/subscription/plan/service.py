from functools import singledispatchmethod
from typing import cast, List

from injector import inject
from returns.result import safe

from dev_droga_courses.shared.service import (
    Command, CommandHandler, Event, Result,
)
from .cmd import Activate, DefineMonthlyPlan, Deactivate
from .exce import AlreadyExists, DoesNotExists, MaxActivePlansReached
from .individual import IndividualPlan
from .repository import IndividualPlanRepository
from .settings import MaxActivePlans


class CommandHandlerService(CommandHandler):
    @inject
    def __init__(
            self,
            repository: IndividualPlanRepository,
            max_active: MaxActivePlans,
    ) -> None:
        self._repository = repository
        self._max_active = max_active

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

    @_handle.register(Activate)
    def _activate_plan(self, command: Activate) -> List[Event]:
        if self._max_active_reached():
            raise MaxActivePlansReached()

        with self._repository(command.name) as plan:
            if not plan:
                raise DoesNotExists(command.name)
            plan.activate()
        return []

    @_handle.register(Deactivate)
    def _deactivate_plan(self, command: Deactivate) -> List[Event]:
        with self._repository(command.name) as plan:
            if not plan:
                raise DoesNotExists(command.name)
            plan.deactivate()
        return []

    def _max_active_reached(self) -> bool:
        active = self._repository.active_plans_count()
        return self._max_active <= active
