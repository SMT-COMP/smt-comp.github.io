from typing import Optional, Iterator, Any
import functools
import smtcomp.defs as defs
import polars as pl
import xml.etree.ElementTree as ET
from pathlib import Path
from smtcomp.unpack import read_cin
from pydantic import BaseModel
from datetime import timedelta
from zipfile import ZipFile


class RunId(BaseModel):
    solver: str
    participation: int
    track: defs.Track
    includefile: str

    @classmethod
    def unmangle(cls, s: str) -> "RunId":
        name_l = s.split(",")
        return RunId(
            solver=name_l[0],
            participation=int(name_l[1]),
            track=defs.Track(name_l[2]),
            # The name "task" is currently added at the end, name of the task
            includefile=name_l[3].split(".")[0],
        )

    def mangle(self) -> str:
        return ",".join([self.solver, str(self.participation), str(self.track), self.includefile])


class Run(BaseModel):
    basename: str
    cputime_s: float
    """ example: 0.211880968s"""
    memory_B: int
    """ example: 21127168B"""
    status: str
    """ example: true"""
    walltime_s: float
    """ example: 0.21279739192686975s"""

    # host: str
    # """ example: pontos07"""
    # blkio-read: str
    # """ example: 0B """
    # blkio-write: str
    # """ example: 0B """
    # category: str
    # """ example: missing """
    # cpuCores: str
    # """ example: 0 """
    # cputime-cpu0: str
    # """ example: 0.211880968s """
    # memoryNodes: str
    # """ example: 0 """
    # returnvalue: str
    # """ example: 1 """
    # starttime: str
    # """ example: 2024-06-07T19:57:32.499898+02:00"""
    # vcloud-additionalEnvironment: str
    # """ example: """
    # vcloud-cpuCoresDetails: str
    # """ example: [Processor{0, core=0, socket=0} """
    # vcloud-debug: str
    # """ example: false """
    # vcloud-generatedFilesCount: str
    # """ example: 1 """
    # vcloud-matchedResultFilesCount: str
    # """ example: 1 """
    # vcloud-maxLogFileSize: str
    # """ example: 20 MB """
    # vcloud-memoryNodesAllocation: str
    # """ example: {0=2.0 GB} """
    # vcloud-newEnvironment: str
    # """ example: """
    # vcloud-outerwalltime: str
    # """ example: 0.554s """
    # vcloud-runId: str
    # """ example: 6a08ebbd-2af2-4c18-af44-429a0439fab """


class Results(BaseModel):
    runid: RunId
    options: str
    runs: list[Run]


def parse_time(s: str) -> float:
    assert s[-1] == "s"
    return float(s[:-1])


def parse_size(s: str) -> int:
    assert s[-1] == "B"
    return int(s[:-1])


def convert_run(r: ET.Element) -> Run:
    basename = Path(r.attrib["name"]).name
    cputime_s: Optional[float] = None
    memory_B: Optional[int] = None
    status: Optional[str] = None
    walltime_s: Optional[float] = None

    for col in r.iterfind("column"):
        value = col.attrib["value"]
        match col.attrib["title"]:
            case "cputime":
                cputime_s = parse_time(value)
            case "memory":
                memory_B = parse_size(value)
            case "status":
                status = value
            case "walltime":
                walltime_s = parse_time(value)

    if cputime_s is None or memory_B is None or status is None or walltime_s is None:
        raise ValueError("xml of results doesn't contains some expected column")

    return Run(basename=basename, cputime_s=cputime_s, memory_B=memory_B, status=status, walltime_s=walltime_s)


def parse_xml(file: Path) -> Results:
    result = ET.fromstring(read_cin(file))
    runs = list(map(convert_run, result.iterfind("run")))
    return Results(runid=RunId.unmangle(result.attrib["name"]), options=result.attrib["options"], runs=runs)


def to_pl(r: Results) -> pl.LazyFrame:
    lf = pl.LazyFrame(r.runs)
    return lf.with_columns(solver=pl.lit(r.runid.solver), participation=r.runid.participation, track=int(r.runid.track))


def parse_dir(dir: Path) -> pl.LazyFrame:
    return pl.concat(map(lambda file: to_pl(parse_xml(file)), dir.glob("*.xml.bz2")))


def log_filename(dir: Path) -> Path:
    l = list(dir.glob("*.logfiles.zip"))
    if len(l) != 1:
        raise (ValueError(f"Directory {dir!r} doesn't contains *.logfiles.zip archive"))
    return l[0]


### Benchexec add this header
# output_file.write(
#     " ".join(map(util.escape_string_shell, args))
#     + "\n\n\n"
#     + "-" * 80
#     + "\n\n\n"
# )


@functools.cache
def benchexec_log_separator() -> str:
    return "\n\n\n" + "-" * 80 + "\n\n\n"


class LogFile:
    def __init__(self: "LogFile", dir: Path) -> None:
        filename = log_filename(dir)
        self.logfiles = ZipFile(filename)
        self.name = Path(filename.name.removesuffix(".zip"))

    def __enter__(self: "LogFile") -> "LogFile":
        return self

    def __exit__(self: "LogFile", exc_type: Any, exc_value: Any, traceback: Any) -> None:
        self.close()

    def close(self) -> None:
        self.logfiles.close()

    def get_log(self: "LogFile", r: RunId, basename: str) -> str:
        """
        Return the output of the prover and the header with the commandline used
        """
        p = str(self.name.joinpath(".".join([r.mangle(), basename, "log"])))
        return self.logfiles.read(p).decode()

    def get_output(self: "LogFile", r: RunId, basename: str) -> str:
        """
        Return the output of the prover
        """
        s = self.get_log(r, basename)
        index = s.find(benchexec_log_separator())
        if index == -1:
            raise ValueError(f"Log Header not found {r!r} {basename!r}")
        index += len(benchexec_log_separator())
        return s[index:]
