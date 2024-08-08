import smtcomp.defs as defs
from pydantic.networks import HttpUrl
from pathlib import Path
from smtcomp.unpack import write_cin

logic = defs.Logic.QF_ABV
""" An arbitrary logic present in all tested tracks """

solver_best = "SolverBest"
""" Solver which prove everything """

solver_sound = "SolverSound"
""" Solver which is sound but don't solve everything """

solver_error = "SolverError"
""" Solver which makes errors """

daisy_family = tuple(["daisy"])

file_sat = defs.Smt2File(incremental=False, logic=defs.Logic.QF_ABV, family=daisy_family, name="sat.smt2")

file_unsat = defs.Smt2File(incremental=False, logic=defs.Logic.QF_ABV, family=daisy_family, name="unsat.smt2")

file_unknown = defs.Smt2File(incremental=False, logic=defs.Logic.QF_ABV, family=daisy_family, name="unkown.smt2")
""" This file is unsat in the generated single query results"""

file_incremental = defs.Smt2File(
    incremental=True, logic=defs.Logic.QF_ABV, family=daisy_family, name="incremental.smt2"
)


def mk_submissions() -> list[defs.Submission]:
    contributor = "Author"
    email = "Author@research.mars"

    def mk_submission(name: str) -> defs.Submission:
        return defs.Submission(
            name=name,
            contributors=[defs.Contributor(name=contributor)],
            contacts=[defs.NameEmail(name=contributor, email=email)],
            command=defs.Command(binary=name),
            archive=defs.Archive(url=HttpUrl("http://research.mars/archive.tgz")),
            website=HttpUrl("http://research.mars/"),
            system_description=HttpUrl("http://research.mars/"),
            solver_type=defs.SolverType.standalone,
            participations=defs.Participations(
                [
                    defs.Participation(
                        tracks=[
                            defs.Track.SingleQuery,
                            defs.Track.UnsatCore,
                            defs.Track.Incremental,
                            defs.Track.ModelValidation,
                        ],
                        logics=defs.Logics([defs.Logic.QF_ABV]),
                    )
                ]
            ),
            seed=42,
        )

    return [
        mk_submission(solver_best),
        mk_submission(solver_sound),
        mk_submission(solver_error),
    ]


def mk_benchmarks() -> defs.Benchmarks:
    # sort file by name
    return defs.Benchmarks(
        non_incremental=[
            defs.InfoNonIncremental(file=file_sat, status=defs.Status.Sat, asserts=10),
            defs.InfoNonIncremental(file=file_unknown, status=defs.Status.Unknown, asserts=10),
            defs.InfoNonIncremental(file=file_unsat, status=defs.Status.Unsat, asserts=10),
        ],
        incremental=[
            defs.InfoIncremental(file=file_incremental, check_sats=10),
        ],
    )


def mk_results(
    track: defs.Track, solver: str, results: list[tuple[defs.Smt2File, defs.Answer, int]]
) -> list[defs.Result]:
    return [
        defs.Result(
            track=track,
            solver=solver,
            file=file,
            result=result,
            cpu_time=10.0,
            wallclock_time=20.0,
            memory_usage=10.0,
            nb_answers=nb_answers,
        )
        for (file, result, nb_answers) in results
    ]


def mk_previous_years_results(config: defs.Config) -> list[tuple[int, Path, defs.Results]]:
    results = [(file_sat, defs.Answer.Sat, 1)]
    return [
        (year, p, defs.Results(results=mk_results(defs.Track.SingleQuery, solver_best, results)))
        for (year, p) in config.previous_results
    ]


def mk_sq_results() -> defs.Results:
    results = [(file_sat, defs.Answer.Sat, 1), (file_unknown, defs.Answer.Unsat, 1), (file_unsat, defs.Answer.Unsat, 1)]

    return defs.Results(
        results=mk_results(defs.Track.SingleQuery, solver_best, results)
        + mk_results(defs.Track.SingleQuery, solver_sound, results[:-1] + [(file_unsat, defs.Answer.Unknown, 1)])
        + mk_results(defs.Track.SingleQuery, solver_error, results[:-1] + [(file_unsat, defs.Answer.Sat, 1)])
    )


def mk_uc_results() -> defs.Results:
    results = [(file_unknown, defs.Answer.Unsat, 7), (file_unsat, defs.Answer.Unsat, 7)]

    return defs.Results(
        results=mk_results(defs.Track.SingleQuery, solver_best, results)
        + mk_results(defs.Track.SingleQuery, solver_sound, results[:-1] + [(file_unsat, defs.Answer.Unknown, 1)])
        + mk_results(defs.Track.SingleQuery, solver_error, results[:-1] + [(file_unsat, defs.Answer.Sat, 1)])
    )


def mk_mv_results() -> defs.Results:

    return defs.Results(
        results=mk_results(defs.Track.SingleQuery, solver_best, [(file_sat, defs.Answer.Sat, 1)])
        + mk_results(defs.Track.SingleQuery, solver_sound, [(file_sat, defs.Answer.ModelParsingError, 1)])
        + mk_results(defs.Track.SingleQuery, solver_error, [(file_sat, defs.Answer.ModelUnsat, 1)])
    )


def mk_inc_results() -> defs.Results:
    results = [(file_incremental, defs.Answer.Incremental, 7)]

    return defs.Results(
        results=mk_results(defs.Track.SingleQuery, solver_best, results)
        + mk_results(defs.Track.SingleQuery, solver_sound, [(file_incremental, defs.Answer.Incremental, 5)])
        + mk_results(defs.Track.SingleQuery, solver_error, [(file_incremental, defs.Answer.IncrementalError, 0)])
    )


def write_test_files(data: Path) -> None:
    config = defs.Config(data)
    submissions = data / ".." / "submissions"
    submissions.mkdir()
    for submission in mk_submissions():
        (submissions / (submission.name + ".json")).write_text(submission.model_dump_json(indent=2))
    write_cin(config.benchmarks, mk_benchmarks().model_dump_json())
    for _, file, results in mk_previous_years_results(config):
        write_cin(file, results.model_dump_json(indent=2))
    for track, gen in [
        (defs.Track.SingleQuery, mk_sq_results),
        (defs.Track.UnsatCore, mk_uc_results),
        (defs.Track.ModelValidation, mk_mv_results),
        (defs.Track.Incremental, mk_inc_results),
    ]:
        write_cin(config.current_results[track], gen().model_dump_json(indent=2))
