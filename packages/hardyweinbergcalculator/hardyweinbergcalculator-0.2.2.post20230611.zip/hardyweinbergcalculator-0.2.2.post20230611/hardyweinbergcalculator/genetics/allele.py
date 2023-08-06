import json
from ..utils.generators.char_generator import random_chars


# --------------------------------------------------------------------------- #
class Allele:
    """Allele class:
    defines a single allele object.

    - symbol: str - the unicode or ascii symbol for the allele. e.g. A or a
    """
    _symbol: str
    _trait: str

    def __init__(self, symbol: str = random_chars().send(None)):
        self._symbol = symbol
        if self._symbol.isupper():
            self._trait = "dominant"
        elif self._symbol.islower():
            self._trait = "recessive"

    @property
    def symbol(self):
        return self._symbol

    @property
    def trait(self):
        return self._trait

    def __dict__(self):
        return dict({"symbol": self._symbol, "trait": self._trait})

    def __iter__(self):
        yield self

    def __next__(self):
        return self.__dict__()

    def __repr__(self):
        return self.__dict__()

    def to_json(self):
        return json.dumps(self.__dict__(), default=lambda o: o.__dict__, indent=4, sort_keys=True)

    def __str__(self):
        return self.__dict__()

# --------------------------------------------------------------------------- #
