# This module is for the test script in the docker image
# It must use only module from the standard library
from pathlib import Path
import shutil
import subprocess, os
import re


def copy_me(dstdir: Path) -> None:
    shutil.copyfile(src=__file__, dst=dstdir.joinpath("test_solver.py"), follow_symlinks=True)


# copied from tools.py should be factorized
def parse_result(returnsignal: int | None, returncode: int, output: list[str]) -> str:
    if returnsignal is None:
        status = None
        for line in output:
            line = line.strip()
            print(line, file=sys.stderr)
            # ignore
            if re.compile(r"^\s*(success|;.*)?\s*$").match(line):
                continue
            if line == "unsat":
                return "unsat"
            elif line == "sat":
                return "sat"
            else:
                return "unknown"
        return "unknown"

    elif (returnsignal == 9) or (returnsignal == 15):
        status = "timeout"

    elif returnsignal == 9:
        status = "KILLED BY SIGNAL 9"
    elif returnsignal == 6:
        status = "ABORTED"
    elif returnsignal == 15:
        status = "KILLED"
    else:
        status = f"ERROR ({returncode})"

    return status


def init_test() -> None:
    os.chdir(os.path.dirname(__file__))


exit_code = 0


# Try to simulate runexec from benchexec
def test(cmd: str, args: list[str], file: str, expected: str) -> None:
    global exit_code
    all = [cmd] + args + [file]
    print(all, flush=True)
    result = subprocess.run(all, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode < 0:
        returnsignal = -result.returncode
    else:
        returnsignal = None
    answer = parse_result(returnsignal, result.returncode, result.stdout.decode().splitlines())
    if answer != expected:
        print(f"\x1b[1;31mError expected {expected} result obtained {answer}\x1b[0m", flush=True)
        exit_code = 1
    else:
        print("\x1b[1;32mOK\x1b[0m", flush=True)


def end() -> None:
    exit(exit_code)
