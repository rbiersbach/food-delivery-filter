import time
from datetime import datetime
from decimal import Decimal
from typing import Set, List, Tuple

from src.examples.koeln_belgisches_viertel import restaurants_unstructured
from src.models.restaurant import Restaurant
from src.models.category import Category


def create_restaurant_from_unstructured(unstructured_restaurant: list) -> Restaurant:
    # category processing
    unstructured_categories = unstructured_restaurant[30]['categories']
    unstructured_categories = unstructured_categories.split(',')
    categories: Set[Category] = set()
    for category in unstructured_categories:
        for category_enum in Category:
            if category_enum.value == category.strip():
                categories.add(category_enum)

    # opening times processing
    unstructured_opening_times = unstructured_restaurant[20]
    opening_times: List[Tuple[time, time]] = []
    shifted_indexes = [1, 2, 3, 4, 5, 6, 0]
    for index in shifted_indexes:
        start_time_str: str = unstructured_opening_times[index][0]['starttime']
        start_time: time = datetime.strptime(start_time_str, "%H:%M:%S").time()
        end_time_str: str = unstructured_opening_times[index][0]['endtime']
        end_time: time = datetime.strptime(end_time_str, "%H:%M:%S").time()
        opening_times.append((start_time, end_time))

    # rating processing
    unstructured_rating = unstructured_restaurant[29]
    rating_stars: float = float(unstructured_rating[0]) / 2.0
    rating_numbers = unstructured_rating[1]

    # min order value
    unstructured_min_order_value = unstructured_restaurant[10]
    min_order_value = Decimal(unstructured_min_order_value)

    # url
    relative_url = unstructured_restaurant[30]["url"].replace("\\", '')
    url = f'https://www.lieferando.de{relative_url}'
    return Restaurant(
        name=unstructured_restaurant[4],
        categories=categories,
        opening_times=opening_times,
        rating_stars=rating_stars,
        rating_numbers=rating_numbers,
        min_order_value=min_order_value,
        url=url
    )


i = 0
for information in restaurants_unstructured[0]:
    print(f'{i}|{information}')
    i = i + 1

restaurants: List[Restaurant] = []
for unstructured_restaurant in restaurants_unstructured:
    restaurant: Restaurant = create_restaurant_from_unstructured(unstructured_restaurant)
    restaurants.append(restaurant)

personal_blacklist = [
    "Pinocchio Pizzeria",
    "Stückwerk Pizzakultur",
    "Smiley's Pizza Profis",
    "Borsalino",
    "Pizza Cento - Steinofen Pizzeria",
    "Pizza Ufo"
]

only_italien_food_restaurants = [print(restaurant) for restaurant in restaurants if all([
    restaurant.only_italien,
    restaurant.open,
    restaurant.rating_stars >= 4.5,
    restaurant.rating_numbers > 50,
    restaurant.min_order_value <= Decimal(20),
    restaurant.name not in personal_blacklist
])]
