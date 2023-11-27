import typer
import smtcomp.solver as solver

from pathlib import Path
from pydantic import ValidationError

app = typer.Typer()

@app.command()
def show(file:str ):
    """
    Show information about a solver submission
    """


@app.command()
def validate(file:str ):
    """
    Validate a json defining a solver submission
    """
    try:
        solver.Solver.model_validate_json(Path(file).read_text())
    except ValidationError as e:
        print(e)
        exit(1)