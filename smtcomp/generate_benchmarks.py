from typing import Set, Dict
from pathlib import Path
from smtcomp import defs
from smtcomp.benchexec import generate_benchmark_yml


def path_trivial_benchmark(dst: Path, track: defs.Track, logic: defs.Logic, status: defs.Status) -> Path:
    match track:
        case defs.Track.Incremental:
            suffix = "_inc"
        case defs.Track.ModelValidation:
            suffix = "_model"
        case defs.Track.SingleQuery:
            suffix = ""
        case defs.Track.UnsatCore | defs.Track.ProofExhibition | defs.Track.Cloud | defs.Track.Parallel:
            raise (ValueError("No trivial benchmarks yet for f{track}"))
    match status:
        case defs.Status.Sat:
            return dst.joinpath(str(logic) + suffix + ".sat.smt2")
        case defs.Status.Unsat:
            return dst.joinpath(str(logic) + suffix + ".unsat.smt2")
        case defs.Status.Incremental:
            return dst.joinpath(str(logic) + suffix + ".incremental.smt2")
        case defs.Status.Unknown:
            raise (ValueError("No trivial benchmarks yet for unknown"))


def generate_trivial_benchmarks(dst: Path) -> None:
    prop_dir = dst.joinpath("properties")
    prop_dir.mkdir(parents=True, exist_ok=True)
    (prop_dir / "SingleQuery.prp").touch()

    dst.joinpath("files").mkdir(parents=True, exist_ok=True)
    for track, divisions in defs.tracks.items():
        match track:
            case defs.Track.Incremental:
                suffix = "_inc"
            case defs.Track.ModelValidation:
                suffix = "_model"
            case defs.Track.SingleQuery:
                suffix = ""
            case defs.Track.UnsatCore | defs.Track.ProofExhibition | defs.Track.Cloud | defs.Track.Parallel:
                continue
        for _, theories in divisions.items():
            for theory in theories:
                theory_name = str(theory) + suffix
                theory_dir = dst.joinpath("files", theory_name)
                theory_dir.mkdir(parents=True, exist_ok=True)
                file = dst.joinpath(theory_name)

                if track == defs.Track.Incremental:
                    file_incremental = path_trivial_benchmark(theory_dir, track, theory, defs.Status.Incremental)

                    file.write_text(f"files/{theory_name}/*.smt2\n")

                    benchmark = "\n".join([
                        "sat",
                        "sat",
                        "unsat",
                        "--- BENCHMARK BEGINS HERE ---",
                        f"(set-logic {theory.value})",
                        "(assert true)",
                        "(check-sat)",
                        "(assert true)",
                        "(check-sat)",
                        "(assert false)",
                        "(check-sat)\n",
                    ])
                    file_incremental.write_text(benchmark)
                else:
                    file_sat = path_trivial_benchmark(theory_dir, track, theory, defs.Status.Sat)
                    file_unsat = path_trivial_benchmark(theory_dir, track, theory, defs.Status.Unsat)
                    file.write_text(f"files/{theory_name}/*.yml\n")


                    file_sat.write_text(f"(set-logic {theory.value})(check-sat)")
                    file_unsat.write_text(f"(set-logic {theory.value})(assert false)(check-sat)")

                    generate_benchmark_yml(file_sat, True, None)
                    generate_benchmark_yml(file_unsat, False, None)

def generate_benchmarks(dst: Path, seed: int) -> None:
    return
