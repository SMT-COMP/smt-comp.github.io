import json
from pathlib import Path

import rich
import typer
from pydantic import ValidationError

import smtcomp.archive as archive
import smtcomp.benchexec as benchexec
import smtcomp.defs as defs
import smtcomp.submission as submission
from smtcomp.benchmarks import clone_group
from smtcomp.convert_csv import convert_csv as convert_csv_file

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
    convert_csv_file(Path(file), Path(dstdir))


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
def generate_benchexec(
    file: Path,
    dst: Path,
    cachedir: Path,
    timelimit_s: int = defs.default["timelimit_s"],
    memlimit_M: int = defs.default["memlimit_M"],
    cpuCores: int = defs.default["cpuCores"],
) -> None:
    """
    Generate benchexec files for the given submission
    """
    dst.mkdir(parents=True, exist_ok=True)
    s = submission.read(str(file))
    if s.command and s.archive:
        benchexec.generate_tool_module(s.command, s.archive, s.name, dst, cachedir)
    benchexec.xmls_for_submission(s, timelimit_s, memlimit_M, cpuCores, dst)


@app.command()
def download_archive(file: Path, dst: Path) -> None:
    """
    Download and unpack
    """
    dst.mkdir(parents=True, exist_ok=True)
    s = submission.read(str(file))
    if s.archive:
        archive.download(s.archive, dst)
        archive.unpack(s.archive, dst)
    for p in s.participations.root:
        if p.archive:
            archive.download(p.archive, dst)
            archive.unpack(p.archive, dst)
