from typing import Optional

from injector import inject
from sqlalchemy.orm import Session

from .cmd import PlanName
from .repository import IndividualPlanRepository
from .individual import IndividualPlan, Status


class ORMIndividualPlanRepository(IndividualPlanRepository):
    @inject
    def __init__(self, session: Session) -> None:
        self._session = session
        self.query = session.query(IndividualPlan)

    def find(self, name: PlanName) -> Optional[IndividualPlan]:
        return self.query.with_for_update().filter_by(name=name).one_or_none()

    def save(self, plan: IndividualPlan) -> None:
        self._session.merge(plan)
        try:
            self._session.commit()
        except:  # noqa
            self._session.rollback()
            raise

    def active_plans_count(self) -> int:
        return self.query.filter_by(status=Status.Activated).count()
