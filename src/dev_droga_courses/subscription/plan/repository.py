from abc import ABC, abstractmethod
from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum
from typing import NewType, Optional
from uuid import UUID

from dev_droga_courses.shared.money import Money
from .cmd import PlanName


class Renewal(Enum):
    Month = 'MONTH'
    Annual = 'ANNUAL'


IndividualPlanID = NewType('IndividualPlanID', UUID)


@dataclass
class IndividualPlanDTO:
    id: IndividualPlanID
    name: PlanName
    fee: Money
    max_no_of_pauses: int
    renewal: Renewal


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
