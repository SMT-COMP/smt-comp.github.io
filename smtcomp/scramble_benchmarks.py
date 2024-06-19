from pathlib import Path
import rich
from rich.progress import track
import subprocess
import concurrent.futures
import smtcomp.defs as defs
from smtcomp.benchexec import generate_benchmark_yml, get_suffix
import polars as pl
import smtcomp.selection
from smtcomp.utils import *
from typing import Optional
import re


def benchmark_files_dir(cachedir: Path, track: defs.Track) -> Path:
    suffix = get_suffix(track)
    return cachedir / "benchmarks" / f"files{suffix}"


status_pattern = re.compile(r"(set-info :status (sat|unsat|unknown))")


def get_expected_result(benchmark: Path) -> Optional[bool]:
    for line in open(benchmark).readlines():
        m = status_pattern.search(line)
        if m and m.group(2) != "unknown":
            return m.group(2) == "sat"

    return None


def scramble_file(fdict: dict, incremental: bool, srcdir: Path, dstdir: Path, args: list) -> None:
    if incremental:
        i = "incremental"
    else:
        i = "non-incremental"
    fsrc = (
        srcdir.joinpath(i)
        .joinpath(str(defs.Logic.of_int(fdict["logic"])))
        .joinpath(Path(fdict["family"]))
        .joinpath(fdict["name"])
    )
    dstdir = dstdir.joinpath(str(defs.Logic.of_int(fdict["logic"])))
    fdst = dstdir.joinpath("scrambled" + str(fdict["scramble_id"]) + ".smt2")
    dstdir.mkdir(parents=True, exist_ok=True)

    if incremental:
        subprocess.run(
            ["grep", "-o", "(set-info :status \\(sat\\|unsat\\|unknown\\))"],
            stdin=fsrc.open("r"),
            stdout=fdst.open("w"),
        )
        subprocess.run(["sed", "-i", "s/(set-info :status \\(.*\\))/\\1/", str(fdst)])
        with fdst.open("a") as dstfile:
            dstfile.write("--- BENCHMARK BEGINS HERE ---\n")
        subprocess.run(args, stdin=fsrc.open("r"), stdout=fdst.open("a"))
    else:
        subprocess.run(args, stdin=fsrc.open("r"), stdout=fdst.open("w"))

    expected = get_expected_result(fsrc) if not incremental else None
    generate_benchmark_yml(fdst, expected, fsrc.relative_to(srcdir))


def create_scramble_id(benchmarks: pl.LazyFrame, config: defs.Config) -> pl.LazyFrame:
    files = benchmarks.sort("file").select(pl.col("file").shuffle(seed=config.seed))
    files = files.with_row_index(name="scramble_id")
    return benchmarks.join(files, on="file")


def create_scramble_id_v2(benchmarks: pl.LazyFrame, config: defs.Config) -> pl.LazyFrame:
    return benchmarks.sort("track", "file").with_columns(
        scramble_id=pl.int_range(0, pl.len()).shuffle(seed=config.seed)
    )


def scramble_lazyframe(
    benchmarks: pl.LazyFrame,
    competition_track: defs.Track,
    config: defs.Config,
    srcdir: Path,
    dstdir: Path,
    scrambler: Path,
    max_workers: int,
) -> None:
    args = []
    df = benchmarks.select("scramble_id", "logic", "family", "name", "file").collect()
    df.select("scramble_id", "file").write_csv(dstdir / "original_id.csv")
    files = df.to_dicts()
    incremental = False
    seed = config.seed

    match competition_track:
        case defs.Track.SingleQuery:
            args = [scrambler, "-term_annot", "pattern", "-seed", str(seed)]
        case defs.Track.Incremental:
            args = [scrambler, "-term_annot", "pattern", "-incremental", "true", "-seed", str(seed)]
            incremental = True
        case defs.Track.ModelValidation:
            args = [scrambler, "-term_annot", "pattern", "-gen-model-val", "true", "-seed", str(seed)]
        case defs.Track.UnsatCore:
            args = [scrambler, "-term_annot", "pattern", "-gen-unsat-core", "true", "-seed", str(seed)]
        case defs.Track.ProofExhibition | defs.Track.Cloud | defs.Track.Parallel:
            rich.print(
                f"[red]The scramble_benchmarks command does not yet work for the competition track: {competition_track}[/red]"
            )
            exit(1)

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(
            track(
                executor.map(lambda fdict: scramble_file(fdict, incremental, srcdir, dstdir, args), files),
                total=len(files),
                description="Scrambling selected benchmarks...",
            )
        )


