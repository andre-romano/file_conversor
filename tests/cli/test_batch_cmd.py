# tests\cli\test_batch_cmd.py

from typer.testing import CliRunner

from file_conversor.cli.app_cmd import app_cmd

runner = CliRunner()


def test_batch_execute():
    result = runner.invoke(
        app_cmd, ["batch", "execute", "--help"])
    assert "batch execute" in result.output


def test_batch_create():
    result = runner.invoke(
        app_cmd, ["batch", "create", "--help"])
    assert "batch create" in result.output


def test_batch():
    result = runner.invoke(
        app_cmd, ["batch", "--help"])
    assert "batch" in result.output
