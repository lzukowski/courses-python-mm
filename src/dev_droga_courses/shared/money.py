from dataclasses import dataclass
from decimal import Decimal
from typing import NewType, Text

Currency = NewType('Currency', Text)


@dataclass
class Money:
    amount: Decimal
    currency: Currency
