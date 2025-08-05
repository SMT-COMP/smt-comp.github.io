import math
import functools, itertools
from collections import defaultdict
from typing import Set, Dict, Optional, cast, List, DefaultDict, Tuple
from pathlib import Path, PurePath
from smtcomp import defs
from rich import progress
from rich import print
from pydantic import BaseModel, RootModel, Field, PlainSerializer, PlainValidator
import polars as pl
import smtcomp.scoring
from smtcomp.utils import *
import smtcomp.results


def to_track_name(track: defs.Track) -> str:
    match track:
        case defs.Track.SingleQuery:
            return "track_single_query"
        case defs.Track.Incremental:
            return "track_incremental"
        case defs.Track.ModelValidation:
            return "track_model_validation"
        case defs.Track.ProofExhibition:
            return "track_proof_exhibition"
        case defs.Track.UnsatCore:
            return "track_unsat_core"
        case defs.Track.UnsatCoreValidation:
            raise (ValueError("No results for this internal track"))
        case defs.Track.Cloud:
            return "track_cloud"
        case defs.Track.Parallel:
            return "track_parallel"


def of_track_name(track: str | defs.Track) -> defs.Track:
    if isinstance(track, defs.Track):
        return track
    match track:
        case "track_single_query":
            return defs.Track.SingleQuery
        case "track_incremental":
            return defs.Track.Incremental
        case "track_model_validation":
            return defs.Track.ModelValidation
        case "track_proof_exhibition":
            return defs.Track.ProofExhibition
        case "track_unsat_core":
            return defs.Track.UnsatCore
        case "track_cloud":
            return defs.Track.Cloud
        case "track_parallel":
            return defs.Track.Parallel
        case _:
            raise (ValueError("Unknown track name"))


track_name = Annotated[
    defs.Track, PlainSerializer(to_track_name, return_type=str, when_used="json"), PlainValidator(of_track_name)
]


def page_track_suffix(track: defs.Track) -> str:
    match track:
        case defs.Track.SingleQuery:
            return "single-query"
        case defs.Track.Incremental:
            return "incremental"
        case defs.Track.ModelValidation:
            return "model-validation"
        case defs.Track.ProofExhibition:
            return "proof-exhibition"
        case defs.Track.UnsatCore:
            return "unsat-core"
        case defs.Track.UnsatCoreValidation:
            raise (ValueError("No results for this internal track"))
        case defs.Track.Cloud:
            return "cloud"
        case defs.Track.Parallel:
            return "parallel"


# Warning: Hugo lowercase all dict keys

float_6dig = Annotated[
    float,
    PlainSerializer(
        lambda x: round(x, 6),
        return_type=float,
        when_used="json",
    ),
]


class PodiumStep(BaseModel):
    name: str
    baseSolver: str
    deltaBaseSolver: int
    competing: str  # yes or no
    errorScore: int
    correctScore: int
    CPUScore: float_6dig
    WallScore: float_6dig
    solved: int
    solved_sat: int
    solved_unsat: int
    unsolved: int
    abstained: int
    timeout: int
    memout: int


class PodiumDivision(BaseModel):
    resultdate: str
    year: int
    divisions: str  # divisions_2023
    participants: str  # participants_2023
    disagreements: str  # disagreements_2023
    division: str  # Arith
    is_competitive: bool  # true = least 2 subst. different solvers were submitted
    track: track_name
    n_benchmarks: int
    time_limit: int
    mem_limit: int
    logics: dict[str, int]
    winner_seq: str
    winner_par: str
    winner_sat: str
    winner_unsat: str
    winner_24s: str

    sequential: list[PodiumStep]
    parallel: list[PodiumStep]
    sat: list[PodiumStep]
    unsat: list[PodiumStep]
    twentyfour: list[PodiumStep]

    layout: Literal["result"] = "result"


class PodiumSummaryResults(BaseModel):
    track: track_name
    divisions: list[PodiumDivision]
    layout: Literal["results_summary"] = "results_summary"


class PodiumStepOverallScore(BaseModel):
    name: str
    contribution: float_6dig  # nn_D * log10 N_D
    division: str
    tieBreakTimeScore: float_6dig


