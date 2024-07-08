import json
import itertools
from pathlib import Path
from typing import List, Optional, cast, Dict, Any, Annotated, TextIO
import rich
from rich.progress import track, Progress
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
import smtcomp.benchexec
import smtcomp.defs as defs
import smtcomp.results
import smtcomp.scoring
import smtcomp.submission as submission
import smtcomp.execution as execution
import smtcomp.model_validation as model_validation
import smtcomp.results as results
from smtcomp.benchmarks import clone_group
import smtcomp.convert_csv
import smtcomp.generate_benchmarks
import smtcomp.list_benchmarks
import smtcomp.selection
from smtcomp.unpack import write_cin, read_cin
import smtcomp.scramble_benchmarks
from rich.console import Console
import smtcomp.test_solver as test_solver
from concurrent.futures import ThreadPoolExecutor
from smtcomp.benchexec import get_suffix
from smtcomp.scramble_benchmarks import benchmark_files_dir
from smtcomp.utils import *
import re

app = typer.Typer()

submissions_panel = "Submissions"
results_panel = "Results"
conversion_panel = "Conversion old format"
benchexec_panel = "Benchexec"
data_panel = "Data"
benchmarks_panel = "Benchmarks"
selection_panel = "Selection process"
scoring_panel = "Scoring process"


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
def get_seed(data: Path) -> None:
    conf = defs.Config(data)
    print(conf.seed)


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
    cachedir: Path,
    timelimit_s: int = defs.Config.timelimit_s,
    memlimit_M: int = defs.Config.memlimit_M,
    cpuCores: int = defs.Config.cpuCores,
) -> None:
    """
    Generate the benchexec file for the given submissions

    (The cachedir directory need to contain unpacked archive only with compa_starexec command)
    """
    config = defs.Config(data=None)
    config.timelimit_s = timelimit_s
    config.memlimit_M = memlimit_M
    config.cpuCores = cpuCores

    (cachedir / "tools").mkdir(parents=True, exist_ok=True)
    for file in track(files):
        s = submission.read(str(file))
        smtcomp.benchexec.generate(s, cachedir, config)


@app.command(rich_help_panel=benchexec_panel)
def convert_benchexec_results(
    results: Path,
) -> None:
    """
    Load benchexec results and aggregates results in feather format
    """

    lf = smtcomp.results.parse_dir(results)
    lf.collect().write_ipc(results / "parsed.feather")


@app.command(rich_help_panel=benchexec_panel)
def store_results(
    data: Path,
    lresults: List[Path],
) -> None:
    """
    Load benchexec results in feather formats and store them in data for adding them to git
    """

    config = defs.Config(data)
    lf = pl.concat(pl.read_ipc(results / "parsed.feather").lazy() for results in lresults)
    benchmarks = pl.read_ipc(config.cached_non_incremental_benchmarks).lazy()
    benchmarks_inc = pl.read_ipc(config.cached_incremental_benchmarks).lazy()
    for track, dst in config.current_results.items():
        match track:
            case defs.Track.Incremental:
                b = benchmarks_inc
                incremental = True
            case _:
                b = benchmarks
                incremental = False
        df = add_columns(
            lf.filter(track=int(track)).drop("logic"),
            b.select("file", "logic", "family", "name"),
            on=["file"],
            defaults={"logic": -1, "family": "", "name": ""},
        ).collect()
        if len(df) > 0:
            results_track = defs.Results(
                results=[
                    defs.Result(
                        track=track,
                        solver=d["solver"],
                        file=defs.Smt2File.of_tuple(
                            incremental=incremental,
                            logic=defs.Logic.of_int(d["logic"]),
                            family=d["family"],
                            name=d["name"],
                        ),
                        result=defs.Answer.of_int(d["answer"]),
                        cpu_time=d["cputime_s"],
                        wallclock_time=d["walltime_s"],
                        memory_usage=d["memory_B"],
                    )
                    for d in df.to_dicts()
                ]
            )
            write_cin(dst, results_track.model_dump_json(indent=1))


