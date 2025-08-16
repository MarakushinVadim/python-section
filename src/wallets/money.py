from dataclasses import dataclass

from src.wallets.currency import Currency, rub, usd
from src.wallets.exceptions import NotComparisonException, NegativeValueException


@dataclass(slots=True)
class Money:
    value: int
    currency: Currency

    def __add__(self, other):
        self.check_currency(other)
        return Money(value=self.value + other.value, currency=self.currency)

    def __sub__(self, other):
        self.check_currency(other)
        if self.value - other.value >= 0:
            return Money(value=self.value - other.value, currency=self.currency)
        raise NegativeValueException

    def check_currency(self, other):
        if not (self.currency is other.currency):
            raise NotComparisonException
        return other


class Wallet:
    __slots__ = ['money', 'currencies']

    def __init__(self, money: Money):
        self.money = money
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
        accounts_with_balance = self.check_balance()
        return len(accounts_with_balance)

    def __contains__(self, item: Currency):
        currency_list = []
        accounts_with_balance = self.check_balance()
        for account in accounts_with_balance:
            currency_list.append(account.currency)
        return item in currency_list

    def add(self, money: Money):
        obj = self.check_currency(money.currency)
        if obj:
            obj.value += money.value
        return self

    def sub(self, money: Money):
        obj = self.check_currency(money.currency)
        if obj:
            if obj.value - money.value >= 0:
                obj.value -= money.value
                return self
            raise NegativeValueException
        return self

    def check_currency(self, other: Currency):
        for money in self.currencies:
            if money.currency == other:
                return money
        raise NotComparisonException

    @staticmethod
    def set_start_currencies(money: Money):
        if money.currency == rub:
            return [money, Money(value=0, currency=usd)]
        return [Money(value=0, currency=rub), money]

    def check_balance(self):
        accounts_with_balance = []
        for account in self.currencies:
            if account.value > 0:
                accounts_with_balance.append(account)
        return accounts_with_balance
