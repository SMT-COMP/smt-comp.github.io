# mypy: allow-any-unimported

import functools, itertools
from typing import Set, Dict, Optional, cast, List, DefaultDict
from pathlib import Path, PurePath
from smtcomp import defs
from rich import progress
from rich import print
from pydantic import BaseModel
import polars as pl
from smtcomp.utils import *

SimpleNonIncrementalTrack = Literal[defs.Track.SingleQuery, defs.Track.ModelValidation, defs.Track.UnsatCore]
SimpleTrack = Literal[defs.Track.SingleQuery, defs.Track.ModelValidation, defs.Track.UnsatCore, defs.Track.Incremental]

c_logic = pl.col("logic")
c_result = pl.col("result")
c_current_result = pl.col("current_result")
c_status = pl.col("status")
c_cpu_time = pl.col("cpu_time")
c_sat = pl.col("sat")
c_unsat = pl.col("unsat")
c_unknown = pl.col("unknown")
c_trivial = pl.col("trivial")
c_new = pl.col("new")
c_new_len = pl.col("new_len")
c_all_len = pl.col("all_len")
c_file = pl.col("file")
c_year = pl.col("year")


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
            ((c_result != int(defs.Status.Unknown)) & (c_cpu_time <= 1.0)).all(),
            # Compute the full result by year
            result=pl.when((c_result == int(defs.Status.Sat)).sum() >= 2)
            .then(int(defs.Status.Sat))
            .when((c_result == int(defs.Status.Unsat)).sum() >= 2)
            .then(int(defs.Status.Unsat))
            .otherwise(int(defs.Status.Unknown)),
        )
        .group_by("file")
        .agg(
            trivial=c_trivial.any() if config.old_criteria else c_trivial.all(),
            run=True,
            result=pl.when((c_result == int(defs.Status.Sat)).any())
            .then(int(defs.Status.Sat))
            .when((c_result == int(defs.Status.Unsat)).any())
            .then(int(defs.Status.Unsat))
            .otherwise(int(defs.Status.Unknown)),
            current_result=pl.when(((c_result == int(defs.Status.Sat)) & (c_year == config.current_year)).any())
            .then(int(defs.Status.Sat))
            .when(((c_result == int(defs.Status.Unsat)) & (c_year == config.current_year)).any())
            .then(int(defs.Status.Unsat))
            .otherwise(int(defs.Status.Unknown)),
        )
    )
    return tally


def join_default_with_False(original: pl.LazyFrame, new: pl.LazyFrame, on: str) -> pl.LazyFrame:
    return original.join(new, on="file", how="left", coalesce=True).fill_null(False)


def add_trivial_run_info(benchmarks: pl.LazyFrame, previous_results: pl.LazyFrame, config: defs.Config) -> pl.LazyFrame:

    is_trivial = find_trivial(previous_results, config)
    with_info = add_columns(
        benchmarks,
        is_trivial,
        on=["file"],
        defaults={
            "trivial": False,
            "run": False,
            "result": int(defs.Status.Unknown),
            "current_result": int(defs.Status.Unknown),
        },
    ).with_columns(new=pl.col("family").str.starts_with(str(config.current_year)))

    if config.use_previous_results_for_status:
        with_info = with_info.with_columns(
            status=pl.when(pl.col("status") != int(defs.Status.Unknown)).then(pl.col("status")).otherwise(c_result)
        )

    return with_info


def track_selection(benchmarks_with_info: pl.LazyFrame, config: defs.Config, target_track: SimpleTrack) -> pl.LazyFrame:
    used_logics = defs.logic_used_for_track(target_track)

    # Keep only logics used by the track
    b = benchmarks_with_info.filter(c_logic.is_in(set(map(int, used_logics))))

    # Specific track filter
    match target_track:
        case defs.Track.SingleQuery | defs.Track.Incremental:
            # Remove trivial benchmarks
            # TODO: Incremental track doesn't normally remove trivial benchmarks
            b = b.filter(trivial=False)
        case defs.Track.ModelValidation:
            # Remove benchmarks with status sat and the one where solvers said sat
            b = b.filter((c_status == int(defs.Answer.Sat)) | (c_current_result == int(defs.Answer.Sat)))
        case defs.Track.UnsatCore:
            # Remove benchmarks with status unsat and the one where solvers said unsat
            # Remove benchmarks with 1 assertions
            b = b.filter((c_status == int(defs.Answer.Unsat)) | (c_current_result == int(defs.Answer.Unsat)))
            b = b.filter(pl.col("asserts") >= config.unsat_core_min_num_asserts)

    b = b.drop("trivial", "run")

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
    return benchmarks_with_info.join(selected_benchmarks, on="file", how="full").with_columns(
        pl.col("selected").fill_null(False)
    )


def helper_compute_non_incremental(config: defs.Config, track: SimpleNonIncrementalTrack) -> pl.LazyFrame:
    """
    Returned columns: file (uniq id), logic, family,name, status, asserts nunmber, trivial, run (in previous year), new (benchmarks), selected
    """
    benchmarks = pl.read_ipc(config.cached_non_incremental_benchmarks).lazy()
    results = pl.read_ipc(config.cached_previous_results).lazy()

    match track:
        case defs.Track.SingleQuery:
            pass
        case defs.Track.ModelValidation | defs.Track.UnsatCore:
            current_sq_result = config.cached_current_results[defs.Track.SingleQuery]
            if current_sq_result.exists():
                results = pl.concat([results, pl.read_ipc(current_sq_result).lazy()])
            else:
                print("[bold][red]Current results not available[/red][/bold]")

    benchmarks_with_info = add_trivial_run_info(benchmarks, results, config)
    if config.invert_triviality:
        trivial_in_logic = pl.col("trivial").any().over(["logic"])
        inverted_or_not_trivial = pl.when(trivial_in_logic).then(pl.col("trivial").not_()).otherwise(pl.col("trivial"))
        benchmarks_with_info = benchmarks_with_info.with_columns(trivial=inverted_or_not_trivial)
    return track_selection(benchmarks_with_info, config, track)


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


