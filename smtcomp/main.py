import json
import itertools
from pathlib import Path
from typing import List, Optional, cast, Dict, Any, Annotated
import rich
from rich.progress import track
import rich.style
from rich.tree import Tree
from rich.table import Table
from rich import print
import typer
from pydantic import ValidationError
from collections import defaultdict

import polars as pl

import smtcomp.archive as archive
import smtcomp.benchexec as benchexec
import smtcomp.defs as defs
import smtcomp.submission as submission
import smtcomp.execution as execution
from smtcomp.benchmarks import clone_group
import smtcomp.convert_csv
import smtcomp.generate_benchmarks
import smtcomp.list_benchmarks
import smtcomp.selection
from smtcomp.unpack import write_cin, read_cin
import smtcomp.scramble_benchmarks

app = typer.Typer()


@app.command()
def show(file: str) -> None:
    """
    Show information about a solver submission
    """
    s = None
    try:
        s = submission.read(file)
    except Exception as e:
        rich.print(f"[red]Error during file parsing of {file}[/red]")
        print(e)
        exit(1)
    if not s:
        rich.print(f"[red]Empty submission??? {file}[/red]")
        exit(1)
    submission.show(s)


@app.command()
def validate(file: str) -> None:
    """
    Validate a json defining a solver submission
    """
    try:
        submission.read(file)
    except ValidationError as e:
        print(e)
        exit(1)


@app.command()
def convert_csv(file: str, dstdir: Path) -> None:
    """
    Convert a csv (old submission format) to json files (new format)
    """
    dstdir.mkdir(parents=True, exist_ok=True)
    smtcomp.convert_csv.convert_csv(Path(file), Path(dstdir))


@app.command()
def dump_json_schema(dst: Path) -> None:
    """
    Dump the json schemas used for submissions at the given file
    """
    with open(dst, "w") as f:
        f.write(json.dumps(defs.Submission.model_json_schema(), indent=2))


@app.command()
def download_benchmarks(dst: Path, dryrun: bool = False) -> None:
    """
    Clone or update all the benchmarks used by the SMTCOMP
    """
    clone_group("SMT-LIB-benchmarks", dst.joinpath("non-incremental"), dryrun)
    clone_group("SMT-LIB-benchmarks-inc", dst.joinpath("incremental"), dryrun)


@app.command()
def prepare_execution(dst: Path) -> None:
    """
    Generate or download all scripts and tools that are necessary for the execution in Benchexec
    """
    execution.download_trace_executor(dst)
    execution.unpack_trace_executor(dst)
    execution.copy_tool_module(dst)


@app.command()
def generate_benchexec(
    files: List[Path],
    dst: Path,
    cachedir: Path,
    timelimit_s: int = defs.Config.timelimit_s,
    memlimit_M: int = defs.Config.memlimit_M,
    cpuCores: int = defs.Config.cpuCores,
) -> None:
    """
    Generate the benchexec file for the given submissions
    """
    cmdtasks: List[benchexec.CmdTask] = []
    for file in track(files):
        s = submission.read(str(file))
        res = benchexec.cmdtask_for_submission(s, cachedir)
        cmdtasks.extend(res)
    benchexec.generate_xml(
        timelimit_s=timelimit_s, memlimit_M=memlimit_M, cpuCores=cpuCores, cmdtasks=cmdtasks, file=dst
    )


@app.command()
def download_archive(files: List[Path], dst: Path) -> None:
    """
    Download and unpack
    """
    for file in track(files):
        dst.mkdir(parents=True, exist_ok=True)
        s = submission.read(str(file))
        if s.archive:
            archive.download(s.archive, dst)
            archive.unpack(s.archive, dst)
        for p in s.participations.root:
            if p.archive:
                archive.download(p.archive, dst)
                archive.unpack(p.archive, dst)


@app.command()
def generate_trivial_benchmarks(dst: Path) -> None:
    """
    Generate trivial benchmarks for testing
    """
    smtcomp.generate_benchmarks.generate_trivial_benchmarks(dst)


