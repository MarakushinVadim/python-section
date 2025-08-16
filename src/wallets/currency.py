from dataclasses import dataclass


@dataclass(slots=True)
class Rub:
    name: str = 'rub'


@dataclass(slots=True)
class USD:
    name: str = 'usd'


@dataclass(slots=True)
class Currency:
    currency: Rub | USD


rub = Rub()
usd = USD()
