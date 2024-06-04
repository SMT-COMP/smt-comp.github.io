import json
import itertools
from pathlib import Path
from typing import List, Optional, cast, Dict, Any, Annotated, TextIO
import rich
from rich.progress import track
import rich.style
from rich.tree import Tree
from rich.table import Table
from rich import print
import typer
from pydantic import ValidationError
from collections import defaultdict
import json

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
from rich.console import Console
import smtcomp.test_solver as test_solver


app = typer.Typer()

submissions_panel = "Submissions"
results_panel = "Results"
conversion_panel = "Conversion old format"
benchexec_panel = "Benchexec"
data_panel = "Data"
benchmarks_panel = "Benchmarks"
selection_panel = "Selection process"


@app.command(rich_help_panel=submissions_panel)
def show(
    files: list[Path] = typer.Argument(None),
    prefix: Optional[Path] = None,
    into_comment_file: Annotated[Optional[Path], typer.Option(help="Write the summary into the given file")] = None,
) -> None:
    """
    Show information about a solver submission
    """

    if prefix is not None:
        files = list(map(prefix.joinpath, files))

    l = list(map(submission.read_submission_or_exit, files))

    console = Console()
    for s in l:
        t = submission.rich_tree_summary(s)
        console.print(t)

    if into_comment_file is not None:
        with into_comment_file.open("w") as md:
            md.write("<details><summary>Summary of modified submissions</summary>\n\n")
            for s in l:
                submission.markdown_tree_summary(s, md)
            md.write("</details>\n")


@app.command(rich_help_panel=submissions_panel)
def show_json(files: list[Path] = typer.Argument(None), prefix: Optional[Path] = None) -> None:
    """
    Show information about solver submissions in JSON format
    """

    if prefix is not None:
        files = list(map(prefix.joinpath, files))

    l = list(map(submission.read_submission_or_exit, files))

    data = [submission.raw_summary(s) for s in l]
    print(json.dumps(data, indent=4))


@app.command(rich_help_panel=submissions_panel)
def get_contacts(files: list[Path] = typer.Argument(None)) -> None:
    """
    Find contact from submissions given as arguments
    """
    l = list(map(submission.read_submission_or_exit, files))
    contacts = list(str(c) for c in itertools.chain.from_iterable([s.contacts for s in l]))
    contacts.sort()
    print("\n".join(contacts))


@app.command(rich_help_panel=submissions_panel)
def merge_pull_requests_locally(C: str = ".") -> None:
    submission.merge_all_submissions(C)


@app.command(rich_help_panel=submissions_panel)
def validate(file: str) -> None:
    """
    Validate a json defining a solver submission
    """
    try:
        submission.read(file)
    except ValidationError as e:
        print(e)
        exit(1)


@app.command(rich_help_panel=conversion_panel)
def convert_csv(file: str, dstdir: Path) -> None:
    """
    Convert a csv (old submission format) to json files (new format)
    """
    dstdir.mkdir(parents=True, exist_ok=True)
    smtcomp.convert_csv.convert_csv(Path(file), Path(dstdir))


@app.command(rich_help_panel=submissions_panel)
def dump_json_schema(dst: Path) -> None:
    """
    Dump the json schemas used for submissions at the given file
    """
    with open(dst, "w") as f:
        f.write(json.dumps(defs.Submission.model_json_schema(), indent=2))


@app.command(rich_help_panel=benchexec_panel)
def prepare_execution(dst: Path) -> None:
    """
    Generate or download all scripts and tools that are necessary for the execution in Benchexec
    """
    execution.download_trace_executor(dst)
    execution.unpack_trace_executor(dst)
    execution.copy_tool_module(dst)


@app.command(rich_help_panel=benchexec_panel)
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


# Should be moved somewhere else
def download_archive_aux(s: defs.Submission, dst: Path) -> None:
    """
    Download and unpack
    """
    dst.mkdir(parents=True, exist_ok=True)
    if s.archive:
        archive.download(s.archive, dst)
        archive.unpack(s.archive, dst)
    for p in s.participations.root:
        if p.archive:
            archive.download(p.archive, dst)
            archive.unpack(p.archive, dst)


@app.command(rich_help_panel=benchexec_panel)
def download_archive(files: List[Path], dst: Path) -> None:
    """
    Download and unpack
    """
    for file in track(files):
        s = submission.read(str(file))
        download_archive_aux(s, dst)


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


@app.command(rich_help_panel=benchmarks_panel)
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


@app.command(rich_help_panel=benchmarks_panel)
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


@app.command(rich_help_panel=conversion_panel)
def convert_csv_result(src: Path, dst: Path, track: defs.Track) -> None:
    results = smtcomp.convert_csv.convert_csv_result(src, track)
    write_cin(dst, results.model_dump_json(indent=1))


def merge_results_aux(files: list[Path]) -> defs.Results:
    results: list[defs.Result] = []
    for file in track(files, description="load results"):
        r = defs.Results.model_validate_json(read_cin(file))
        results.extend(r.results)
    return defs.Results(results=results)


@app.command(rich_help_panel=results_panel)
def merge_results(files: list[Path], dst: Path) -> None:
    write_cin(dst, merge_results_aux(files).model_dump_json(indent=1))


@app.command(rich_help_panel=benchmarks_panel)
def merge_benchmarks(files: list[Path], dst: Path) -> None:
    incremental: list[defs.InfoIncremental] = []
    non_incremental: list[defs.InfoNonIncremental] = []
    for file in track(files):
        r = defs.Benchmarks.model_validate_json(read_cin(file))
        incremental.extend(r.incremental)
        non_incremental.extend(r.non_incremental)
    write_cin(dst, defs.Benchmarks(incremental=incremental, non_incremental=non_incremental).model_dump_json(indent=1))


