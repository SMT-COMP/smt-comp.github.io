from pathlib import Path
import rich
from os.path import relpath
from typing import List, cast, Dict, Optional

from yattag import Doc, indent

from smtcomp import defs
from smtcomp.archive import find_command, archive_unpack_dir, command_path
from pydantic import BaseModel

import shlex
from re import sub


def get_suffix(track: defs.Track) -> str:
    match track:
        case defs.Track.Incremental:
            return "_inc"
        case defs.Track.ModelValidation:
            return "_model"
        case defs.Track.UnsatCore:
            return "_unsatcore"
        case defs.Track.SingleQuery:
            return ""
        case _:
            raise ValueError("No Cloud or Parallel")


def get_xml_name(s: defs.Submission, track: defs.Track, division: defs.Division) -> str:
    suffix = get_suffix(track)
    return sub(r"\W+", "", s.name.lower()) + suffix + "_" + str(division) + ".xml"


def tool_module_name(s: defs.Submission, incremental: bool) -> str:
    suffix = "_inc" if incremental else ""
    return sub(r"\W+", "", s.name.lower()) + suffix


class CmdTask(BaseModel):
    name: str
    options: List[str]
    taskdirs: List[str]


def generate_benchmark_yml(benchmark: Path, expected_result: Optional[bool], orig_file: Optional[Path]) -> None:
    ymlfile = benchmark.with_suffix(".yml")
    with ymlfile.open("w") as f:
        f.write("format_version: '2.0'\n\n")

        f.write(f"input_files: '{str(benchmark.name)}'\n\n")

        if orig_file is not None:
            f.write(f"# original_files: '{str(orig_file)}'\n\n")

        expected_str = "true" if expected_result else "false"
        f.write("properties:\n")
        f.write(f"  - property_file: '../../properties/SMT.prp'\n")
        if expected_result is not None:
            f.write(f"    expected_verdict: {expected_str}\n")


def generate_tool_module(s: defs.Submission, cachedir: Path, incremental: bool) -> None:
    name = tool_module_name(s, incremental)
    file = cachedir / "tools" / f"{name}.py"

    with file.open("w") as f:
        if incremental:
            base_module = "incremental_tool"
            base_class = "IncrementalSMTCompTool"
        else:
            base_module = "tool"
            base_class = "SMTCompTool"
        f.write(f"from tools.{base_module} import {base_class}\n\n")
        f.write(f"class Tool({base_class}):  # type: ignore\n")

        f.write(f"    NAME = '{s.name}'\n")
        if s.command is not None:
            assert s.archive is not None
            if s.command.compa_starexec:
                executable_path = find_command(s.command, s.archive, cachedir)
                executable = str(relpath(executable_path, start=str(cachedir)))
            else:
                executable = str(command_path(s.command, s.archive, Path()))
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


def generate_tool_modules(s: defs.Submission, cachedir: Path) -> None:
    generate_tool_module(s, cachedir, True)
    generate_tool_module(s, cachedir, False)


def generate_xml(config: defs.Config, cmdtasks: List[CmdTask], file: Path, tool_module_name: str) -> None:
    doc, tag, text = Doc().tagtext()

    doc.asis('<?xml version="1.0"?>')
    doc.asis(
        '<!DOCTYPE benchmark PUBLIC "+//IDN sosy-lab.org//DTD BenchExec benchmark 2.3//EN"'
        ' "https://www.sosy-lab.org/benchexec/benchmark-2.2.3dtd">'
    )
    with tag(
        "benchmark",
        tool=f"tools.{tool_module_name}",
        walltimelimit=f"{config.timelimit_s}s",
        memlimit=f"{config.memlimit_M} MB",
        cpuCores=f"{config.cpuCores}",
    ):
        with tag("require", cpuModel="Intel Xeon E3-1230 v5 @ 3.40 GHz"):
            text()

        with tag("resultfiles"):
            text("**/error.log")

        for cmdtask in cmdtasks:
            with tag("rundefinition", name=f"{cmdtask.name}"):
                for option in cmdtask.options:
                    with tag("option"):
                        text(option)
                with tag("tasks", name="task"):
                    for taskdir in cmdtask.taskdirs:
                        with tag("include"):
                            text(f"{taskdir}/*.yml")

        with tag("propertyfile"):
            text("benchmarks/properties/SMT.prp")

    file.write_text(indent(doc.getvalue()))


def cmdtask_for_submission(s: defs.Submission, cachedir: Path, target_track: defs.Track, target_division: defs.Division) -> List[CmdTask]:
    res: List[CmdTask] = []
    i = -1
    for p in s.participations.root:
        command = cast(defs.Command, p.command if p.command else s.command)
        archive = cast(defs.Archive, p.archive if p.archive else s.archive)
        for track, divisions in p.get().items():
            if track != target_track:
                continue

            i = i + 1
            suffix = get_suffix(track)
            taskdirs: list[str] = [f"../benchmarks/files{suffix}/{logic}" for logic in divisions.get(target_division, [])]

            if taskdirs:
                if command.compa_starexec:
                    assert command.arguments == []
                    executable_path = find_command(command, archive, cachedir)
                    executable = str(relpath(executable_path, start=str(cachedir)))
                    dirname = str(relpath(executable_path.parent, start=str(cachedir)))

                    options = [
                        "bash",
                        "-c",
                        f'FILE=$(realpath $1); (cd {shlex.quote(dirname)}; exec ./{shlex.quote(executable_path.name)} "$FILE")',
                        "compa_starexec",
                    ]
                else:
                    executable = str(command_path(command, archive, Path()))
                    options = [executable] + command.arguments
                cmdtask = CmdTask(
                    name=f"{s.name},{i},{track}",
                    options=options,
                    taskdirs=taskdirs,
                )
                res.append(cmdtask)
    return res


def generate(s: defs.Submission, cachedir: Path, config: defs.Config) -> None:
    generate_tool_modules(s, cachedir)

    dst = cachedir / "benchmarks"
    prop_dir = dst.joinpath("properties")
    prop_dir.mkdir(parents=True, exist_ok=True)
    (prop_dir / "SMT.prp").touch()

    run_defs = cachedir / "run_definitions"
    run_defs.mkdir(parents=True, exist_ok=True)

    for target_track, divisions in defs.tracks.items():
        for division in divisions.keys():
            res = cmdtask_for_submission(s, cachedir, target_track, division)
            if res:
                basename = get_xml_name(s, target_track, division)
                file = run_defs / basename
                generate_xml(
                    config=config,
                    cmdtasks=res,
                    file=file,
                    tool_module_name=tool_module_name(s, target_track == defs.Track.Incremental),
                )
