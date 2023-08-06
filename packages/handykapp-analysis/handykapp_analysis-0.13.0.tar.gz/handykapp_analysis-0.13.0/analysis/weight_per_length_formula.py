from horsetalk import RaceDistance  # type: ignore
from measurement.measures import Weight  # type: ignore
from pendulum.duration import Duration
from typing import Any, Callable, Type


class WeightPerLengthFormula:
    def __init__(
        self,
        input_type: Type[RaceDistance | Duration],
        formula: Callable[[Any], Weight],
        weight_unit: str = "lb",
    ):
        self.input_type = input_type
        self.unit = weight_unit
        self._formula = formula

    def __call__(self, value: RaceDistance | Duration) -> Weight:
        if not isinstance(value, self.input_type):
            raise TypeError(f"Expected {self.input_type}, got {type(value)}")
        return Weight(**{self.unit: self._formula(value)})
