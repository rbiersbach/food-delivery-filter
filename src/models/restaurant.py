from datetime import datetime, time
from decimal import Decimal

import attr
from typing import Set, List, Tuple

from src.models.category import Category


@attr.dataclass
class Restaurant(object):
    name: str
    categories: Set[Category]
    opening_times: List[Tuple[time, time]]
    rating_stars: float
    rating_numbers: int
    min_order_value: Decimal
    url: str

    @property
    def open(self) -> bool:
        now = datetime.now()
        opening_time_today = self.opening_times[now.weekday()]
        return opening_time_today[0] < now.time() < opening_time_today[1]

    @property
    def only_italien(self) -> bool:
        return all([
            Category.PASTA in self.categories,
            Category.ITALIENISCHE_PIZZA in self.categories or Category.AMERIKANISCHE_PIZZA in self.categories,
            not self.asien,
            not self.turkish,
            not self.mexican,
        ])

    @property
    def asien(self) -> bool:
        asien_categories = [
            Category.ASIATISCH,
            Category.CHINESISCH,
            Category.VIETNAMESISCH,
            Category.THAILAENDISCH,
            Category.CURRY,
            Category.INDISCH,
            Category.INDONESISCH,
            Category.JAPANISCH,
            Category.KOREANISCH
        ]
        return any([category in asien_categories for category in self.categories])

    @property
    def turkish(self) -> bool:
        turkish_categories = [
            Category.TUERKISCH,
            Category.TUERKISCHE_PIZZA,
            Category.GYROS,
            Category.DOENER,
        ]
        return any([category in turkish_categories for category in self.categories])

    @property
    def mexican(self) -> bool:
        mexican_categories = [
            Category.MEXIKANISCH,
        ]
        return any([category in mexican_categories for category in self.categories])

    @property
    def burger(self) -> bool:
        burger_categories = [
            Category.BURGER,
        ]
        return any([category in burger_categories for category in self.categories])

    def __str__(self):
        return f'{self.name}({self.url})'
