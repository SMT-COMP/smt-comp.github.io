from typing import Set, Dict
from pathlib import Path
from smtcomp import defs
from smtcomp.benchexec import generate_benchmark_yml, get_suffix


def path_trivial_benchmark(dst: Path, track: defs.Track, logic: defs.Logic, status: defs.Status) -> Path:
    """
    dst is the root of the generated benchmarks directory
    """
    match track:
        case defs.Track.Incremental:
            assert status == defs.Status.Incremental
            suffix = get_suffix(track)
        case defs.Track.ModelValidation:
            assert status != defs.Status.Incremental
            suffix = get_suffix(track)
        case defs.Track.SingleQuery:
            assert status != defs.Status.Incremental
            suffix = get_suffix(track)
        case defs.Track.UnsatCore | defs.Track.ProofExhibition | defs.Track.Cloud | defs.Track.Parallel:
            raise (ValueError("No trivial benchmarks yet for f{track}"))
    logic_dir = dst.joinpath(f"files{suffix}", str(logic))
    match status:
        case defs.Status.Sat:
            return logic_dir.joinpath(str(logic) + suffix + ".sat.smt2")
        case defs.Status.Unsat:
            return logic_dir.joinpath(str(logic) + suffix + ".unsat.smt2")
        case defs.Status.Incremental:
            return logic_dir.joinpath(str(logic) + suffix + ".incremental.smt2")
        case defs.Status.Unknown:
            raise (ValueError("No trivial benchmarks yet for unknown"))


def generate_trivial_benchmarks(dst: Path) -> None:
    prop_dir = dst.joinpath("properties")
    prop_dir.mkdir(parents=True, exist_ok=True)
    (prop_dir / "SingleQuery.prp").touch()

    dst.joinpath("files").mkdir(parents=True, exist_ok=True)
    dst.joinpath("files_inc").mkdir(parents=True, exist_ok=True)
    for track, divisions in defs.tracks.items():
        match track:
            case defs.Track.Incremental | defs.Track.ModelValidation | defs.Track.SingleQuery:
                suffix = get_suffix(track)
            case defs.Track.UnsatCore | defs.Track.ProofExhibition | defs.Track.Cloud | defs.Track.Parallel:
                continue
        for _, logics in divisions.items():
            for logic in logics:
                logic_name = str(logic)
                logic_dir = dst.joinpath(f"files{suffix}", logic_name)
                logic_dir.mkdir(parents=True, exist_ok=True)
                file = dst.joinpath(logic_name + suffix)

                if track == defs.Track.Incremental:
                    file_incremental = path_trivial_benchmark(dst, track, logic, defs.Status.Incremental)

                    file.write_text(f"files{suffix}/{logic_name}/*.smt2\n")

                    benchmark = "\n".join([
                        "sat",
                        "sat",
                        "unsat",
                        "--- BENCHMARK BEGINS HERE ---",
                        f"(set-logic {logic.value})",
                        "(assert true)",
                        "(check-sat)",
                        "(assert true)",
                        "(check-sat)",
                        "(assert false)",
                        "(check-sat)\n",
                    ])
                    file_incremental.write_text(benchmark)
                else:
                    file_sat = path_trivial_benchmark(dst, track, logic, defs.Status.Sat)
                    file_unsat = path_trivial_benchmark(dst, track, logic, defs.Status.Unsat)
                    file.write_text(f"files{suffix}/{logic_name}/*.yml\n")

                    file_sat.write_text(f"(set-logic {logic.value})(check-sat)")
                    file_unsat.write_text(f"(set-logic {logic.value})(assert false)(check-sat)")

                    generate_benchmark_yml(file_sat, True, None)
                    generate_benchmark_yml(file_unsat, False, None)


def generate_benchmarks(dst: Path, seed: int) -> None:
    """
    Generate files included by benchexec
    """
    prop_dir = dst.joinpath("properties")
    prop_dir.mkdir(parents=True, exist_ok=True)
    (prop_dir / "SMT.prp").touch()

    dst.joinpath("files").mkdir(parents=True, exist_ok=True)
    dst.joinpath("files_inc").mkdir(parents=True, exist_ok=True)
    for track, divisions in defs.tracks.items():
        match track:
            case defs.Track.Incremental | defs.Track.ModelValidation | defs.Track.SingleQuery:
                suffix = get_suffix(track)
            case defs.Track.UnsatCore | defs.Track.ProofExhibition | defs.Track.Cloud | defs.Track.Parallel:
                continue
        for _, theories in divisions.items():
            for theory in theories:
                theory_name = str(theory)
                file = dst.joinpath(theory_name + suffix)
                file.write_text(f"files{suffix}/{theory_name}/*.yml\n")