class PodiumBestOverall(BaseModel):
    resultdate: str
    year: int
    results: str
    participants: str
    track: track_name
    recognition: Literal["best_overall"] = "best_overall"
    winner_seq: str
    winner_par: str
    winner_sat: str
    winner_unsat: str
    winner_24s: str
    winner_seq_score: float_6dig
    winner_par_score: float_6dig
    winner_sat_score: float_6dig
    winner_unsat_score: float_6dig
    winner_24s_score: float_6dig
    sequential: list[PodiumStepOverallScore]
    parallel: list[PodiumStepOverallScore]
    sat: list[PodiumStepOverallScore]
    unsat: list[PodiumStepOverallScore]
    twentyfour: list[PodiumStepOverallScore]
    layout: Literal["result_comp"] = "result_comp"


class PodiumStepBiggestLead(BaseModel):
    name: str
    second: str
    correctScore: float_6dig
    timeScore: float_6dig
    division: str


class PodiumBiggestLead(BaseModel):
    resultdate: str
    year: int
    results: str
    participants: str
    track: track_name
    recognition: Literal["biggest_lead"] = "biggest_lead"
    winner_seq: str
    winner_par: str
    winner_sat: str
    winner_unsat: str
    winner_24s: str
    sequential: list[PodiumStepBiggestLead]
    parallel: list[PodiumStepBiggestLead]
    sat: list[PodiumStepBiggestLead]
    unsat: list[PodiumStepBiggestLead]
    twentyfour: list[PodiumStepBiggestLead]
    layout: Literal["result_comp"] = "result_comp"


class PodiumStepLargestContribution(BaseModel):
    name: str
    correctScore: float_6dig
    timeScore: float_6dig
    division: str
    experimental: str = "false"


class PodiumLargestContribution(BaseModel):
    resultdate: str
    year: int
    results: str
    participants: str
    track: track_name
    recognition: Literal["largest_contribution"] = "largest_contribution"
    winner_seq: str
    winner_par: str
    winner_sat: str
    winner_unsat: str
    winner_24s: str
    sequential: list[PodiumStepLargestContribution]
    parallel: list[PodiumStepLargestContribution]
    sat: list[PodiumStepLargestContribution]
    unsat: list[PodiumStepLargestContribution]
    twentyfour: list[PodiumStepLargestContribution]
    layout: Literal["result_comp"] = "result_comp"


class PodiumCrossDivision(RootModel):
    root: PodiumBestOverall | PodiumLargestContribution | PodiumBiggestLead = Field(..., discriminator="recognition")


class Podium(RootModel):
    root: PodiumDivision | PodiumCrossDivision | PodiumSummaryResults = Field(..., discriminator="layout")


def podium_steps(config: defs.Config, podium: List[dict[str, Any]] | None) -> List[PodiumStep]:
    if podium is None:
        return []
    else:
        podiums = []
        non_competitive = []
        for s in podium:
            cscore = s["correctly_solved_score"]
            delta = 0
            derived_solver = defs.Config.baseSolverMap2025.get(s["solver"], "")
            if derived_solver != "":
                for sprime in podium:
                    if sprime["solver"] == defs.Config.baseSolverMap2025.get(s["solver"], ""):
                        delta = cscore - sprime["correctly_solved_score"]
                        break

            ps = PodiumStep(
                name=s["solver"],
                baseSolver=derived_solver,
                deltaBaseSolver=delta,
                competing="yes" if s["solver"] in config.competitive_solvers else "no",
                errorScore=s["error_score"],
                correctScore=s["correctly_solved_score"],
                CPUScore=s["cpu_time_score"],
                WallScore=s["wallclock_time_score"],
                solved=s["solved"],
                solved_sat=s["solved_sat"],
                solved_unsat=s["solved_unsat"],
                unsolved=s["unsolved"],
                abstained=s["abstained"],
                timeout=s["timeout"],
                memout=s["memout"],
            )

            if not s["solver"] in config.competitive_solvers:
                non_competitive.append(ps)
            else:
                podiums.append(ps)

        return podiums + non_competitive