def select_and_scramble(
    competition_track: defs.Track,
    config: defs.Config,
    srcdir: Path,
    cachedir: Path,
    scrambler: Path,
    max_workers: int,
) -> None:
    dstdir = benchmark_files_dir(cachedir, competition_track)
    dstdir.mkdir(parents=True, exist_ok=True)
    match competition_track:
        case defs.Track.SingleQuery:
            selected = smtcomp.selection.helper_compute_sq(config)
        case defs.Track.Incremental:
            selected = smtcomp.selection.helper_compute_incremental(config)
        case defs.Track.ModelValidation:
            selected = smtcomp.selection.helper_compute_sq(config)
            selected = selected.filter(status=int(defs.Status.Sat))
        case defs.Track.UnsatCore:
            selected = smtcomp.selection.helper_compute_sq(config)
            selected = selected.filter(status=int(defs.Status.Unsat))
        case defs.Track.ProofExhibition | defs.Track.Cloud | defs.Track.Parallel:
            selected = smtcomp.selection.helper_compute_sq(config)
            rich.print(
                f"[red]The scramble_benchmarks command does not yet work for the competition track: {competition_track}[/red]"
            )
            exit(1)

    selected = create_scramble_id(selected, config).filter(selected=True)
    scramble_lazyframe(selected, competition_track, config, srcdir, dstdir, scrambler, max_workers)


pl_name_of_track = pl.col("track").map_elements(defs.Track.name_of_int, return_dtype=pl.String)
pl_name_of_logic = pl.col("logic").map_elements(defs.Logic.name_of_int, return_dtype=pl.String)
pl_name_of_status = pl.col("status").map_elements(defs.Status.name_of_int, return_dtype=pl.String)


def select_and_scramble_aws(
    config: defs.Config,
    srcdir: Path,
    dstdir: Path,
    scrambler: Path,
    max_workers: int,
) -> None:
    selected = smtcomp.selection.helper_aws_selection(config)
    selected = create_scramble_id_v2(selected, config).filter(selected=True).drop("selected").collect().lazy()
    solvers = smtcomp.selection.solver_competing_logics(config)
    # Add a line for each solver that compet
    all = intersect(solvers, selected, on=["track", "logic"]).collect().lazy()

    for name, track in [("cloud", defs.Track.Cloud), ("parallel", defs.Track.Parallel)]:
        dst = dstdir / name / "non-incremental"
        dst.mkdir(parents=True, exist_ok=True)

        scramble_lazyframe(
            selected.filter(track=(int(track))),
            defs.Track.SingleQuery,
            config,
            srcdir,
            dst,
            scrambler,
            max_workers,
        )

        # Generate csv files
        pairs = all.filter(track=int(track))

        # Define original file, and input file
        pairs = pairs.with_columns(logic=pl_name_of_logic)
        input_file = pl.concat_str(
            pl.lit("non-incremental/"), "logic", pl.lit("/scrambled"), "scramble_id", pl.lit(".smt2")
        )
        original_file = pl.concat_str(pl.lit("non-incremental/"), "logic", pl.lit("/"), "family", pl.lit("/"), "name")
        pairs = pairs.select("solver", input_file.alias("input file"), original_file.alias("original file"))
        pairs.collect().write_csv(file=dstdir / f"{name}-pairs.csv")

    all.with_columns(
        track=pl_name_of_track,
        logic=pl_name_of_logic,
        status=pl_name_of_status,
    ).collect().write_csv(dstdir / "all.csv")
