
# tests\cli\test_app__init.py

import pytest
import typer

from tests.utils import Test, DATA_PATH, app_cmd


class TestApp:
    def test_no_log_flag(self,):
        result = Test.invoke("-nl", "config", "-h")
        assert result.exit_code == 0

    def test_no_progress_flag(self,):
        result = Test.invoke("-np", "config", "-h")
        assert result.exit_code == 0

    def test_quiet_flag(self,):
        result = Test.invoke("-q", "config", "-h")
        assert result.exit_code == 0

    def test_verbose_flag(self,):
        result = Test.invoke("--verbose", "config", "-h")
        assert result.exit_code == 0

    def test_version_flag(self,):
        result = Test.invoke("--version")
        assert result.exit_code == 0

    def test_debug_flag(self,):
        result = Test.invoke("-d", "config", "-h")
        assert result.exit_code == 0

    def test_help_flag(self,):
        result = Test.invoke("--help")
        ctx = typer.Context(typer.main.get_command(app_cmd))
        assert ctx.command.get_help(ctx) in result.output

    def test_help_short_flag(self,):
        result = Test.invoke("-h")
        ctx = typer.Context(typer.main.get_command(app_cmd))
        assert ctx.command.get_help(ctx) in result.output
