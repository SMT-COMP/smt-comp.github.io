from smtcomp import defs
import polars as pl
from smtcomp.utils import *
from typing import assert_never

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

scores = [
    ("error_score", False),
    ("correctly_solved_score", True),
    ("wallclock_time_score", False),
    ("cpu_time_score", False),
]
"""
Columns to sort with and if it should be sorted in descending order
"""


class Kind(defs.EnumAutoInt):
    par = "par"
    seq = "seq"
    sat = "sat"
    unsat = "unsat"
    twentyfour = "24"


def sanity_check(config: defs.Config, result: pl.LazyFrame) -> None:
    result = result.filter(known_answer & (config.timelimit_s < pl.col("walltime_s")))
    assert result.select(n=pl.len()).collect()["n"][0] == 0


def add_disagreements_info(results: pl.LazyFrame, track: defs.Track) -> pl.LazyFrame:
    """
    Add column "disagreements"
    For each division:
      - Sound solver are solvers that agree with the status of the benchmarks
      - Disagreements are benchmarks where sound solvers disagree (so status unknown)
    """

    match track:
        case defs.Track.Incremental:
            sound_solver = (
                (c_answer == int(defs.Answer.IncrementalError)).any().over("track", "division", "solver").not_()
            )
            results = results.with_columns(sound_solver=sound_solver)
            # All the benchmarks have a status
            return results.with_columns(disagreements=False, sound_status=int(defs.Answer.Incremental))

        case defs.Track.UnsatCore:
            sound_solver = (
                ((c_answer == int(defs.Answer.UnsatCoreNotValidated)) | sat_answer)
                .any()
                .over("track", "division", "solver")
                .not_()
            )
            results = results.with_columns(sound_solver=sound_solver)
            # All the benchmarks have a status
            return results.with_columns(disagreements=False, sound_status=int(defs.Answer.Unsat))

        case defs.Track.ModelValidation:
            sound_solver = (
                ((c_answer == int(defs.Answer.ModelUnsat)) | unsat_answer)
                .any()
                .over("track", "division", "solver")
                .not_()
            )
            results = results.with_columns(sound_solver=sound_solver)
            # All the benchmarks have a status
            return results.with_columns(disagreements=False, sound_status=int(defs.Answer.Sat))

    sound_solver = (
        ((sat_status & unsat_answer) | (unsat_status & sat_answer)).any().over("track", "division", "solver").not_()
    )
    results = results.with_columns(sound_solver=sound_solver)
    disagreements = (pl.col("sound_solver") & sat_answer).any().over("track", "file") & (
        pl.col("sound_solver") & unsat_answer
    ).any().over("track", "file")
    sound_status = (
        pl.when((pl.col("sound_solver") & sat_answer).any().over("track", "file"))
        .then(int(defs.Answer.Sat))
        .when((pl.col("sound_solver") & unsat_answer).any().over("track", "file"))
        .then(int(defs.Answer.Unsat))
        .otherwise(c_status)
    )

    return results.with_columns(disagreements=disagreements, sound_status=sound_status)


def benchmark_scoring(results: pl.LazyFrame, track: defs.Track) -> pl.LazyFrame:
    """
    Requires disagreements
    Add "error_score", "correctly_solved_score", "wallclock_time_score","cpu_time_score"
    """

    wallclock_time_score = pl.when(known_answer).then(c_walltime_s).otherwise(0.0)
    """Time if answered"""
    cpu_time_score = pl.when(known_answer).then(c_cputime_s).otherwise(0.0)

    match track:
        case defs.Track.Incremental:
            # Since in Incremental track all the status are known, the values are already correct
            error_score = pl.when(c_answer == int(defs.Answer.IncrementalError)).then(1).otherwise(0)
            correctly_solved_score = pl.col("nb_answers")
            wallclock_time_score = c_walltime_s
            cpu_time_score = c_cputime_s
        case defs.Track.UnsatCore:
            error_score = (
                pl.when(sat_answer | (c_answer == int(defs.Answer.UnsatCoreNotValidated))).then(1).otherwise(0)
            )
            correctly_solved_score = pl.when(unsat_answer).then(pl.col("asserts") - pl.col("nb_answers")).otherwise(0)
        case defs.Track.ModelValidation:
            error_score = pl.when(unsat_answer | (c_answer == int(defs.Answer.ModelUnsat))).then(1).otherwise(0)
            correctly_solved_score = pl.when(sat_answer).then(1).otherwise(0)
        case defs.Track.SingleQuery | defs.Track.Cloud | defs.Track.Parallel:
            error = (sat_sound_status & unsat_answer) | (unsat_sound_status & sat_answer)
            error_score = pl.when(error).then(1).otherwise(0)
            correctly_solved_score = pl.when(error.not_() & known_answer).then(1).otherwise(0)

        case defs.Track.UnsatCoreValidation | defs.Track.ProofExhibition:
            raise (ValueError("Can't score those track yet", track))
        case _:
            # Because mypy can't automatically check match exhaustiveness
            assert_never(track)

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
