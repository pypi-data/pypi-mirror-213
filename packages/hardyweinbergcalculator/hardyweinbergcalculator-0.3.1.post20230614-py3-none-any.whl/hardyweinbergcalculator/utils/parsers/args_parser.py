import argparse
import sys
from typing import List

import numpy as np
from ...genetics.gene import Gene
from ...genetics.allele import Allele
from ...config import get_logger

log = get_logger(__name__)


# --------------------------------------------------------------------------- #
def parse_args():
    parser = argparse.ArgumentParser(
        prog=sys.argv[0].split("/")[-1],
        description="""
        \nHardy-Weinberg Equilibrium Calculator.
        \nCalculates the expected genotype frequencies based on the allele frequencies of a population 
        in Hardy-Weinberg equilibrium. 
      
        \nSee: https://en.wikipedia.org/wiki/Hardy%E2%80%93Weinberg_principle""",
        usage="hwc [-h] [--version] [--verbose] [--debug] [--samples SAMPLES] [--p P] [--q Q] [--tpop TPOP] ["
        "--ppop PPOP] [--qpop QPOP] [--pq2pop PQ2POP] [--genes GENES [GENES ...]] [--json JSON [JSON ...]]",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog="""Example: python3 -m hwc --ppop 10 --qpop 10 --pq2pop 200 --verbose""",
        add_help=True,
        allow_abbrev=True,
        exit_on_error=True,
    )
    parser.add_argument(
        "--version", action="version", version="HardyWeinberg Calculator 0.1"
    )
    parser.add_argument(
        "--verbose", action="store_true", default=False, help="Enable verbose logging."
    )
    parser.add_argument(
        "--debug", action="store_true", default=False, help="Enable debug logging."
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=None,
        help="Number of samples to generate, if using random data generator.",
    )
    parser.add_argument(
        "--p", type=float, default=None, help="Frequency of dominant allele."
    )
    parser.add_argument(
        "--q", type=float, default=None, help="Frequency of recessive allele."
    )
    parser.add_argument("--tpop", type=float, default=None, help="Total population.")
    parser.add_argument(
        "--ppop",
        type=float,
        default=None,
        help="Original population of dominant allele.",
    )
    parser.add_argument(
        "--qpop",
        type=float,
        default=None,
        help="Original population of recessive allele.",
    )
    parser.add_argument(
        "--pq2pop",
        type=float,
        default=None,
        help="Original population of heterozygous allele.",
    )
    return parser


# --------------------------------------------------------------------------- #
def parse_genes_from_cli(genes: List = None):
    if genes is None:
        log.error(f"\nGenes: {genes} is not a valid gene.")
        return None
    gene_list = np.array([0] * 1, dtype=Gene, ndmin=1, copy=False)
    log.info(f"\nShape of genes: {np.shape(genes)}")
    if isinstance(genes, list):
        for gene in genes:
            log.debug(f"\nGene: {gene}")
            if isinstance(gene, dict):
                np.append(
                    gene_list,
                    Gene(
                        mother=Allele(
                            gene.get("mother").get("Alleles")[0].get("symbols")
                        ),
                        father=Allele(
                            gene.get("father").get("Alleles")[0].get("symbols")
                        ),
                        description=gene.get("description"),
                    ),
                )
            elif isinstance(gene, Gene):
                np.append(gene_list, gene)
            else:
                log.error(f"\nGene: {gene} is not a valid gene.")
    elif isinstance(genes, Gene):
        np.append(gene_list, genes)
    else:
        raise ValueError(
            f"\nGenes: {genes} is not a valid gene.",
            f"\nParsed Gene List size: {len(gene_list)}",
        )
    return gene_list


# --------------------------------------------------------------------------- #
