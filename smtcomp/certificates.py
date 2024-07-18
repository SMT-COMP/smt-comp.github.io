#!/usr/bin/python3

import sys
import csv
from typing import Any, Callable, Tuple
from pathlib import Path
import json
import os
from collections import defaultdict
import smtcomp.defs as defs
import smtcomp.results as results
import smtcomp.generate_website_page as page

show_experimental = False


class category(dict):
    def latex(self) -> str:
        l = []
        if self.get("sq_seq"):
            l.append("\\seq")
        if self.get("sq_par"):
            l.append("\\paral")
        if self.get("sq_sat"):
            l.append("\\sat")
        if self.get("sq_unsat"):
            l.append("\\unsat")
        if self.get("sq_24"):
            l.append("\\fast")
        if self.get("inc"):
            l.append("\\inc")
        if self.get("uc_seq") and self.get("uc_par"):
            l.append("\\uc")
        else:
            if self.get("uc_seq"):
                l.append("\\uc\\textsuperscript\\seq")
            if self.get("uc_par"):
                l.append("\\uc\\textsuperscript\\paral")
        if self.get("mv_seq") and self.get("mv_par"):
            l.append("\\mv")
        else:
            if self.get("mv_seq"):
                l.append("\\mv\\seq")
            if self.get("mv_par"):
                l.append("\\mv\\paral")
        if self.get("cloud"):
            l.append("\\cloud")
        if self.get("parallel"):
            l.append("\\paralTrack")
        return ",".join(l)

    def isNotEmpty(self) -> bool:
        for _, v in self.items():
            if v:
                return True
        return False

    def update(self, name: Any, value: Any) -> None:  # type: ignore
        if self.get(name, False) is None:
            return
        else:
            self[name] = value


def withtrack(l: list[str], name: str, category: category) -> None:
    if category.isNotEmpty():
        l.append("\\withtrack{{{name}}}{{{category}}}".format(name=name.replace("_", "\\_"), category=category.latex()))


class overall:

    def __init__(self) -> None:
        self.biggest = category()
        self.largest = category()

    def latex(self) -> str:
        l: list[str] = []
        withtrack(l, "Biggest Lead", self.biggest)
        withtrack(l, "Largest Contribution", self.largest)
        return ", ".join(l)

    def __str__(self) -> str:
        return self.latex()

    def isNotEmpty(self) -> bool:
        return self.biggest.isNotEmpty() and self.largest.isNotEmpty()


class info:
    def __init__(self) -> None:
        self.overall = overall()
        self.divisions: defaultdict[str, category] = defaultdict(category)
        self.logics: defaultdict[str, category] = defaultdict(category)
        self.members: int = 0

    def latex(self, name: str) -> str:
        l: list[str] = []
        for k, v in sorted(self.divisions.items()):
            withtrack(l, k, v)
        s_for_divisions = "s" if len(l) >= 2 else ""
        divisions = ", ".join(l)

        l.clear()
        for k, v in sorted(self.logics.items()):
            withtrack(l, k, v)
        s_for_logics = "s" if len(l) >= 2 else ""
        logics = ", ".join(l)

        return "\\MakeOnePage{{{name}}}{{{overall}}}{{{divisions}}}{{{logics}}}{{{s_for_divisions}}}{{{s_for_logics}}}".format(
            name=name,
            overall=self.overall.latex(),
            divisions=divisions,
            logics=logics,
            s_for_divisions=s_for_divisions,
            s_for_logics=s_for_logics,
        )

    def isNotEmpty(self) -> bool:
        return (
            self.overall.isNotEmpty()
            or any(cat.isNotEmpty() for _, cat in self.divisions.items())
            or any(cat.isNotEmpty() for _, cat in self.logics.items())
        )

    def __str__(self) -> str:
        return str(self.overall)

    def __repr__(self) -> str:
        return str(self.overall)


