from typing import Self
from horsetalk import RaceDistance, Surface  # type: ignore
from pendulum import DateTime
from .going import Going
from .similarity import Similarity


class RaceConditions:
    def __init__(
        self, date: DateTime, distance: RaceDistance, going: Going, surface: Surface
    ):
        self.date = date
        self.distance = distance
        self.going = going
        self.surface = surface

    def similarity_to(self, other: Self) -> float:
        return (
            Similarity.date(self.date, other.date)
            * Similarity.race_distance(self.distance, other.distance)
            * self.going.similarity_to(other.going)
            * Similarity.surface(self.surface, other.surface)
        )