@app.command()
def generate_benchmarks(dst: Path, seed: int = 0) -> None:
    """
    Generate benchmarks for smtcomp
    """
    smtcomp.generate_benchmarks.generate_benchmarks(dst, seed)


@app.command()
def create_benchmarks_list(src: Path, data: Path, scrambler: Optional[Path] = None, j: int = 8) -> None:
    """
    List the benchmarks found in SMTLIB releases.
        https://zenodo.org/communities/smt-lib/

    The tar.zst must be uncompressed.
    The given directory must contain "non-incremental" and "incremental", or be one of them itself.

    The scrambler is used if the path to its binary is given
    """
    if src.name == "incremental":
        files_incremental = smtcomp.list_benchmarks.list_benchmarks(src, scrambler, j, True)
        files_non_incremental = []
    elif src.name == "non-incremental":
        files_incremental = []
        files_non_incremental = smtcomp.list_benchmarks.list_benchmarks(src, scrambler, j, False)
    else:
        incremental = src.joinpath("incremental")
        non_incremental = src.joinpath("non-incremental")
        if incremental.exists():
            files_incremental = smtcomp.list_benchmarks.list_benchmarks(incremental, scrambler, j, True)
        else:
            files_incremental = []
        if non_incremental.exists():
            files_non_incremental = smtcomp.list_benchmarks.list_benchmarks(non_incremental, scrambler, j, False)
        else:
            files_non_incremental = []

        if incremental is [] and non_incremental is []:
            raise (ValueError("The directory must contain non-incremental or incremental"))

    benchmarks = defs.Benchmarks(
        incremental=cast(List[defs.InfoIncremental], files_incremental),
        non_incremental=cast(List[defs.InfoNonIncremental], files_non_incremental),
    )
    datafiles = defs.DataFiles(data)
    print("Writing benchmarks file")
    write_cin(datafiles.benchmarks, benchmarks.model_dump_json(indent=1))


@app.command()
def benchmarks_stats(src: Path) -> None:
    tree = Tree(src.name)
    benchmarks = defs.Benchmarks.model_validate_json(src.read_text())
    d: defaultdict[defs.Logic, defaultdict[tuple[str, ...], int]] = defaultdict(lambda: defaultdict(int))

    def tree_info(tree: Tree, l: List[defs.InfoIncremental] | List[defs.InfoNonIncremental]) -> None:
        for s in l:
            d[s.file.logic][s.file.family] = d[s.file.logic][s.file.family] + 1
        for k, v in d.items():
            t1 = tree.add(str(k))
            for f, v2 in v.items():
                fn = "/".join(f)
                t2 = t1.add(f"{v2:4d}: [bold magenta]{fn}[/bold magenta]")

    tree_info(tree.add("non-incremental"), benchmarks.non_incremental)
    tree_info(tree.add("incremental"), benchmarks.incremental)
    print(tree)


@app.command()
def convert_csv_result(src: Path, dst: Path, track: defs.Track) -> None:
    results = smtcomp.convert_csv.convert_csv_result(src, track)
    write_cin(dst, results.model_dump_json(indent=1))


def merge_results_aux(files: list[Path]) -> defs.Results:
    results: list[defs.Result] = []
    for file in track(files, description="load results"):
        r = defs.Results.model_validate_json(read_cin(file))
        results.extend(r.results)
    return defs.Results(results=results)


@app.command()
def merge_results(files: list[Path], dst: Path) -> None:
    write_cin(dst, merge_results_aux(files).model_dump_json(indent=1))


@app.command()
def merge_benchmarks(files: list[Path], dst: Path) -> None:
    incremental: list[defs.InfoIncremental] = []
    non_incremental: list[defs.InfoNonIncremental] = []
    for file in track(files):
        r = defs.Benchmarks.model_validate_json(read_cin(file))
        incremental.extend(r.incremental)
        non_incremental.extend(r.non_incremental)
    write_cin(dst, defs.Benchmarks(incremental=incremental, non_incremental=non_incremental).model_dump_json(indent=1))


OLD_CRITERIA = Annotated[bool, typer.Option(help="Simulate previous year criteria (needs only to be trivial one year)")]


