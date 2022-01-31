"""
Supporting modules that will only be used in support of answering
Day 14's question.
https://adventofcode.com/2021/day/14
"""

import collections


class FrozenDict(collections.abc.Mapping):
    """
    A barebones hashable dictionary class.  This is not complete
    in that it is not actually immutable, but it gives us the 
    functionality required to use it to answer this question.
    """

    def __init__(self, *args, **kwargs):
        self._d = dict(*args, **kwargs)
        self._hash = None

    def __iter__(self):
        return iter(self._d)

    def __len__(self):
        return len(self._d)

    def __getitem__(self, key):
        return self._d[key]

    def __hash__(self):
        if self._hash is None:
            hash_ = 0
            for pair in self.items():
                hash_ ^= hash(pair)
            self._hash = hash_
        return self._hash