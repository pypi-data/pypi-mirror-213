import json
from typing import List

import numpy as np
from ..utils.generators.char_generator import random_chars


# --------------------------------------------------------------------------- #
class Allele:
    """Allele class:
    defines a single allele object.

    :param symbols: List - the unicode or ascii symbols for the allele. e.g. 'A' or 'a'
    """

    _symbols: List
    _traits: List
    _matrix: np.array

    def __init__(self, symbols: List = random_chars().__next__()):
        self._symbols = symbols
        self._traits = []
        for symbol in self._symbols:
            if symbol.isupper():
                self._traits.append([f"{symbol}", "dominant"])
            elif symbol.islower():
                self._traits.append([f"{symbol}", "recessive"])
        self._matrix = np.array(
            object=[
                {"symbols": self._symbols},
                {"traits": self._traits},
            ],
            dtype=object,
        )

    @property
    def symbols(self):
        return self._symbols

    @property
    def traits(self):
        return self._traits

    def __dict__(self):
        return {
            "Alleles": self._matrix.tolist(),
        }

    def __iter__(self):
        yield self

    def __next__(self):
        return self.__dict__()

    def __repr__(self):
        return self.__dict__()

    def to_json(self):
        return json.dumps(
            self.__dict__(), default=lambda o: o.__dict__(), indent=4, sort_keys=True
        )

    def __str__(self):
        return self.__dict__()


# --------------------------------------------------------------------------- #