@app.command()
def show_benchmarks_trivial_stats(data: Path, old_criteria: OLD_CRITERIA = False) -> None:
    """
    Show statistics on the trivial benchmarks

    Never compet.: old benchmarks never run competitively (more than one prover)
    """
    datafiles = defs.DataFiles(data)
    benchmarks = pl.read_ipc(datafiles.cached_non_incremental_benchmarks)
    results = pl.read_ipc(datafiles.cached_previous_results)
    benchmarks_with_trivial_info = smtcomp.selection.add_trivial_run_info(
        benchmarks.lazy(), results.lazy(), old_criteria
    )
    b3 = (
        benchmarks_with_trivial_info.group_by(["logic"])
        .agg(
            trivial=pl.col("file").filter(trivial=True).len(),
            not_trivial=pl.col("file").filter(trivial=False, run=True).len(),
            old_never_ran=pl.col("file").filter(run=False, new=False).len(),
            new=pl.col("file").filter(new=True).len(),
        )
        .sort(by="logic")
        .collect()
    )
    table = Table(title="Statistics on the benchmark pruning")

    table.add_column("Logic", justify="left", style="cyan", no_wrap=True)
    table.add_column("trivial", justify="right", style="green")
    table.add_column("not trivial", justify="right", style="orange_red1")
    table.add_column("never compet.", justify="right", style="magenta")
    table.add_column("new", justify="right", style="magenta1")

    for d in b3.to_dicts():
        table.add_row(
            str(defs.Logic.of_int(d["logic"])),
            str(d["trivial"]),
            str(d["not_trivial"]),
            str(d["old_never_ran"]),
            str(d["new"]),
        )

    table.add_section()
    table.add_row(
        "Total",
        str(b3["trivial"].sum()),
        str(b3["not_trivial"].sum()),
        str(b3["old_never_ran"].sum()),
        str(b3["new"].sum()),
    )

    print(table)


@app.command()
def show_sq_selection_stats(data: Path, seed: int, old_criteria: OLD_CRITERIA = False) -> None:
    """
    Show statistics on the benchmarks selected for single query track

    Logics that are not in any division are printed in red.

    Never compet.: old benchmarks never run competitively (more than one prover)
    """
    datafiles = defs.DataFiles(data)
    benchmarks = pl.read_ipc(datafiles.cached_non_incremental_benchmarks)
    results = pl.read_ipc(datafiles.cached_previous_results)
    benchmarks_with_info = smtcomp.selection.add_trivial_run_info(benchmarks.lazy(), results.lazy(), old_criteria)
    benchmarks_with_info = smtcomp.selection.sq_selection(benchmarks_with_info, seed)
    b3 = (
        benchmarks_with_info.group_by(["logic"])
        .agg(
            trivial=pl.col("file").filter(trivial=True).len(),
            not_trivial=pl.col("file").filter(trivial=False, run=True).len(),
            old_never_ran=pl.col("file").filter(run=False, new=False).len(),
            new=pl.col("new").sum(),
            selected=pl.col("file").filter(selected=True).len(),
        )
        .sort(by="logic")
        .collect()
    )
    table = Table(title="Statistics on the benchmark selection for single query")

    table.add_column("Logic", justify="left", style="cyan", no_wrap=True)
    table.add_column("trivial", justify="right", style="green")
    table.add_column("not trivial", justify="right", style="orange_red1")
    table.add_column("never compet.", justify="right", style="magenta")
    table.add_column("new", justify="right", style="magenta1")
    table.add_column("selected", justify="right", style="green3")

    used_logics = defs.logic_used_for_track(defs.Track.SingleQuery)
    for d in b3.to_dicts():
        logic = defs.Logic.of_int(d["logic"])
        if logic in used_logics:
            slogic = f"{str(logic)}"
        else:
            slogic = f"[bold red]{str(logic)}[/bold red]"

        table.add_row(
            slogic,
            str(d["trivial"]),
            str(d["not_trivial"]),
            str(d["old_never_ran"]),
            str(d["new"]),
            str(d["selected"]),
        )

    table.add_section()
    table.add_row(
        "Total",
        str(b3["trivial"].sum()),
        str(b3["not_trivial"].sum()),
        str(b3["old_never_ran"].sum()),
        str(b3["new"].sum()),
        str(b3["selected"].sum()),
    )

    print(table)


