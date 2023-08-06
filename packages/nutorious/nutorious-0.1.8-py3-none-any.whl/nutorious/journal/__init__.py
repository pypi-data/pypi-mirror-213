from __future__ import annotations

import re
from datetime import date
from datetime import datetime
from pathlib import Path

import cattrs
from attrs import Factory, define
from pydash import py_

from nutorious.config import Config
from nutorious.model import Journal, Day, Food, Meal
from nutorious.utils.commons import load_yaml_data

ItemData = list[str]
DayData = dict[str, ItemData]
Data = dict[date, DayData]

weight_spec_pattern = re.compile(r"^(\d+(?:\.\d+)?)g$")
count_spec_pattern = re.compile(r"^(\d+(?:\.\d+)?)x$")
ingredient_spec_pattern = re.compile(r"^(\d+(?:\.\d+)?) (\S+)$", re.U)


@define
class FoodRegistry:
    foods: dict[str, Food] = Factory(dict)

    def register(self, food: Food):
        self.foods[food.name] = food

    def lookup_or_create(self, name: str):
        if name in self.foods:
            return self.foods.get(name)
        else:
            new_food = Food(name=name, amount=1, countable=True, weight=0)
            self.register(new_food)
            return new_food


def load_journal(config: Config, journal_path: str) -> Journal:
    data = __load_data(journal_path)
    journal = __build_journal(data, meal_names=config.meals)

    return journal


def __load_data(journal_path: str) -> Data:
    journal_config_path = Path(journal_path) / "config.yml"

    data_file_paths = Path(journal_path).glob("**/*.yml")

    data_raw = {}
    for data_file_path in data_file_paths:
        if data_file_path != journal_config_path:
            file_data = load_yaml_data(data_file_path)
            data_raw = data_raw | file_data

    return cattrs.structure(data_raw, Data)


def __build_journal(data: Data, meal_names: list[str]) -> Journal:
    sorted_by_dt = sorted(data.items())

    registry = FoodRegistry()
    days = []
    for dt, entries in sorted_by_dt:
        for name, spec in entries.items():
            registry.register(__build_food(registry, name, spec))

        meals = (
            py_(meal_names)
            .filter(lambda meal_name: meal_name in entries)
            .map(lambda meal_name: __build_meal(registry, meal_name, entries[meal_name]))
            .value()
        )

        days.append(Day(dt, meals))

    return Journal(days)


def __build_food(registry: FoodRegistry, food_name: str, spec: list[str]) -> Food:
    countable = False
    countable_count = 1

    weight = None
    ingredients_weight = 0.0

    ingredients = []
    for spec_entry in spec:
        if spec_entry == "countable":
            countable = True
            continue

        count_match = count_spec_pattern.match(spec_entry)
        if count_match:
            countable = True
            countable_count = float(count_match.group(1))
            continue

        weight_match = weight_spec_pattern.match(spec_entry)
        if weight_match:
            weight = float(weight_match.group(1))
            continue

        ingredient_match = ingredient_spec_pattern.match(spec_entry)
        if not ingredient_match:
            raise ValueError(f"Invalid food specification entry: {spec_entry}")

        ingredient_amount = float(ingredient_match.group(1))
        ingredient_name = ingredient_match.group(2)

        food = registry.lookup_or_create(ingredient_name)
        ingredient = food.of_amount(ingredient_amount)
        ingredients.append(ingredient)
        ingredients_weight += ingredient.weight

    if weight is None:
        weight = ingredients_weight if ingredients_weight > 0 else 100.0

    amount = countable_count if countable else weight

    return Food(
        name=food_name,
        amount=amount,
        countable=countable,
        weight=weight,
        ingredients=ingredients,
    )


def __build_meal(registry: FoodRegistry, meal_name: str, spec: list[str]) -> Meal:
    food = __build_food(registry, meal_name, spec)
    return Meal(
        name=food.name,
        amount=food.amount,
        countable=food.countable,
        weight=food.weight,
        ingredients=food.ingredients,
    )


def __cattrs_date_structure_hook(raw, _) -> date:
    if type(raw) == date:
        return raw
    elif type(raw) == datetime:
        return raw.date()
    elif type(raw) == str:
        return datetime.strptime(raw, "%Y-%m-%d")
    else:
        raise ValueError(f"Can't convert {raw} to date")


cattrs.register_structure_hook(date, __cattrs_date_structure_hook)
