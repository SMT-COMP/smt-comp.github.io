# mypy: allow-any-unimported

import functools, itertools
from typing import Set, Dict, Optional, cast, List, DefaultDict
from pathlib import Path, PurePath
from smtcomp import defs
from rich import progress
from rich import print
from pydantic import BaseModel
import polars as pl

c_logic = pl.col("logic")
c_result = pl.col("result")
c_cpu_time = pl.col("cpu_time")
c_sat = pl.col("sat")
c_unsat = pl.col("unsat")
c_unknown = pl.col("unknown")
c_trivial = pl.col("trivial")
c_new = pl.col("new")
c_new_len = pl.col("new_len")
c_all_len = pl.col("all_len")
c_file = pl.col("file")


def find_trivial(results: pl.LazyFrame, config: defs.Config) -> pl.LazyFrame:
    incoherence_scope = ["file", "year"] if config.old_criteria else ["file"]
    tally = (
        results
        # Remove incoherent results
        .filter(
            (c_result != int(defs.Status.Sat)).all().over(*incoherence_scope)
            | (c_result != int(defs.Status.Unsat)).all().over(*incoherence_scope)
        )
        # Remove the results of non-competitive year (the only result for this file for this year)
        .filter(c_file.len().over("file", "year") > 1)
        # Aggregate information for each file
        .group_by("file", "year")
        .agg(
            trivial=
            # All the results are sat or unsat and the time is below 1s
            ((c_result != int(defs.Status.Unknown)) & (c_cpu_time <= 1.0)).all()
        )
        .group_by("file")
        .agg(
            trivial=c_trivial.any() if config.old_criteria else c_trivial.all(),
            run=True,
        )
    )
    return tally


def join_default_with_False(original: pl.LazyFrame, new: pl.LazyFrame, on: str) -> pl.LazyFrame:
    return original.join(new, on="file", how="left", coalesce=True).fill_null(False)


def add_trivial_run_info(benchmarks: pl.LazyFrame, previous_results: pl.LazyFrame, config: defs.Config) -> pl.LazyFrame:

    is_trivial = find_trivial(previous_results, config)
    return join_default_with_False(benchmarks, is_trivial, on="file").with_columns(
        new=pl.col("family").str.starts_with(str(config.current_year))
    )


def track_selection(benchmarks_with_info: pl.LazyFrame, config: defs.Config, target_track: defs.Track) -> pl.LazyFrame:
    used_logics = defs.logic_used_for_track(target_track)

    # Keep only logics used by single query
    b = benchmarks_with_info.filter(c_logic.is_in(set(map(int, used_logics))))

    # Remove trivial benchmarks
    b = b.filter(c_trivial == False).drop("trivial", "run")

    # Count number of benchmarks in each logic (all and new benchmarks)
    logics = b.group_by("logic", maintain_order=True).agg(
        new_len=c_file.filter(c_new == True).len(),
        all_len=c_file.len(),
        new_benchmarks=c_file.filter(c_new == True),
        old_benchmarks=c_file.filter(c_new == False),
    )

    # Expression computing the number of sample to take for each logic
    sample_size = pl.min_horizontal(
        c_all_len,
        pl.max_horizontal(
            config.min_used_benchmarks, (c_all_len * config.ratio_of_used_benchmarks).floor().cast(pl.UInt32)
        ),
    )
    new_sample_size = pl.min_horizontal(sample_size, c_new_len).cast(pl.UInt32)
    old_sample_size = sample_size - new_sample_size

    # Sampling
    # A bug with sample when n=0 force the use of the filter
    # https://github.com/pola-rs/polars/issues/16232

    new_benchmarks_sampled = (
        pl.col("new_benchmarks")
        .filter(new_sample_size > 0)
        .list.sample(n=new_sample_size.filter(new_sample_size > 0), seed=config.seed)
        .list.explode()
        .drop_nulls()
    )
    old_benchmarks_sampled = (
        pl.col("old_benchmarks")
        .filter(old_sample_size > 0)
        .list.sample(n=old_sample_size.filter(old_sample_size > 0), seed=config.seed)
        .list.explode()
        .drop_nulls()
    )

    selected_benchmarks = logics.select(file=new_benchmarks_sampled.append(old_benchmarks_sampled)).with_columns(
        selected=True
    )

    # Filter with the selected benchmarks
    return benchmarks_with_info.join(selected_benchmarks, on="file", how="outer_coalesce").with_columns(
        pl.col("selected").fill_null(False)
    )


