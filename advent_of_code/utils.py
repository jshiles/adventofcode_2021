"""
Simple utilities that could be used by the notebooks across the entire event.
"""
import os


def test_input_location(day: int, filename: str = "test_input.txt") -> str:
    """returns location of test file"""
    return os.path.join(f"data/day_{day}", filename)


def input_location(day: int, filename: str = "input.txt") -> str:
    """returns location of the production file"""
    return os.path.join(f"data/day_{day}", filename)


def hex_to_binary(hex: str) -> str:
    """
    Converts a hexidecimal number to the string reppresentation
    of the binary equivalent.
    """
    return format(int(hex, 16), f"0>{len(hex*4)}b")


def bin_to_dec(binary: str) -> int:
    """convert binary to decimal."""
    return int(binary, 2)
