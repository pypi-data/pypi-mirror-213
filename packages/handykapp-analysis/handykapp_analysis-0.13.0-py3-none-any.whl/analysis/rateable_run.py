from decimal import Decimal
from typing import Self
from pendulum.datetime import DateTime
from measurement.measures import Weight  # type: ignore
from horsetalk import HorseAge, Horselength  # type: ignore


class RateableRun:
    def __init__(
        self,
        beaten_distance: Horselength,
        weight_carried: Weight,
        weight_allowance: Weight,
        age: HorseAge,
    ):
        self.beaten_distance = beaten_distance
        self.weight_carried = weight_carried
        self.weight_allowance = weight_allowance
        self.age = age

    @classmethod
    def parse(
        cls,
        beaten_distance: str,
        weight_carried: str,
        weight_allowance: str,
        age: str,
        date: DateTime | None = None,
    ) -> Self:
        stones, lbs = weight_carried.split("-")
        horse_age = (
            HorseAge(int(age), context_date=date) if date else HorseAge(int(age))
        )
        return cls(
            beaten_distance=Horselength(beaten_distance),
            weight_carried=Weight(stone=Decimal(stones)) + Weight(lb=Decimal(lbs)),
            weight_allowance=Weight(lb=Decimal(weight_allowance)),
            age=horse_age,
        )