def helper_compute_sq(config: defs.Config) -> pl.LazyFrame:
    """
    Returned columns: file (uniq id), logic, family,name, status, asserts nunmber, trivial, run (in previous year), new (benchmarks), selected
    """
    benchmarks = pl.read_ipc(config.cached_non_incremental_benchmarks)
    results = pl.read_ipc(config.cached_previous_results)
    benchmarks_with_info = add_trivial_run_info(benchmarks.lazy(), results.lazy(), config)
    if config.invert_triviality:
        trivial_in_logic = pl.col("trivial").any().over(["logic"])
        inverted_or_not_trivial = pl.when(trivial_in_logic).then(pl.col("trivial").not_()).otherwise(pl.col("trivial"))
        benchmarks_with_info = benchmarks_with_info.with_columns(trivial=inverted_or_not_trivial)
    return track_selection(benchmarks_with_info, config, defs.Track.SingleQuery)


def helper_compute_incremental(config: defs.Config) -> pl.LazyFrame:
    """
    Returned columns: file (uniq id), logic, family,name, status, asserts nunmber, trivial, run (in previous year), new (benchmarks), selected
    """
    benchmarks = pl.read_ipc(config.cached_incremental_benchmarks)
    results = pl.read_ipc(config.cached_previous_results)
    benchmarks_with_info = add_trivial_run_info(benchmarks.lazy(), results.lazy(), config)
    if config.invert_triviality:
        trivial_in_logic = pl.col("trivial").any().over(["logic"])
        inverted_or_not_trivial = pl.when(trivial_in_logic).then(pl.col("trivial").not_()).otherwise(pl.col("trivial"))
        benchmarks_with_info = benchmarks_with_info.with_columns(trivial=inverted_or_not_trivial)
    return track_selection(benchmarks_with_info, config, defs.Track.Incremental)


def competitive_logics(config: defs.Config) -> pl.LazyFrame:
    """
    returned columns track, logic, competitive:bool
    """
    l = (s.participations.get_logics_by_track() for s in config.submissions)
    dd = list(itertools.chain.from_iterable(map((lambda x: ((int(k), list(map(int, s))) for k, s in x.items())), l)))
    return (
        pl.DataFrame(dd, schema=["track", "logic"])
        .lazy()
        .explode("logic")
        .group_by("track", "logic")
        .agg(competitive=(pl.col("logic").len() > 1))
    )


@functools.cache
def tracks() -> pl.LazyFrame:
    """
    returned columns track, division, logic
    """
    l = (
        (int(track), int(division), int(logic))
        for track, divisions in defs.tracks.items()
        for division, logics in divisions.items()
        for logic in logics
    )
    return pl.DataFrame(l, schema=["track", "division", "logic"]).lazy()


def aws_selection(benchmarks: pl.LazyFrame, previous_results: pl.LazyFrame, config: defs.Config) -> pl.LazyFrame:
    aws_track = [defs.Track.Cloud, defs.Track.Parallel]

    # Add division information to competitive logic
    logics = competitive_logics(config).filter(pl.col("track").is_in(list(map(int, aws_track))), competitive=True)
    logics = logics.join(tracks(), on=["track", "logic"], how="inner")

    # Keep only competitive logic from this track
    b = benchmarks.join(logics, on="logic", how="inner")
    previous_results = previous_results.join(b, on="file", how="semi")

    # Keep only hard and unsolved benchmarks
    solved = c_result.is_in({int(defs.Status.Sat), int(defs.Status.Unsat)})
    solved_within_timelimit = solved & (c_cpu_time <= config.aws_timelimit_hard)

    hard_unsolved = (
        previous_results
        # Remove bench solved within the timelimit by any solver
        .filter(solved_within_timelimit.not_().all().over("file"))
        .group_by("file")
        .agg(hard=solved.any(), unsolved=solved.not_().all())
    )

    b = b.join(hard_unsolved, how="inner", on="file")

    def sample(lf: pl.LazyFrame) -> pl.LazyFrame:
        n = pl.min_horizontal(pl.col("file").list.len(), config.aws_num_selected)
        return lf.with_columns(file=pl.col("file").list.sample(n=n, seed=config.seed))

    # Sample at the logic level
    b = sample(b.group_by("track", "division", "logic").agg(file=c_file))

    # Sample at the division level
    b = sample(b.group_by("track", "division").agg(file=c_file.flatten()))

    # Sample at the track level
    b = sample(b.group_by("track").agg(file=c_file.flatten()))

    return b.explode("file").join(benchmarks, on="file", how="inner")
