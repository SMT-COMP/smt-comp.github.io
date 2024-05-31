from pathlib import Path

import rich
from rich.tree import Tree

from smtcomp.defs import Submission
import smtcomp.defs as defs


def read(file: str) -> Submission:
    return Submission.model_validate_json(Path(file).read_text())


def tree_summary(s: Submission) -> Tree:
    tree = Tree(f"[bold]{s.name}[/bold]")
    tree.add(f"{len(s.contributors)} authors")
    tree.add(f"website: {s.website}")
    tracks = s.participations.get()
    tree_part = tree.add("Participations")
    for track, divs in sorted(tracks.items()):
        tree_track = tree_part.add(str(track))
        for div, logics in sorted(divs.items()):
            tree_div = tree_track.add(str(div))
            not_logics = defs.tracks[track][div].difference(logics)
            if len(not_logics) == 0:
                tree_div.add("[italic]all[/italic]")
            elif len(not_logics) <= 3 and len(not_logics) < len(logics):
                slogics = map(str, not_logics)
                for logic in sorted(slogics):
                    tree_div.add(f"[strike]{logic}[/strike]")
            else:
                slogics = map(str, logics)
                for logic in sorted(slogics):
                    tree_div.add(logic)
    return tree


def show(s: Submission) -> None:
    rich.print(tree_summary(s))
