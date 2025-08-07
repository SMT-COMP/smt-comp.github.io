import math
import functools, itertools
from collections import defaultdict
from typing import Set, Dict, Optional, cast, List, DefaultDict, Tuple
from pathlib import Path, PurePath
from smtcomp import defs

import polars as pl
import smtcomp.scoring
from smtcomp.utils import *
import smtcomp.results

c_file = pl.col("file")
c_logic = pl.col("logic")
c_solver = pl.col("solver")
c_answer = pl.col("answer")
c_cputime_s = pl.col("cputime_s")
c_run = pl.col("run")


def output_for_logic(config: defs.Config, results: pl.LazyFrame, logic: defs.Logic, output_dir: Path) -> None:
    results = results.filter(c_run == True, c_logic == int(logic)).select(
        c_file, c_solver, c_answer, c_cputime_s, "nb_answers"
    )
    print(results.collect())
    return None
