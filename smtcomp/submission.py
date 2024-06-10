from pathlib import Path
import rich
from rich.tree import Tree
from rich.progress import track
from typing import Any, TextIO
from smtcomp.defs import Submission
import smtcomp.defs as defs
from github import Github
from github.Repository import Repository
from github.ContentFile import ContentFile
import itertools
import subprocess
import git


def read(file: str) -> Submission:
    return Submission.model_validate_json(Path(file).read_text())


def read_submission_or_exit(file: Path) -> defs.Submission:
    try:
        return read(str(file))
    except Exception as e:
        rich.print(f"[red]Error during file parsing of {file}[/red]")
        print(e)
        exit(1)


def rich_tree_summary(s: Submission) -> Tree:
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


def md_item(md: TextIO, s: str, level: int) -> None:
    md.write("  " * level)
    md.write("* ")
    md.write(s)
    md.write("\n")


def markdown_tree_summary(s: Submission, md: TextIO) -> None:
    md.write(f"#### {s.name}\n\n")
    md_item(md, f"{len(s.contributors)} authors", level=1)
    md_item(md, f"website: {s.website}", level=1)
    tracks = s.participations.get()
    md_item(md, "Participations", level=1)
    for track, divs in sorted(tracks.items()):
        md_item(md, str(track), level=2)
        for div, logics in sorted(divs.items()):
            md_item(md, str(div), level=3)
            not_logics = defs.tracks[track][div].difference(logics)
            if len(not_logics) == 0:
                md_item(md, "_all_", level=4)
            elif len(not_logics) <= 3 and len(not_logics) < len(logics):
                slogics = map(str, not_logics)
                for logic in sorted(slogics):
                    md_item(md, f"~~{logic}~~", level=4)
            else:
                slogics = map(str, logics)
                for logic in sorted(slogics):
                    md_item(md, logic, level=4)


def show(s: Submission) -> None:
    rich.print(rich_tree_summary(s))


def smtcomp_repo(g: Github) -> Repository:
    return g.get_repo("SMT-COMP/smt-comp.github.io")


def commit_exists(repo: git.Repo, sha: str) -> git.Commit | None:
    try:
        return repo.commit(sha)
    except Exception as e:
        return None


def merge_all_submissions(local_repo_path: str) -> None:
    with Github() as g:
        with git.Repo(local_repo_path) as local_repo:
            repo = smtcomp_repo(g)
            pulls = repo.get_pulls(state="open")
            fpulls = [p for p in pulls if "submission" in map(lambda l: l.name, p.labels)]
            for p in track(fpulls, description="Fetch branch", total=pulls.totalCount):
                if commit_exists(local_repo, p.head.sha) is None:
                    print(p.head.repo.ssh_url)
                    subprocess.run(
                        ["git", "-C", local_repo_path, "fetch", "--no-auto-gc", p.head.repo.ssh_url, p.head.ref]
                    )
            print("merge")
            shas = [p.head.sha for p in fpulls]
            message = "merge submissions\n\n" + "\n".join(f"#{p.number}: {p.title}" for p in fpulls)
            print(shas)
            subprocess.run(["git", "-C", local_repo_path, "merge", "-m", message] + shas)
