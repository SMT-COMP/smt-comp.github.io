"""Test smtcomp."""

import smtcomp


def test_import() -> None:
    """Test that the package can be imported."""
    assert isinstance(smtcomp.__name__, str)