@app.command(rich_help_panel=benchexec_panel)
def stats_of_benchexec_results(
    data: Path, results: Path, only_started: bool = False, track: defs.Track = defs.Track.SingleQuery
) -> None:
    """
    Load benchexec results and print some results about them
    """
    config = defs.Config(data)

    selected = smtcomp.results.helper_get_results(config, results, track)

    sum_answer = (pl.col("answer") == -1).sum()
    waiting = (pl.col("answer") == -1).all()

    if only_started:
        selected = selected.filter(waiting.over("logic").not_())

    df = (
        selected.group_by("division", "logic")
        .agg(
            n=pl.len(),
            done=pl.len() - sum_answer,
            sum_missing=sum_answer,
            missing=pl.struct(sum=sum_answer, waiting=waiting),
            solver=pl.col("solver").filter((pl.col("answer") == -1)).value_counts(),
        )
        .sort("division", "logic")
        .collect()
    )

    def print_solver(d: List[Dict[str, Any]]) -> str:
        return ",".join(map(lambda x: "{}({})".format(x["solver"], x["count"]), d))

    def print_missing(d: Dict[str, Any]) -> str:
        if d["waiting"]:
            return "[bold red]{}[/bold red]".format(d["sum"])
        elif d["sum"] == 0:
            return "[bold green]{}[/bold green]".format(d["sum"])
        else:
            return "[bold orange1]{}[/bold orange1]".format(d["sum"])

    rich_print_pl(
        "Results",
        df,
        Col(
            "division",
            "Division",
            footer="Total",
            justify="left",
            style="cyan",
            no_wrap=True,
            custom=defs.Division.name_of_int,
        ),
        Col(
            "logic",
            "Logic",
            footer="",
            justify="left",
            style="cyan",
            no_wrap=True,
            custom=defs.Logic.name_of_int,
        ),
        Col("n", "Selected"),
        Col("done", "Done"),
        Col("missing", "Missing", custom=print_missing, footer=(lambda df: str(df["sum_missing"].sum()))),
        Col("solver", "Missing", footer="", custom=print_solver),
    )


slash = pl.lit("/")
path_of_logic_family_name = pl.concat_str(
    pl.col("logic").first().map_elements(defs.Logic.name_of_int, return_dtype=pl.String),
    slash,
    pl.col("family").first(),
    slash,
    pl.col("name").first(),
)


@app.command(rich_help_panel=benchexec_panel)
def find_disagreement_results(
    data: Path, results: Path, use_previous_year_results: bool = defs.Config.use_previous_results_for_status
) -> None:
    """
    Load benchexec results and print some results about them
    """
    config = defs.Config(data)
    config.use_previous_results_for_status = use_previous_year_results
    selected = smtcomp.results.helper_get_results(config, results)

    df = (
        selected.filter(pl.col("answer").is_in([int(defs.Answer.Sat), int(defs.Answer.Unsat)]))
        .filter(
            (
                ((pl.col("answer") == int(defs.Answer.Sat)).any().over("file"))
                | (pl.col("status") == int(defs.Status.Sat))
            )
            & (
                ((pl.col("answer") == int(defs.Answer.Unsat)).any().over("file"))
                | (pl.col("status") == int(defs.Status.Unsat))
            )
        )
        .group_by("track", "logic", "file")
        .agg(answers=pl.struct("solver", "answer"), status=pl.col("status").first(), name=path_of_logic_family_name)
        .sort("track", "logic", "file")
        .collect()
    )

    def print_answers(d: List[Dict[str, Any]]) -> str:
        return ",".join(map(lambda x: "{}({})".format(x["solver"], defs.Answer.name_of_int(x["answer"])), d))

    rich_print_pl(
        "Disagreements",
        df,
        Col(
            "name",
            "Name",
            footer=lambda df: str(len(df)),
            justify="left",
            style="cyan",
            no_wrap=False,
            custom=str,
        ),
        Col(
            "status",
            "Expected",
            footer="",
            justify="left",
            style="cyan",
            no_wrap=False,
            custom=defs.Status.name_of_int,
        ),
        Col("answers", "Disagreement", custom=print_answers, footer=""),
    )


@app.command(rich_help_panel=scoring_panel)
def scoring_removed_benchmarks(
    data: Path, src: Path, use_previous_year_results: bool = defs.Config.use_previous_results_for_status
) -> None:
    config = defs.Config(data)
    config.use_previous_results_for_status = use_previous_year_results
    results = smtcomp.results.helper_get_results(config, src)

    results = smtcomp.scoring.add_disagreements_info(results)

    df = results.filter(disagreements=True).group_by("track", "file").agg(name=path_of_logic_family_name).collect()

    rich_print_pl(
        "Removed results (disagrements)",
        df,
        Col(
            "name",
            "Name",
            footer=lambda df: str(len(df)),
            justify="left",
            style="cyan",
            no_wrap=False,
            custom=str,
        ),
    )


