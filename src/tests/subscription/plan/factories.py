from factory import Factory, SubFactory
from factory.faker import Faker

from dev_droga_courses.subscription import plan
from tests.shared.factories import MoneyFactory


class DefineMonthlyPlanFactory(Factory):
    class Meta:
        model = plan.cmd.DefineMonthlyPlan

    name = Faker('name', locale='pl_PL')
    monthlyFee = SubFactory(MoneyFactory)
    pauses = plan.cmd.MAX_NUMBER_OF_PAUSES
