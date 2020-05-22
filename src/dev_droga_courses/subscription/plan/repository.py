from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Optional

from .cmd import PlanName
from .individual import IndividualPlanDTO


class IndividualPlanRepository(ABC):
    @abstractmethod
    def find(self, name: PlanName) -> Optional[IndividualPlanDTO]:
        raise NotImplementedError

    @abstractmethod
    def save(self, dto: IndividualPlanDTO) -> None:
        raise NotImplementedError

    @contextmanager
    def __call__(self, name: PlanName) -> IndividualPlanDTO:
        dto = self.find(name)
        yield dto
        self.save(dto)
