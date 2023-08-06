from horsetalk import RaceDistance  # type: ignore
from measurement.measures import Weight  # type: ignore
from pendulum.duration import Duration
from analysis.form_rating import FormRating
from analysis.rateable_result import RateableResult
from analysis.rateable_run import RateableRun
from analysis.weight_for_age_converter import WeightForAgeConverter
from analysis.weight_for_age_scale import WeightForAgeScale
from analysis.weight_per_length_formula import WeightPerLengthFormula


class FormRater:
    """
    A class for calculating form ratings for a race using cumulative beaten distances and selected other variables.

    Attributes:
        _weight_per_length_formula: The formula to calculate the weight equivalent of being beaten by a length.
        _weight_for_age_converter: The converter to adjust weights for horse age.

    Methods:
        rate(): Calculate the form ratings for each horse in a race.
    """

    def __init__(
        self,
        weight_per_length_formula: WeightPerLengthFormula = WeightPerLengthFormula(
            RaceDistance, lambda x: 3
        ),
        weight_for_age_converter: WeightForAgeConverter = WeightForAgeScale(),
    ):
        """
        Initialize a new FormRater instance.

        Args:
            **kwargs: Optional keyword arguments:
                weight_per_length_formula: The formula for converting distance to weight per length. Default returns Weight(lb=3)
                weight_for_age_converter: The converter for calculating weight for age. Default returns Weight(lb=0)
        """
        self._weight_per_length_formula = weight_per_length_formula
        self._weight_for_age_converter = weight_for_age_converter

    def rate(self, result: RateableResult) -> tuple[FormRating, ...]:
        """
        Calculate the form ratings for each horse in the race.

        Args:
            result: The result to be rated.

        Returns:
            Tuple[FormRating, ...]: A tuple of FormRating instances representing the ratings for each horse in the race.
        """
        base_weight = self._weight_differential(result.runs[0])
        return tuple(
            FormRating.calculate(
                beaten_distance=run.beaten_distance,
                weight_per_length=self.weight_per_length(result),
                weight_differential=self._weight_differential(run, base_weight),
                weight_for_age=self._weight_for_age_converter.lookup(
                    result.distance, run.age
                ),
            )
            for run in result.runs
        )

    def weight_per_length(self, result: RateableResult) -> Weight:
        """
        Calculate the weight equivalent of being beaten by a length.

        Args:
            result: The result to be rated.

        Returns:
            Weight: The weight equivalent of being beaten by a length.
        """
        input_type = self._weight_per_length_formula.input_type
        wpl_input: RaceDistance | Duration = (
            result.distance if input_type == RaceDistance else result.win_time
        )
        return self._weight_per_length_formula(wpl_input)

    def _weight_differential(
        self, run: RateableRun, base_weight: Weight = Weight(lb=0)
    ) -> Weight:
        return run.weight_carried + run.weight_allowance - base_weight
