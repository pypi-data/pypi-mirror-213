import json
from itertools import product
import numpy as np
from ..genetics import Allele


# --------------------------------------------------------------------------- #
class Gene:
    """
    A Gene contains pairs of alleles, an early example of a traits encoded by
    a single gene with multiple alleles, in this case two alleles, a diploid.

    A Diploid is the result of the fusion of two gametes (sperm and egg)
    that contain one allele each.  A diploid contains two alleles, one from
    each parent.

    - mother: Allele - first allele
    - father: Allele - second allele
    - description: str - description of the gene
    """

    mother: Allele = None  # first allele
    father: Allele = None  # second allele
    description: str = None
    matrix: np.array = None
    metadata: dict = dict()

    def __init__(self, mother: Allele, father: Allele, description: str = None):
        self.mother = mother
        self.father = father
        self.description = description
        self.matrix = np.array(
            list(product(self.mother.symbols, self.father.symbols)), dtype=object
        )
        self.metadata = dict()
        self.metadata = self._get_metadata()

    def _get_metadata(self):
        # get metadata about the gene's alleles
        metadata = dict()
        metadata["dominant_traits"] = 0
        metadata["recessive_traits"] = 0
        metadata["zygous"] = []
        metadata["homocount"] = 0
        metadata["hetercount"] = 0
        metadata["homozygous"] = []
        metadata["heterozygous"] = []
        metadata["traits"] = []
        cnt = len(self.matrix)
        for allele in self.matrix.tolist():
            if str(allele[0]).isupper() and str(allele[1]).isupper():
                metadata["dominant_traits"] += 1
                metadata["zygous"].append(["homozgous", allele])
                metadata["homocount"] += 1
                metadata["homozygous"].append(allele)
                metadata["traits"].append(["dominant", allele])
            elif str(allele[0]).islower() and str(allele[1]).islower():
                metadata["recessive_traits"] += 1
                metadata["zygous"].append(["homozgous", allele])
                metadata["homocount"] += 1
                metadata["homozygous"].append(allele)
                metadata["traits"].append(["recessive", allele])
            else:
                metadata["dominant_traits"] += 1
                metadata["zygous"].append(["heterozygous", allele])
                metadata["hetercount"] += 1
                metadata["heterozygous"].append(allele)
                metadata["traits"].append(["dominant", allele])

        return metadata

    def __dict__(self):
        # print out all class attributes in a dictionary
        return {
            "mother": self.mother.__dict__(),
            "father": self.father.__dict__(),
            "description": self.description,
            "gene_mapping": self.matrix.tolist(),
            "metadata": self.metadata,
        }

    def __iter__(self):
        yield self

    def __next__(self):
        return self.__dict__()

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        return json.dumps(
            self.__dict__(), default=lambda o: o.__dict__, indent=4, sort_keys=True
        )

    def __str__(self):
        return str(self.__dict__())
