# tests\cli\test_doc_cmd.py

from typer.testing import CliRunner
from pathlib import Path

from file_conversor.cli.app_cmd import app_cmd

runner = CliRunner()


def test_doc_convert():
    result = runner.invoke(app_cmd, ["doc", "convert", "--help"])
    assert "doc convert" in result.output


def test_doc():
    result = runner.invoke(app_cmd, ["doc", "--help"])
    assert "doc" in result.output
