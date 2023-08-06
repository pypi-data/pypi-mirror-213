from horsetalk import RaceDistance  # type: ignore
from typing import List, Self
import pendulum
from pendulum.datetime import DateTime
from pendulum.duration import Duration
from analysis.rateable_run import RateableRun


class RateableResult:
    def __init__(
        self,
        datetime: DateTime,
        distance: RaceDistance,
        win_time: Duration,
        runs: List[RateableRun],
    ):
        self.datetime = datetime
        self.distance = distance
        self.win_time = win_time
        self.runs = runs

    @classmethod
    def parse(
        cls,
        datetime: DateTime,
        distance: str,
        win_time: str,
        runs: List[List[str | DateTime | None]],
    ) -> Self:
        mins, secs = win_time.split(":")
        return cls(
            datetime=datetime,
            distance=RaceDistance(distance),
            win_time=pendulum.duration(minutes=int(mins), seconds=float(secs)),
            runs=[RateableRun.parse(*run) for run in runs],  # type: ignore
        )
