# tests\cli\test_batch_cmd.py

from typer.testing import CliRunner

from file_conversor.cli.app_cmd import app_cmd

runner = CliRunner()


def test_config_show():
    result = runner.invoke(app_cmd, ["config", "show", "--help"])
    assert "config show" in result.output


def test_config_set():
    result = runner.invoke(app_cmd, ["config", "set", "--help"])
    assert "config set" in result.output


def test_config():
    result = runner.invoke(app_cmd, ["config", "--help"])
    assert "config" in result.output
