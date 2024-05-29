from pathlib import Path
from smtcomp.unpack import extract_all_with_executable_permission

import wget
from rich import print


def trace_executor_url() -> str:
    return (
        "https://github.com/SMT-COMP/trace-executor/releases/download/smtcomp2022/SMT-COMP-2022-trace-executor.tar.gz"
    )


def trace_executor_filename() -> str:
    return "SMT-COMP-2022-trace-executor.tar.gz"


def download_trace_executor(dst: Path) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    url = trace_executor_url()
    wget.download(url, str(dst))
    print("Download done")


def unpack_trace_executor(dst: Path) -> None:
    filename = trace_executor_filename()
    extract_all_with_executable_permission(dst.joinpath(filename), dst)
    print("Unpacking done")


import subprocess


def copy_tool_module(dst: Path) -> None:
    script_path = Path(__file__).parent
    tools = dst / "tools"
    tools.mkdir(parents=True, exist_ok=True)
    subprocess.run(["cp", script_path / "tool.py", tools])
    subprocess.run(["touch", "__init__.py"])
