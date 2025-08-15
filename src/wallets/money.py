from src.wallets.currency import Currency, rub, usd
from src.wallets.exceptions import NotComparisonException


class Money:
    def __init__(self, value: int, currency: Currency):
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
        self.currencies = self.set_start_currencies(money)

    def __getitem__(self, item: Currency):
        return self.check_currency(item)

    def __setitem__(self, key: Currency, value: int):
        obj = self.check_currency(key)
        if obj:
            obj.value += value
        else:
            self.currencies.append(Money(value=value, currency=key))

    def __delitem__(self, key: Currency):
        obj = self.check_currency(key)
        if obj:
            self.currencies.remove(obj)

    def __len__(self):
        return len(self.currencies)

    def __contains__(self, item: Currency):
        return item in self.currencies

    def add(self, money: Money) -> None:
        obj = self.check_currency(money.currency)
        if obj:
            obj.value += money.value


    def check_currency(self, other: Currency):
        for money in self.currencies:
            if money.currency == other:
                return money
        return None

    @staticmethod
    def set_start_currencies(money: Money):
        if money.currency == rub:
            return [money, Money(value=0, currency=usd)]
        return [Money(value=0, currency=rub), money]

