import csv as csv
import re
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

from pydantic.networks import HttpUrl

import smtcomp.defs as defs


class CsvColumn(str, Enum):
    name = "Name of Solver"
    homepage = "Solver homepage"
    system_description = (
        "System description URL (note that the system description is already part of the submission of the  preliminary"
        " solvers)."
    )
    title_system_description = "Title of the system description"
    starexec_id = (
        "StarExec ID of your preliminary solver.    If you have different solver ids for several track, please provide"
        ' them as "12345,12346(uc),12347(inc)".  The tracks are single-query (sq), unsat-core (uc), incremental'
        " (inc), model-validation (mv), proof-exhibition (pe)."
    )
    main_solver_id = (
        "If this solver is a VARIANT of another submission, e.g. an experimental version, provide the name and the"
        " StarExec ID of the main solver, otherwise leave blank."
    )
    wrapped_tool = (
        "If this solver is a WRAPPER TOOL (i.e., it includes and calls one or more other SMT solvers, see Section 4"
        " of the competition rules at https://smt-comp.github.io/2023/rules.pdf), list ALL wrapped solvers and"
        " their exact version here, otherwise leave blank."
    )
    derived_tool = (
        "If this solver is a DERIVED TOOL (i.e., any solver that is based on or extends another SMT solver, see"
        " Section 4 of the competition rules at https://smt-comp.github.io/2023/rules.pdf), provide the name of the"
        " original tool here. A derived tool should follow the naming convention"
        " [name-of-base-solver]-[my-solver-name]."
    )
    track_single_query = "For the Single-Query Track, give a regular expression for the supported logics."
    track_incremental = "For the Incremental Track, give a regular expression for the supported logics."
    track_unsat_core = "For the Unsat-Core Track, give a regular expression for the supported logics."
    track_model_validation = "For the Model-Validation Track, give a regular expression for the supported logics."
    track_proof = "For the Proof-Exhibition Track, give a regular expression for the supported logics."
    track_parallel = (
        "For the Parallel Track, give a regular expression for the supported logics.  (You need to register for the"
        " parallel track separately)"
    )
    track_cloud = (
        "For the Cloud Track, give a regular expression for the supported logics.  (You need to register for the"
        " cloud track separately)"
    )
    contributors = "Please list all contributors that you wish to be acknowledged here"


def convert_row(row: Dict[str, str], dstdir: Path) -> defs.Submission:
    def archive_of_solver_id(solver_id: str) -> defs.Archive:
        return defs.Archive(
            url=HttpUrl("https://www.starexec.org/starexec/secure/download?type=solver&id=" + solver_id),
            h=None,
        )

    solver_ids = row[CsvColumn.starexec_id].split(",")

    def find_archive(track_id: Optional[str]) -> Optional[defs.Archive]:
        r = re.compile(" *([0-9]+)+\\(" + track_id + "\\) *") if track_id else re.compile(" *([0-9]+) *")
        for solver_id in solver_ids:
            g = r.fullmatch(solver_id)
            if g:
                return archive_of_solver_id(g.group(1))
        return None

    archive = find_archive(None)
    contributors = [
        defs.Contributor(name=name) for line in row[CsvColumn.contributors].splitlines() for name in line.split(",")
    ]
    participations: List[defs.Participation] = []

    def add_track(col: CsvColumn, track: defs.Track, shortcut: str) -> None:
        if row[col] != "" and row[col] != "-":
            participations.append(
                defs.Participation(
                    tracks=[track], logics=defs.Logics.from_regexp(row[col].strip()), archive=find_archive(shortcut)
                )
            )

    add_track(CsvColumn.track_single_query, defs.Track.SingleQuery, "sq")
    add_track(CsvColumn.track_unsat_core, defs.Track.UnsatCore, "unsat")
    add_track(CsvColumn.track_incremental, defs.Track.Incremental, "inc")
    add_track(CsvColumn.track_model_validation, defs.Track.ModelValidation, "mv")
    add_track(CsvColumn.track_proof, defs.Track.ProofExhibition, "proof")
    add_track(CsvColumn.track_parallel, defs.Track.Parallel, "par")
    add_track(CsvColumn.track_cloud, defs.Track.Cloud, "cloud")
    return defs.Submission(
        name=row[CsvColumn.name],
        contributors=contributors,
        contacts=[defs.NameEmail(name="unset", email="unset@example.com")],
        archive=archive,
        website=HttpUrl(row[CsvColumn.homepage]),
        system_description=HttpUrl(row[CsvColumn.system_description]),
        command=defs.Command(binary="bin/default"),
        solver_type=defs.SolverType.standalone,
        participations=defs.Participations(root=participations),
    )


def convert_csv(file: Path, dstdir: Path) -> None:
    with open(file) as dcsv:
        registrations = csv.DictReader(dcsv)
        for row in registrations:
            submission = convert_row(row, dstdir)
            with open(Path.joinpath(dstdir, submission.name + ".json"), "w") as f:
                f.write(submission.model_dump_json())