def update(
    solvers: defaultdict[str, info],
    select: Callable[[info, str], None],
    podium: page.PodiumDivision | page.PodiumBiggestLead | page.PodiumLargestContribution,
) -> None:
    if podium.track == "track_single_query":
        select(solvers[podium.winner_seq], "sq_seq")
        select(solvers[podium.winner_par], "sq_par")
        select(solvers[podium.winner_sat], "sq_sat")
        select(solvers[podium.winner_unsat], "sq_unsat")
        select(solvers[podium.winner_24s], "sq_24")

    if podium.track == "track_incremental":
        select(solvers[podium.winner_par], "inc")

    if podium.track == "track_unsat_core":
        select(solvers[podium.winner_par], "uc_par")
        select(solvers[podium.winner_seq], "uc_seq")

    if podium.track == "track_model_validation":
        select(solvers[podium.winner_par], "mv_par")
        select(solvers[podium.winner_seq], "mv_seq")

    if show_experimental and podium.track == "track_cloud":
        select(solvers[podium.winner_par], "cloud")

    if show_experimental and podium.track == "track_parallel":
        select(solvers[podium.winner_par], "parallel")


def select_division(division: str, logics: dict[str, int]) -> Callable[[info, str], None]:
    def select(solver: info, track: str) -> None:
        for v, _ in logics.items():
            solver.logics[v].update(track, None)
        solver.divisions[division].update(track, True)

    return select


def add_logic(logics: dict[Tuple[str, str], bool], list: dict[str, int], track: str) -> None:
    for v, _ in list.items():
        logics[v, track] = True


def parse_pretty_names(solvers: defaultdict[str, info], pretty_names: Path) -> None:
    with open(pretty_names, newline="") as input:
        input = csv.DictReader(input)  # type: ignore

        for row in input:
            solvers[row["Solver Name"]].members = int(row["Members"])  # type: ignore


def parse_experimental_division(solvers: Any, experimental_division: Path) -> dict[str, bool]:
    res: dict[str, bool] = {}
    with open(experimental_division, newline="") as input:
        input = csv.DictReader(input)  # type: ignore

        for row in input:
            res[(row["division"], "track_" + row["track"])] = True  # type: ignore
    return res


def generate_certificates(
    website_results: Path, input_for_certificates: Path, pretty_names: Path, experimental_division: Path
) -> None:
    solvers: defaultdict[str, info] = defaultdict(info)

    parse_pretty_names(solvers, pretty_names)
    solvers["-"].members = 0

    # Remove experimental division
    if show_experimental:
        experimental_divisions = {}
    else:
        experimental_divisions = parse_experimental_division(solvers, experimental_division)

    existing_logics: dict[Tuple[str, str], bool] = {}
    delayed_logic: list[page.PodiumDivision] = []  # we wait to know which logic are competitive

    list_dir = list(os.listdir(website_results))
    list_dir.sort()
    for result_basename in list_dir:
        file = website_results / result_basename
        if not file.is_file():
            break

        result = page.Podium.model_validate_json(file.read_text()).root

        match result:
            case page.Summary():
                print("Useless: ", file)
                continue
            case page.PodiumCrossDivision():
                match result.root:
                    case page.PodiumBiggestLead():
                        update(solvers, (lambda x, k: x.overall.biggest.update(k, True)), result.root)
                    case page.PodiumLargestContribution():
                        update(solvers, (lambda x, k: x.overall.largest.update(k, True)), result.root)
            case page.PodiumDivision():
                if result.logics:
                    if not (result.division, result.track) in experimental_divisions:
                        update(solvers, select_division(result.division, result.logics), result)
                        add_logic(existing_logics, result.logics, result.track)
                    else:
                        print("experimental division:", result.division, result.track)
                else:
                    delayed_logic.append(result)

    for dresult in delayed_logic:
        if (dresult.division, dresult.track) in existing_logics:
            update(solvers, (lambda x, k: x.logics[dresult.division].update(k, True)), dresult)
        else:
            print("experimental logic:", dresult.division, dresult.track)

    # print the result
    with open(input_for_certificates, "w", newline="") as output:
        for key, value in sorted(solvers.items(), key=lambda x: x[0].lower()):
            if value.isNotEmpty() and value.members != 0:
                print("solver: ", key, "(", value.members, ")")
                if True:
                    #                for i in range(0,value.members):
                    output.write(value.latex(key))
                    output.write("\n\\newpage\n")
                    output.flush()
            else:
                print("solver: ", key, "( no certificate )")
