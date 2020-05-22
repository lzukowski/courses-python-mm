from uuid import uuid1

from factory import Factory, LazyAttribute, SubFactory
from factory.faker import Faker
from factory.fuzzy import FuzzyChoice, FuzzyDecimal

from dev_droga_courses.subscription import plan
from dev_droga_courses.subscription.plan.individual import (
    IndividualPlan, Renewal,
)
from tests.shared.factories import MoneyFactory


class DefineMonthlyPlanFactory(Factory):
    class Meta:
        model = plan.cmd.DefineMonthlyPlan

    name = Faker('name', locale='pl_PL')
    monthlyFee = SubFactory(MoneyFactory)
    pauses = plan.cmd.MAX_NUMBER_OF_PAUSES


class IndividualPlanFactory(Factory):
    class Meta:
        model = IndividualPlan

    id = LazyAttribute(lambda _: uuid1())
    name = Faker('name', locale='pl_PL')
    fee_amount = FuzzyDecimal(low=10)
    fee_currency = FuzzyChoice(['PLN', 'USD', 'EUR', 'GBP'])
    max_no_of_pauses = plan.cmd.MAX_NUMBER_OF_PAUSES
    renewal = FuzzyChoice(Renewal)
