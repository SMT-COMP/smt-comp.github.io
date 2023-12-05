from pathlib import Path

import rich

from smtcomp.defs import Submission


def read(file: str) -> Submission:
    return Submission.model_validate_json(Path(file).read_text())


def show(s: Submission) -> None:
    rich.print(f"[bold]{s.name}:[/bold]")
    rich.print(f"  - {len(s.authors)} authors")
    rich.print(f"  - url: {s.website}")
