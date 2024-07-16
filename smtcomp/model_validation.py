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
from pydantic import BaseModel, RootModel, Field
from typing import Union
import pydantic
from smtcomp.unpack import write_cin, read_cin


def is_error(x: defs.Validation) -> defs.ValidationError | None:
    match x:
        case defs.ValidationError():
            return x
        case defs.ValidationOk() | defs.NoValidation():
            return None


def raise_stack_limit() -> None:
    soft, hard = resource.getrlimit(resource.RLIMIT_STACK)
    soft = min(40_000_000_000, hard)
    resource.setrlimit(resource.RLIMIT_STACK, (soft, hard))


def check_locally(config: defs.Config, smt2_file: Path, model: str) -> defs.Validation:
    opts: list[str | Path] = []
    opts.append(config.dolmen_binary)
    opts.extend(
        [
            "--time=1h",
            "--size=40G",
            "--strict=false",
            "--check-model=true",
            "--report-style=minimal",
            "--warn=-all",
        ]
    )
    if config.dolmen_force_logic_ALL:
        opts.append("--force-smtlib2-logic=ALL")
    opts.append(smt2_file)

    r = subprocess.run(
        opts,
        input=model.encode(),
        capture_output=True,
        # preexec_fn slows a lot the execution, and is not safe with threads (cf python doc)
    )
    match r.returncode:
        case 0:
            return defs.ValidationOk(stderr=r.stderr.decode())
        case 2:
            # LimitReached
            status = defs.Answer.ModelValidatorTimeout
        case _:
            if r.stderr.endswith(b"E:bad-model\n"):
                status = defs.Answer.ModelUnsat
            elif r.stderr.endswith(b"E:timeout\n"):
                status = defs.Answer.ModelValidatorTimeout
            elif r.stderr.endswith(b"E:uncaught-exn\n"):
                status = defs.Answer.ModelValidatorException
            elif r.stderr.endswith(b"E:forbidden-array-sort\n") or r.stderr.endswith(b"E:non-linear-expr\n"):
                status = defs.Answer.ModelValidatorBenchmarkStrictTyping
            elif (
                r.stderr.endswith(b"E:id-def-conflict\n")
                or r.stderr.endswith(b"E:parsing-error\n")
                or r.stderr.endswith(b"E:unbound-id\n")
                or r.stderr.endswith(b"E:undefined-constant\n")
            ):
                status = defs.Answer.ModelParsingError
            elif r.stderr.endswith(b"E:partial-dstr\n"):
                status = defs.Answer.ModelPartialFunctionMissing
            else:
                raise (ValueError("Unknown validator error"))
    return defs.ValidationError(status=status, stderr=r.stderr.decode(), model=model)


def check_result_locally(
    config: defs.Config,
    resultdir: Path,
    cachedir: Path,
    rid: results.RunId,
    r: results.Run,
    model: str,
) -> defs.Validation:
    d = resultdir / "model_validation_results"
    file_cache = d / f"{str(r.scramble_id)}.json.gz"
    if file_cache.is_file():
        val = defs.ValidationResult.model_validate_json(read_cin(file_cache)).root
        match val:
            case defs.ValidationError():
                if val.stderr.endswith("E:timeout\n"):
                    val.status = defs.Answer.ModelValidatorTimeout
                    s = defs.ValidationResult(val).model_dump_json(indent=1)
                    write_cin(file_cache, s)
                    return val
                else:
                    file_cache.unlink()
                    return check_result_locally(config, resultdir, cachedir, rid, r, model)
            case _:
                return val
    else:
        match r.answer:
            case defs.Answer.Sat:
                filedir = smtcomp.scramble_benchmarks.benchmark_files_dir(cachedir, rid.track)
                basename = smtcomp.scramble_benchmarks.scramble_basename(r.scramble_id)
                smt2_file = filedir / str(r.logic) / basename
                val = check_locally(config, smt2_file, model)
            case _:
                val = defs.noValidation
        d.mkdir(parents=True, exist_ok=True)
        s = defs.ValidationResult(val).model_dump_json(indent=1)
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
) -> list[tuple[results.RunId, results.Run, defs.Validation]]:
    raise_stack_limit()
    l = list(
        itertools.chain.from_iterable(
            prepare_model_validation_tasks(d.parent)
            for d in progress.track(
                list(resultdir.glob("**/*.logfiles.zip")),
                description="Preparing tasks",
            )
        ),
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