OLD_CRITERIA = Annotated[bool, typer.Option(help="Simulate previous year criteria (needs only to be trivial one year)")]


@app.command(rich_help_panel=selection_panel)
def show_benchmarks_trivial_stats(data: Path, old_criteria: OLD_CRITERIA = False) -> None:
    """
    Show statistics on the trivial benchmarks

    Never compet.: old benchmarks never run competitively (more than one prover)
    """
    config = defs.Config(seed=None)
    config.old_criteria = old_criteria
    datafiles = defs.DataFiles(data)
    benchmarks = pl.read_ipc(datafiles.cached_non_incremental_benchmarks)
    results = pl.read_ipc(datafiles.cached_previous_results)
    benchmarks_with_trivial_info = smtcomp.selection.add_trivial_run_info(benchmarks.lazy(), results.lazy(), config)
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


@app.command(rich_help_panel=selection_panel)
def show_sq_selection_stats(
    data: Path,
    seed: int,
    old_criteria: OLD_CRITERIA = False,
    min_use_benchmarks: int = defs.Config.min_used_benchmarks,
    ratio_of_used_benchmarks: float = defs.Config.ratio_of_used_benchmarks,
    invert_triviality: bool = False,
) -> None:
    """
    Show statistics on the benchmarks selected for single query track

    Logics that are not in any division are printed in red.

    Never compet.: old benchmarks never run competitively (more than one prover)
    """
    config = defs.Config(seed=seed)
    config.min_used_benchmarks = min_use_benchmarks
    config.ratio_of_used_benchmarks = ratio_of_used_benchmarks
    config.invert_triviality = invert_triviality
    config.old_criteria = old_criteria
    benchmarks_with_info = smtcomp.selection.helper_compute_sq(data, config)
    b3 = (
        benchmarks_with_info.group_by(["logic"])
        .agg(
            trivial=pl.col("file").filter(trivial=True).len(),
            not_trivial=pl.col("file").filter(trivial=False, run=True).len(),
            old_never_ran=pl.col("file").filter(run=False, new=False).len(),
            new=pl.col("new").sum(),
            selected=pl.col("file").filter(selected=True).len(),
            selected_already_run=pl.col("file").filter(selected=True, run=True).len(),
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
    table.add_column("selected already run", justify="right", style="green4")

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
            str(d["selected_already_run"]),
        )

    table.add_section()
    table.add_row(
        "Total",
        str(b3["trivial"].sum()),
        str(b3["not_trivial"].sum()),
        str(b3["old_never_ran"].sum()),
        str(b3["new"].sum()),
        str(b3["selected"].sum()),
        str(b3["selected_already_run"].sum()),
    )

    print(table)


def print_iterable(i: int, tree: Tree, a: Any) -> None:
    for k, v in a.items():
        if i == 1:
            tree.add(f"{str(k)}:{v}")
        else:
            t1 = tree.add(str(k))
            print_iterable(i - 1, t1, v)


@app.command(rich_help_panel=data_panel)
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


@app.command(rich_help_panel=benchexec_panel)
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


@app.command()
def generate_test_script(outdir: Path, submissions: list[Path] = typer.Argument(None)) -> None:
    def read_submission(file: Path) -> defs.Submission:
        try:
            return submission.read(str(file))
        except Exception as e:
            rich.print(f"[red]Error during file parsing of {file}[/red]")
            print(e)
            exit(1)

    outdir.mkdir(parents=True, exist_ok=True)
    test_solver.copy_me(outdir)

    trivial_bench = outdir.joinpath("trivial_bench")
    smtcomp.generate_benchmarks.generate_trivial_benchmarks(trivial_bench)

    l = list(map(read_submission, submissions))
    script_output = outdir.joinpath("test_script.py")
    with script_output.open("w") as out:
        out.write("from test_solver import *\n")
        out.write("init_test()\n")
        out.write("\n")
        out.write("""print("Testing provers")\n""")
        for sub in l:
            out.write(f"print({sub.name!r})\n")
            download_archive_aux(sub, outdir)
            for part in sub.complete_participations():
                for track, divisions in part.tracks.items():
                    match track:
                        case defs.Track.Incremental:
                            statuses = [defs.Status.Sat, defs.Status.Unsat]
                        case defs.Track.ModelValidation:
                            statuses = [defs.Status.Sat]
                        case defs.Track.SingleQuery:
                            statuses = [defs.Status.Sat, defs.Status.Unsat]
                        case defs.Track.UnsatCore | defs.Track.ProofExhibition | defs.Track.Cloud | defs.Track.Parallel:
                            continue
                    for _, logics in divisions.items():
                        for logic in logics:
                            for status in statuses:
                                file_sat = smtcomp.generate_benchmarks.path_trivial_benchmark(
                                    trivial_bench, track, logic, status
                                ).relative_to(outdir)
                                cmd = (
                                    archive.archive_unpack_dir(part.archive, outdir)
                                    .joinpath(part.command.binary)
                                    .relative_to(outdir)
                                )
                                if status == defs.Status.Sat:
                                    expected = "sat"
                                else:
                                    expected = "unsat"
                                out.write(
                                    f"test({str(cmd)!r},{part.command.arguments!r},{str(file_sat)!r},{expected!r})\n"
                                )
        out.write("end()\n")
