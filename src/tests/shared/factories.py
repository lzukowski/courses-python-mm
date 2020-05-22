from factory import Factory
from factory.fuzzy import FuzzyChoice, FuzzyDecimal

from dev_droga_courses.shared.money import Money


class MoneyFactory(Factory):
    class Meta:
        model = Money

    amount = FuzzyDecimal(low=10)
    currency = FuzzyChoice(['PLN', 'USD', 'EUR', 'GBP'])
