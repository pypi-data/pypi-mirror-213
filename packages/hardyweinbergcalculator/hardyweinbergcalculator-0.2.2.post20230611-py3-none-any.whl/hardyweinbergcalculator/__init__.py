__VERSION__ = '0.2.2'

from .utils.generators.population_generator import generate_population
from .utils.generators.char_generator import random_chars
from .utils.parsers.args_parser import parse_args, parse_genes_from_cli
from .hardy_weinberg.hardy_weinberg import HardyWeinberg
from .hardy_weinberg.hardy_weinberg_stats import HardyWeinbergStats
from .genetics.gene import Gene
from .genetics.allele import Allele
from .config import get_logger
from .__main__ import app
