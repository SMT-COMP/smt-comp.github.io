from os import path
from pathlib import Path

import pytest
from typer.testing import CliRunner

from smtcomp.convert_csv import convert_csv
from smtcomp.main import app
import smtcomp.defs as defs
from smtcomp.submission import read
from smtcomp.generate_benchmarks import generate_trivial_benchmarks, path_trivial_benchmark

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
