import logging
import sys
import traceback
from typing import Union, List
from . import Gene, HardyWeinberg, generate_population, parse_args, get_logger

log = get_logger(__name__)


# --------------------------------------------------------------------------- #
def app(
    total_population: float = None,
    homozygous_dominant_population: float = None,
    homozygous_recessive_population: float = None,
    heterozygous_population: float = None,
    genes: Union[List[Gene]] = None,
    **kwargs,
):
    try:  # check for None inputs
        if (
            total_population is None
            and genes is None
            and heterozygous_population is None
        ):
            raise ValueError("Genes or population data must be provided.")
        return HardyWeinberg(
            total_population=total_population,
            homozygous_dominant_population=homozygous_dominant_population,
            homozygous_recessive_population=homozygous_recessive_population,
            heterozygous_population=heterozygous_population,
            genes=genes,
            **kwargs,
        )
    except Exception as e:
        log.error(e)
        log.error(traceback.format_exc())


# --------------------------------------------------------------------------- #
def main():
    try:
        parser = parse_args()
        args = parser.parse_args()
        log.debug(f"CLi Args: \n{args}")
        # _________________________________________________________________ #
        # print help message if no arguments are passed
        if len(sys.argv) <= 1:
            parser.print_help()
            sys.exit(1)
        # _________________________________________________________________ #
        if args.debug:
            log.setLevel(logging.DEBUG)
        elif args.verbose:
            log.setLevel(logging.INFO)
        # _________________________________________________________________ #
        if args.samples is not None:
            args.genes = generate_population(int(args.samples))
        else:
            args.genes = []
        return app(
            total_population=args.tpop,
            homozygous_dominant_population=args.ppop,
            homozygous_recessive_population=args.qpop,
            heterozygous_population=args.pq2pop,
            genes=args.genes,
        )
    except Exception as e:
        log.error(e)
        log.error(traceback.format_exc())


# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log.error(e)
        log.error(traceback.format_exc())
