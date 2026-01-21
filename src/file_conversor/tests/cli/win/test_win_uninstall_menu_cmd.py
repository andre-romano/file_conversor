# tests\cli\win\test_win_uninstall_menu_cmd.py

import platform
import pytest

from pathlib import Path

# user-provided imports
from file_conversor.cli._typer import AppCommands, WinTyperGroup
from file_conversor.cli.win import WinUninstallMenuTyperCommand

from file_conversor.tests.utils import TestTyper, DATA_PATH


@pytest.mark.skipif(platform.system() != "Windows", reason="Windows-only test class")
@pytest.mark.skipif(not TestTyper.dependencies_installed(WinUninstallMenuTyperCommand.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestWindowsUninstallMenu:
    def test_win_uninstall_menu_help(self,):
        TestTyper.invoke_test_help(AppCommands.WIN.value, WinTyperGroup.Commands.UNINSTALL_MENU.value)