def helper(config: defs.Config, track: defs.Track) -> pl.LazyFrame:
    match track:
        case defs.Track.SingleQuery:
            selected = helper_compute_non_incremental(config, track)
        case defs.Track.Incremental:
            selected = helper_compute_incremental(config)
        case defs.Track.ModelValidation:
            selected = helper_compute_non_incremental(config, track)
        case defs.Track.UnsatCore:
            selected = helper_compute_non_incremental(config, track)
        case defs.Track.Cloud | defs.Track.Parallel:
            selected = helper_aws_selection(config).drop("division")
        case defs.Track.ProofExhibition:
            selected = helper_compute_non_incremental(config, defs.Track.SingleQuery)
            rich.print(
                f"[red]The selection and scramble_benchmarks command does not yet work for the competition track: {track}[/red]"
            )
            exit(1)
    return selected


def solver_competing_logics(config: defs.Config) -> pl.LazyFrame:
    """
    returned columns solver, track, logic
    """
    l = (
        (s.name, int(track), int(logic), p_id)
        for s in config.submissions
        for p_id, p in enumerate(s.participations.root)
        for (track, logics) in p.get_logics_by_track().items()
        for logic in logics
    )
    return pl.LazyFrame(
        l, schema={"solver": pl.String, "track": pl.Int32, "logic": pl.Int64, "participation": pl.Int32}
    )


def competitive_logics(config: defs.Config) -> pl.LazyFrame:
    """
    returned columns track, logic, competitive:bool
    """
    return solver_competing_logics(config).group_by("track", "logic").agg(competitive=(pl.len() > 1))


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
    return pl.DataFrame(l, schema={"track": pl.Int32, "division": pl.Int32, "logic": pl.Int64}).lazy()


def aws_selection(benchmarks: pl.LazyFrame, previous_results: pl.LazyFrame, config: defs.Config) -> pl.LazyFrame:
    aws_track = [defs.Track.Cloud, defs.Track.Parallel]

    # Add division information to competitive logic
    logics = (
        competitive_logics(config)
        .filter(pl.col("track").is_in(list(map(int, aws_track))), competitive=True)
        .drop("competitive")
    )
    df_logics = logics.collect()
    if len(df_logics) == 0:
        raise ValueError("No logics selected")
    logics = df_logics.lazy().join(tracks(), on=["track", "logic"], how="left")

    # Keep only competitive logic from the tracks
    benchmarks = intersect(benchmarks, logics, on=["logic"])
    previous_results = filter_with(previous_results, benchmarks, on=["file"])

    # Keep only hard and unsolved benchmarks
    solved = c_result.is_in({int(defs.Status.Sat), int(defs.Status.Unsat)})
    solved_within_timelimit = solved & (c_cpu_time <= config.aws_timelimit_hard)

    hard_unsolved = (
        previous_results
        # Remove bench solved within the timelimit by any solver
        .filter(solved_within_timelimit.not_().all().over("file"))
        .group_by("file")
        .agg(hard=solved.any())
    )

    hard_unsolved = intersect(hard_unsolved, benchmarks, on=["file"])

    def sample(lf: pl.LazyFrame) -> pl.LazyFrame:
        n = pl.min_horizontal(pl.col("file").list.len(), config.aws_num_selected / 2)
        return lf.with_columns(file=pl.col("file").list.sample(n=n, seed=config.seed))

    b = hard_unsolved

    b = sample(b.group_by("track", "hard", "logic").agg(file=c_file.sort())).sort(by="logic")

    b = b.group_by("track", "hard", maintain_order=True).agg(file=pl.col("file"))

    def round_robbin(files: list[list[int]]) -> list[int]:
        result: list[int] = []
        while True:
            empty = True
            for l in files:
                if 0 < len(l):
                    result.append(l.pop())
                    empty = False
                    if len(result) >= config.aws_num_selected / 2:
                        return result
            if empty:
                raise (ValueError("Not enough elements, decrease aws_timelimit_hard"))

    d = b.collect().to_dict(as_series=False)
    d["file"] = list(map(round_robbin, d["file"]))

    b = pl.LazyFrame(d).cast({"track": pl.Int32})

    b = b.explode("file").with_columns(selected=True)

    b = add_columns(
        hard_unsolved.select("file", "hard", "track"), b, on=["track", "hard", "file"], defaults={"selected": False}
    ).with_columns(unsolved=pl.col("hard").not_())

    return add_columns(
        benchmarks, b, on=["track", "file"], defaults={"hard": False, "unsolved": False, "selected": False}
    )


def removed_benchmarks(config: defs.Config) -> pl.LazyFrame:
    return pl.LazyFrame(config.removed_benchmarks)


def helper_aws_selection(config: defs.Config) -> pl.LazyFrame:
    """
    Returned columns: file (uniq id), logic, family,name, status, asserts nunmber, trivial, run (in previous year), new (benchmarks), selected
    """
    benchmarks = pl.read_ipc(config.cached_non_incremental_benchmarks).lazy()
    benchmarks = benchmarks.join(removed_benchmarks(config), on=["logic", "family", "name"], how="anti")
    results = pl.read_ipc(config.cached_previous_results)
    return aws_selection(benchmarks, results.lazy(), config)
