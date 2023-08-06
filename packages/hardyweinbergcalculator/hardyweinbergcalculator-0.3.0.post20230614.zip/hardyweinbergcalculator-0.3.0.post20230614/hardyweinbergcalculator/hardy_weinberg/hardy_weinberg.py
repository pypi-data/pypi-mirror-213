import json
import traceback
from typing import List
from ..genetics import Gene
from ..config import get_logger
from .hardy_weinberg_stats import HardyWeinbergStats

log = get_logger(__name__)


# --------------------------------------------------------------------------- #
class HardyWeinberg:
    stats: HardyWeinbergStats = None

    def __init__(
        self,
        homozygous_dominant_population: float = None,
        homozygous_recessive_population: float = None,
        heterozygous_population: float = None,
        total_population: float = None,
        genes: List[Gene] = None,
        p: float = None,
        q: float = None,
        *args,
        **kwargs,
    ):
        # log.info(f"Args: {args}")
        # log.info(f"Kwargs: {kwargs}")
        try:
            self.stats: HardyWeinbergStats = HardyWeinbergStats(
                p=p,
                q=q,
                total_population=total_population,
                homozygous_dominant_population=homozygous_dominant_population,
                homozygous_recessive_population=homozygous_recessive_population,
                heterozygous_population=heterozygous_population,
                genes=genes,
                *args,
                **kwargs,
            )
        except Exception as e:
            log.error(e)
            log.error(traceback.format_exc())

    def __dict__(self):
        return self.stats.__dict__()

    def __repr__(self):
        return self.stats.__repr__()

    def __str__(self):
        return self.stats.__str__()

    def to_json(self):
        return json.dumps(
            self.__dict__(), default=lambda o: o.__dict__, indent=4, sort_keys=False
        )
