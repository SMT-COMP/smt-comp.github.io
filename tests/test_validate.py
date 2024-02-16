from os import path
from pathlib import Path

import pytest
from typer.testing import CliRunner

from smtcomp.convert_csv import convert_csv
from smtcomp.main import app
from smtcomp.submission import read

runner = CliRunner()
good_cases = ["tests/test1.json", "submissions/template/template.json"]
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


submissions = list(Path("submissions").glob("*.json"))


@pytest.mark.parametrize("submission", submissions)
def test_submission(submission: str) -> None:
    read(submission)


csv = ["tests/SMT-COMP 2023 System Registration.csv"]


@pytest.mark.parametrize("csv", csv)
def test_csv(csv: str, tmp_path: Path) -> None:
    convert_csv(Path(csv), tmp_path)
