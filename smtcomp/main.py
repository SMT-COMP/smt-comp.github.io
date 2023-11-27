import rich
import typer
from pydantic import ValidationError

import smtcomp.submission as submission

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
