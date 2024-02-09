from pathlib import Path
from shutil import unpack_archive
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
    return bool(next(d.iterdir()))


def find_command(command: defs.Command, archive: defs.Archive, dst: Path) -> Path:
    d = archive_cache_dir(archive, dst)
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
                print("current", current, "total", total)
                progress.update(task1, completed=current, total=total)

            y = archive_cache_dir(archive, dst)
            y.mkdir(parents=True, exist_ok=True)
            wget.download(str(archive.url), str(y), bar=bar_progress)
        print("Download done")


def unpack(archive: defs.Archive, dst: Path) -> None:
    dst.joinpath(unpack_dir()).mkdir(parents=True, exist_ok=True)
    archive_file = is_archive_cache_present(archive, dst)
    if not archive_file:
        raise ValueError("unpack ith archive")

    print("unpack archive", archive_file)
    dst.mkdir(parents=True, exist_ok=True)
    udir = archive_unpack_dir(archive, dst)
    unpack_archive(archive_file, udir)  # , filter="data")
    if not (is_unpack_present(archive, dst)):
        print("[red]Empty archive", archive_file)
        exit(1)