@app.command(rich_help_panel=scoring_panel)
def show_scores(data: Path, src: Path, kind: smtcomp.scoring.Kind = typer.Argument(default="par")) -> None:
    config = defs.Config(data)
    results = smtcomp.results.helper_get_results(config, src)

    smtcomp.scoring.sanity_check(config, results)

    results = smtcomp.scoring.add_disagreements_info(results).filter(disagreements=False).drop("disagreements")

    results = smtcomp.scoring.benchmark_scoring(results)

    results = smtcomp.scoring.filter_for(kind, config, results)

    divisions = smtcomp.scoring.division_score(results)

    divisions = divisions.sort(
        "division", *smtcomp.scoring.scores, descending=[False] + [True] * len(smtcomp.scoring.scores)
    )

    rich_print_pl(
        "Scores",
        divisions.collect(),
        Col(
            "division",
            "divisions",
            footer="",
            justify="left",
            style="cyan",
            no_wrap=False,
            custom=defs.Division.name_of_int,
        ),
        Col(
            "solver",
            "Name",
            footer="",
            justify="left",
            style="cyan",
            no_wrap=False,
            custom=str,
        ),
        Col(
            "error_score",
            "Error Score",
            justify="left",
            style="red",
            no_wrap=False,
        ),
        Col(
            "correctly_solved_score",
            "Correct Score",
            justify="left",
            style="green",
            no_wrap=False,
        ),
        Col(
            "wallclock_time_score",
            "Wallclock Score",
            justify="left",
            style="cyan",
            no_wrap=False,
        ),
        Col(
            "cpu_time_score",
            "Cpu Time Score ",
            justify="left",
            style="cyan",
            no_wrap=False,
        ),
    )


@app.command(rich_help_panel=benchexec_panel)
def download_archive(files: List[Path], dst: Path) -> None:
    """
    Download and unpack
    """
    for file in track(files):
        s = submission.read(str(file))
        archive.download_unpack(s, dst)


@app.command()
def generate_trivial_benchmarks(dst: Path) -> None:
    """
    Generate trivial benchmarks for testing
    """
    smtcomp.generate_benchmarks.generate_trivial_benchmarks(dst)


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
    config = defs.Config(data)
    print("Writing benchmarks file")
    write_cin(config.benchmarks, benchmarks.model_dump_json(indent=1))


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
def show_selection_stats(
    data: Path,
    old_criteria: OLD_CRITERIA = False,
    min_use_benchmarks: int = defs.Config.min_used_benchmarks,
    ratio_of_used_benchmarks: float = defs.Config.ratio_of_used_benchmarks,
    invert_triviality: bool = False,
    use_previous_results_for_status: bool = defs.Config.use_previous_results_for_status,
    track: defs.Track = defs.Track.SingleQuery,
) -> None:
    """
    Show statistics on the benchmarks selected

    Logics that are not in any division are printed in red.

    Never compet.: old benchmarks never run competitively (more than one prover)
    """
    config = defs.Config(data)
    config.min_used_benchmarks = min_use_benchmarks
    config.ratio_of_used_benchmarks = ratio_of_used_benchmarks
    config.invert_triviality = invert_triviality
    config.old_criteria = old_criteria
    config.use_previous_results_for_status = use_previous_results_for_status
    benchmarks_with_info = smtcomp.selection.helper(config, track)

    used_logics = defs.logic_used_for_track(track)

    def print_logic(id: int) -> str:
        logic = defs.Logic.of_int(id)
        if logic in used_logics:
            return f"{str(logic)}"
        else:
            return f"[bold red]{str(logic)}[/bold red]"

    if track == defs.Track.Incremental:
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

        rich_print_pl(
            f"Statistics on the benchmark selection for {track!s}",
            b3,
            Col("logic", "Logic", footer="Total", justify="left", style="cyan", no_wrap=True, custom=print_logic),
            Col("trivial", "trivial", justify="right", style="green"),
            Col("not_trivial", "not trivial", justify="right", style="orange_red1"),
            Col("old_never_ran", "never compet.", justify="right", style="magenta"),
            Col("new", "new", justify="right", style="magenta1"),
            Col("selected", "selected", justify="right", style="green3"),
            Col("selected_already_run", "selected already run", justify="right", style="green4"),
        )
    else:
        b3 = (
            benchmarks_with_info.group_by(["logic"])
            .agg(
                trivial=pl.col("file").filter(trivial=True).len(),
                not_trivial=pl.col("file").filter(trivial=False, run=True).len(),
                old_never_ran=pl.col("file").filter(run=False, new=False).len(),
                new=pl.col("new").sum(),
                selected=pl.col("file").filter(selected=True).len(),
                selected_sat=pl.col("file").filter(selected=True, status=int(defs.Status.Sat)).len(),
                selected_unsat=pl.col("file").filter(selected=True, status=int(defs.Status.Unsat)).len(),
                selected_already_run=pl.col("file").filter(selected=True, run=True).len(),
            )
            .sort(by="logic")
            .collect()
        )

        rich_print_pl(
            f"Statistics on the benchmark selection for {track!s}",
            b3,
            Col("logic", "Logic", footer="Total", justify="left", style="cyan", no_wrap=True, custom=print_logic),
            Col("trivial", "trivial", justify="right", style="green"),
            Col("not_trivial", "not trivial", justify="right", style="orange_red1"),
            Col("old_never_ran", "never compet.", justify="right", style="magenta"),
            Col("new", "new", justify="right", style="magenta1"),
            Col("selected", "selected", justify="right", style="green3"),
            Col("selected_sat", "selected sat", justify="right", style="green4"),
            Col("selected_unsat", "selected unsat", justify="right", style="green4"),
            Col("selected_already_run", "selected already run", justify="right", style="green4"),
        )


