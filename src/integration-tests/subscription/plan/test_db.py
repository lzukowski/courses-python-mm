from unittest import TestCase

from sqlalchemy.orm import Session

from dev_droga_courses.app import register
from dev_droga_courses.subscription.plan.db import ORMIndividualPlanRepository
from tests.subscription.plan.factories import IndividualPlanFactory
from tests.utils import expect, given, then, when


class ORMIndividualPlanRepositoryTest(TestCase):
    def setUp(self) -> None:
        self.session = register.get(Session)
        self.repository = ORMIndividualPlanRepository(self.session)

    def test_can_save_a_plan(self):
        with given('plan'):
            plan = IndividualPlanFactory()

        with when('saves in repository'):
            self.repository.save(plan)
            self.session.close()

        with then('plan can be found by name'):
            entry = self.repository.find(plan.name)
            self.assertIsNotNone(entry)

        with expect('same values in entry'):
            self.assertEqual(plan.name, entry.name)
            self.assertEqual(plan.status, entry.status)
            self.assertEqual(plan.fee_amount, entry.fee_amount)
            self.assertEqual(plan.fee_currency, entry.fee_currency)
            self.assertEqual(plan.max_no_of_pauses, entry.max_no_of_pauses)
            self.assertEqual(plan.renewal, entry.renewal)
