import functools, itertools
from typing import Set, Dict, Optional, cast, List, DefaultDict
from pathlib import Path, PurePath
from smtcomp import defs
from rich import progress
from rich import print
from pydantic import BaseModel, RootModel, Field
import polars as pl
import smtcomp.scoring
from smtcomp.utils import *
import smtcomp.results

# Warning: Hugo lowercase all dict keys


class PodiumStep(BaseModel):
    name: str
    competing: str  # yes or no
    errorScore: int
    correctScore: int
    CPUScore: float
    WallScore: float
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
    track: str  # track_single_query
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


class PodiumStepBiggestLead(BaseModel):
    name: str
    second: str
    correctScore: float
    timeScore: float
    division: str


class PodiumBiggestLead(BaseModel):
    resultdate: str
    year: int
    results: str
    participants: str
    track: str
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
    correctScore: float
    timeScore: float
    division: str
    experimental: str = "false"


class PodiumLargestContribution(BaseModel):
    resultdate: str
    year: int
    results: str
    participants: str
    track: str
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
    root: PodiumLargestContribution | PodiumBiggestLead = Field(..., discriminator="recognition")


class Summary(BaseModel):
    layout: Literal["results_summary"] = "results_summary"
    track: str
    scores: str = "sequential,parallel,sat,unsat,twentyfour"
    year: int
    results: str = "results"
    divisions: str = "divisions"
    participants: str = "participants"
    disagreements: str = "disagreements"


class Podium(RootModel):
    root: PodiumDivision | PodiumCrossDivision | Summary = Field(..., discriminator="layout")


