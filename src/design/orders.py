import abc
from dataclasses import dataclass
from typing import TypeAlias


@dataclass
class Order:
    """There is no need to describe anything here."""

class Discount(abc.ABC):
    def __init__(self, order: Order):
        self.order = order

    @abc.abstractmethod
    def discount(self) -> float:
        pass

DiscountList: TypeAlias = list[Discount]

class FixedDiscount(Discount):
    def discount(self) -> float: #Возвращает фиксированную сумму скидки
        pass

class LoyaltyDiscount(Discount): # принимает сумму заказа из класса order
    def discount(self) -> float: # считает процент от заказа и возвращает сумму скидки
        pass

class PercentageOfOrderDiscount(Discount):# принимает сумму заказа из класса order
    def discount(self) -> float: # считает процент от заказа и возвращает сумму скидки
        pass


class DiscountGetter:
    def __init__(self, order: Order, discount_list: DiscountList):
        self.order = order
        self.discount_list = discount_list


    @property
    def get_discount(self) -> float: #Возвращает сумму всех скидок
        sum_of_discounts = 0
        for discount in self.discount_list:
            sum_of_discounts += discount.discount()
        return float(sum_of_discounts)
