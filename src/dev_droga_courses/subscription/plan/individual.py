from datetime import datetime
from enum import Enum
from uuid import uuid1

from sqlalchemy import Column, DateTime, Enum as SQLEnum, Float, Integer, String
from sqlalchemy.ext.mutable import MutableComposite
from sqlalchemy.orm import composite
from sqlalchemy_utils import CurrencyType, UUIDType

from dev_droga_courses.db import Base
from dev_droga_courses.shared.money import Money
from .cmd import PlanName


class Renewal(Enum):
    Month = 'MONTH'
    Annual = 'ANNUAL'


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


class IndividualPlan(Base):
    __tablename__ = 'individual_plans'

    @classmethod
    def createMonthly(
            cls, name: PlanName, fee: Money, max_no_of_pauses: int,
    ) -> 'IndividualPlan':
        return IndividualPlan(
            name=name,
            fee=fee,
            max_no_of_pauses=max_no_of_pauses,
            renewal=Renewal.Month,
        )

    id = Column(UUIDType(binary=True), primary_key=True, default=uuid1)
    name: PlanName = Column(
        String(100), nullable=False, index=True, unique=True,
    )
    max_no_of_pauses = Column(Integer, nullable=False)
    renewal = Column(
        SQLEnum(Renewal, create_constraint=False, native_enum=False),
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
