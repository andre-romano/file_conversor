# tests\cli\win\test_win_uninstall_menu_cmd.py

import pytest

# user-provided imports
from file_conversor.cli import AppTyperGroup, WinTyperGroup
from file_conversor.cli.win import WinUninstallMenuCLI
from file_conversor.system.abstract_system import AbstractSystem
from file_conversor.tests.utils import TestTyper


@pytest.mark.skipif(AbstractSystem.Platform.get() != AbstractSystem.Platform.WINDOWS, reason="Windows-only test class")
@pytest.mark.skipif(not TestTyper.dependencies_installed(WinUninstallMenuCLI.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestWindowsUninstallMenuCLI:
    def test_win_uninstall_menu_help(self,):
        TestTyper.invoke_test_help(AppTyperGroup.Commands.WIN.value, WinTyperGroup.Commands.UNINSTALL_MENU.value)
