from unittest import TestCase

from dev_droga_courses.subscription import plan
from tests.utils import given, succeeded, then, raises, failed
from . import register
from .factories import (
    DefineMonthlyPlanFactory,
    ActivateFactory,
    DeactivateFactory,
)


class DeactivateIndividualPlanTest(TestCase):
    def setUp(self) -> None:
        self.handle = register.get(plan.CommandHandlerService)

    def test_can_deactivate_an_existing_plan(self):
        with given('activate monthly plan'):
            define = DefineMonthlyPlanFactory()
            succeeded(self.handle(define))
            succeeded(self.handle(ActivateFactory(name=define.name)))

        name = define.name

        with then('plan can be deactivated'):
            succeeded(self.handle(DeactivateFactory(name=name)))

    def test_cannot_deactivate_a_plan_which_does_not_exist(self):
        failed(
            self.handle(DeactivateFactory(name='Not existing plan')),
            plan.exce.DoesNotExists,
        )
