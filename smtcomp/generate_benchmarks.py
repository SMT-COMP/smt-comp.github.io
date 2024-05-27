from typing import Set, Dict
from pathlib import Path
from smtcomp import defs


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
            return dst.joinpath("files", str(logic) + suffix + ".sat.smt2")
        case defs.Status.Unsat:
            return dst.joinpath("files", str(logic) + suffix + ".unsat.smt2")
        case defs.Status.Unknown:
            raise (ValueError("No trivial benchmarks yet for unknown"))


def generate_trivial_benchmarks(dst: Path) -> None:
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
                file = dst.joinpath(str(theory) + suffix)
                file_sat = path_trivial_benchmark(dst, track, theory, defs.Status.Sat)
                file_unsat = path_trivial_benchmark(dst, track, theory, defs.Status.Unsat)

                file.write_text("\n".join([str(file_sat.relative_to(dst)), str(file_unsat.relative_to(dst))]))

                file_sat.write_text(f"(set-logic {theory.value})(check-sat)")
                file_unsat.write_text(f"(set-logic {theory.value})(assert false)(check-sat)")


def generate_benchmarks(dst: Path, seed: int) -> None:
    return
