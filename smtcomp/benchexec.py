from pathlib import Path
from os.path import relpath
from typing import List, cast, Dict, Optional

from yattag import Doc, indent

from smtcomp import defs
from smtcomp.archive import find_command, archive_unpack_dir
from pydantic import BaseModel

import shlex
from re import sub

class CmdTask(BaseModel):
    name: str
    options: List[str]
    includesfiles: List[str]


def tool_module_name(s: defs.Submission) -> str:
    return sub(r'\W+', '', s.name.lower())


def generate_tool_module(s: defs.Submission, cachedir: Path) -> None:
    name = tool_module_name(s)

    file = cachedir / "tools" / f"{name}.py"
    with file.open("w") as f:

        f.write("from tools.tool import SMTCompTool\n\n")
        f.write("class Tool(SMTCompTool):  # type: ignore\n")

        f.write(f"    NAME = '{s.name}'\n")
        if s.command is not None:
            assert s.archive is not None
            executable_path = find_command(s.command, s.archive, cachedir)
            executable = str(relpath(executable_path, start=str(cachedir)))
            f.write(f"    EXECUTABLE = '{executable}'\n")

        required_paths = []

        if s.archive is not None:
            archive_path = relpath(archive_unpack_dir(s.archive, cachedir), start=str(cachedir))
            required_paths.append(str(archive_path))
        for p in s.participations.root:
            if p.archive is not None:
                archive_path = relpath(archive_unpack_dir(p.archive, cachedir), start=str(cachedir))
                required_paths.append(str(archive_path))
        if required_paths:
            f.write(f"    REQUIRED_PATHS = {required_paths}\n")


def generate_xml(timelimit_s: int, memlimit_M: int, cpuCores: int, cmdtasks: List[CmdTask], cachedir: Path, tool_module_name: str) -> None:
    doc, tag, text = Doc().tagtext()

    doc.asis('<?xml version="1.0"?>')
    doc.asis(
        '<!DOCTYPE benchmark PUBLIC "+//IDN sosy-lab.org//DTD BenchExec benchmark 2.3//EN"'
        ' "https://www.sosy-lab.org/benchexec/benchmark-2.2.3dtd">'
    )
    with tag(
        "benchmark",
        tool=f"tools.{tool_module_name}",
        timelimit=f"{timelimit_s}s",
        hardlimit=f"{timelimit_s+30}s",
        memlimit=f"{memlimit_M} MB",
        cpuCores=f"{cpuCores}"
    ):
        for cmdtask in cmdtasks:
            for includesfile in cmdtask.includesfiles:
                with tag("rundefinition", name=f"{cmdtask.name},{includesfile}"):
                    for option in cmdtask.options:
                        with tag("option"):
                            text(option)
                    with tag("tasks", name="task"):
                        with tag("includesfile"):
                            text(f"benchmarks/{includesfile}")

    file = cachedir.joinpath(f"{tool_module_name}.xml")
    file.write_text(indent(doc.getvalue()))


def get_suffix(track: defs.Track):
    match track:
        case defs.Track.Incremental:
            return "_inc"
        case defs.Track.ModelValidation:
            return "_model"
        case _:
            return ""

def cmdtask_for_submission(s: defs.Submission, cachedir: Path) -> List[CmdTask]:
    res: List[CmdTask] = []
    i = -1
    for p in s.participations.root:
        command = cast(defs.Command, p.command if p.command else s.command)
        archive = cast(defs.Archive, p.archive if p.archive else s.archive)
        for track, divisions in p.get().items():
            i = i + 1
            suffix = get_suffix(track)
            match track:
                case defs.Track.Incremental:
                    mode = "trace"
                    continue
                case defs.Track.ModelValidation:
                    mode = "direct"
                    continue
                case defs.Track.UnsatCore:
                    mode = "direct"
                    continue
                case defs.Track.ProofExhibition:
                    mode = "direct"
                    continue
                case defs.Track.SingleQuery:
                    mode = "direct"
                case defs.Track.Cloud | defs.Track.Parallel:
                    continue
            tasks: list[str] = []
            for _, logics in divisions.items():
                tasks.extend([str(logic) + suffix for logic in logics])
            if tasks:
                executable_path = find_command(command, archive, cachedir)
                executable = str(relpath(executable_path, start=str(cachedir)))
                if command.compa_starexec:
                    assert command.arguments == []
                    dirname = str(relpath(executable_path.parent, start=str(cachedir)))

                    if mode == "direct":
                        options = [
                            "bash",
                            "-c",
                            f'FILE=$(realpath $1); (cd {shlex.quote(dirname)}; exec ./{shlex.quote(executable_path.name)} "$FILE")',
                            "compa_starexec",
                        ]
                    else:
                        assert mode == "trace"
                        options = [
                            "bash",
                            "-c",
                            f'ROOT=$(pwd); FILE=$(realpath $1); (cd {shlex.quote(dirname)}; exec $ROOT/smtlib2_trace_executor ./{shlex.quote(executable_path.name)} "$FILE")',
                            "compa_starexec",
                        ]
                else:
                    if mode == "direct":
                        options = [executable] + command.arguments
                    else:
                        options = ["./smtlib2_trace_executor", executable] + command.arguments
                cmdtask = CmdTask(
                    name=f"{s.name},{i},{track}",
                    options=options,
                    includesfiles=tasks,
                )
                res.append(cmdtask)
    return res
