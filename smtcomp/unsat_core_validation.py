from pathlib import Path
from typing import Sequence
import smtcomp.defs as defs
import subprocess
import smtcomp.results as results
import smtcomp.scramble_benchmarks
from rich.progress import track
import rich
import re
from tempfile import NamedTemporaryFile
from os.path import splitext
from collections import defaultdict
import json

unsat_core_re = re.compile(r"\(\s*((smtcomp(\d+)\s*)+)\)")
core_item_re = re.compile(r"smtcomp(\d+)(\s|$)")

UnsatCore = list[int]
FrozenUnsatCore = Sequence[int]


def get_unsat_core(output: str) -> UnsatCore | None:
    answers = unsat_core_re.findall(output)
    assert len(answers) <= 1, "Multiple unsat cores!"

    if not answers:
        print("No unsat core")
        return None

    core = answers[0][0]
    items = sorted([int(m[0]) for m in core_item_re.findall(core)])
    return items


def create_validation_file(benchmark: Path, core: UnsatCore, scrambler: Path, outpath: Path) -> None:
    with NamedTemporaryFile() as corefile, open(benchmark, "r") as fsrc, open(outpath, "w") as fdst:
        core_str = "(" + " ".join(f"smtcomp{item}" for item in core) + ")"
        corefile.write("unsat\n".encode("utf-8"))
        corefile.write(core_str.encode("utf-8"))
        corefile.flush()

        # remove all assert commands that are not in unsat core and remove named terms, do not scramble again (seed 0)
        args = [str(scrambler), "-seed", "0", "-term_annot", "false", "-core", str(corefile.name)]
        subprocess.run(args, stdin=fsrc, stdout=fdst, check=True)


def generate_validation_file(
    cachedir: Path,
    logfiles: results.LogFile,
    rid: results.RunId,
    r: results.Run,
    scrambler: Path,
    generated_files: defaultdict[Path, dict[FrozenUnsatCore, Path]],
) -> None:
    assert r.answer == defs.Answer.Unsat

    filedir = smtcomp.scramble_benchmarks.benchmark_files_dir(cachedir, rid.track)
    basename = smtcomp.scramble_benchmarks.scramble_basename(r.scramble_id)
    benchmark_name = Path(str(r.logic)) / basename
    smt2_file = filedir / benchmark_name
    solver_output = logfiles.get_output(rid, smtcomp.scramble_benchmarks.scramble_basename(r.scramble_id, suffix="yml"))

    core = get_unsat_core(solver_output)
    if core is None:
        return

    basename_file, basename_ext = splitext(basename)
    (cachedir / "benchmarks" / "files_unsatcorevalidation" / str(r.logic)).mkdir(parents=True, exist_ok=True)
    outdir = cachedir / "benchmarks" / "files_unsatcorevalidation"

    frozen_core = tuple(core)
    if frozen_core in generated_files[benchmark_name]:
        return

    core_id = len(generated_files[benchmark_name])
    validation_file = Path(str(r.logic)) / f"{basename_file}_{core_id}{basename_ext}"
    validation_filepath = outdir / validation_file

    create_validation_file(smt2_file, core, scrambler, validation_filepath)
    generated_files[benchmark_name][frozen_core] = validation_file


def generate_validation_files(cachedir: Path, resultdirs: list[Path], scrambler: Path) -> None:
    target_dir = cachedir / "benchmarks" / "files_unsatcorevalidation"
    target_dir.mkdir(parents=True, exist_ok=True)

    generated_files: defaultdict[Path, dict[FrozenUnsatCore, Path]] = defaultdict(dict)

    for resultdir in resultdirs:
        rich.print(f"[green]Processing[/green] {resultdir}")
        with results.LogFile(resultdir) as logfiles:
            l = [
                (r.runid, b) for r in results.parse_results(resultdir) for b in r.runs if b.answer == defs.Answer.Unsat
            ]
            for r in track(l):
                generate_validation_file(cachedir, logfiles, r[0], r[1], scrambler, generated_files)

    with open(target_dir / "mapping.json", "w") as f:
        data = {str(k): [{"core": c, "file": str(f)} for (c, f) in v.items()] for (k, v) in generated_files.items()}
        json.dump(data, f)
