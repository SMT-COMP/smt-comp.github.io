from __future__ import annotations
from types import TracebackType
from typing import TypeVar, Union, Iterable, Sequence, Optional, Callable, Tuple

import time

ProgressType = TypeVar("ProgressType")

import gitlab
import subprocess
from rich.progress import Progress
from pathlib import Path
from operator import length_hint

import git
from rich import console, progress
from rich.progress import _TrackThread


class GitRemoteProgress(git.RemoteProgress):
    """
    From https://stackoverflow.com/questions/51045540/python-progress-bar-for-git-clone
    """

    OP_CODES = [
        "BEGIN",
        "CHECKING_OUT",
        "COMPRESSING",
        "COUNTING",
        "END",
        "FINDING_SOURCES",
        "RECEIVING",
        "RESOLVING",
        "WRITING",
    ]
    OP_CODE_MAP = {getattr(git.RemoteProgress, _op_code): _op_code for _op_code in OP_CODES}

    def __init__(self) -> None:
        super().__init__()
        self.progressbar = progress.Progress(
            progress.SpinnerColumn(),
            # *progress.Progress.get_default_columns(),
            progress.TextColumn("[progress.description]{task.description}"),
            progress.BarColumn(),
            progress.TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            "eta",
            progress.TimeRemainingColumn(),
            progress.TextColumn("{task.fields[message]}"),
            console=console.Console(),
            transient=False,
            auto_refresh=False,
        )
        self.progressbar.start()
        self.active_task: Progress.TaskId | None = None

    def __del__(self) -> None:
        # logger.info("Destroying bar...")
        self.progressbar.stop()

    @classmethod
    def get_curr_op(cls, op_code: int) -> str:
        """Get OP name from OP code."""
        # Remove BEGIN- and END-flag and get op name
        op_code_masked = op_code & cls.OP_MASK
        return cls.OP_CODE_MAP.get(op_code_masked, "?").title()

    def update(
        self,
        op_code: int,
        cur_count: str | float,
        max_count: str | float | None = None,
        message: str | None = "",
    ) -> None:
        # Start new bar on each BEGIN-flag
        if op_code & self.BEGIN:
            self.curr_op = self.get_curr_op(op_code)
            # logger.info("Next: %s", self.curr_op)
            self.active_task = self.progressbar.add_task(
                description=self.curr_op,
                total=float(max_count) if max_count else None,
                message=message,
            )

        if self.active_task:
            # Should always be set if protocol respected
            self.progressbar.update(
                task_id=self.active_task,
                completed=float(cur_count),
                message=message,
            )

            # End progress monitoring on each END-flag
            if op_code & self.END:
                # logger.info("Done: %s", self.curr_op)
                self.progressbar.update(
                    task_id=self.active_task,
                    message=f"[bright_black]{message}",
                )

    @classmethod
    def __enter__(cls) -> GitRemoteProgress:
        return GitRemoteProgress()

    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None:
        self.progressbar.__exit__(exc_type, exc_val, exc_tb)


def track(
    progress: Progress,
    sequence: Union[Iterable[ProgressType], Sequence[ProgressType]],
    total: float | None = None,
    task_id: Optional[progress.TaskID] = None,
    description: str = "Working...",
    update_period: float = 0.1,
) -> Iterable[Tuple[(Callable[[str], None]), ProgressType]]:
    """Track progress by iterating over a sequence.

    Args:
        sequence (Sequence[ProgressType]): A sequence of values you want to iterate over and track progress.
        total: (float, optional): Total number of steps. Default is len(sequence).
        task_id: (TaskID): Task to track. Default is new task.
        description: (str, optional): Description of task, if new task is created.
        update_period (float, optional): Minimum time (in seconds) between calls to update(). Defaults to 0.1.

    Returns:
        Iterable[ProgressType]: An iterable of values taken from the provided sequence.
    """
    if total is None:
        total = float(length_hint(sequence)) or None

    if task_id is None:
        task_id = progress.add_task(description, total=total, message="")
    else:
        progress.update(task_id, total=total, message="")

    def update_message(message: str) -> None:
        progress.update(task_id, total=total, message=message)

    if progress.live.auto_refresh:
        with _TrackThread(progress, task_id, update_period) as track_thread:
            for value in sequence:
                yield (update_message, value)
                track_thread.completed += 1
    else:
        advance = progress.advance
        refresh = progress.refresh
        for value in sequence:
            yield (update_message, value)
            advance(task_id, 1)
            refresh()


gl = gitlab.Gitlab("https://clc-gitlab.cs.uiowa.edu:2443")


class P:
    def __init__(self, i: int) -> None:
        self.name = "Project" + str(i)
        self.http_url_to_repo = self.name

    def __str__(self) -> str:
        return self.name


class MyNumbers:
    def __iter__(self) -> MyNumbers:
        self.a = 1
        return self

    def __next__(self) -> P:
        x = self.a
        time.sleep(0.5)
        self.a += 1
        if x < 5:
            return P(x)
        else:
            raise StopIteration


def clone_group(name: str, dir: Path, dryrun: bool) -> None:
    """clone the group named name in directory dir"""
    with GitRemoteProgress() as gitprogress:
        progress = gitprogress.progressbar
        progress.console.print("Start downloading benchmarks:", name)
        # group = gl.groups.get(name)
        # projects = list(progress.track(group.projects.list(iterator=True), description="List logics..."))
        projects = [p for _, p in track(progress, iter(MyNumbers()), description="List logics...", total=6)]
        dir.mkdir(exist_ok=True, parents=True)
        for update_message, project in track(progress, projects, description="Downloading..."):
            update_message(project.name)
            if project.name in ["QF_BV_legacy", "Sage2_legacy"]:
                progress.console.print(project.name, "skipped")
                continue
            path = dir.joinpath(project.name)
            if path.exists():
                update_message(project.name + " update")
                if dryrun:
                    time.sleep(0.5)
                else:
                    subprocess.run(["git", "-C", path, "fetch", "--depth=1"])
                    subprocess.run(["git", "-C", path, "reset", "--hard", "FETCH_HEAD"])
            else:
                update_message(project.name + " clone")
                if dryrun:
                    time.sleep(0.5)
                else:
                    git.Repo.clone_from(
                        url=project.http_url_to_repo,
                        to_path=path,
                        depth=1,
                        progress=gitprogress.update,
                    )