def make_podium(
    config: defs.Config, d: dict[str, Any], for_division: bool, track: defs.Track, results: pl.LazyFrame
) -> PodiumDivision:
    def get_winner(l: List[dict[str, str]] | None) -> str:
        if l is None or not l:
            return "-"

        l = [e for e in l if e["solver"] in config.competitive_solvers]

        if l is None or not l or l[0]["correctly_solved_score"] == 0:
            return "-"
        else:
            return l[0]["solver"]

    def is_competitive_division(results: pl.LazyFrame, division: int, for_division: bool) -> bool:
        """
        A division in a track is competitive if at least two substantially different
        solvers (i.e., solvers from two different teams) were submitted.
        """

        solvers = (
            results.filter(pl.col("division" if for_division else "logic") == division)
            .select("solver")
            .unique()
            .collect()
            .get_column("solver")
            .to_list()
        )

        # Avoid solvers of the same solver family under the assumption
        # of the following format: <solver-family>-<suffix> (holds for SMT-COMP 2025)
        # TODO: improve this criterion in the future
        return len(set([sol.split("-")[0].lower() for sol in solvers])) >= 2

    if for_division:
        competitive_division = is_competitive_division(results, d["division"], for_division)
        division = defs.Division.name_of_int(d["division"])
        logics = dict((defs.Logic.name_of_int(d2["logic"]), d2["n"]) for d2 in d["logics"])
    else:
        division = defs.Logic.name_of_int(d["logic"])
        competitive_division = is_competitive_division(results, d["logic"], for_division)
        logics = dict()

    if (track == defs.Track.Cloud) | (track == defs.Track.Parallel):
        winner_seq = "-"
        steps_seq = []
    else:
        winner_seq = get_winner(d[smtcomp.scoring.Kind.seq.name])
        steps_seq = podium_steps(config, d[smtcomp.scoring.Kind.seq.name])

    return PodiumDivision(
        resultdate="2025-08-11",
        year=config.current_year,
        divisions=f"divisions_{config.current_year}",
        is_competitive=competitive_division,
        participants=f"participants_{config.current_year}",
        disagreements=f"disagreements_{config.current_year}",
        division=division,
        track=track,
        n_benchmarks=d["total"],
        time_limit=config.timelimit_s,
        mem_limit=config.memlimit_M,
        logics=dict(sorted(logics.items())),
        winner_seq=winner_seq,
        winner_par=get_winner(d[smtcomp.scoring.Kind.par.name]),
        winner_sat=get_winner(d[smtcomp.scoring.Kind.sat.name]),
        winner_unsat=get_winner(d[smtcomp.scoring.Kind.unsat.name]),
        winner_24s=get_winner(d[smtcomp.scoring.Kind.twentyfour.name]),
        sequential=steps_seq,
        parallel=podium_steps(config, d[smtcomp.scoring.Kind.par.name]),
        sat=podium_steps(config, d[smtcomp.scoring.Kind.sat.name]),
        unsat=podium_steps(config, d[smtcomp.scoring.Kind.unsat.name]),
        twentyfour=podium_steps(config, d[smtcomp.scoring.Kind.twentyfour.name]),
    )


def sq_generate_datas(
    config: defs.Config, selection: pl.LazyFrame, results: pl.LazyFrame, for_division: bool, track: defs.Track
) -> dict[str, PodiumDivision]:
    """
    Generate datas for divisions or for logics
    """

    if for_division:
        group_by = "division"
        name_of_int = defs.Division.name_of_int
    else:
        group_by = "logic"
        name_of_int = defs.Logic.name_of_int

    selection = selection.filter(selected=True)

    # TODO it should be done after filter_for
    len_by_division = selection.group_by(group_by).agg(total=pl.len())

    def info_for_podium_step(kind: smtcomp.scoring.Kind, config: defs.Config, results: pl.LazyFrame) -> pl.LazyFrame:
        results = smtcomp.scoring.filter_for(kind, config, results)
        return (
            sort(
                intersect(results, len_by_division, on=[group_by])
                .group_by(group_by, "solver")
                .agg(
                    pl.sum("error_score"),
                    pl.sum("correctly_solved_score"),
                    pl.sum("cpu_time_score"),
                    pl.sum("wallclock_time_score"),
                    solved=(smtcomp.scoring.known_answer).sum(),
                    solved_sat=(smtcomp.scoring.sat_answer).sum(),
                    solved_unsat=(smtcomp.scoring.unsat_answer).sum(),
                    unsolved=(smtcomp.scoring.unknown_answer).sum(),
                    timeout=(smtcomp.scoring.timeout_answer).sum(),
                    memout=(smtcomp.scoring.memout_answer).sum(),
                    abstained=pl.col("total").first() - pl.len(),
                ),
                [(group_by, False)] + smtcomp.scoring.scores + [("solver", False)],
            )
            .group_by(group_by, maintain_order=True)
            .agg(
                pl.struct(
                    "solver",
                    "error_score",
                    "correctly_solved_score",
                    "cpu_time_score",
                    "wallclock_time_score",
                    "solved",
                    "solved_sat",
                    "solved_unsat",
                    "unsolved",
                    "timeout",
                    "memout",
                    "abstained",
                ).alias(kind.name)
            )
        )

    if for_division:
        lf_logics = [
            selection.group_by("division", "logic")
            .agg(n=pl.len())
            .group_by("division")
            .agg(logics=pl.struct("logic", "n"))
        ]
    else:
        lf_logics = []

    l = [len_by_division] + lf_logics + [info_for_podium_step(kind, config, results) for kind in smtcomp.scoring.Kind]

    r = functools.reduce(lambda x, y: x.join(y, validate="1:1", on=[group_by], how="left"), l)

    df = r.collect()

    return dict((name_of_int(d[group_by]), make_podium(config, d, for_division, track, results)) for d in df.to_dicts())


