# mypy: allow-any-unimported

import functools
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


def add_trivial_run_info(benchmarks: pl.LazyFrame, previous_results: pl.LazyFrame, config: defs.Config) -> pl.LazyFrame:

    is_trivial = find_trivial(previous_results, config)
    return (
        benchmarks.join(is_trivial, on="file", how="outer_coalesce")
        .fill_null(False)
        .with_columns(new=pl.col("family").str.starts_with(str(config.current_year)))
    )


def sq_selection(benchmarks_with_info: pl.LazyFrame, config: defs.Config) -> pl.LazyFrame:
    used_logics = defs.logic_used_for_track(defs.Track.SingleQuery)

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
        .list.sample(n=new_sample_size.filter(new_sample_size > 0), seed=config.seed())
        .list.explode()
        .drop_nulls()
    )
    old_benchmarks_sampled = (
        pl.col("old_benchmarks")
        .filter(old_sample_size > 0)
        .list.sample(n=old_sample_size.filter(old_sample_size > 0), seed=config.seed())
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
    return sq_selection(benchmarks_with_info, config)