def podium_steps(podium: List[dict[str, Any]] | None) -> List[PodiumStep]:
    if podium is None:
        return []
    else:
        return [
            PodiumStep(
                name=s["solver"],
                competing="yes",  # TODO
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
            for s in podium
        ]


def make_podium(config: defs.Config, d: dict[str, Any], for_division: bool) -> PodiumDivision:
    def get_winner(l: List[dict[str, str]] | None) -> str:
        # TODO select only participating
        if l is None or l[0]["correctly_solved_score"] == 0:
            return "-"
        else:
            return l[0]["solver"]

    if for_division:
        division = defs.Division.name_of_int(d["division"])
        logics = dict((defs.Logic.name_of_int(d2["logic"]), d2["n"]) for d2 in d["logics"])
    else:
        division = defs.Logic.name_of_int(d["logic"])
        logics = dict()

    return PodiumDivision(
        resultdate="2024-07-08",
        year=config.current_year,
        divisions=f"divisions_{config.current_year}",
        participants=f"participants_{config.current_year}",
        disagreements=f"disagreements_{config.current_year}",
        division=division,
        track="track_single_query",
        n_benchmarks=d["total"],
        time_limit=config.timelimit_s,
        mem_limit=config.memlimit_M,
        logics=dict(sorted(logics.items())),
        winner_seq=get_winner(d[smtcomp.scoring.Kind.seq.name]),
        winner_par=get_winner(d[smtcomp.scoring.Kind.par.name]),
        winner_sat=get_winner(d[smtcomp.scoring.Kind.sat.name]),
        winner_unsat=get_winner(d[smtcomp.scoring.Kind.unsat.name]),
        winner_24s=get_winner(d[smtcomp.scoring.Kind.twentyfour.name]),
        sequential=podium_steps(d[smtcomp.scoring.Kind.seq.name]),
        parallel=podium_steps(d[smtcomp.scoring.Kind.par.name]),
        sat=podium_steps(d[smtcomp.scoring.Kind.sat.name]),
        unsat=podium_steps(d[smtcomp.scoring.Kind.unsat.name]),
        twentyfour=podium_steps(d[smtcomp.scoring.Kind.twentyfour.name]),
    )


def sq_generate_datas(
    config: defs.Config, selection: pl.LazyFrame, results: pl.LazyFrame, for_division: bool
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

    # results = results.filter(track=int(defs.Track.SingleQuery)).drop("track")

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

    return dict((name_of_int(d[group_by]), make_podium(config, d, for_division)) for d in df.to_dicts())


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
# division and the second solver in a division as defined in secion 7.3.1 of
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


def biggest_lead_ranking(config: defs.Config, data: dict[str, PodiumDivision]) -> PodiumBiggestLead:

    def get_winner(l: List[PodiumStepBiggestLead] | None) -> str:
        # TODO select only participating
        if l is None:
            return "-"
        else:
            return l[0].name

    sequential = biggest_lead_ranking_for_kind(data, smtcomp.scoring.Kind.seq)
    parallel = biggest_lead_ranking_for_kind(data, smtcomp.scoring.Kind.par)
    sat = biggest_lead_ranking_for_kind(data, smtcomp.scoring.Kind.sat)
    unsat = biggest_lead_ranking_for_kind(data, smtcomp.scoring.Kind.unsat)
    twentyfour = biggest_lead_ranking_for_kind(data, smtcomp.scoring.Kind.twentyfour)

    return PodiumBiggestLead(
        resultdate="2024-07-08",
        year=config.current_year,
        track="track_single_query",
        results=f"results_{config.current_year}",
        participants=f"participants_{config.current_year}",
        winner_seq=get_winner(sequential),
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


def largest_contribution_ranking(
    config: defs.Config,
    virtual_datas: Dict[str, PodiumDivision],
    virtual_without_solver_datas: Dict[str, PodiumDivision],
    ratio_by_division: Dict[str, float],
) -> PodiumLargestContribution:

    def get_winner(l: List[PodiumStepLargestContribution] | None) -> str:
        # TODO select only participating
        if l is None:
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
        return [
            PodiumStepLargestContribution(
                name=step.name,
                correctScore=ratio * (1.0 - (step.correctScore / virtual.correctScore)),
                timeScore=ratio
                * (
                    1.0
                    - (
                        (virtual.CPUScore / step.CPUScore)
                        if k == smtcomp.scoring.Kind.seq
                        else (virtual.WallScore / step.WallScore)
                    )
                ),
                division=div,
            )
            for step in vws_steps
        ]

    ld = dict(
        (
            k,
            sorted(
                itertools.chain.from_iterable(aux(k, div) for div in ratio_by_division),
                key=lambda k: (k.correctScore, k.timeScore, k.division),
                reverse=True,
            ),
        )
        for k in smtcomp.scoring.Kind
    )

    return PodiumLargestContribution(
        resultdate="2024-07-08",
        year=config.current_year,
        track="track_single_query",
        results=f"results_{config.current_year}",
        participants=f"participants_{config.current_year}",
        winner_seq=get_winner(ld[smtcomp.scoring.Kind.seq]),
        winner_par=get_winner(ld[smtcomp.scoring.Kind.par]),
        winner_sat=get_winner(ld[smtcomp.scoring.Kind.sat]),
        winner_unsat=get_winner(ld[smtcomp.scoring.Kind.unsat]),
        winner_24s=get_winner(ld[smtcomp.scoring.Kind.twentyfour]),
        sequential=ld[smtcomp.scoring.Kind.seq],
        parallel=ld[smtcomp.scoring.Kind.par],
        sat=ld[smtcomp.scoring.Kind.sat],
        unsat=ld[smtcomp.scoring.Kind.unsat],
        twentyfour=ld[smtcomp.scoring.Kind.twentyfour],
    )


def largest_contribution(
    config: defs.Config, selection: pl.LazyFrame, scores: pl.LazyFrame
) -> PodiumLargestContribution:
    for_division = True
    # For each solver compute its corresponding best solver
    # TODO: check what is competitive solver (unsound?)

    scores = scores.filter(error_score=0, sound_solver=True).filter(smtcomp.scoring.known_answer)
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
    virtual_datas = sq_generate_datas(config, selection, virtual_scores, for_division)

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
    virtual_without_solver_datas = sq_generate_datas(config, selection, virtual_without_solver_scores, for_division)

    large = largest_contribution_ranking(
        config,
        virtual_datas,
        virtual_without_solver_datas,
        ratio_by_division,
    )

    if False:
        print(virtual_datas)
        print(virtual_without_solver_datas)
        print(large)

    return large


def export_results(config: defs.Config, selection: pl.LazyFrame, results: pl.LazyFrame) -> None:

    dst = config.web_results
    dst.mkdir(parents=True, exist_ok=True)

    scores = smtcomp.scoring.add_disagreements_info(results)
    scores = smtcomp.scoring.benchmark_scoring(scores)
    scores = scores.filter(disagreements=False).drop("disagreements")
    scores = scores.filter(track=int(defs.Track.SingleQuery)).drop("track")
    scores = scores.collect().lazy()

    for for_division in [True, False]:
        datas = sq_generate_datas(config, selection, scores, for_division)

        for name, data in datas.items():
            (dst / f"{name.lower()}-single-query.md").write_text(data.model_dump_json(indent=1))

        if for_division:
            bigdata = biggest_lead_ranking(config, datas)
            (dst / f"biggest-lead-single-query.md").write_text(bigdata.model_dump_json(indent=1))

            largedata = largest_contribution(config, selection, scores)
            (dst / f"largest-contribution-single-query.md").write_text(largedata.model_dump_json(indent=1))

    (dst / "results-single-query.md").write_text(
        Summary(year=config.current_year, track="track_single_query").model_dump_json(indent=1)
    )
