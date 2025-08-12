# tests\cli\test_doc_cmd.py

from typer.testing import CliRunner
from pathlib import Path

from file_conversor.cli.app_cmd import app_cmd

runner = CliRunner()


def test_ppt_convert():
    result = runner.invoke(app_cmd, ["ppt", "convert", "--help"])
    assert "ppt convert" in result.output


def test_ppt():
    result = runner.invoke(app_cmd, ["ppt", "--help"])
    assert "ppt" in result.output
