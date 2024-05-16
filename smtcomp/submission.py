from pathlib import Path

import rich
from rich.tree import Tree

from smtcomp.defs import Submission


def read(file: str) -> Submission:
    return Submission.model_validate_json(Path(file).read_text())


def show(s: Submission) -> None:
    tree = Tree(f"[bold]{s.name}[/bold]")
    tree.add(f"{len(s.contributors)} authors")
    tree.add(f"website: {s.website}")
    tracks = s.participations.get()
    tree_part = tree.add("Participations")
    for track, divs in sorted(tracks.items()):
        tree_track = tree_part.add(str(track))
        for div, logics in sorted(divs.items()):
            tree_div = tree_track.add(str(div))
            slogics = map(str, logics)
            for logic in sorted(slogics):
                tree_div.add(logic)
    rich.print(tree)
