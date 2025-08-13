
# tests/test_app_cmd.py

import typer

from tests.utils import Test, DATA_PATH, app_cmd


def test_no_log_flag():
    result = Test.invoke("-nl", "help")
    assert result.exit_code == 0


def test_no_progress_flag():
    result = Test.invoke("-np", "help")
    assert result.exit_code == 0


def test_quiet_flag():
    result = Test.invoke("-q", "help")
    assert result.exit_code == 0


def test_verbose_flag():
    result = Test.invoke("--verbose", "help")
    assert result.exit_code == 0


def test_debug_flag():
    result = Test.invoke("-d", "help")
    assert result.exit_code == 0


def test_help_cmd():
    result = Test.invoke("help")
    ctx = typer.Context(typer.main.get_command(app_cmd))
    assert ctx.command.get_help(ctx) in result.output


def test_help_flag():
    result = Test.invoke("--help")
    ctx = typer.Context(typer.main.get_command(app_cmd))
    assert ctx.command.get_help(ctx) in result.output


def test_help_short_flag():
    result = Test.invoke("-h")
    ctx = typer.Context(typer.main.get_command(app_cmd))
    assert ctx.command.get_help(ctx) in result.output
