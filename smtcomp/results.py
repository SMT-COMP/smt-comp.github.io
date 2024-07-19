from typing import Optional, Iterator, Any
import functools, concurrent
import smtcomp.defs as defs
import polars as pl
import xml.etree.ElementTree as ET
from pathlib import Path
import smtcomp.selection
from smtcomp.unpack import read_cin
import smtcomp.scramble_benchmarks
from pydantic import BaseModel
from zipfile import ZipFile
from rich.progress import track
from smtcomp.utils import *
import re
import json


class RunId(BaseModel):
    solver: str
    participation: int
    track: defs.Track

    @classmethod
    def unmangle(cls, s: str) -> "RunId":
        name_l = s.split(",")
        return RunId(solver=name_l[0], participation=int(name_l[1]), track=defs.Track(name_l[2].split(".")[0]))

    def mangle(self) -> str:
        return ",".join([self.solver, str(self.participation), str(self.track)])


class Run(BaseModel):
    scramble_id: int
    logic: defs.Logic
    cputime_s: float
    """ example: 0.211880968s"""
    memory_B: int
    """ example: 21127168B"""
    answer: defs.Answer
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


def parse_result(s: str) -> defs.Answer:
    if s.startswith("TIMEOUT"):
        # TIMEOUT (true), TIMEOUT (false), TIMEOUT
        return defs.Answer.Timeout
    if s.startswith("DONE"):
        return defs.Answer.Incremental
    if s.startswith("OUT OF MEMORY"):
        return defs.Answer.OOM
    match s:
        case "false":
            return defs.Answer.Unsat
        case "true":
            return defs.Answer.Sat
        case "unknown":
            return defs.Answer.Unknown
        case "OUT OF MEMORY" | "OUT OF JAVA MEMORY":
            return defs.Answer.OOM
        case _:
            raise ValueError(f"Unknown result value {s}")


def convert_run(r: ET.Element) -> Run:
    parts = r.attrib["name"].split("/")
    logic = defs.Logic(parts[-2])
    scramble_id = smtcomp.scramble_benchmarks.unscramble_yml_basename(parts[-1])
    cputime_s: Optional[float] = None
    memory_B: Optional[int] = None
    answer: Optional[defs.Answer] = None
    walltime_s: Optional[float] = None

    for col in r.iterfind("column"):
        value = col.attrib["value"]
        match col.attrib["title"]:
            case "cputime":
                cputime_s = parse_time(value)
            case "memory":
                memory_B = parse_size(value)
            case "status":
                answer = parse_result(value)
            case "walltime":
                walltime_s = parse_time(value)

    if cputime_s is None or memory_B is None or answer is None or walltime_s is None:
        raise ValueError("xml of results doesn't contains some expected column")

    return Run(
        scramble_id=scramble_id,
        logic=logic,
        cputime_s=cputime_s,
        memory_B=memory_B,
        answer=answer,
        walltime_s=walltime_s,
    )


def parse_xml(file: Path) -> Results:
    result = ET.fromstring(read_cin(file))
    runs = list(map(convert_run, result.iterfind("run")))
    return Results(runid=RunId.unmangle(result.attrib["name"]), options=result.attrib["options"], runs=runs)


def parse_results(resultdir: Path) -> Iterator[Results]:
    return map(parse_xml, (resultdir.glob("*.xml.bz2")))


def log_filename(dir: Path) -> Path:
    l = list(dir.glob("*.logfiles.zip"))
    if len(l) != 1:
        raise (ValueError(f"Directory {dir!r} doesn't contains *.logfiles.zip archive"))
    return l[0]


@functools.cache
def benchexec_log_separator() -> str:
    """
    #Benchexec add this header
    output_file.write(
    " ".join(map(util.escape_string_shell, args))
    + "\n\n\n"
    + "-" * 80
    + "\n\n\n"
    )
    """
    return "\n\n\n" + "-" * 80 + "\n\n\n"


class LogFile:
    def __init__(self: "LogFile", dir: Path) -> None:
        self.filename = log_filename(dir)
        self.logfiles: None | ZipFile = None
        self.name = Path(self.filename.name.removesuffix(".zip"))

    def get_logfiles(self) -> ZipFile:
        if self.logfiles is None:
            self.logfiles = ZipFile(self.filename)
        return self.logfiles

    def __enter__(self: "LogFile") -> "LogFile":
        return self

    def __exit__(self: "LogFile", exc_type: Any, exc_value: Any, traceback: Any) -> None:
        self.close()

    def close(self) -> None:
        if not self.logfiles is None:
            self.logfiles.close()

    def get_log(self: "LogFile", r: RunId, basename: str) -> str:
        """
        Return the output of the prover and the header with the commandline used
        """
        p = str(self.name.joinpath(".".join([r.mangle(), basename, "log"])))
        return self.get_logfiles().read(p).decode()

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


