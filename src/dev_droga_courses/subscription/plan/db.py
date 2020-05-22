from datetime import datetime
from typing import Optional

from injector import inject
from sqlalchemy import Column, DateTime, Enum, Float, Integer, String
from sqlalchemy.ext.mutable import MutableComposite
from sqlalchemy.orm import composite, Session
from sqlalchemy_utils import CurrencyType, UUIDType

from dev_droga_courses.db import Base
from dev_droga_courses.shared.money import Money
from .cmd import PlanName
from .repository import IndividualPlanRepository, IndividualPlanDTO, Renewal


class MoneyComposite(Money, MutableComposite):
    def __composite_values__(self):
        return self.amount, self.currency

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        self.changed()

    @classmethod
    def coerce(cls, key, value):
        return (
            value if isinstance(value, MoneyComposite)
            else MoneyComposite(value.amount, value.currency)
        )

    def __eq__(self, other):
        return (
            self.amount == other.amount and
            self.currency == other.currency
        )


class IndividualPlanModel(IndividualPlanDTO, Base):
    __tablename__ = 'individual_plans'

    @classmethod
    def from_dto(cls, dto: IndividualPlanDTO) -> 'IndividualPlanModel':
        return IndividualPlanModel(
            id=dto.id,
            name=dto.name,
            fee=MoneyComposite(dto.fee.amount, dto.fee.currency),
            max_no_of_pauses=dto.max_no_of_pauses,
            renewal=dto.renewal,
        )

    id = Column(UUIDType(binary=True), primary_key=True)
    name = Column(String(100), nullable=False, index=True, unique=True)
    max_no_of_pauses = Column(Integer, nullable=False)
    renewal = Column(
        Enum(Renewal, create_constraint=False, native_enum=False),
        nullable=False,
    )
    when_created = Column(DateTime, nullable=False, default=datetime.utcnow)
    when_updated = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    fee = composite(
        MoneyComposite,
        Column('fee_amount', Float(asdecimal=True), nullable=False),
        Column('fee_currency', CurrencyType, nullable=False),
    )

    def __hash__(self):
        return hash(self.id)


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
