from unittest import TestCase

from dev_droga_courses.app import register
from dev_droga_courses.subscription import plan
from dev_droga_courses.subscription.plan.individual import Renewal
from tests.utils import failed, given, succeeded, then, when, expect
from .factories import DefineMonthlyPlanFactory
from .in_memory import InMemoryIndividualPlanRepository


class DefineIndividualPlanTest(TestCase):
    def setUp(self) -> None:
        self.repository = InMemoryIndividualPlanRepository()
        register.binder.bind(plan.IndividualPlanRepository, to=self.repository)
        self.handle = register.get(plan.CommandHandlerService)

    def test_should_not_create_a_plan_when_a_name_already_exists(self):
        with given('defined plan'):
            name = plan.cmd.PlanName("Very cool plan for 10 bucks")
            succeeded(self.handle(DefineMonthlyPlanFactory(name=name)))

        with when('defining plan with same name'):
            result = self.handle(DefineMonthlyPlanFactory(name=name))

        with expect('failure'):
            failed(result, plan.exce.AlreadyExists)

    def test_should_create_a_plan_when_there_is_no_plan_with_such_a_name(self):
        with given('defined plan'):
            succeeded(self.handle(DefineMonthlyPlanFactory()))

        with then('defining yet another plan should succeed'):
            succeeded(self.handle(DefineMonthlyPlanFactory()))

    def test_plan_is_created_with_correct_values(self):
        command = DefineMonthlyPlanFactory()

        with when('defining new plan'):
            succeeded(self.handle(command))

        with when('find a plan'):
            entry = self.repository.find(command.name)

        with then('plan is present'):
            self.assertIsNotNone(entry)

        with expect('correct values'):
            self.assertEqual(entry.name, command.name)
            self.assertEqual(entry.max_no_of_pauses, command.pauses)
            self.assertEqual(entry.fee_amount, command.monthlyFee.amount)
            self.assertEqual(entry.fee_currency, command.monthlyFee.currency)
            self.assertEqual(entry.renewal, Renewal.Month)
