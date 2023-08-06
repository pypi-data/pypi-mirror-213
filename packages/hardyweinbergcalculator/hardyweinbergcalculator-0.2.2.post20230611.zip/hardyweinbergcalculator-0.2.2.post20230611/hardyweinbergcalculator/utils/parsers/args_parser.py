import argparse
import json
import sys
import numpy as np
from ...genetics.gene import Gene
from ...genetics.allele import Allele
from ...config import get_logger

log = get_logger(__name__)


# --------------------------------------------------------------------------- #
def parse_args():
    parser = argparse.ArgumentParser(
        prog=sys.argv[0].split('/')[-1],
        description="""
        \nHardy-Weinberg Equilibrium Calculator.
        \nCalculates the expected genotype frequencies based on the allele frequencies of a population 
        in Hardy-Weinberg equilibrium. 
      
        \nSee: https://en.wikipedia.org/wiki/Hardy%E2%80%93Weinberg_principle""",
        usage='%(prog)s [-h] [--version] [--verbose] [--debug] [--samples SAMPLES] [--p P] [--q Q] [--tpop TPOP] ['
              '--ppop PPOP] [--qpop QPOP] [--pq2pop PQ2POP] [--genes GENES [GENES ...]]',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog=("""\nExample: python3 -m %(prog)s --ppop 10 --qpop 10 --pq2pop 200 --verbose | """
                """\nExample: python3 -m [package].[module] --samples 1000 --verbose"""),
        add_help=True,
        allow_abbrev=True,
        exit_on_error=True,
    )
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')
    parser.add_argument('--verbose', action='store_true', default=False,
                        help='Enable verbose logging.')
    parser.add_argument('--debug', action='store_true', default=False,
                        help='Enable debug logging.')
    parser.add_argument('--samples', type=int, default=None,

                        help='Number of samples to generate, if using random data generator.')
    parser.add_argument('--p', type=float, default=None,
                        help='Frequency of dominant allele.')
    parser.add_argument('--q', type=float, default=None,
                        help='Frequency of recessive allele.')
    parser.add_argument('--tpop', type=float, default=None,
                        help='Total population.')
    parser.add_argument('--ppop', type=float, default=None,
                        help='Original population of dominant allele.')
    parser.add_argument('--qpop', type=float, default=None,
                        help='Original population of recessive allele.')
    parser.add_argument('--pq2pop', type=float, default=None,
                        help='Original population of heterozygous allele.')
    parser.add_argument('--genes', type=json.loads, nargs='+', default=lambda o: o.__dict__(),
                        help='List of JSON[Genes] to calculate. Note: This is list of json objects representing of '
                             'Gene class.')

    return parser


# --------------------------------------------------------------------------- #
def parse_genes_from_cli(genes: list):
    gene_list = []
    log.info(f"\nShape of genes: {np.shape(genes)}")
    if isinstance(genes, list):
        for gene in genes[0]:
            # log.debug(f"\nGene: {gene}")
            if isinstance(gene, dict):
                gene_list.append(Gene(mother=Allele(gene.get('mother').get('symbol')),
                                      father=Allele(gene.get('father').get('symbol')),
                                      description=gene.get('description')))
            elif isinstance(gene, Gene):
                gene_list.append(gene)
            else:
                log.error(f"\nGene: {gene} is not a valid gene.")
    elif isinstance(genes, Gene):
        gene_list.append(genes)
    else:
        log.error(f"\nGenes: {genes} is not a valid gene.")
    log.debug(f"\nParsed Gene List size: {len(gene_list)}")
    return gene_list
# --------------------------------------------------------------------------- #
