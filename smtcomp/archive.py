from pathlib import Path
from smtcomp.unpack import extract_all_with_executable_permission
import zipfile
from typing import Optional

import wget
from rich import print
from rich.progress import Progress

from smtcomp import defs


def cache_dir() -> str:
    return "download"


def unpack_dir() -> str:
    return "unpack"


def archive_cache_dir(archive: defs.Archive, dst: Path) -> Path:
    return dst.joinpath(cache_dir(), archive.uniq_id())


def archive_unpack_dir(archive: defs.Archive, dst: Path) -> Path:
    return dst.joinpath(unpack_dir(), archive.uniq_id())


def is_archive_cache_present(archive: defs.Archive, dst: Path) -> Optional[Path]:
    d = archive_cache_dir(archive, dst)
    d.mkdir(parents=True, exist_ok=True)
    return next(d.iterdir(), None)


def is_unpack_present(archive: defs.Archive, dst: Path) -> bool:
    d = archive_unpack_dir(archive, dst)
    d.mkdir(parents=True, exist_ok=True)
    return any(True for _ in d.iterdir())


def command_path(command: defs.Command, archive: defs.Archive, dst: Path) -> Path:
    return archive_unpack_dir(archive, dst).joinpath(command.binary)


def find_command(command: defs.Command, archive: defs.Archive, dst: Path) -> Path:
    d = archive_unpack_dir(archive, dst)
    if not (d.exists()):
        raise Exception("Archive not unpacked", archive)
    path = d.joinpath(command.binary)
    if path.exists():
        return path
    possibilities = list(d.rglob(command.binary))
    if len(possibilities) == 0:
        raise Exception("Command not found in the archive", command, archive)
    if len(possibilities) >= 2:
        raise Exception("Too many candidate for the command", command, archive, possibilities)
    return possibilities[0]


def download(archive: defs.Archive, dst: Path) -> None:
    dst.joinpath(cache_dir()).mkdir(parents=True, exist_ok=True)
    x = is_archive_cache_present(archive, dst)
    if x:
        print("archive in cache:", x)
    else:
        with Progress() as progress:
            task1 = progress.add_task("[red]Downloading...")

            # create this bar_progress method which is invoked automatically from wget
            def bar_progress(current: float, total: float, width: int) -> None:
                progress.update(task1, completed=current, total=total)

            y = archive_cache_dir(archive, dst)
            y.mkdir(parents=True, exist_ok=True)
            wget.download(str(archive.url), str(y), bar=bar_progress)
        print("Download done")


import subprocess


# For testing with last year final solver we need some patch
# on starexec things seems to be executed particularly
def patch(udir: Path) -> None:
    if udir.name == "e0873e12a04fcfcf1bf2e449f04101c2812d4c533fb634beb6e92e8eaa6d78f7":
        # For COLIBRI
        subprocess.run(["chmod", "-R", "u+x", udir.joinpath("COLIBRI 2023_05_10")])
        subprocess.run(["mv", udir.joinpath("COLIBRI 2023_05_10"), udir.joinpath("COLIBRI_2023_05_10")])


def unpack(archive: defs.Archive, dst: Path) -> None:
    dst.joinpath(unpack_dir()).mkdir(parents=True, exist_ok=True)
    archive_file = is_archive_cache_present(archive, dst)
    if not archive_file:
        raise ValueError("unpack ith archive")

    dst.mkdir(parents=True, exist_ok=True)
    udir = archive_unpack_dir(archive, dst)
    if is_unpack_present(archive, dst):
        print("archive already unpacked:", udir)
    else:
        print("unpack archive", archive_file)
        extract_all_with_executable_permission(archive_file, udir)
        patch(udir)
    if not (is_unpack_present(archive, dst)):
        print("[red]Empty archive", archive_file)
        exit(1)


def download_unpack(s: defs.Submission, dst: Path) -> None:
    """
    Download and unpack
    """
    dst.mkdir(parents=True, exist_ok=True)
    if s.archive:
        download(s.archive, dst)
        unpack(s.archive, dst)
    for p in s.participations.root:
        if p.archive:
            download(p.archive, dst)
            unpack(p.archive, dst)
