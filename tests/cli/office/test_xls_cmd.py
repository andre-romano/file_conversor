# tests\cli\test_xls_cmd.py

from typer.testing import CliRunner
from pathlib import Path

from file_conversor.cli.app_cmd import app_cmd

runner = CliRunner()


def test_xls_convert():
    result = runner.invoke(app_cmd, ["xls", "convert", "--help"])
    assert "xls convert" in result.output


def test_xls():
    result = runner.invoke(app_cmd, ["xls", "--help"])
    assert "xls" in result.output
