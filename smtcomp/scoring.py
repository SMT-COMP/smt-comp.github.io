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
sat_answer = c_answer == int(defs.Answer.Sat)
unsat_answer = c_answer == int(defs.Answer.Unsat)
known_answer = sat_answer | unsat_answer
not_known_answer = known_answer.not_()

c_status = pl.col("status")
sat_status = c_status == int(defs.Status.Sat)
unsat_status = c_status == int(defs.Status.Unsat)

c_walltime_s = pl.col("walltime_s")
c_cputime_s = pl.col("cputime_s")


def sanity_check(config: defs.Config, result: pl.LazyFrame) -> None:
    result = result.filter(known_answer & (config.timelimit_s < pl.col("walltime_s")))
    assert result.select(n=pl.len()).collect()["n"][0] == 0


def add_disagreements_info(results: pl.LazyFrame) -> pl.LazyFrame:
    """
    Add column "disagreements"
    For each division:
      - Sound solver are solvers that agree with the status of the benchmarks
      - Disagreements are benchmarks where sound solvers disagree (so status unknown)
    """

    sound_solvers = (
        ((sat_status & unsat_answer) | (unsat_status & sat_answer)).any().over("track", "division", "solver").not_()
    )
    results = results.with_columns(sound_solvers=sound_solvers)
    disagreements = (pl.col("sound_solvers") & sat_answer).any().over("track", "file") & (
        pl.col("sound_solvers") & unsat_answer
    ).any().over("track", "file")
    return results.with_columns(disagreements=disagreements).drop("sound_solvers")


def benchmark_scoring(config: defs.Config, results: pl.LazyFrame) -> pl.LazyFrame:
    """
    Add "parallel_score", "sequential_score" column for each results
    """

    error_score = pl.when((sat_status & unsat_answer) | (unsat_status & sat_answer)).then(-1).otherwise(0)
    """
    Use -1 instead of 1 for error so that we can use lexicographic comparison
    """
    correctly_solved_score = pl.when(known_answer).then(1).otherwise(0)
    """Even if said correct, it is just solved """
    wallclock_time_score = pl.when(known_answer).then(c_walltime_s).otherwise(0.0)
    """Time if answered"""
    cpu_time_score = pl.when(known_answer).then(c_cputime_s).otherwise(0.0)

    def virtual_cpu(e: pl.Expr, default: Any) -> pl.Expr:
        return pl.when(c_cputime_s <= config.timelimit_s).then(e).otherwise(default)

    return results.with_columns(
        parallel_score=pl.struct(
            error=error_score,
            correct=correctly_solved_score,
            wallclock=wallclock_time_score,
            cputime=cpu_time_score,
        ),
        sequential_score=pl.struct(
            error=virtual_cpu(error_score, 0),
            correct=virtual_cpu(correctly_solved_score, 0),
            cputime=virtual_cpu(cpu_time_score, 0.0),
        ),
    )


def division_score(config: defs.Config, results: pl.LazyFrame) -> pl.LazyFrame:
    """
    Compute the score of each solver for each division
    """

    def struct_sum(e: pl.Expr, size: int) -> pl.Expr:
        l = [e.struct[i].sum() for i in range(0, size)]
        return pl.struct(*l)

    return results.group_by("track", "division", "solver").agg(
        parallel_score=struct_sum(pl.col("parallel_score"), 4),
        sequential_score=struct_sum(pl.col("sequential_score"), 3),
        s24_score=struct_sum(pl.col("parallel_score").filter(c_walltime_s <= 24), 4),
    )
