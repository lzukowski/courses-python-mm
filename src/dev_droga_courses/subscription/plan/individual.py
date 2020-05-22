from uuid import uuid1

from dev_droga_courses.shared.money import Money
from .cmd import PlanName
from .repository import IndividualPlanDTO, IndividualPlanID, Renewal


class IndividualPlan:
    def __init__(self, dto: IndividualPlanDTO) -> None:
        self._dto = dto

    @classmethod
    def createMonthly(
            cls, name: PlanName, fee: Money, max_no_of_pauses: int,
    ) -> IndividualPlanDTO:
        plan_id = IndividualPlanID(uuid1())
        return IndividualPlanDTO(
            plan_id, name, fee, max_no_of_pauses, Renewal.Month,
        )