def mv_get_cached_results(resultdir: Path, scramble_id: int) -> defs.Validation | None:
    d = resultdir / "model_validation_results"
    file_cache = d / f"{str(scramble_id)}.json.gz"
    if file_cache.is_file():
        return defs.ValidationResult.model_validate_json(read_cin(file_cache)).root
    else:
        return None


def mv_get_cached_answer(resultdir: Path, scramble_id: int) -> defs.Answer:
    val = mv_get_cached_results(resultdir, scramble_id)
    if val is None:
        return defs.Answer.ModelNotValidated
    else:
        match val:
            case defs.ValidationOk():
                return defs.Answer.Sat
            case defs.NoValidation():
                return defs.Answer.ModelNotValidated
            case defs.ValidationError():
                return val.status


re_inc_trace_executor_wrong_output = re.compile(r"WRONG solver response: got")
re_inc_sat_unsat = re.compile(r"^sat|unsat$", flags=re.MULTILINE)
re_inc_time = re.compile(r"^time ([0-9.]*)$", flags=re.MULTILINE)


def inc_get_nb_answers(logfiles: LogFile, runid: RunId, scramble_id: int) -> Tuple[defs.Answer, int, float | None]:
    output = logfiles.get_output(runid, smtcomp.scramble_benchmarks.scramble_basename(scramble_id, suffix="yml"))

    if re_inc_trace_executor_wrong_output.search(output):
        return (defs.Answer.IncrementalError, 0, None)

    nb_answers = sum(1 for _ in re_inc_sat_unsat.finditer(output))

    last_match: Match[str] | None = None
    for m in re_inc_time.finditer(output):
        last_match = m

    if last_match is not None:
        last_time = float(last_match.group(1))
    else:
        last_time = None

    return (defs.Answer.Incremental, nb_answers, last_time)


## Copied from branch final-execution
unsat_core_re = re.compile(r"\(\s*((smtcomp(\d+)\s*)+)\)")
core_item_re = re.compile(r"smtcomp(\d+)(\s|$)")

UnsatCore = list[int]
FrozenUnsatCore = Sequence[int]


def get_unsat_core(output: str) -> UnsatCore | None:
    answers = unsat_core_re.findall(output)
    assert len(answers) <= 1, "Multiple unsat cores!"

    if not answers:
        return None

    core = answers[0][0]
    items = sorted([int(m[0]) for m in core_item_re.findall(core)])
    return items


def uc_get_uc(logfiles: LogFile, runid: RunId, scramble_id: int) -> UnsatCore | None:
    output = logfiles.get_output(runid, smtcomp.scramble_benchmarks.scramble_basename(scramble_id, suffix="yml"))

    return get_unsat_core(output)


def to_pl(resultdir: Path, logfiles: LogFile, r: Results) -> pl.LazyFrame:
    def convert(a: Run) -> Dict[str, Any]:
        d = dict(a)
        if r.runid.track == defs.Track.ModelValidation and a.answer == defs.Answer.Sat:
            a.answer = mv_get_cached_answer(resultdir, a.scramble_id)

        if r.runid.track == defs.Track.Incremental:
            answer, nb_answers, last_time = inc_get_nb_answers(logfiles, r.runid, a.scramble_id)
            a.answer = answer
            d["nb_answers"] = nb_answers
            # TODO: Since we forgot to readd timestamp for some answer
            # we don't have the time of the last answer for now
            # So we take the total for nowwhen no time
            if last_time is not None:
                d["walltime_s"] = last_time
                d["cputime_s"] = last_time

        if r.runid.track == defs.Track.UnsatCore:
            if d["answer"] == defs.Answer.Unsat:
                uc = uc_get_uc(logfiles, r.runid, a.scramble_id)
                if uc is None:
                    d["answer"] = defs.Answer.Unknown
                    d["unsat_core"] = []
                    d["nb_answers"] = 0
                else:
                    d["unsat_core"] = uc
                    d["nb_answers"] = len(uc)
            else:
                d["unsat_core"] = []
                d["nb_answers"] = 0
            # TODO: Since we forgot to readd timestamp for each answer
            # we don't have the time of the last answer for now
            # So we take the total for now

        d["answer"] = int(d["answer"])
        d["logic"] = int(d["logic"])
        return d

    lf = pl.LazyFrame(map(convert, r.runs))
    return lf.with_columns(solver=pl.lit(r.runid.solver), participation=r.runid.participation, track=int(r.runid.track))


def parse_to_pl(file: Path) -> pl.LazyFrame:
    feather = file.with_suffix(".feather")
    if feather.exists():
        return pl.read_ipc(feather).lazy()

    with LogFile(file.parent) as logfiles:
        r = to_pl(file.parent, logfiles, parse_xml(file)).collect()
        r.write_ipc(feather)
        return r.lazy()


