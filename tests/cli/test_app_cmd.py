
# tests/test_app_cmd.py

import pytest
import typer

from typer.testing import CliRunner

from file_conversor.cli.app_cmd import app_cmd

runner = CliRunner()


def test_no_log_flag():
    result = runner.invoke(app_cmd, ["-nl", "help"])
    assert result.exit_code == 0


def test_no_progress_flag():
    result = runner.invoke(app_cmd, ["-np", "help"])
    assert result.exit_code == 0


def test_quiet_flag():
    result = runner.invoke(app_cmd, ["-q", "help"])
    assert result.exit_code == 0


def test_verbose_flag():
    result = runner.invoke(app_cmd, ["--verbose", "help"])
    assert result.exit_code == 0


def test_debug_flag():
    result = runner.invoke(app_cmd, ["-d", "help"])
    assert result.exit_code == 0


def test_help_cmd():
    result = runner.invoke(app_cmd, ["help"])
    ctx = typer.Context(typer.main.get_command(app_cmd))
    assert ctx.command.get_help(ctx) in result.output


def test_help_flag():
    result = runner.invoke(app_cmd, ["--help"])
    ctx = typer.Context(typer.main.get_command(app_cmd))
    assert ctx.command.get_help(ctx) in result.output


def test_help_short_flag():
    result = runner.invoke(app_cmd, ["-h"])
    ctx = typer.Context(typer.main.get_command(app_cmd))
    assert ctx.command.get_help(ctx) in result.output
