from dataclasses import dataclass, field
from itertools import batched
from typing import Iterable, TypeAlias

SomeRemoteData: TypeAlias = int


@dataclass
class Query:
    per_page: int = 3
    page: int = 1


@dataclass
class Page:
    per_page: int = 3
    results: Iterable[SomeRemoteData] = field(default_factory=list)
    next: int | None = None


def request(query: Query) -> Page:
    data = [i for i in range(0, 10)]
    chunks = list(batched(data, query.per_page))
    return Page(
        per_page=query.per_page,
        results=chunks[query.page - 1],
        next=query.page + 1 if query.page < len(chunks) else None,
    )


class RetrieveRemoteData:

    def __init__(self, per_page: int = 3):
        self.per_page = per_page

    def __iter__(self) -> Iterable[SomeRemoteData]:
        return self.take_generator()

    def take_generator(self) -> Iterable[SomeRemoteData]:

        counter = 1
        x = True
        while x:
            page_obj = request(Query(per_page=self.per_page, page=counter))
            for obj in page_obj.results:
                yield obj

            if page_obj.next is None:
                x = False
            counter += 1


class Fibo:

    def __init__(self, n: int, start=0):
        self.index = 0
        self.end = n
        self.start = start
        self.last = [0, 1]

    def __iter__(self):
        return self

    def __next__(self) -> int:
        if self.index == self.end:
            raise StopIteration
        self.index += 1

        if self.index == 1:
            return 0

        elif self.index == 2:
            return 1

        result = sum(self.last)
        self.last = [self.last[1], result]

        return result
