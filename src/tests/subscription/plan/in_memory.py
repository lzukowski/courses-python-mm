from typing import Dict, Optional

from dev_droga_courses.subscription import plan
from dev_droga_courses.subscription.plan.repository import IndividualPlanDTO


class InMemoryIndividualPlanRepository(plan.IndividualPlanRepository):
    def __init__(self):
        self._plans: Dict[plan.cmd.PlanName, IndividualPlanDTO] = {}

    def find(self, name: plan.cmd.PlanName) -> Optional[IndividualPlanDTO]:
        return self._plans.get(name, None)

    def save(self, dto: IndividualPlanDTO) -> None:
        self._plans[dto.name] = dto

    def __repr__(self):
        return (
            f'<InMemory[{id(self)}] '
            f'IndividualPlanRepository '
            f'[{len(self._plans)}]>'
        )
