from dataclasses import dataclass
from pathlib import Path
import smtcomp.defs as defs
import subprocess
import smtcomp.results as results
from smtcomp.benchexec import get_suffix
from smtcomp.scramble_benchmarks import benchmark_files_dir
from concurrent.futures import ThreadPoolExecutor
from rich.progress import Progress


# ./dolmen --time=1h --size=40G --strict=false --check-model=true --report-style=minimal "$2" < "$1" &> error.txt
# EXITSTATUS=$?

# if [ "$EXITSTATUS" = "0" ]; then
#     echo "starexec-result=sat"
#     echo "model_validator_status=VALID"
# elif [ "$EXITSTATUS" = "2" ]; then
#     echo "starexec-result=unknown"
#     echo "model_validator_status=LIMITREACHED"
# elif [ "$EXITSTATUS" = "5" ]; then
#     echo "starexec-result=unsat"
#     echo "model_validator_status=INVALID"
# else
#     echo "starexec-result=unknown"
#     echo "model_validator_status=UNKNOWN"
# fi
# echo "dolmenexit=$EXITSTATUS"
# if grep -q '^[EF]:' error.txt; then
#     echo "model_validator_error="$(grep '^[EF]:' error.txt | head -1)
# fi
# exit 0


@dataclass
class ValidationOk:
    stderr: str


@dataclass
class ValidationError:
    status: defs.Status
    stderr: str
    model: str | None


@dataclass
class NoValidation:
    """No validation possible"""


noValidation = NoValidation()

Validation = ValidationOk | ValidationError | NoValidation


def is_error(x: Validation) -> ValidationError | None:
    match x:
        case ValidationError(_):
            return x
        case ValidationOk(_) | NoValidation():
            return None


def check_locally(smt2_file: Path, model: str) -> Validation:
    r = subprocess.run(
        [
            "dolmen",
            "--time=1h",
            "--size=40G",
            "--strict=false",
            "--check-model=true",
            "--report-style=minimal",
            smt2_file,
        ],
        input=model.encode(),
        capture_output=True,
    )
    match r.returncode:
        case 0:
            return ValidationOk(r.stderr.decode())
        case 5:
            status = defs.Status.Unsat
        case 2:
            # LimitReached
            status = defs.Status.Unknown
        case _:
            status = defs.Status.Unknown
    return ValidationError(status, r.stderr.decode(), model)


def check_result_locally(cachedir: Path, logfiles: results.LogFile, rid: results.RunId, r: results.Run) -> Validation:
    if r.status == "true":
        filedir = benchmark_files_dir(cachedir, rid.track)
        logic = rid.includefile.removesuffix(get_suffix(rid.track))
        smt2_file = filedir / logic / (r.basename.removesuffix(".yml") + ".smt2")
        model = logfiles.get_output(rid, r.basename)
        return check_locally(smt2_file, model)
    else:
        return noValidation


def check_results_locally(
    cachedir: Path, resultdir: Path, executor: ThreadPoolExecutor, progress: Progress
) -> list[tuple[results.RunId, results.Run, Validation]]:
    with results.LogFile(resultdir) as logfiles:
        l = [(r.runid, b) for r in results.parse_results(resultdir) for b in r.runs if b.status == "true"]
        return list(
            progress.track(
                executor.map((lambda v: (v[0], v[1], check_result_locally(cachedir, logfiles, v[0], v[1]))), l),
                total=len(l),
                description=f"checking models for {resultdir.name}",
            )
        )
