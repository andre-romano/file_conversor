# tests\cli\win\test_win__init.py

import pytest

# user-provided modules
from file_conversor.cli import AppTyperGroup, WinTyperGroup

from file_conversor.system.abstract_system import AbstractSystem
from file_conversor.tests.utils import TestTyper, DATA_PATH


@pytest.mark.skipif(AbstractSystem.Platform.get() != AbstractSystem.Platform.WINDOWS, reason="Windows-only test class")
class TestWindowsHelp:
    def test_win_help(self,):
        result = TestTyper.invoke(AppTyperGroup.Commands.WIN.value, "--help")
        for mode in WinTyperGroup.Commands:
            assert mode.value in result.output
        assert result.exit_code == 0