@app.command(rich_help_panel=selection_panel)
def show_aws_stats(
    data: Path,
) -> None:
    """
    Show statistics on the benchmarks selected for aws tracks
    """
    config = defs.Config(data)
    benchmarks = smtcomp.selection.helper_aws_selection(config)
    solvers = smtcomp.selection.solver_competing_logics(config).group_by(["track", "logic"]).agg("solver")
    b3 = (
        add_columns(
            benchmarks.group_by(["track", "logic"]).agg(
                n=pl.len(),
                hard=(pl.col("hard") == True).sum(),
                unsolved=(pl.col("unsolved") == True).sum(),
                selected=(pl.col("selected") == True).sum(),
                hard_selected=((pl.col("hard") == True) & (pl.col("selected") == True)).sum(),
                unsolved_selected=((pl.col("unsolved") == True) & (pl.col("selected") == True)).sum(),
            ),
            solvers,
            on=["track", "logic"],
            defaults={"solver": []},
        )
        .sort(by=["track", "logic"])
        .collect()
    )

    rich_print_pl(
        "Statistics on the benchmark selection for AWS tracks",
        b3,
        Col(
            "track",
            "Track",
            footer="Total",
            justify="left",
            style="cyan",
            no_wrap=True,
            custom=defs.Track.name_of_int,
        ),
        Col(
            "logic",
            "Logic",
            footer="",
            justify="left",
            style="cyan",
            no_wrap=True,
            custom=defs.Logic.name_of_int,
        ),
        Col("n", "Benchmarks", justify="right", style="magenta"),
        Col("hard", "Hard", justify="right", style="green"),
        Col("unsolved", "Unsolved", justify="right", style="orange_red1"),
        Col("hard_selected", "Sel. Hard", justify="right", style="green"),
        Col("unsolved_selected", "Sel. Unsolved", justify="right", style="orange_red1"),
        Col("selected", "Selected", justify="right", style="orange_red1"),
        Col(
            "solver",
            "Solvers",
            justify="left",
            custom=lambda x: ", ".join(x),
            footer=lambda df: str(
                (df.select(n=pl.col("solver").list.len() * (pl.col("hard_selected") + pl.col("unsolved_selected"))))[
                    "n"
                ].sum()
            ),
        ),
    )


@app.command(rich_help_panel=selection_panel)
def scramble_aws(
    data: Path,
    srcdir: Path,
    dstdir: Path,
    scrambler: Path,
    max_workers: int = 8,
) -> None:
    """
    Show statistics on the benchmarks selected for aws tracks
    """
    config = defs.Config(data)

    smtcomp.scramble_benchmarks.select_and_scramble_aws(config, srcdir, dstdir, scrambler, max_workers)


def print_iterable(i: int, tree: Tree, a: Any) -> None:
    for k, v in a.items():
        if i == 1:
            tree.add(f"{str(k)}:{v}")
        else:
            t1 = tree.add(str(k))
            print_iterable(i - 1, t1, v)


