from typing import NewType, Text

from dev_droga_courses.shared.money import Money
from dev_droga_courses.shared.service import Command

PlanName = NewType('PlanName', Text)
MAX_NUMBER_OF_PAUSES = 3


class PlanCommand(Command):
    name: PlanName


class DefineMonthlyPlan(PlanCommand):
    monthlyFee: Money
    pauses: int = MAX_NUMBER_OF_PAUSES


class Activate(PlanCommand):
    pass


class Deactivate(PlanCommand):
    pass