def get_kind(a: PodiumDivision, k: smtcomp.scoring.Kind) -> list[PodiumStep]:
    match k:
        case smtcomp.scoring.Kind.seq:
            return a.sequential
        case smtcomp.scoring.Kind.par:
            return a.parallel
        case smtcomp.scoring.Kind.sat:
            return a.sat
        case smtcomp.scoring.Kind.unsat:
            return a.unsat
        case smtcomp.scoring.Kind.twentyfour:
            return a.twentyfour


# Computes the new global ranking based on the distance between the winner of a
# division and the second solver in a division as defined in section 7.3.1 of
# the SMT-COMP'19 rules.
#
# data      : The podium as returned by process_csv.
# sequential: True if results are to be computed for sequential performance.
#
# return    : A list of PodimStepBiggestLead
def biggest_lead_ranking_for_kind(
    data: dict[str, PodiumDivision], k: smtcomp.scoring.Kind
) -> list[PodiumStepBiggestLead]:
    scores = []
    for division, div_data in data.items():
        l = get_kind(div_data, k)
        # Skip non-competitive divisions, TODO
        if len(l) <= 1:
            continue
        assert len(l) >= 2
        first = l[0]
        second = l[1]

        # If no solver was able to solve a single instance, there is no
        # winner for this division.
        if first.correctScore == 0:
            continue

        if k == smtcomp.scoring.Kind.seq:
            time_first = first.CPUScore
            time_second = second.CPUScore
        else:
            time_first = first.WallScore
            time_second = second.WallScore

        # Compute score and time distance between first and second in the
        # division.
        # Note: The time score is only used if solvers have the same score
        # lead.
        score = (1 + first.correctScore) / (1 + second.correctScore)
        time = (1 + time_second) / (1 + time_first)
        scores.append(
            PodiumStepBiggestLead(
                name=first.name, second=second.name, correctScore=score, timeScore=time, division=division
            )
        )

        scores = sorted(scores, key=lambda x: (x.correctScore, x.timeScore), reverse=True)

    return scores


def biggest_lead_ranking(config: defs.Config, data: dict[str, PodiumDivision], track: defs.Track) -> PodiumBiggestLead:

    def get_winner(l: List[PodiumStepBiggestLead] | None) -> str:
        # TODO select only participating
        if l is None or not l:
            return "-"
        else:
            return l[0].name

    sequential = biggest_lead_ranking_for_kind(data, smtcomp.scoring.Kind.seq)
    parallel = biggest_lead_ranking_for_kind(data, smtcomp.scoring.Kind.par)
    sat = biggest_lead_ranking_for_kind(data, smtcomp.scoring.Kind.sat)
    unsat = biggest_lead_ranking_for_kind(data, smtcomp.scoring.Kind.unsat)
    twentyfour = biggest_lead_ranking_for_kind(data, smtcomp.scoring.Kind.twentyfour)

    if (track == defs.Track.Cloud) | (track == defs.Track.Parallel):
        winner_seq = "-"
        sequential = []
    else:
        winner_seq = get_winner(sequential)

    return PodiumBiggestLead(
        resultdate="2025-08-11",
        year=config.current_year,
        track=track,
        results=f"results_{config.current_year}",
        participants=f"participants_{config.current_year}",
        winner_seq=winner_seq,
        winner_par=get_winner(parallel),
        winner_sat=get_winner(sat),
        winner_unsat=get_winner(unsat),
        winner_24s=get_winner(twentyfour),
        sequential=sequential,
        parallel=parallel,
        sat=sat,
        unsat=unsat,
        twentyfour=twentyfour,
    )


