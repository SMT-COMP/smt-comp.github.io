import pytest  # type: ignore
from typer.testing import CliRunner

from smtcomp.main import app

runner = CliRunner()
cases = ["tests/test1.json"]

@pytest.mark.parametrize("name", cases)
def test_arg(name: str):
    result = runner.invoke(app, ["validate",name])
    assert result.stdout == ""
    assert result.exit_code == 0
