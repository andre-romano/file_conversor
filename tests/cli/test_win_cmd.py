# tests\cli\test_win_cmd.py

from typer.testing import CliRunner

from file_conversor.cli.app_cmd import app_cmd

runner = CliRunner()


def test_win_uninstall_menu():
    result = runner.invoke(app_cmd, ["win", "uninstall-menu", "--help"])
    assert "win uninstall-menu" in result.output


def test_win_install_menu():
    result = runner.invoke(app_cmd, ["win", "install-menu", "--help"])
    assert "win install-menu" in result.output


def test_win():
    result = runner.invoke(app_cmd, ["win", "--help"])
    assert "win" in result.output