# Compute normalized correctness score
#
# normalized correctness score: nnD = (nD /ND)**2 if eD == 0
#                                   = -2          otherwise
def normalized_correctness_score(
    data: dict[str, PodiumDivision], scores: pl.LazyFrame, track: defs.Track, k: smtcomp.scoring.Kind
) -> list[PodiumStepOverallScore]:

    podiumSteps: list[PodiumStepOverallScore] = []

    for division, div_data in data.items():
        solvers_in_div = get_kind(div_data, k)
        if len(solvers_in_div) <= 1:
            continue

        N_D = get_N_D(scores, data, division, track)
        for sol_in_div in solvers_in_div:
            if sol_in_div.errorScore == 0:
                nn_D = (sol_in_div.correctScore / N_D) ** 2
            else:
                nn_D = -2

            podiumSteps.append(
                PodiumStepOverallScore(
                    name=sol_in_div.name,
                    contribution=nn_D * (math.log10(N_D) if N_D > 0 else 0),
                    tieBreakTimeScore=sol_in_div.CPUScore if k == smtcomp.scoring.Kind.seq else sol_in_div.WallScore,
                    division=division,
                )
            )
        podiumSteps = sorted(podiumSteps, key=lambda x: (x.contribution, x.tieBreakTimeScore), reverse=True)
    return podiumSteps


#  N_D  :=         total number of check sats in division D    if Incremental Track
#                  total number of asserts in division D       if Unsat Core Track
#                  total number of benchmarks                  otherwise
def get_N_D(scores: pl.LazyFrame, data: dict[str, PodiumDivision], division: str, track: defs.Track) -> int:
    if track == defs.Track.Incremental:
        return int(
            scores.unique(["division", "file"])
            .group_by(["division"])
            .agg([pl.col("check_sats").sum().alias("total_check_sats")])
            .filter(pl.col("division") == int(defs.Division[division]))
            .collect()["total_check_sats"][0]
        )

    elif track == defs.Track.UnsatCore:
        return int(
            scores.unique(["division", "file"])
            .group_by(["division"])
            .agg([pl.col("asserts").sum().alias("total_asserts")])
            .filter(pl.col("division") == int(defs.Division[division]))
            .collect()["total_asserts"][0]
        )

    return data[division].n_benchmarks


# Computes the best overall ranking as specified in Section 7.3.1 of
# SMT-COMP 2025 rules. I.e:
#
# normalized correctness score: nnD = (nD /ND)**2 if eD == 0
#                                  = -2          otherwise
# overall score               : sum_D nnD*log10 ND
#
# For the choices, see the footnote in the rules.
#
def best_overall_ranking(
    config: defs.Config, scores: pl.LazyFrame, data: dict[str, PodiumDivision], track: defs.Track
) -> PodiumBestOverall:
    def get_winner(
        l: Optional[List[PodiumStepOverallScore]],
        scores: pl.LazyFrame,
        data: dict[str, PodiumDivision],
        track: defs.Track,
    ) -> Tuple[str, float]:
        if l is None or not l:
            return ("-", 0.0)
        else:
            podium: DefaultDict[str, Dict[str, float]] = defaultdict(lambda: {"score": 0.0, "tie_break_time": 0.0})
            for entry in l:
                podium[entry.name]["score"] += entry.contribution
                podium[entry.name]["tie_break_time"] += entry.tieBreakTimeScore
            winner, winner_data = max(podium.items(), key=lambda item: (item[1]["score"], -item[1]["tie_break_time"]))
            return (winner, winner_data["score"])

    sequential = normalized_correctness_score(data, scores, track, smtcomp.scoring.Kind.seq)
    parallel = normalized_correctness_score(data, scores, track, smtcomp.scoring.Kind.par)
    sat = normalized_correctness_score(data, scores, track, smtcomp.scoring.Kind.sat)
    unsat = normalized_correctness_score(data, scores, track, smtcomp.scoring.Kind.unsat)
    twentyfour = normalized_correctness_score(data, scores, track, smtcomp.scoring.Kind.twentyfour)

    if track in (defs.Track.Cloud, defs.Track.Parallel):
        winner_seq = ("-", 0.0)
        sequential = []
    else:
        winner_seq = get_winner(sequential, scores, data, track)

    return PodiumBestOverall(
        resultdate="2025-08-11",
        year=config.current_year,
        track=track,
        results=f"results_{config.current_year}",
        participants=f"participants_{config.current_year}",
        recognition="best_overall",
        winner_seq=winner_seq[0],
        winner_par=get_winner(parallel, scores, data, track)[0],
        winner_sat=get_winner(sat, scores, data, track)[0],
        winner_unsat=get_winner(unsat, scores, data, track)[0],
        winner_24s=get_winner(twentyfour, scores, data, track)[0],
        winner_seq_score=winner_seq[1],
        winner_par_score=get_winner(parallel, scores, data, track)[1],
        winner_sat_score=get_winner(sat, scores, data, track)[1],
        winner_unsat_score=get_winner(unsat, scores, data, track)[1],
        winner_24s_score=get_winner(twentyfour, scores, data, track)[1],
        sequential=sequential,
        parallel=parallel,
        sat=sat,
        unsat=unsat,
        twentyfour=twentyfour,
    )


