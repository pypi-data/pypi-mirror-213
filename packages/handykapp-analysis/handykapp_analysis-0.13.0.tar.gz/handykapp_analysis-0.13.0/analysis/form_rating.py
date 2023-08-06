from decimal import Decimal
from typing import Self
from measurement.measures import Weight  # type: ignore
from horsetalk import Horselength  # type: ignore


class FormRating(Decimal):
    """
    A Decimal subclass that represents the form rating for one horse in one race.
    """

    solidity: Decimal

    def __new__(
        cls, value: int | float | Decimal | str, *, solidity: Decimal = Decimal(1)
    ) -> Self:
        """
        Creates a new FormRating instance.

        Args:
            value: The value to create the FormRating instance from.
            solidity: The solidity (i.e. reliability) of the rating on a scale from 0 to 1.

        Returns:
            A new FormRating instance.
        """
        instance = super().__new__(cls, value)
        instance.solidity = solidity
        return instance

    def adjust(self, delta: int | float | Decimal | str) -> Self:
        """
        Returns a new FormRating instance with the given delta added to the value.

        Args:
            delta: The delta to add to the value.

        Returns:
            A new FormRating instance.
        """
        return self.__class__(self + Decimal(delta), solidity=self.solidity)

    @classmethod
    def calculate(
        cls,
        *,
        beaten_distance: Horselength,
        weight_per_length: Weight,
        weight_differential: Weight = Weight(lb=0),
        weight_for_age: Weight = Weight(lb=0),
        baseline: Decimal = Decimal(0),
    ) -> Self:
        """
        Calculates the FormRating for a horse from its beaten distance and a given weight per length

        Args:
            beaten_distance: The beaten distance to use in the calculation.
            weight_per_length: The weight per length to use in the calculation.
            weight_differential: The weight adjustment, e.g due to weight carried/jockey allowance, to use in the calculation.
            weight_for_age: The weight for age allowance to use in the calculation.
            baseline: The baseline rating to use in the calculation.

        Returns:
            The FormRating for the horse.
        """
        raw_delta = beaten_distance * round(Decimal(weight_per_length.lb), 2)
        weight_adjustment = round(Decimal((weight_differential + weight_for_age).lb), 2)
        value = baseline - raw_delta + weight_adjustment
        solidity = 1 - (beaten_distance.sqrt()) / 10
        return cls(value, solidity=solidity)
