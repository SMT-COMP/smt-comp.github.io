from pathlib import Path
import rich
from rich.progress import track
import subprocess
import concurrent.futures
import smtcomp.defs as defs
import polars as pl
import smtcomp.selection


def scramble_file(files: pl.Series(), line: int, dstdir: Path, args: list) -> None:
    dst = Path.joinpath(dstdir, "scrambled" + str(line) + ".smt2")
    subprocess.run(args, stdin=Path(str(files[line]).strip()).open("r"), stdout=dst.open("w"))


def scramble(
    competition_track: defs.Track, data: Path, dstdir: Path, scrambler: Path, seed: int, max_workers: int
) -> None:
    args = []
    
    match track:
        case defs.Track.SingleQuery:
            args = [scrambler, "-term_annot", "pattern", "-seed", str(seed)]
            datafiles = defs.DataFiles(data)
            benchmarks = pl.read_ipc(datafiles.cached_non_incremental_benchmarks)
            results = pl.read_ipc(datafiles.cached_previous_results)
            benchmarks_with_info = smtcomp.selection.add_trivial_run_info(benchmarks.lazy(), results.lazy(), False)
            benchmarks_with_info = smtcomp.selection.sq_selection(benchmarks_with_info, seed)
            selected = benchmarks_with_info.filter(selected=True).select("file")
#            sorted_by_seed = selected.sort("file").list()
        case defs.Track.Incremental:
            args = [scrambler, "-term_annot", "pattern", "-incremental", "true", "-seed", str(seed)]
            rich.print(f"[red]The scramble_benchmarks command does not yet work for the competition track: {competition_track}[/red]")
            exit(1)
        case defs.Track.ModelValidation:
            args = [scrambler, "-term_annot", "pattern", "-gen-model-val", "true", "-seed", str(seed)]
            rich.print(f"[red]The scramble_benchmarks command does not yet work for the competition track: {competition_track}[/red]")
            exit(1)
        case defs.Track.UnsatCore:
            args = [scrambler, "-term_annot", "pattern", "-gen-unsat-core", "true", "-seed", str(seed)]
            rich.print(f"[red]The scramble_benchmarks command does not yet work for the competition track: {competition_track}[/red]")
            exit(1)
        case defs.Track.ProofExhibition | defs.Track.Cloud | defs.Track.Parallel:
            rich.print(f"[red]The scramble_benchmarks command does not yet work for the competition track: {competition_track}[/red]")
            exit(1)

    files = selected.collect().to_series()            
    line = int(0)
    dstdir.mkdir(parents=True, exist_ok=True)
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
    results = list(
        track(
            executor.map(lambda line: scramble_file(files, line, dstdir, args), range(len(files))),
            total=files.len(),
            description="Scrambling selected benchmarks...",
        )
    )
    executor.shutdown()
