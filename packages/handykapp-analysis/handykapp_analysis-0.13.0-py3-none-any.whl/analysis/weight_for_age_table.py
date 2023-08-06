from decimal import Decimal
from analysis.weight_for_age_converter import WeightForAgeConverter


class WeightForAgeTable(WeightForAgeConverter):
    """
    A class that represents a weight for age table, such as may be found issued by a horseracing authority or form analyst.

    Inherits from WeightForAgeConverter and adds the ability to lookup weights from a table based on age, distance, and date.
    """

    def _process(self, key: range, val: int, age_in_days: int) -> Decimal:
        return Decimal(str(val))
