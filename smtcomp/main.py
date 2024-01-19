import json
from pathlib import Path

import rich
import typer
from pydantic import ValidationError

import smtcomp.defs as defs
import smtcomp.submission as submission
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
def convert_csv(file: str, dstdir: str) -> None:
    """
    Convert a csv (old submission format) to json files (new format)
    """
    convert_csv_file(Path(file), Path(dstdir))


@app.command()
def dump_json_schema(dst: Path) -> None:
    """
    Dump the json schemas used for submissions at the given file
    """
    with open(dst, "w") as f:
        f.write(json.dumps(defs.Submission.model_json_schema(), indent=2))
