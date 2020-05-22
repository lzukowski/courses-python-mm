from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import NewType
from uuid import UUID, uuid1

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


IndividualPlanID = NewType('IndividualPlanID', UUID)


@dataclass
class IndividualPlanDTO:
    id: IndividualPlanID
    name: PlanName
    fee: Money
    max_no_of_pauses: int
    renewal: Renewal


class IndividualPlan:
    def __init__(self, dto: IndividualPlanDTO) -> None:
        self._dto = dto

    @classmethod
    def createMonthly(
            cls, name: PlanName, fee: Money, max_no_of_pauses: int,
    ) -> IndividualPlanDTO:
        plan_id = IndividualPlanID(uuid1())
        return IndividualPlanDTO(
            plan_id, name, fee, max_no_of_pauses, Renewal.Month,
        )


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
