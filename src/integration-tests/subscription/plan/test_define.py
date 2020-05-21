from unittest import TestCase

from dev_droga_courses.app import register
from dev_droga_courses.subscription import plan
from dev_droga_courses.subscription.plan.repository import Renewal
from tests.subscription.plan.factories import DefineMonthlyPlanFactory
from tests.subscription.plan.in_memory import InMemoryIndividualPlanRepository


class DefineIndividualPlanTest(TestCase):
    def setUp(self) -> None:
        self.repository = InMemoryIndividualPlanRepository()
        register.binder.bind(plan.IndividualPlanRepository, to=self.repository)
        self.handle = register.get(plan.CommandHandlerService)

    def test_plan_is_created_with_correct_values(self):
        command = DefineMonthlyPlanFactory()
        self.handle(command)

        entry = self.repository.find(command.name)

        self.assertIsNotNone(entry)
        self.assertEqual(entry.name, command.name)
        self.assertEqual(entry.max_no_of_pauses, command.pauses)
        self.assertEqual(entry.fee, command.monthlyFee)
        self.assertEqual(entry.renewal, Renewal.Month)
