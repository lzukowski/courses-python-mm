from typing import Optional

from sqlalchemy import Column
from sqlalchemy_utils import UUIDType

from dev_droga_courses.db import Base
from .cmd import PlanName
from .repository import IndividualPlanRepository, IndividualPlanDTO


class IndividualPlanModel(IndividualPlanDTO, Base):
    __tablename__ = 'individual_plans'

    id = Column(UUIDType(binary=True), primary_key=True)


class ORMIndividualPlanRepository(IndividualPlanRepository):
    def find(self, name: PlanName) -> Optional[IndividualPlanDTO]:
        raise NotImplementedError

    def save(self, dto: IndividualPlanDTO) -> None:
        raise NotImplementedError
