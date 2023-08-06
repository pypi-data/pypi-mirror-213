from __future__ import annotations

from datetime import date
from typing import Optional

from attrs import Factory, define
from pydash import py_


@define
class Food:
    name: str
    amount: float = 100.0
    countable: bool = False
    weight: float = 100.0
    ingredients: list[Food] = Factory(list)

    @property
    def title(self):
        return self.name

    def of_amount(self, amount: float):
        ratio = 0 if self.amount == 0 else amount / self.amount
        return self.of_ratio(ratio)

    def of_ratio(self, ratio: float):
        new_amount = ratio * self.amount
        new_weight = ratio * self.weight
        new_ingredients = py_.map(self.ingredients, lambda i: i.of_ratio(ratio))
        return Food(
            name=self.name,
            amount=new_amount,
            countable=self.countable,
            weight=new_weight,
            ingredients=new_ingredients,
        )

    def amount_of(self, ingredient_name: str) -> float:
        if self.name == ingredient_name:
            return self.amount
        else:
            return py_.sum_by(self.ingredients, lambda i: i.amount_of(ingredient_name))


@define
class Meal(Food):
    pass


@define
class Day:
    dt: date
    meals: list[Meal] = Factory(list)

    @property
    def dts(self):
        return self.dt.strftime("%Y-%m-%d")

    @property
    def title(self):
        return self.dts

    def meal_by_name(self, meal_name: str) -> Optional[Meal]:
        return py_.find(self.meals, lambda m: m.name == meal_name)

    def amount_of(self, ingredient_name: str) -> float:
        return py_.sum_by(self.meals, lambda i: i.amount_of(ingredient_name))


@define
class Journal:
    days: list[Day]

    def closest_day(self, dt: date) -> Day:
        day = py_.find_last(self.days, lambda d: d.dt <= dt)
        if day is None:
            raise ValueError(f"Journal entry for day '{dt}' wasn't found")

        return day


@define
class Registry:
    foods: dict[str, Food] = Factory(dict)
