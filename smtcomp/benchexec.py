from pathlib import Path
from typing import List, cast

from yattag import Doc

from smtcomp import defs
from smtcomp.archive import find_command


def generate_tool_module(command: defs.Command, archive: defs.Archive, name: str, dstdir: Path, cachedir: Path) -> None:
    code = f"""
import benchexec.util as util
import benchexec.tools.smtlib2


class Tool(benchexec.tools.smtlib2.Smtlib2Tool):
    \"""
    Tool info for {name} generated by smtcomp command.
    \"""

    def executable(self):
        return util.find_executable({find_command(command,archive,cachedir)!r})

    def version(self, executable):
        return ""

    def name(self):
        return {name!r}

    def cmdline(self, executable, options, tasks, propertyfile=None, rlimits={{}}):
        assert len(tasks) <= 1, "only one inputfile supported"
        return [executable] + {command.arguments!r} + options + tasks
    """
    # Check the parsing of the file directly
    compile(code, "<string>", "exec")
    dstdir.joinpath(f"tool_{command.uniq_id(name,archive)}.py").write_text(code)


def generate_xml(
    command: defs.Command,
    archive: defs.Archive,
    name: str,
    timelimit_s: int,
    memlimit_M: int,
    cpuCores: int,
    tasks: List[str],
    file: Path,
) -> None:
    doc, tag, text = Doc().tagtext()

    doc.asis('<?xml version="1.0"?>')
    doc.asis(
        '<!DOCTYPE benchmark PUBLIC "+//IDN sosy-lab.org//DTD BenchExec benchmark 2.3//EN" "https://www.sosy-lab.org/benchexec/benchmark-2.2.3dtd">'
    )
    with tag(
        "benchmark",
        tool=f"tools.tool_{command.uniq_id(name,archive)}",
        timelimit=f"{timelimit_s}s",
        hardlimit=f"{timelimit_s+30}s",
        memlimit=f"{memlimit_M} MB",
        cpuCores=f"{cpuCores}",
    ):
        tag("rundefinition", name="default")
        for task in tasks:
            with tag("tasks", name="task"):
                with tag("includesfile"):
                    text(task)

    file.write_text(doc.getvalue())


def tool_module_for_submission(s: defs.Submission, dst: Path, cachedir: Path) -> None:
    id = s.uniq_id()
    if s.command and s.archive:
        generate_tool_module(s.command, s.archive, s.name, dst, cachedir)
    for i, p in enumerate(s.participations.root):
        if p.command or p.archive:
            command = cast(defs.Command, p.command if p.command else s.command)
            archive = cast(defs.Archive, p.archive if p.archive else s.archive)
            generate_tool_module(command, archive, s.name, dst, cachedir)


def xmls_for_submission(s: defs.Submission, timelimit_s: int, memlimit_M: int, cpuCores: int, dst: Path) -> None:
    id = s.uniq_id()
    for i, p in enumerate(s.participations.root):
        command = cast(defs.Command, p.command if p.command else s.command)
        archive = cast(defs.Archive, p.archive if p.archive else s.archive)
        file = dst.joinpath("{id}_{i}.xml")
        tasks: list[str] = []
        for track, divisions in p.get().items():
            for _, logics in divisions.items():
                match track:
                    case defs.Track.Incremental:
                        suffix = "_inc"
                    case defs.Track.ModelValidation:
                        suffix = "_model"
                    case _:
                        suffix = ""
                tasks.append(*[logic + suffix for logic in logics])
        if tasks:
            generate_xml(command, archive, s.name, timelimit_s, memlimit_M, cpuCores, tasks, file)