def largest_contribution_ranking(
    config: defs.Config,
    virtual_datas: Dict[str, PodiumDivision],
    virtual_without_solver_datas: Dict[str, PodiumDivision],
    ratio_by_division: Dict[str, float],
    track: defs.Track,
) -> PodiumLargestContribution:

    def get_winner(l: List[PodiumStepLargestContribution] | None) -> str:
        # TODO select only participating
        if l is None or not l:
            return "-"
        else:
            return l[0].name

    def aux(k: smtcomp.scoring.Kind, div: str) -> List[PodiumStepLargestContribution]:
        v_steps = get_kind(virtual_datas[div], k)
        vws_steps = get_kind(virtual_without_solver_datas[div], k)
        if not v_steps:
            assert not vws_steps
            return []
        if len(vws_steps) <= 2:
            return []
        virtual = v_steps[0]
        assert virtual.name == "virtual"
        ratio = ratio_by_division[div]

        def timeScore(vws_step: PodiumStep) -> float:
            assert vws_step.correctScore <= virtual.correctScore
            if k == smtcomp.scoring.Kind.seq:
                v_time_score = virtual.CPUScore
                vws_time_score = vws_step.CPUScore
            else:
                v_time_score = virtual.WallScore
                vws_time_score = vws_step.WallScore
            if vws_time_score == 0:
                # The rules do not take into account this case
                return ratio
            else:
                return ratio * (1.0 - ((v_time_score / vws_time_score)))

        return [
            PodiumStepLargestContribution(
                name=vws_step.name,
                correctScore=ratio * (1.0 - (vws_step.correctScore / virtual.correctScore)),
                timeScore=timeScore(vws_step),
                division=div,
            )
            for vws_step in vws_steps
        ]

    ld = dict(
        (
            k,
            sorted(
                itertools.chain.from_iterable(aux(k, div) for div in ratio_by_division),
                key=lambda k: (k.correctScore, k.timeScore, k.division),
                reverse=True,
            )[0:19],
        )
        for k in smtcomp.scoring.Kind
    )

    if (track == defs.Track.Cloud) | (track == defs.Track.Parallel):
        winner_seq = "-"
        steps_seq = []
    else:
        winner_seq = get_winner(ld[smtcomp.scoring.Kind.seq])
        steps_seq = ld[smtcomp.scoring.Kind.seq]

    return PodiumLargestContribution(
        resultdate="2025-08-11",
        year=config.current_year,
        track=track,
        results=f"results_{config.current_year}",
        participants=f"participants_{config.current_year}",
        winner_seq=winner_seq,
        winner_par=get_winner(ld[smtcomp.scoring.Kind.par]),
        winner_sat=get_winner(ld[smtcomp.scoring.Kind.sat]),
        winner_unsat=get_winner(ld[smtcomp.scoring.Kind.unsat]),
        winner_24s=get_winner(ld[smtcomp.scoring.Kind.twentyfour]),
        sequential=steps_seq,
        parallel=ld[smtcomp.scoring.Kind.par],
        sat=ld[smtcomp.scoring.Kind.sat],
        unsat=ld[smtcomp.scoring.Kind.unsat],
        twentyfour=ld[smtcomp.scoring.Kind.twentyfour],
    )


