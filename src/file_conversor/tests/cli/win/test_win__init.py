# tests\cli\win\test_win__init.py

import pytest
import platform

# user-provided modules
from file_conversor.cli._typer import AppCommands, WinTyperGroup

from file_conversor.tests.utils import TestTyper, DATA_PATH, app_cmd


@pytest.mark.skipif(platform.system() != "Windows", reason="Windows-only test class")
class TestWindowsHelp:
    def test_win_help(self,):
        result = TestTyper.invoke(AppCommands.WIN.value, "--help")
        for mode in WinTyperGroup.Commands:
            assert mode.value in result.output
        assert result.exit_code == 0
