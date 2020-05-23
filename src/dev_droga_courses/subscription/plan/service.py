from functools import singledispatchmethod
from typing import cast, List

from injector import inject
from returns.result import safe

from dev_droga_courses.shared.service import CommandHandler, Event, Result
from .cmd import Activate, DefineMonthlyPlan, Deactivate, PlanCommand
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
    def __call__(self, command: PlanCommand) -> Result:
        return cast(Result, self._handle(command))

    @singledispatchmethod
    def _handle(self, command: PlanCommand) -> List[Event]:
        with self._repository(command.name) as plan:
            if not plan:
                raise DoesNotExists(command.name)
            self._handle_with_plan(command, plan)
        return []

    @singledispatchmethod
    def _handle_with_plan(self, c: PlanCommand, p: IndividualPlan,) -> None:
        raise NotImplementedError

    @_handle_with_plan.register(Activate)
    def _activate_plan(self, _: Activate, plan: IndividualPlan) -> None:
        if self._max_active_reached():
            raise MaxActivePlansReached()
        plan.activate()

    def _max_active_reached(self) -> bool:
        active = self._repository.active_plans_count()
        return self._max_active <= active

    @_handle_with_plan.register(Deactivate)
    def _deactivate_plan(self, _: Deactivate, plan: IndividualPlan) -> None:
        plan.deactivate()

    @_handle.register(DefineMonthlyPlan)
    def _define_monthly_plan(self, command: DefineMonthlyPlan) -> List[Event]:
        if self._repository.find(command.name):
            raise AlreadyExists(command.name)

        plan = IndividualPlan.create_monthly(
            command.name, command.monthlyFee, command.pauses,
        )
        self._repository.save(plan)
        return []
