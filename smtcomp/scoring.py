import functools, itertools
from typing import Set, Dict, Optional, cast, List, DefaultDict
from pathlib import Path, PurePath
from smtcomp import defs
from rich import progress
from rich import print
from pydantic import BaseModel
import polars as pl
from smtcomp.utils import *

c_answer = pl.col("answer")
is_sat = c_answer == int(defs.Answer.Sat)
is_unsat = c_answer == int(defs.Answer.Sat)
is_known = is_sat | is_unsat
is_not_known = is_known.not_()


def sanity_check(config: defs.Config, result: pl.LazyFrame) -> None:
    result = result.filter(is_known & (config.timelimit_s < pl.col("walltime_s")))
    assert result.select(n=pl.len()).collect()["n"][0] == 0
