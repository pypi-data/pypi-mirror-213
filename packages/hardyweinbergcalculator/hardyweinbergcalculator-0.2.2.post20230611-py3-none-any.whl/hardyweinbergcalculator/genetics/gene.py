import json

from .allele import Allele


# --------------------------------------------------------------------------- #
class Gene:
    """
    A Gene contains pairs of alleles, an early example of a trait encoded by
    a single gene with multiple alleles, in this case two alleles, a diploid.

    A Diploid is the result of the fusion of two gametes (sperm and egg)
    that contain one allele each.  A diploid contains two alleles, one from
    each parent.

    - mother: Allele
    - father: Allele
    """
    mother: Allele = None  # first allele
    father: Allele = None  # second allele
    metadata: dict = dict()
    description: str = "TESTING 1, 2, 3..."

    def __init__(self, mother: Allele(), father: Allele(), description: str = "TESTING 1, 2, 3..."):
        self.mother = mother
        self.father = father
        self.description = description
        self.metadata = dict()
        self.metadata["traits"] = []
        if str(self.mother.trait) == "dominant" == str(self.father.trait):
            self.metadata["dominant_trait"] = True
            self.metadata["zygous"] = "homozgous"
            self.metadata["homocount"] = 1
            self.metadata["traits"].extend(
                [{self.mother.symbol: self.mother.trait},
                 {self.father.symbol: self.father.trait}]
            )
        elif str(self.mother.trait) == "recessive" == str(self.father.trait):
            self.metadata["dominant_trait"] = False
            self.metadata["zygous"] = "homozgous"
            self.metadata["homocount"] = 1
            self.metadata["traits"].extend(
                [{self.mother.symbol: self.mother.trait},
                 {self.father.symbol: self.father.trait}]
            )
        else:
            self.metadata["dominant_trait"] = True
            self.metadata["zygous"] = "heterozygous"
            self.metadata["hetercount"] = 1
            self.metadata["traits"].extend(
                [{self.mother.symbol: self.mother.trait},
                 {self.father.symbol: self.father.trait}]
            )

    def __dict__(self):
        # print out all class attributes in a dictionary
        return {
            "gene": f"{self.mother.symbol}:{self.father.symbol}",
            "mother": self.mother.__dict__(),
            "father": self.father.__dict__(),
            "metadata": self.metadata,
            "description": self.description}

    def __iter__(self):
        yield self

    def __next__(self):
        return self.__dict__()

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        return json.dumps(self.__dict__(), default=lambda o: o.__dict__, indent=4, sort_keys=True)

    def __str__(self):
        return str(self.__dict__())


