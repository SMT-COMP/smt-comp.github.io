from pathlib import Path
import rich
from rich.progress import track
import subprocess
import concurrent.futures
import smtcomp.defs as defs
import polars as pl
import smtcomp.selection


def scramble_file(fdict: dict, incremental: bool, srcdir: Path, dstdir: Path, args: list) -> None:
    if incremental:
        i = "incremental"
    else:
        i = "non-incremental"
    fsrc = srcdir.joinpath(i).joinpath(str(defs.Logic.of_int(fdict["logic"]))).joinpath(Path(fdict["family"])).joinpath(fdict["name"])
    dstdir = dstdir.joinpath(str(defs.Logic.of_int(fdict["logic"])))
    fdst = dstdir.joinpath("scrambled" + str(fdict["scramble_id"]) + ".smt2")
    dstdir.mkdir(parents=True, exist_ok=True)
    subprocess.run(args, stdin=fsrc.open("r"), stdout=fdst.open("w"))


def create_scramble_id(benchmarks: pl.LazyFrame, config: defs.Config) -> pl.LazyFrame:
    files = benchmarks.sort("file").select(pl.col("file").shuffle(seed=config.seed()))
    files = files.with_row_index(name="scramble_id")
    return benchmarks.join(files,on="file")

def scramble_lazyframe(benchmarks: pl.LazyFrame, competition_track: defs.Track, config: defs.Config, srcdir: Path, dstdir: Path, scrambler: Path, max_workers: int
) -> None:
    args = []
    files = benchmarks.select("scramble_id","logic","family","name").collect().to_dicts()
    incremental = False
    seed = config.seed()
    
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
            rich.print(f"[red]The scramble_benchmarks command does not yet work for the competition track: {competition_track}[/red]")
            exit(1)

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
    results = list(
        track(
            executor.map(lambda fdict : scramble_file(fdict, incremental, srcdir, dstdir, args),files),
            total=len(files),
            description="Scrambling selected benchmarks...",
        )
    )
    executor.shutdown()

def test_select_and_scramble(
        competition_track: defs.Track, data: Path, config: defs.Config, srcdir: Path, dstdir: Path, scrambler: Path, max_workers: int
) -> None:
    seed = config.seed()
    
    match competition_track:
        case defs.Track.SingleQuery:
            selected = smtcomp.selection.helper_compute_sq(data, config)
        case defs.Track.Incremental:
            selected = smtcomp.selection.helper_compute_sq(data, config)
            rich.print(f"[red]The scramble_benchmarks command does not yet work for the competition track: {competition_track}[/red]")
            exit(1)
        case defs.Track.ModelValidation:
            selected = smtcomp.selection.helper_compute_sq(data, config)
            rich.print(f"[red]The scramble_benchmarks command does not yet work for the competition track: {competition_track}[/red]")
            exit(1)
        case defs.Track.UnsatCore:
            selected = smtcomp.selection.helper_compute_sq(data, config)
            rich.print(f"[red]The scramble_benchmarks command does not yet work for the competition track: {competition_track}[/red]")
            exit(1)
        case defs.Track.ProofExhibition | defs.Track.Cloud | defs.Track.Parallel:
            selected = smtcomp.selection.helper_compute_sq(data, config)
            rich.print(f"[red]The scramble_benchmarks command does not yet work for the competition track: {competition_track}[/red]")
            exit(1)
    selected = create_scramble_id(selected, config).filter(selected=True).filter(pl.col("logic") < 3)
    scramble_lazyframe(selected,competition_track,config,srcdir,dstdir,scrambler,max_workers)
    
def select_and_scramble(
        competition_track: defs.Track, data: Path, config: defs.Config, srcdir: Path, dstdir: Path, scrambler: Path, max_workers: int
) -> None:
    seed = config.seed()
    
    match competition_track:
        case defs.Track.SingleQuery:
            selected = smtcomp.selection.helper_compute_sq(data, config)
        case defs.Track.Incremental:
            selected = smtcomp.selection.helper_compute_sq(data, config)
            rich.print(f"[red]The scramble_benchmarks command does not yet work for the competition track: {competition_track}[/red]")
            exit(1)
        case defs.Track.ModelValidation:
            selected = smtcomp.selection.helper_compute_sq(data, config)
            rich.print(f"[red]The scramble_benchmarks command does not yet work for the competition track: {competition_track}[/red]")
            exit(1)
        case defs.Track.UnsatCore:
            selected = smtcomp.selection.helper_compute_sq(data, config)
            rich.print(f"[red]The scramble_benchmarks command does not yet work for the competition track: {competition_track}[/red]")
            exit(1)
        case defs.Track.ProofExhibition | defs.Track.Cloud | defs.Track.Parallel:
            selected = smtcomp.selection.helper_compute_sq(data, config)
            rich.print(f"[red]The scramble_benchmarks command does not yet work for the competition track: {competition_track}[/red]")
            exit(1)

    selected = create_scramble_id(selected, config).filter(selected=True)
    scramble_lazyframe(selected,competition_track,config,srcdir,dstdir,scrambler,max_workers)
    