def parse_mapping(p: Path) -> pl.LazyFrame:
    with p.open("rt") as o:
        d = json.load(o)

    return pl.LazyFrame(
        (
            (
                smtcomp.scramble_benchmarks.unscramble_yml_basename(Path(k).name),
                sorted(v["core"]),
                smtcomp.scramble_benchmarks.unscramble_yml_basename(Path(v["file"]).name),
            )
            for k, l in d.items()
            for v in l
        ),
        {
            "scramble_id_orig": pl.Int64,
            "unsat_core": pl.List(pl.Int64),
            "scramble_id": pl.Int64,
        },
    )


json_mapping_name = "mapping.json"


def parse_dir(dir: Path) -> pl.LazyFrame:
    """
    output columns: solver, participation, track, basename, cputime_s, memory_B, status, walltime_s, scramble_id, file

    The track stored in the results is *not* used for some decisions:
    - if a file mapping.json is present it used and the original_id.csv is not needed
    - if original_id is present it is used (all the other track)
    - if it ends with "unsatcore" and the directory "../unsat_core_valisation_results" is present and converted (feather file) it is used to validate the unsat cores

    TODO: streamline the results directory hierarchy
    """
    csv = dir / smtcomp.scramble_benchmarks.csv_original_id_name
    json = dir / json_mapping_name
    if not csv.exists() and not json.exists():
        raise (ValueError(f"No file {csv!s} or {json!s} in the directory"))

    if csv.exists():
        lf = pl.read_csv(csv).lazy()
        defaults: dict[str, Any] = {"file": -1}
    else:
        lf = parse_mapping(json)
        defaults = {"unsat_core": [], "scramble_id_orig": -1}

    l = list(dir.glob("**/*.xml.bz2"))
    if len(l) == 0:
        raise (ValueError(f"No results in the directory {dir!s}"))
    l_parsed = list(track(map(parse_to_pl, l), total=len(l)))
    results = pl.concat(l_parsed)
    results = add_columns(results, lf, on=["scramble_id"], defaults=defaults)

    ucvr = dir / "../unsat_core_validation_results" / "parsed.feather"
    if (dir.name).endswith("unsatcore") and ucvr.is_file():
        vr = pl.read_ipc(ucvr).lazy()
        vr = (
            vr.select("answer", "unsat_core", scramble_id="scramble_id_orig")
            .group_by("scramble_id", "unsat_core")
            .agg(unsat=(pl.col("answer") == int(defs.Answer.Unsat)).any(), validation_attempted=True)
        )
        results = add_columns(
            results, vr, on=["scramble_id", "unsat_core"], defaults={"unsat": False, "validation_attempted": False}
        )
        results = results.with_columns(
            answer=pl.when((pl.col("answer") == int(defs.Answer.Unsat)) & (pl.col("unsat")).not_())
            .then(int(defs.Answer.UnsatCoreNotValidated))
            .otherwise("answer")
        ).drop("unsat", "unsat_core")

    return results


def helper_get_results(
    config: defs.Config, results: List[Path], track: defs.Track
) -> Tuple[pl.LazyFrame, pl.LazyFrame]:
    """
    If results is empty use the one in data

    Return on all the selected benchmarks for each solver that should run it
    "track", "file", "logic", "division", "status", "solver", "answer", "cputime_s", "memory_B", "walltime_s".

    -1 is used when no answer is available.

    """
    if len(results) == 0:
        lf = (
            pl.read_ipc(config.cached_current_results[track])
            .lazy()
            .with_columns(track=int(track))
            .rename(
                {
                    "result": "answer",
                    "memory_usage": "memory_B",
                    "cpu_time": "cputime_s",
                    "wallclock_time": "walltime_s",
                }
            )
            .drop("year")
        )
    else:
        lf = pl.concat(pl.read_ipc(p / "parsed.feather").lazy() for p in results)
        lf = lf.filter(track=int(track)).drop("scramble_id")
    selection = smtcomp.selection.helper(config, track).filter(selected=True).with_columns(track=int(track))

    selection = (
        add_columns(selection, smtcomp.selection.tracks(), on=["track", "logic"], defaults={"division": -1})
        .collect()  # Improve later works
        .lazy()
    )

    selected = intersect(selection, smtcomp.selection.solver_competing_logics(config), on=["logic", "track"])

    selected = add_columns(
        selected,
        lf.drop("logic", "participation"),  # Hack for participation 0 bug move "participation" to on= for 2025
        on=["file", "solver", "track"],
        defaults={
            "answer": -1,
            "cputime_s": -1,
            "memory_B": -1,
            "walltime_s": -1,
            "nb_answers": -1,
        },
    )

    return selected, selection
