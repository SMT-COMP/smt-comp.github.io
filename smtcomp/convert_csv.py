import csv as csv
import re
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests
from bs4 import BeautifulSoup
from pydantic.networks import HttpUrl
from option import Option, Some
from rich.progress import track

import smtcomp.defs as defs


class CsvColumn(str, Enum):
    name = "Solver Name"
    homepage = "Solver homepage"
    system_description = "System description URL"
    title_system_description = "System description name"
    starexec_id = "Solver ID"
    wrapped_tool = "Wrapper Tool"
    derived_tool = "Derived Tool"
    track_single_query = "Single Query Regex"
    track_incremental = "Incremental Regex"
    track_unsat_core = "Unsat Core Regex"
    track_model_validation = "Model Validation Regex"
    track_proof = "Proof Exhibition Regex"
    track_parallel = "Parallel Regex"
    track_cloud = "Cloud Regex"
    contact = "Contact"
    contributors = "Team Members"


def configurations_on_starexec(id: int, cache: Dict[int, list[str]]) -> list[str]:
    if id in cache:
        return cache[id]

    URL = "https://www.starexec.org/starexec/secure/details/solver.jsp?id=" + str(id)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    cache[id] = [i.a.text.strip() for i in soup.find_all(name="td", id="configItem")]
    return cache[id]


def convert_row(row: Dict[str, str], dstdir: Path) -> defs.Submission:
    # print(row[CsvColumn.name])

    def archive_of_solver_id(solver_id: int) -> defs.Archive:
        return defs.Archive(
            url=HttpUrl(f"https://www.starexec.org/starexec/secure/download?type=solver&id={solver_id}"),
            h=None,
        )

    solver_ids = row[CsvColumn.starexec_id].split(";")

    def find_archive_id(track_id: Option[str]) -> Option[int]:
        r = (
            re.compile(" *([0-9]+)+\\(" + track_id.unwrap() + "\\) *")
            if track_id.is_some
            else re.compile(" *([0-9]+) *")
        )
        for solver_id in solver_ids:
            g = r.fullmatch(solver_id)
            if g:
                return Some(int(g.group(1)))
        return Option.NONE()

    cache_confs: Dict[int, list[str]] = {}

    def has_configuration(id: int, track_id: str) -> bool:
        return track_id in configurations_on_starexec(id, cache_confs)

    def find_archive(track_id: Option[str]) -> Tuple[Option[defs.Archive], Option[defs.Command]]:
        main_id = find_archive_id(track_id)
        archive = main_id.map(archive_of_solver_id)

        id = main_id if main_id else find_archive_id(Option.NONE())
        track_id2 = track_id.unwrap_or("default")
        if id:
            if has_configuration(id.unwrap(), track_id2):
                command = Some(defs.Command(binary="bin/starexec_run_" + track_id2))
            elif has_configuration(id.unwrap(), "default"):
                command = Some(defs.Command(binary="bin/starexec_run_default"))
            elif track_id2 == "default" and len(configurations_on_starexec(id.unwrap(), cache_confs)) == 1:
                # Seems that if there is only one configuration it is accepted
                # as the default
                command = Some(
                    defs.Command(binary="bin/starexec_run_" + configurations_on_starexec(id.unwrap(), cache_confs)[0])
                )
            else:
                command = Option.NONE()

        else:
            command = Option.NONE()
        return archive, command

    archive, command = find_archive(Option.NONE())
    contributors = [
        defs.Contributor(name=name) for line in row[CsvColumn.contributors].splitlines() for name in line.split(",")
    ]
    participations: List[defs.Participation] = []

    def add_track(col: CsvColumn, track: defs.Track, shortcut: str) -> None:
        if row[col] != "" and row[col] != "-":
            archive, command = find_archive(Some(shortcut))
            participations.append(
                defs.Participation(
                    tracks=[track],
                    logics=defs.Logics.from_regexp(row[col].strip()),
                    archive=archive.unwrap_or(None),
                    command=command.unwrap_or(None),
                )
            )

    add_track(CsvColumn.track_single_query, defs.Track.SingleQuery, "sq")
    add_track(CsvColumn.track_unsat_core, defs.Track.UnsatCore, "uc")
    add_track(CsvColumn.track_incremental, defs.Track.Incremental, "inc")
    add_track(CsvColumn.track_model_validation, defs.Track.ModelValidation, "mv")
    add_track(CsvColumn.track_proof, defs.Track.ProofExhibition, "proof")
    add_track(CsvColumn.track_parallel, defs.Track.Parallel, "par")
    add_track(CsvColumn.track_cloud, defs.Track.Cloud, "cloud")
    return defs.Submission(
        name=row[CsvColumn.name],
        contributors=contributors,
        contacts=[defs.NameEmail(name="", email=row[CsvColumn.contact])],
        archive=archive.unwrap_or(None),
        website=HttpUrl(row[CsvColumn.homepage]),
        system_description=HttpUrl(row[CsvColumn.system_description]),
        command=command.unwrap_or(None),
        solver_type=defs.SolverType.standalone,
        participations=defs.Participations(root=participations),
    )


def convert_csv(file: Path, dstdir: Path) -> None:
    with open(file) as dcsv:
        registrations = csv.DictReader(dcsv)
        for row in track(list(registrations), description="Asking StarExec for prover configurations"):
            if row[CsvColumn.starexec_id] != "-1":
                submission = convert_row(row, dstdir)
                with open(Path.joinpath(dstdir, submission.name + ".json"), "w") as f:
                    f.write(submission.model_dump_json())
