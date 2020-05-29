from typing import Dict, Optional

from dev_droga_courses.subscription.plan import cmd, IndividualPlanRepository
from dev_droga_courses.subscription.plan.individual import IndividualPlan


class InMemoryIndividualPlanRepository(IndividualPlanRepository):
    def __init__(self):
        self._plans: Dict[cmd.PlanName, IndividualPlan] = {}

    def find(self, name: cmd.PlanName) -> Optional[IndividualPlan]:
        return self._plans.get(name, None)

    def save(self, plan: IndividualPlan) -> None:
        self._plans[plan.name] = plan

    def active_plans_count(self) -> int:
        return sum(p.is_active() for p in self._plans.values())

    def __repr__(self):
        return (
            f'<InMemory[{id(self)}] '
            f'IndividualPlanRepository '
            f'[{len(self._plans)}]>'
        )