def largest_contribution(
    config: defs.Config, selection: pl.LazyFrame, scores: pl.LazyFrame, track: defs.Track
) -> PodiumLargestContribution:
    for_division = True
    # For each solver compute its corresponding best solver
    # TODO: check what is competitive solver (unsound?)

    scores = scores.filter(error_score=0, sound_solver=True).filter(pl.col("correctly_solved_score") > 0)
    scores_col = scores.collect()
    total_len = len(scores_col)
    scores = scores_col.lazy()
    ratio_by_division_ = scores.group_by("division").agg(total=(pl.len() / float(total_len))).collect().to_dict()
    ratio_by_division = dict(
        zip(map(defs.Division.name_of_int, ratio_by_division_["division"]), ratio_by_division_["total"])
    )

    # Virtual solver
    virtual_scores = (
        scores.group_by("division", "file")
        .agg(
            pl.max("correctly_solved_score"),
            pl.min("walltime_s"),
            pl.min("wallclock_time_score"),
            pl.min("cputime_s"),
            pl.min("cpu_time_score"),
            sound_status=pl.col("sound_status").first(),
            answer=pl.col("answer").first(),
        )
        .with_columns(solver=pl.lit("virtual"), error_score=0)
    )
    virtual_datas = sq_generate_datas(config, selection, virtual_scores, for_division, track)

    # For each solver Compute virtual solver without the solver
    solvers = scores.select("division", "solver").unique()
    virtual_without_solver_scores = (
        intersect(scores.rename({"solver": "other_solver"}), solvers, on=["division"])
        .filter(pl.col("solver") != pl.col("other_solver"))
        .drop("other_solver")
        .group_by("division", "solver", "file")
        .agg(
            pl.max("correctly_solved_score"),
            pl.min("walltime_s"),
            pl.min("wallclock_time_score"),
            pl.min("cputime_s"),
            pl.min("cpu_time_score"),
            sound_status=pl.col("sound_status").first(),
            error_score=0,
            answer=pl.col("answer").first(),
        )
    )
    virtual_without_solver_datas = sq_generate_datas(
        config, selection, virtual_without_solver_scores, for_division, track
    )

    large = largest_contribution_ranking(config, virtual_datas, virtual_without_solver_datas, ratio_by_division, track)

    if False:
        print(virtual_datas)
        print(virtual_without_solver_datas)
        print(large)

    return large


def export_results(config: defs.Config, selection: pl.LazyFrame, results: pl.LazyFrame, track: defs.Track) -> None:
    page_suffix = page_track_suffix(track)

    dst = config.web_results
    dst.mkdir(parents=True, exist_ok=True)

    scores = smtcomp.scoring.add_disagreements_info(results, track)
    scores = smtcomp.scoring.benchmark_scoring(scores, track)
    scores = scores.filter(disagreements=False).drop("disagreements")
    scores = scores.filter(track=int(track)).drop("track")
    scores = scores.collect().lazy()

    all_divisions: list[PodiumDivision] = []

    for for_division in [True, False]:
        datas = sq_generate_datas(config, selection, scores, for_division, track)

        for name, data in datas.items():
            (dst / f"{name.lower()}-{page_suffix}.md").write_text(data.model_dump_json(indent=1))

            if data.logics:
                all_divisions.append(data)

        if for_division:
            data_best_overall = best_overall_ranking(config, scores, datas, track)
            (dst / f"best-overall-{page_suffix}.md").write_text(data_best_overall.model_dump_json(indent=1))

            bigdata = biggest_lead_ranking(config, datas, track)
            (dst / f"biggest-lead-{page_suffix}.md").write_text(bigdata.model_dump_json(indent=1))

            largedata = largest_contribution(config, selection, scores, track)
            (dst / f"largest-contribution-{page_suffix}.md").write_text(largedata.model_dump_json(indent=1))

    all_divisions.sort(key=lambda x: x.division)
    summary_results = PodiumSummaryResults(track=track, divisions=all_divisions)
    (dst / f"results-{page_suffix}.md").write_text(summary_results.model_dump_json(indent=1))
