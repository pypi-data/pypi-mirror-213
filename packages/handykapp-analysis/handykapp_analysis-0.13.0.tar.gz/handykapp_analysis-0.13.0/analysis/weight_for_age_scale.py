from decimal import Decimal
from analysis.weight_for_age_converter import WeightForAgeConverter


class WeightForAgeScale(WeightForAgeConverter):
    """
    A class that represents a weight for age scale, which is a dictionary of dictionaries of Weight objects.

    Inherits from WeightForAgeConverter and adds the ability to lookup weights from a table based on age, distance, and date.
    """

    def _process(self, key: range, val: int, age_in_days: int) -> Decimal:
        proportion = (key[-1] - age_in_days) / len(key)
        allowance = proportion * val
        return Decimal(str(allowance))
