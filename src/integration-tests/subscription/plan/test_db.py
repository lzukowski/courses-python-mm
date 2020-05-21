from decimal import Decimal
from unittest import TestCase

from sqlalchemy.orm import Session

from dev_droga_courses.app import register
from dev_droga_courses.shared.money import Currency, Money
from dev_droga_courses.subscription.plan.db import ORMIndividualPlanRepository
from tests.subscription.plan.factories import IndividualPlanDTOFactory
from tests.utils import expect, given, then, when


class ORMIndividualPlanRepositoryTest(TestCase):
    def setUp(self) -> None:
        self.session = register.get(Session)
        self.repository = ORMIndividualPlanRepository(self.session)

    def test_can_save_a_plan(self):
        with given('plan dto'):
            dto = IndividualPlanDTOFactory()

        with when('saves in repository'):
            self.repository.save(dto)
            self.session.close()

        with then('plan can be found by name'):
            entry = self.repository.find(dto.name)
            self.assertIsNotNone(entry)

        with expect('same values in entry'):
            self.assertEqual(dto.name, entry.name)
            self.assertEqual(dto.fee, entry.fee)
            self.assertEqual(dto.max_no_of_pauses, entry.max_no_of_pauses)
            self.assertEqual(dto.renewal, entry.renewal)

    def test_fee_composite_changes(self):
        with given('plan dto'):
            dto = IndividualPlanDTOFactory()
            name = dto.name
            self.repository.save(dto)
            self.session.close()

        with then('stores replacing whole fee'):
            with self.repository(name) as dto:
                fee = Money(Decimal('10'), currency=Currency('PLN'))
                dto.fee = fee

            self.session.close()

            with self.repository(name) as dto:
                dto = self.repository.find(dto.name)
                self.assertEqual(fee, dto.fee)

        with then('stores replacing amount only'):
            with self.repository(name) as dto:
                amount = Decimal('432')
                dto.fee.amount = amount

            self.session.close()

            with self.repository(name) as dto:
                dto = self.repository.find(dto.name)
                self.assertEqual(amount, dto.fee.amount)

        with then('stores replacing currency only'):
            with self.repository(name) as dto:
                currency = Currency('XXX')
                dto.fee.currency = currency

            self.session.close()

            with self.repository(name) as dto:
                dto = self.repository.find(dto.name)
                self.assertEqual(currency, dto.fee.currency)
