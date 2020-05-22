from typing import Optional

from injector import inject
from sqlalchemy.orm import Session

from .cmd import PlanName
from .repository import IndividualPlanRepository
from .individual import IndividualPlanDTO, IndividualPlanModel


class ORMIndividualPlanRepository(IndividualPlanRepository):
    @inject
    def __init__(self, session: Session) -> None:
        self._session = session
        self.query = session.query(IndividualPlanModel)

    def find(self, name: PlanName) -> Optional[IndividualPlanDTO]:
        return self.query.with_for_update().filter_by(name=name).one_or_none()

    def save(self, dto: IndividualPlanDTO) -> None:
        model = (
            dto
            if isinstance(dto, IndividualPlanModel)
            else IndividualPlanModel.from_dto(dto)
        )
        self._session.merge(model)
        try:
            self._session.commit()
        except:
            self._session.rollback()
            raise
