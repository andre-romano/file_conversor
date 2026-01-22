# tests\cli\win\test_win_install_menu_cmd.py

import pytest

from pathlib import Path

# user-provided imports
from file_conversor.cli import AppTyperGroup, WinTyperGroup
from file_conversor.cli.win import WinInstallMenuTyperCommand

from file_conversor.system.abstract_system import AbstractSystem
from file_conversor.tests.utils import TestTyper, DATA_PATH


@pytest.mark.skipif(AbstractSystem.Platform.get() != AbstractSystem.Platform.WINDOWS, reason="Windows-only test class")
@pytest.mark.skipif(not TestTyper.dependencies_installed(WinInstallMenuTyperCommand.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestWindowsInstallMenu:
    def test_win_install_menu_help(self,):
        TestTyper.invoke_test_help(AppTyperGroup.Commands.WIN.value, WinTyperGroup.Commands.INSTALL_MENU.value)
