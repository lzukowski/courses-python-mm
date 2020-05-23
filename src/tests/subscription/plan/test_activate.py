from unittest import TestCase

from dev_droga_courses.app import register
from dev_droga_courses.shared.service import Result
from dev_droga_courses.subscription import plan
from tests.utils import expect, failed, given, raises, succeeded, then, when
from .factories import ActivateFactory, DefineMonthlyPlanFactory
from .in_memory import InMemoryIndividualPlanRepository


class ActivateIndividualPlanTest(TestCase):
    def setUp(self) -> None:
        self.repository = InMemoryIndividualPlanRepository()
        register.binder.bind(plan.IndividualPlanRepository, to=self.repository)
        self.handle = register.get(plan.CommandHandlerService)

    def test_cannot_activate_not_existing_plan(self):
        with when('Activating not existing plan'):
            command = plan.cmd.Activate(name='Not Existing Plan')
            result = self.handle(command)

        with expect('failure'):
            failed(result, plan.exce.DoesNotExists)

    def test_cannot_activate_plan_when_max_number_of_plans_activated(self):
        with given('max number of active plans'):
            for _ in range(register.get(plan.settings.MaxActivePlans)):
                self._define_and_activate_random_plan()

        with when('define and activate plan'):
            result = self._define_and_activate_random_plan()

        with expect('failure'):
            failed(result, plan.exce.MaxActivePlansReached)

    def test_can_activate_a_plan(self):
        with given('defined not active plan'):
            command = DefineMonthlyPlanFactory()
            succeeded(self.handle(command))

        name = command.name

        with then('plan can be activated'):
            succeeded(self.handle(ActivateFactory(name=name)))

    def _define_and_activate_random_plan(self) -> Result:
        define = DefineMonthlyPlanFactory()
        succeeded(self.handle(define))
        return self.handle(ActivateFactory(name=define.name))
