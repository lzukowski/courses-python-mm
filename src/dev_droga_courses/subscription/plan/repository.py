from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Optional

from .cmd import PlanName
from .individual import IndividualPlan


class IndividualPlanRepository(ABC):
    @abstractmethod
    def find(self, name: PlanName) -> Optional[IndividualPlan]:
        raise NotImplementedError

    @abstractmethod
    def save(self, plan: IndividualPlan) -> None:
        raise NotImplementedError

    @contextmanager
    def __call__(self, name: PlanName) -> IndividualPlan:
        plan = self.find(name)
        yield plan
        self.save(plan)
