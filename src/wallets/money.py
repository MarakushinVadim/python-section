from typing_extensions import TypeAlias

from src.wallets.currency import Currency, Rub
from src.wallets.exceptions import NotComparisonException

CurrencyType: TypeAlias = list[Currency]

class Money:
    def __init__(self, value: float, currency: Currency):
        self.value = value
        self.currency = currency

    def __add__(self, other):
        self.check_currency(other)
        return Money(value=self.value + other.value, currency=self.currency)

    def __sub__(self, other):
        self.check_currency(other)
        return Money(value=self.value - other.value, currency=self.currency)

    def __eq__(self, other):
        return self.value == other

    def check_currency(self, other):
        if not(self.currency is other.currency):
            raise NotComparisonException


class Wallet:


    def __init__(self, money: Money):
        self.currencies = [money]

