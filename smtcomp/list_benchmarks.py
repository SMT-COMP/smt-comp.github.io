from typing import Set, Dict, Optional, cast, List
from pathlib import Path, PurePath
from smtcomp import defs
import subprocess
import re
from rich.progress import track
import concurrent.futures


def get_status(src: Path) -> defs.Status:
    with src.open() as fd_src:
        grep = subprocess.run(
            ["grep", "([ \t]*set-info[ \t][ \t]*:status[ \t].*[ \t]*)"], capture_output=True, text=True, stdin=fd_src
        )
    l = re.findall(r'[ \t]"?(unsat|sat|unknown)"?', grep.stdout)
    if len(l) == 1:
        return defs.Status(l[0])
    else:
        raise ValueError(f"Can't find status in {src}: { grep.stdout } and {l}")


def get_nb_asserts_with_scrambler(src: Path, scrambler: Path) -> int:
    with src.open() as fd_src:
        pscrambler = subprocess.run(
            [scrambler, "-count-asserts", "true"], stderr=subprocess.PIPE, text=True, stdin=fd_src
        )
    l = re.findall(r"Number of assertions: ([0-9][0-9]*)", pscrambler.stderr)
    if len(l) == 1:
        return int(l[0])
    else:
        raise ValueError(f"Can't compute asserts in {src}: { pscrambler.stderr } and {l}")


def get_nb_asserts_with_grep(src: Path) -> int:
    with src.open() as fd_src:
        grep = subprocess.run(
            ["grep", "-c", r"([[:space:]]*assert\([[:space:]]\|$\)"], capture_output=True, text=True, stdin=fd_src
        )
    return int(grep.stdout)


def get_nb_asserts(src: Path, scrambler: Optional[Path]) -> int:
    if scrambler is None:
        return get_nb_asserts_with_grep(src)
    else:
        return get_nb_asserts_with_scrambler(src, scrambler)


def get_nb_check_sats(src: Path) -> int:
    with src.open() as fd_src:
        grep = subprocess.run(["grep", "-c", "(check-sat)"], capture_output=True, text=True, stdin=fd_src)
    return int(grep.stdout)


def get_smt2_file(src: Path | None, file: Path, incremental: bool) -> defs.Smt2File:
    if src is None:
        p = list(PurePath(file).parts)
        parts: tuple[str, ...] = tuple()
        for i in range(0, len(p) - 1):
            if p[i] in defs.Logic.__members__:
                parts = tuple(p[i:])
                break
    else:
        parts = PurePath(file.relative_to(src)).parts

    return defs.Smt2File(
        incremental=incremental,
        logic=defs.Logic(parts[0]),
        family=parts[1:-1],
        name=parts[-1],
    )


def get_info_smt2_file(
    src: Path, file: Path, scrambler: Optional[Path], incremental: bool
) -> defs.InfoIncremental | defs.InfoNonIncremental:
    if incremental:
        return defs.InfoIncremental(
            file=get_smt2_file(src, file, True),
            check_sats=get_nb_check_sats(file),
        )
    else:
        return defs.InfoNonIncremental(
            file=get_smt2_file(src, file, False),
            status=get_status(file),
            asserts=get_nb_asserts(file, scrambler),
        )


def list_benchmarks(
    src: Path, scrambler: Optional[Path], max_workers: int, incremental: bool
) -> List[defs.InfoIncremental | defs.InfoNonIncremental]:
    l = list(track(src.rglob("*.smt2"), description="Scanning directories..."))
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        files = list(
            track(
                executor.map(lambda file: get_info_smt2_file(src, file, scrambler, incremental), l),
                total=len(l),
                description="Scanning files...",
            )
        )
    files.sort(key=(lambda k: k.file.path()))
    return files