@app.command(rich_help_panel=data_panel)
def create_cache(data: Path, only_current: bool = False) -> None:
    config = defs.Config(data)
    print("Loading benchmarks")
    bench = defs.Benchmarks.model_validate_json(read_cin(config.benchmarks))
    bd: Dict[defs.Smt2File, int] = {}
    for i, smtfile in enumerate(
        itertools.chain(map(lambda x: x.file, bench.non_incremental), map(lambda x: x.file, bench.incremental))
    ):
        assert smtfile not in bd
        bd[smtfile] = i

    if not only_current:
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
        df.write_ipc(config.cached_non_incremental_benchmarks)

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
        df.write_ipc(config.cached_incremental_benchmarks)

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

    if not only_current:
        results_filtered: list[Any] = []
        for year, file in track(config.previous_results, description="Loading json results"):
            results = defs.Results.model_validate_json(read_cin(file))
            results_filtered.extend(filter(lambda x: x is not None, map(lambda r: convert(r, year), results.results)))

        print("Creating old results cached as feather file")
        df = pl.DataFrame(results_filtered)
        # df["solver"] = df["solver"].astype("string")
        df.write_ipc(config.cached_previous_results)

    for tra, file in config.current_results.items():
        if file.exists():
            print(f"Creating current results for {tra!s} cached as feather file")
            results = defs.Results.model_validate_json(read_cin(file))
            df = pl.DataFrame(
                filter(lambda x: x is not None, map(lambda r: convert(r, config.current_year), results.results))
            )
            df.write_ipc(config.cached_current_results[tra])


@app.command(rich_help_panel=benchexec_panel)
def select_and_scramble(
    competition_track: defs.Track,
    data: Path,
    srcdir: Path,
    cachedir: Path,
    scrambler: Path,
    max_workers: int = 8,
    test: bool = False,
) -> None:
    """
    Selects and scrambles the benchmarks and
    writes them to the destination directory.
    The srcdir must contain all benchmarks as
    outlined in the data.
    """

    config = defs.Config(data)

    if test:
        config.min_used_benchmarks = 20
        config.ratio_of_used_benchmarks = 0.0
        config.invert_triviality = True
        config.seed = 1

    smtcomp.scramble_benchmarks.select_and_scramble(competition_track, config, srcdir, cachedir, scrambler, max_workers)


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
            archive.download_unpack(sub, outdir)
            for part in sub.complete_participations():
                for track, divisions in part.tracks.items():
                    match track:
                        case defs.Track.ModelValidation:
                            statuses = [defs.Status.Sat]
                        case defs.Track.SingleQuery:
                            statuses = [defs.Status.Sat, defs.Status.Unsat]
                        case (
                            defs.Track.Incremental
                            | defs.Track.UnsatCore
                            | defs.Track.ProofExhibition
                            | defs.Track.Cloud
                            | defs.Track.Parallel
                        ):
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


@app.command()
def check_model_locally(
    cachedir: Path, resultdirs: list[Path], max_workers: int = 8, outdir: Optional[Path] = None
) -> None:
    l: list[tuple[results.RunId, results.Run, model_validation.ValidationError]] = []
    with Progress() as progress:
        with ThreadPoolExecutor(max_workers) as executor:
            for resultdir in resultdirs:
                l2 = model_validation.check_results_locally(cachedir, resultdir, executor, progress)
                l.extend(filter_map(map_none3(model_validation.is_error), l2))
    keyfunc = lambda v: v[0].solver
    l.sort(key=keyfunc)
    d = itertools.groupby(l, key=keyfunc)
    t = Tree("Unvalidated models")
    for solver, rs in d:
        t2 = t.add(solver)
        for rid, r, result in rs:
            stderr = result.stderr.strip().replace("\n", ", ")
            basename = smtcomp.scramble_benchmarks.scramble_basename(r.scramble_id)
            t2.add(f"{basename}: {stderr}")
    print(t)
    if outdir is not None:
        for solver, models in d:
            dst = outdir / solver
            dst.mkdir(parents=True, exist_ok=True)
            for rid, r, result in models:
                filedir = benchmark_files_dir(cachedir, rid.track)
                basename = smtcomp.scramble_benchmarks.scramble_basename(r.scramble_id)
                basename_model = smtcomp.scramble_benchmarks.scramble_basename(r.scramble_id, suffix="rsmt2")
                smt2_file = filedir / str(r.logic) / basename
                (dst / basename).unlink(missing_ok=True)
                (dst / basename).symlink_to(smt2_file)
                (dst / basename_model).write_text(result.model)
