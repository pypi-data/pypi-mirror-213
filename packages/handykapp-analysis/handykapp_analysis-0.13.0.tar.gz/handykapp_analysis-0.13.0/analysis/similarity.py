from pendulum import DateTime
from horsetalk import RaceDistance, Surface  # type: ignore


class Similarity:
    @staticmethod
    def date(date_1: DateTime, date_2: DateTime) -> float:
        """
        Returns a similarity score between 0 and 1, where 1 is identical dates and 0 is dates 1000 days apart.

        Args:
            date_1: The first date.
            date_2: The second date.

        Returns:
            A similarity score between 0 and 1.
        """
        days_delta = abs((date_1 - date_2).days)
        # similarity reaches 0 after 1000 days
        return max(1 - ((days_delta / 10) ** 0.5) / 10, 0)

    @staticmethod
    def race_distance(distance_1: RaceDistance, distance_2: RaceDistance) -> float:
        """
        Returns a similarity score between 0 and 1, where 1 is identical distances and 0 is the larger distance
        being > 1.5 times the smaller distance.

        Args:
            distance_1: The first distance.
            distance_2: The second distance.

        Returns:
            A similarity score between 0 and 1.
        """
        diff = abs(distance_1.furlong - distance_2.furlong)
        lower = min(distance_1.furlong, distance_2.furlong)
        proportion = float(diff / lower)
        similarity = 1 - ((proportion / 1.5) ** 0.5)
        return max(similarity, 0)

    @staticmethod
    def surface(surface_1: Surface, surface_2: Surface) -> float:
        """
        Returns a similarity score between 0 and 1, where 1 is identical surface, 0.9 are different all-weather surfaces
        and 0.7 are different fundamental surfaces.

        Args:
            surface_1: The first surface.
            surface_2: The second surface.

        Returns:
            A similarity score between 0 and 1.
        """
        return (
            1
            if surface_1 == surface_2
            else 0.9
            if all(
                x in [Surface.FIBRESAND, Surface.POLYTRACK, Surface.TAPETA]
                for x in [surface_1, surface_2]
            )
            else 0.7
        )
