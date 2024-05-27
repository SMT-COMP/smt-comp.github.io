# This module is for the test script in the docker image
# It must use only module from the standard library
from pathlib import Path
import shutil
import subprocess, os


def copy_me(dstdir: Path) -> None:
    shutil.copyfile(src=__file__, dst=dstdir.joinpath("test_solver.py"), follow_symlinks=True)


def init_test() -> None:
    os.chdir(os.path.dirname(__file__))


def test(cmd: str, args: list[str], file: str) -> None:
    all = [cmd] + args + [file]
    print(all, flush=True)
    subprocess.run(all)
