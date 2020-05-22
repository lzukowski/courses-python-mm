from decimal import Decimal
from unittest import TestCase

from sqlalchemy.orm import Session

from dev_droga_courses.app import register
from dev_droga_courses.shared.money import Currency, Money
from dev_droga_courses.subscription.plan.db import ORMIndividualPlanRepository
from tests.subscription.plan.factories import IndividualPlanFactory
from tests.utils import expect, given, then, when


class ORMIndividualPlanRepositoryTest(TestCase):
    def setUp(self) -> None:
        self.session = register.get(Session)
        self.repository = ORMIndividualPlanRepository(self.session)

    def test_can_save_a_plan(self):
        with given('plan plan'):
            plan = IndividualPlanFactory()

        with when('saves in repository'):
            self.repository.save(plan)
            self.session.close()

        with then('plan can be found by name'):
            entry = self.repository.find(plan.name)
            self.assertIsNotNone(entry)

        with expect('same values in entry'):
            self.assertEqual(plan.name, entry.name)
            self.assertEqual(plan.fee, entry.fee)
            self.assertEqual(plan.max_no_of_pauses, entry.max_no_of_pauses)
            self.assertEqual(plan.renewal, entry.renewal)

    def test_fee_composite_changes(self):
        with given('plan'):
            plan = IndividualPlanFactory()
            name = plan.name
            self.repository.save(plan)
            self.session.close()

        with then('stores replacing whole fee'):
            with self.repository(name) as plan:
                fee = Money(Decimal('10'), currency=Currency('PLN'))
                plan.fee = fee

            self.session.close()

            with self.repository(name) as plan:
                plan = self.repository.find(plan.name)
                self.assertEqual(fee, plan.fee)

        with then('stores replacing amount only'):
            with self.repository(name) as plan:
                amount = Decimal('432')
                plan.fee.amount = amount

            self.session.close()

            with self.repository(name) as plan:
                plan = self.repository.find(plan.name)
                self.assertEqual(amount, plan.fee.amount)

        with then('stores replacing currency only'):
            with self.repository(name) as plan:
                currency = Currency('XXX')
                plan.fee.currency = currency

            self.session.close()

            with self.repository(name) as plan:
                plan = self.repository.find(plan.name)
                self.assertEqual(currency, plan.fee.currency)
