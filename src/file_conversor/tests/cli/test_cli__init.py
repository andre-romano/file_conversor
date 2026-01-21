
# tests\cli\test_app__init.py

import pytest
import typer

from file_conversor.tests.utils import TestTyper, DATA_PATH, app_cmd


class TestCLI:
    def test_no_log_flag(self,):
        result = TestTyper.invoke("-nl", "config", "-h")
        assert result.exit_code == 0

    def test_no_progress_flag(self,):
        result = TestTyper.invoke("-np", "config", "-h")
        assert result.exit_code == 0

    def test_quiet_flag(self,):
        result = TestTyper.invoke("-q", "config", "-h")
        assert result.exit_code == 0

    def test_verbose_flag(self,):
        result = TestTyper.invoke("--verbose", "config", "-h")
        assert result.exit_code == 0

    def test_version_flag(self,):
        result = TestTyper.invoke("--version")
        assert result.exit_code == 0

    def test_debug_flag(self,):
        result = TestTyper.invoke("-d", "config", "-h")
        assert result.exit_code == 0

    def test_help_flag(self,):
        result = TestTyper.invoke("--help")
        ctx = typer.Context(typer.main.get_command(app_cmd))
        assert ctx.command.get_help(ctx) in result.output

    def test_help_short_flag(self,):
        result = TestTyper.invoke("-h")
        ctx = typer.Context(typer.main.get_command(app_cmd))
        assert ctx.command.get_help(ctx) in result.output
