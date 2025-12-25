from math import hypot
from typing import Optional


class Location:

    def __init__(self, x_coord: int, y_coord: int) -> None:
        self._x = x_coord
        self._y = y_coord

    def get_distance_to_location(self, other: Location) -> float:
        if not isinstance(other, Location):
            raise TypeError(f"Cannot calculate distance to {type(other)}")
        return hypot(other._x - self._x, other._y - self._y)

    def determine_closes_location(
            self,
            locations: list[Location]
    ) -> Optional[Location]:
        others = [loc for loc in locations if loc is not self]

        if not others:
            return None

        return min(others, key=lambda loc: self.get_distance_to_location(loc))
