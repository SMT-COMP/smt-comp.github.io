from pathlib import Path
from typing import Sequence
import smtcomp.defs as defs
import subprocess
import smtcomp.results as results
import smtcomp.scramble_benchmarks
from rich.progress import track
import rich
import polars as pl
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
    scramble_mapping: dict[int, int],
    generated_files: defaultdict[int, dict[FrozenUnsatCore, Path]],
    target_dir: Path
) -> None:
    assert r.answer == defs.Answer.Unsat

    filedir = smtcomp.scramble_benchmarks.benchmark_files_dir(cachedir, rid.track)

    scramble_id = scramble_mapping[r.file]
    basename = smtcomp.scramble_benchmarks.scramble_basename(scramble_id)
    benchmark_name = Path(str(r.logic)) / basename
    smt2_file = filedir / benchmark_name

    solver_output = logfiles.get_output(rid, r.benchmark_yml)
    core = get_unsat_core(solver_output)
    if core is None:
        print(f"No unsat core for {r.benchmark_yml}")
        return

    (target_dir / str(r.logic)).mkdir(parents=True, exist_ok=True)

    frozen_core = tuple(core)
    if frozen_core in generated_files[r.file]:
        return

    basename_file, basename_ext = splitext(basename)
    core_id = len(generated_files[r.file])
    validation_file = Path(str(r.logic)) / f"{basename_file}_{core_id}{basename_ext}"
    validation_filepath = target_dir / validation_file

    create_validation_file(smt2_file, core, scrambler, validation_filepath)
    generated_files[r.file][frozen_core] = validation_file


def generate_validation_files(cachedir: Path, resultdir: Path, scrambler: Path) -> None:
    benchmark_dir = smtcomp.scramble_benchmarks.benchmark_files_dir(cachedir, defs.Track.UnsatCore)
    target_dir = cachedir / "benchmarks" / "files_unsatcorevalidation"
    target_dir.mkdir(parents=True, exist_ok=True)

    mapping_csv = benchmark_dir / smtcomp.scramble_benchmarks.csv_original_id_name
    assert mapping_csv.exists()
    scramble_mapping = dict(pl.read_csv(mapping_csv).select("file", "scramble_id").iter_rows())

    generated_files: defaultdict[int, dict[FrozenUnsatCore, Path]] = defaultdict(dict)

    logfiles = list(resultdir.glob("**/*.logfiles.zip"))
    for logfile in logfiles:
        resultdir = logfile.parent
        rich.print(f"[green]Processing[/green] {logfile}")
        with results.LogFile(resultdir) as f:
            l = [
                (r.runid, b)
                for r in results.parse_results(resultdir)
                for b in r.runs
                if b.answer == defs.Answer.Unsat
            ]
            for runid, run in track(l):
                generate_validation_file(cachedir, f, runid, run, scrambler, scramble_mapping, generated_files, target_dir)

    with open(target_dir / "mapping.json", "w") as f:
        data = {k: [{"core": c, "file": str(f)} for (c, f) in v.items()] for (k, v) in generated_files.items()}
        json.dump(data, f)
