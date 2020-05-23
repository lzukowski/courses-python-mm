from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import uuid1

from sqlalchemy import Column, DateTime, Enum as SQLEnum, Float, Integer, String
from sqlalchemy_utils import CurrencyType, UUIDType

from dev_droga_courses.db import Base
from dev_droga_courses.shared.money import Currency, Money
from .cmd import PlanName


class Renewal(Enum):
    Month = 'MONTH'
    Annual = 'ANNUAL'


class IndividualPlan(Base):
    __tablename__ = 'individual_plans'

    @classmethod
    def createMonthly(
            cls, name: PlanName, fee: Money, max_no_of_pauses: int,
    ) -> 'IndividualPlan':
        return IndividualPlan(
            name=name,
            fee_amount=fee.amount,
            fee_currency=fee.currency,
            max_no_of_pauses=max_no_of_pauses,
            renewal=Renewal.Month,
        )

    id = Column(UUIDType(binary=True), primary_key=True, default=uuid1)
    name: PlanName = Column(
        String(100), nullable=False, index=True, unique=True,
    )
    max_no_of_pauses = Column(Integer, nullable=False)
    fee_amount: Decimal = Column(Float(asdecimal=True), nullable=False)
    fee_currency: Currency = Column(CurrencyType, nullable=False)
    renewal: Renewal = Column(
        SQLEnum(Renewal, create_constraint=False, native_enum=False),
        nullable=False,
    )
    when_created = Column(DateTime, nullable=False, default=datetime.utcnow)
    when_updated = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    def __hash__(self):
        return hash(self.id)

    def activate(self) -> None:
        raise NotImplementedError
