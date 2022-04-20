"""
Advent of Code 2021 - Day 18: Snailfish
https://adventofcode.com/2021/day/18
https://github.com/jshiles/adventofcode_2021

Contains the additional modules and logic.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List
import copy
import re


@dataclass(frozen=True, eq=True, order=True)
class Element:
    """Sailfish numbers are made of pairs of elements at a depth."""

    value: int
    depth: int


@dataclass(frozen=True, eq=True, order=True)
class SailFishNumber:
    """
    Snailfish numbers aren't like regular numbers. Instead, every
    snailfish number is a pair - an ordered list of two elements.
    Each element of the pair can be either a regular number or
    another pair.

    Class maintains the sailfish number as an flat list of Elements,
    which are a value and depth.
    """

    elements: List[Element]

    def add(self, b: SailFishNumber) -> SailFishNumber:
        """
        Adds SailFishNumber b to this object and returns a new object
        containing the two numbers added reduced.
        """

        def reducer(s: SailFishNumber) -> SailFishNumber:
            # attempt to explode; if mutated recurse else try split
            exploded_sfn = s.explode()
            if not s == exploded_sfn:
                return reducer(exploded_sfn)

            # attempt to split; if mutated recurse else return s.
            split_sfn = s.split()
            if not s == split_sfn:
                return reducer(split_sfn)

            # no change so must be fully reduced.
            return s

        sfn = SailFishNumber(
            [Element(e.value, e.depth + 1) for e in self.elements + b.elements]
        )
        return reducer(sfn)

    def __add__(self, x: SailFishNumber) -> SailFishNumber:
        """
        Wrapper for function add(self, b: SailFishNumber) -> SailFishNumber
        """
        return self.add(x)

    def split(self) -> SailFishNumber:
        x = copy.deepcopy(self.elements)
        for i, e in enumerate(x):
            if e.value < 10:
                continue
            down = e.value // 2
            up = e.value - down
            return SailFishNumber(
                x[:i]
                + [Element(down, e.depth + 1), Element(up, e.depth + 1)]
                + x[i + 1 :]
            )
        return self

    def explode(self) -> SailFishNumber:
        x = copy.deepcopy(self.elements)
        for i, (e1, e2) in enumerate(zip(x, x[1:])):

            if e1.depth < 5 or e1.depth != e2.depth:
                continue
            if i > 0:
                x[i - 1] = Element(x[i - 1].value + e1.value, x[i - 1].depth)

            if i < len(x) - 2:
                x[i + 2] = Element(x[i + 2].value + e2.value, x[i + 2].depth)

            return SailFishNumber(
                x[:i] + [Element(0, e1.depth - 1)] + x[i + 2 :]
            )
        return self

    def magnitude(self) -> int:
        """Recursively compute magnitude from bottom up."""
        x = copy.deepcopy(self.elements)
        while len(x) > 1:
            for i, (e1, e2) in enumerate(zip(x, x[1:])):
                (value1, depth1) = (
                    (e1.value, e1.depth) if isinstance(e1, Element) else e1
                )
                (value2, depth2) = (
                    (e2.value, e2.depth) if isinstance(e2, Element) else e2
                )
                if depth1 != depth2:
                    continue
                val = value1 * 3 + value2 * 2
                x = x[:i] + [(val, depth1 - 1)] + x[i + 2 :]
                break
        return x[0][0]


def str2sailfishnumber(s: str) -> SailFishNumber:
    """Turn a string into a sailfish number"""
    elements, depth = [], 0
    for c in re.findall(r"\d+|\[|\]", s):
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
        elif c.isdigit():
            elements.append(Element(int(c), depth))
    return SailFishNumber(elements)