def print_iterable(i: int, tree: Tree, a: Any) -> None:
    for k, v in a.items():
        if i == 1:
            tree.add(f"{str(k)}:{v}")
        else:
            t1 = tree.add(str(k))
            print_iterable(i - 1, t1, v)


@app.command()
def create_cache(data: Path) -> None:
    datafiles = defs.DataFiles(data)
    print("Loading benchmarks")
    bench = defs.Benchmarks.model_validate_json(read_cin(datafiles.benchmarks))
    bd: Dict[defs.Smt2File, int] = {}
    for i, smtfile in enumerate(
        itertools.chain(map(lambda x: x.file, bench.non_incremental), map(lambda x: x.file, bench.incremental))
    ):
        assert smtfile not in bd
        bd[smtfile] = i

    print("Creating non-incremental benchmarks cache as feather file")
    bench_simplified = map(
        lambda x: {
            "file": bd[x.file],
            "logic": int(x.file.logic),
            "family": str(x.file.family_path()),
            "name": x.file.name,
            "status": int(x.status),
            "asserts": x.asserts,
        },
        bench.non_incremental,
    )
    df = pl.DataFrame(bench_simplified)
    # df["family"] = df["family"].astype("string")
    # df["name"] = df["name"].astype("string")
    df.write_ipc(datafiles.cached_non_incremental_benchmarks)

    print("Creating incremental benchmarks cache as feather file")
    bench_simplified = map(
        lambda x: {
            "file": bd[x.file],
            "logic": int(x.file.logic),
            "family": str(x.file.family_path()),
            "name": x.file.name,
            "check_sats": x.check_sats,
        },
        bench.incremental,
    )
    df = pl.DataFrame(bench_simplified)
    # df["family"] = df["family"].astype("string")
    # df["name"] = df["name"].astype("string")
    df.write_ipc(datafiles.cached_incremental_benchmarks)

    def convert(x: defs.Result, year: int) -> dict[str, int | str | float] | None:
        if x.file not in bd:
            return None
        return {
            "file": bd[x.file],
            "track": int(x.track),
            "solver": x.solver,
            "result": int(x.result),
            "cpu_time": x.cpu_time,
            "wallclock_time": x.wallclock_time,
            "memory_usage": x.memory_usage,
            "year": year,
        }

    results_filtered: list[Any] = []
    for year, file in track(datafiles.previous_results, description="Loading json results"):
        results = defs.Results.model_validate_json(read_cin(file))
        results_filtered.extend(filter(lambda x: x is not None, map(lambda r: convert(r, year), results.results)))

    print("Creating old results cache as feather file")
    df = pl.DataFrame(results_filtered)
    # df["solver"] = df["solver"].astype("string")
    df.write_ipc(datafiles.cached_previous_results)


# def conv(x:defs.Smt2FileOld) -> defs.Info:
#     return defs.Info( file = defs.Smt2File(logic=x.logic,family=x.family,name=x.name), status= x.status, asserts = x.asserts, check_sats = x.check_sats)

# @app.command()
# def convert(src:Path,dst:Path) -> None:
#     benchmarks = defs.BenchmarksOld.model_validate_json(read_cin(src))
#     benchmarks2 = defs.Benchmarks(files=list(map(conv,benchmarks.files)))
#     write_cin(dst,benchmarks2.model_dump_json(indent=1))


@app.command()
def scramble_benchmarks(
    competition_track: str, src: Path, dstdir: Path, scrambler: Path, seed: int, max_workers: int = 8
) -> None:
    """
    Use the scrambler to scramble the listed benchmarks and
    write them to the destination directory.
    Acceptable competition track names are single-query,
    incremental, unsat-core, and model-validation.
    The src file must contain one benchmark path per line.
    """

    smtcomp.scramble_benchmarks.scramble(competition_track, src, dstdir, scrambler, seed, max_workers)
