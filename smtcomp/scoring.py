from smtcomp import defs
import polars as pl
from smtcomp.utils import *

c_answer = pl.col("answer")
sat_answer = c_answer == int(defs.Answer.Sat)
unsat_answer = c_answer == int(defs.Answer.Unsat)
known_answer = sat_answer | unsat_answer
unknown_answer = known_answer.not_()
timeout_answer = c_answer == int(defs.Answer.Timeout)
memout_answer = c_answer == int(defs.Answer.OOM)

c_status = pl.col("status")
sat_status = c_status == int(defs.Status.Sat)
unsat_status = c_status == int(defs.Status.Unsat)

c_sound_status = pl.col("sound_status")
sat_sound_status = c_sound_status == int(defs.Status.Sat)
unsat_sound_status = c_sound_status == int(defs.Status.Unsat)


c_walltime_s = pl.col("walltime_s")
c_cputime_s = pl.col("cputime_s")
twentyfour = c_walltime_s <= 24

scores = ["error_score", "correctly_solved_score", "wallclock_time_score", "cpu_time_score"]


class Kind(defs.EnumAutoInt):
    par = "par"
    seq = "seq"
    sat = "sat"
    unsat = "unsat"
    twentyfour = "24"


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
    sound_status = (
        pl.when((pl.col("sound_solvers") & sat_answer).any().over("track", "file"))
        .then(int(defs.Answer.Sat))
        .when((pl.col("sound_solvers") & unsat_answer).any().over("track", "file"))
        .then(int(defs.Answer.Unsat))
        .otherwise(c_status)
    )

    return results.with_columns(disagreements=disagreements, sound_status=sound_status).drop("sound_solvers")


def benchmark_scoring(results: pl.LazyFrame) -> pl.LazyFrame:
    """
    Requires disagreements
    Add "error_score", "correctly_solved_score", "wallclock_time_score","cpu_time_score"
    """

    error_score = pl.when((sat_sound_status & unsat_answer) | (unsat_sound_status & sat_answer)).then(-1).otherwise(0)
    """
    Use -1 instead of 1 for error so that we can use lexicographic comparison
    """
    correctly_solved_score = pl.when(known_answer).then(1).otherwise(0)
    """Even if said correct, it is just solved """
    wallclock_time_score = pl.when(known_answer).then(c_walltime_s).otherwise(0.0)
    """Time if answered"""
    cpu_time_score = pl.when(known_answer).then(c_cputime_s).otherwise(0.0)

    return results.with_columns(
        error_score=error_score,
        correctly_solved_score=correctly_solved_score,
        wallclock_time_score=wallclock_time_score,
        cpu_time_score=cpu_time_score,
    )


def virtual_sequential_score(config: defs.Config, results: pl.LazyFrame) -> pl.LazyFrame:
    """
    Apply a virtual cpu filter on parallel score
    """

    def virtual_cpu(e: str, default: Any) -> pl.Expr:
        return pl.when(c_cputime_s <= config.timelimit_s).then(pl.col(e)).otherwise(default)

    return results.with_columns(
        error_score=virtual_cpu("error_score", 0),
        correctly_solved_score=virtual_cpu("correctly_solved_score", 0),
        cpu_time_score=virtual_cpu("cpu_time_score", 0.0),
        wallclock_time_score=virtual_cpu("wallclock_time_score", 0.0),
    )


def division_score(results: pl.LazyFrame) -> pl.LazyFrame:
    """
    Sum the benchmarks score of each solver for each division
    """

    return results.group_by("track", "division", "solver").agg(
        pl.sum("error_score"),
        pl.sum("correctly_solved_score"),
        pl.sum("cpu_time_score"),
        pl.sum("wallclock_time_score"),
    )


def filter_for(kind: Kind, config: defs.Config, results: pl.LazyFrame) -> pl.LazyFrame:
    match kind:
        case Kind.par:
            return results
        case Kind.seq:
            return virtual_sequential_score(config, results)
        case Kind.sat:
            return results.filter(sat_sound_status)
        case Kind.unsat:
            return results.filter(unsat_sound_status)
        case Kind.twentyfour:
            return results.filter(twentyfour)
