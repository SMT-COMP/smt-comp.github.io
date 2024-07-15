import itertools
from dataclasses import dataclass
from pathlib import Path
import smtcomp.defs as defs
import subprocess, resource
import smtcomp.results as results
from smtcomp.benchexec import get_suffix
import smtcomp.scramble_benchmarks
from multiprocessing.pool import ThreadPool
from rich.progress import Progress, TaskID
from pydantic import BaseModel, RootModel
import pydantic
from smtcomp.unpack import write_cin, read_cin


class ValidationOk(BaseModel):
    stderr: str


class ValidationError(BaseModel):
    status: defs.Status
    stderr: str
    model: str


class NoValidation(BaseModel):
    """No validation possible"""


noValidation = NoValidation()

Validation = ValidationOk | ValidationError | NoValidation


class ValidationResult(RootModel):
    root: Validation


def is_error(x: Validation) -> ValidationError | None:
    match x:
        case ValidationError():
            return x
        case ValidationOk() | NoValidation():
            return None


def raise_stack_limit() -> None:
    soft, hard = resource.getrlimit(resource.RLIMIT_STACK)
    soft = min(40_000_000_000, hard)
    resource.setrlimit(resource.RLIMIT_STACK, (soft, hard))


def check_locally(config: defs.Config, smt2_file: Path, model: str) -> Validation:
    r = subprocess.run(
        [
            config.dolmen_binary,
            "--time=1h",
            "--size=40G",
            "--strict=false",
            "--check-model=true",
            "--report-style=minimal",
            smt2_file,
        ],
        input=model.encode(),
        capture_output=True,
        preexec_fn=raise_stack_limit,
    )
    match r.returncode:
        case 0:
            return ValidationOk(stderr=r.stderr.decode())
        case 5:
            status = defs.Status.Unsat
        case 2:
            # LimitReached
            status = defs.Status.Unknown
        case _:
            status = defs.Status.Unknown
    return ValidationError(status=status, stderr=r.stderr.decode(), model=model)


def check_result_locally(
    config: defs.Config,
    resultdir: Path,
    cachedir: Path,
    rid: results.RunId,
    r: results.Run,
    model: str,
) -> Validation:
    d = resultdir / "model_validation_results"
    file_cache = d / f"{str(r.scramble_id)}.json.gz"
    if file_cache.is_file():
        try:
            val = ValidationResult.model_validate_json(read_cin(file_cache)).root
            return val
        except pydantic.ValidationError:
            file_cache.unlink()
            return check_result_locally(config, resultdir, cachedir, rid, r, model)
    else:
        match r.answer:
            case defs.Answer.Sat:
                filedir = smtcomp.scramble_benchmarks.benchmark_files_dir(cachedir, rid.track)
                basename = smtcomp.scramble_benchmarks.scramble_basename(r.scramble_id)
                smt2_file = filedir / str(r.logic) / basename
                val = check_locally(config, smt2_file, model)
            case _:
                val = noValidation
        d.mkdir(parents=True, exist_ok=True)
        s = ValidationResult(val).model_dump_json(indent=1)
        write_cin(file_cache, s)
        return val


def prepare_model_validation_tasks(
    resultdir: Path,
) -> list[tuple[results.RunId, results.Run, str, Path]]:
    with results.LogFile(resultdir) as logfiles:
        l = [
            (
                r.runid,
                b,
                logfiles.get_output(
                    r.runid, smtcomp.scramble_benchmarks.scramble_basename(b.scramble_id, suffix="yml")
                ),
                resultdir,
            )
            for r in results.parse_results(resultdir)
            for b in r.runs
            if b.answer == defs.Answer.Sat
        ]
        return l


def check_all_results_locally(
    config: defs.Config, cachedir: Path, resultdir: Path, executor: ThreadPool, progress: Progress
) -> list[tuple[results.RunId, results.Run, Validation]]:
    l = list(
        itertools.chain.from_iterable(
            prepare_model_validation_tasks(d.parent)
            for d in progress.track(
                list(resultdir.glob("**/*.logfiles.zip")),
                description="Preparing tasks",
            )
        )
    )
    return list(
        progress.track(
            executor.imap_unordered(
                (lambda v: (v[0], v[1], check_result_locally(config, v[3], cachedir, v[0], v[1], v[2]))), l
            ),
            description="Model validation",
            total=len(l),
        ),
    )
