"""Day 22 Modules"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class Cube:
    """A Cube class for containing these Cubes and computing intersections."""

    add: bool
    xmin: int
    xmax: int
    ymin: int
    ymax: int
    zmin: int
    zmax: int

    def intersection(self, c1: Cube) -> Cube:
        """
        Returns the intersetion between this Cube
        and c1 or None if no intersection.
        """
        inter: Cube = Cube(
            not self.add,
            max(self.xmin, c1.xmin),
            min(self.xmax, c1.xmax),
            max(self.ymin, c1.ymin),
            min(self.ymax, c1.ymax),
            max(self.zmin, c1.zmin),
            min(self.zmax, c1.zmax),
        )
        return (
            None
            if inter.xmin > inter.xmax
            or inter.ymin > inter.ymax
            or inter.zmin > inter.zmax
            else inter
        )

    def count_on(self):
        """Returns cores to count in this Cube."""
        return (
            (1 if self.add else -1)
            * (self.xmax - self.xmin + 1)
            * (self.ymax - self.ymin + 1)
            * (self.zmax - self.zmin + 1)
        )

    def in_bounds(self, lower: int = -50, upper: int = 50) -> bool:
        """Returns True if all points are within the bounds"""
        return (
            lower <= self.xmin <= upper
            and lower <= self.xmax <= upper
            and lower <= self.ymin <= upper
            and lower <= self.ymax <= upper
            and lower <= self.zmin <= upper
            and lower <= self.zmax <= upper
        )
