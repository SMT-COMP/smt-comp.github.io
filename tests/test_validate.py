from os import path
from pathlib import Path

import pytest
from typer.testing import CliRunner

from smtcomp.convert_csv import convert_csv
from smtcomp.main import app
import smtcomp.defs as defs
from smtcomp.submission import read
from smtcomp.generate_benchmarks import generate_trivial_benchmarks, path_trivial_benchmark

import smtcomp.test_generation as gtests
import smtcomp.results, smtcomp.scoring, smtcomp.generate_website_page

runner = CliRunner()
good_cases = ["tests/test1.json", "submissions/template/template.json", "submissions/template/template_aws_tracks.json"]
bad_cases = ["test_bad.json"]


@pytest.mark.parametrize("name", good_cases)
def test_good_json(name: str) -> None:
    result = runner.invoke(app, ["validate", name])
    assert result.stdout == ""
    assert result.exit_code == 0


@pytest.mark.parametrize("name", bad_cases)
def test_bad_json(name: str) -> None:
    result = runner.invoke(app, ["validate", path.join("tests", name)])
    assert result.exit_code == 1


@pytest.mark.parametrize("name", good_cases)
def test_show_json(name: str) -> None:
    result = runner.invoke(app, ["show", name])
    assert result.exit_code == 0


submissions = list(Path("submissions").glob("*.json"))


@pytest.mark.parametrize("submission", submissions)
def test_submission(submission: str) -> None:
    read(submission)


def test_generate_trivial(tmp_path: Path) -> None:
    generate_trivial_benchmarks(tmp_path)
    for track, divisions in defs.tracks.items():
        match track:
            case defs.Track.Incremental:
                statuses = [defs.Status.Incremental]
            case defs.Track.ModelValidation | defs.Track.SingleQuery:
                statuses = [defs.Status.Unsat, defs.Status.Sat]
            case defs.Track.UnsatCore | defs.Track.ProofExhibition | defs.Track.Cloud | defs.Track.Parallel:
                continue
        for _, logics in divisions.items():
            for logic in logics:
                for status in statuses:
                    assert path_trivial_benchmark(tmp_path, track, logic, status).exists()


@pytest.fixture(scope="session")
def config(tmp_path_factory: pytest.TempPathFactory) -> defs.Config:
    fn = tmp_path_factory.mktemp("tmp")
    data = fn / "data"
    data.mkdir()
    gtests.write_test_files(data)
    result = runner.invoke(app, ["create-cache", str(data.absolute())])
    assert result.exit_code == 0
    return defs.Config(data)


def test_results_sq_export(config: defs.Config) -> None:
    print(config.data)
    podium = gtests.compute_results_read_podium_division(
        config, defs.Track.SingleQuery, check_sound_solvers=[gtests.solver_best, gtests.solver_sound]
    )

    print(podium.model_dump_json(indent=1))
    assert podium.winner_seq == gtests.solver_best

    assert podium.sequential[0].name == gtests.solver_best
    assert podium.sequential[0].errorScore == 0
    assert podium.sequential[0].correctScore == 3
    assert podium.sequential[1].name == gtests.solver_sound
    assert podium.sequential[1].errorScore == 0
    assert podium.sequential[1].correctScore == 2
    assert podium.sequential[2].name == gtests.solver_error
    assert podium.sequential[2].errorScore == 1
    assert podium.sequential[2].correctScore == 2


def test_results_uc_export(config: defs.Config) -> None:
    print(config.data)
    podium = gtests.compute_results_read_podium_division(
        config, defs.Track.UnsatCore, check_sound_solvers=[gtests.solver_best, gtests.solver_sound]
    )
    print(podium.model_dump_json(indent=1))

    assert podium.winner_seq == gtests.solver_best

    assert podium.sequential[0].name == gtests.solver_best
    assert podium.sequential[0].errorScore == 0
    assert podium.sequential[0].correctScore == 6
    assert podium.sequential[1].name == gtests.solver_sound
    assert podium.sequential[1].errorScore == 0
    assert podium.sequential[1].correctScore == 3
    assert podium.sequential[2].name == gtests.solver_error
    assert podium.sequential[2].errorScore == 1
    assert podium.sequential[2].correctScore == 3


def test_results_mv_export(config: defs.Config) -> None:
    print(config.data)
    podium = gtests.compute_results_read_podium_division(
        config, defs.Track.ModelValidation, check_sound_solvers=[gtests.solver_best, gtests.solver_sound]
    )
    print(podium.model_dump_json(indent=1))

    assert podium.winner_seq == gtests.solver_best

    assert podium.sequential[0].name == gtests.solver_best
    assert podium.sequential[0].errorScore == 0
    assert podium.sequential[0].correctScore == 1
    assert podium.sequential[1].name == gtests.solver_sound
    assert podium.sequential[1].errorScore == 0
    assert podium.sequential[1].correctScore == 0
    assert podium.sequential[2].name == gtests.solver_error
    assert podium.sequential[2].errorScore == 1
    assert podium.sequential[2].correctScore == 0


def test_results_inc_export(config: defs.Config) -> None:
    print(config.data)
    podium = gtests.compute_results_read_podium_division(config, defs.Track.Incremental)
    print(podium.model_dump_json(indent=1))

    assert podium.winner_seq == gtests.solver_best

    assert podium.sequential[0].name == gtests.solver_best
    assert podium.sequential[0].errorScore == 0
    assert podium.sequential[0].correctScore == 7
    assert podium.sequential[1].name == gtests.solver_sound
    assert podium.sequential[1].errorScore == 0
    assert podium.sequential[1].correctScore == 5
    assert podium.sequential[2].name == gtests.solver_error
    assert podium.sequential[2].errorScore == 1
    assert podium.sequential[2].correctScore == 0
