# tests\cli\win\test_win_install_menu_cmd.py

import platform
import pytest

from pathlib import Path

# user-provided imports
from file_conversor.cli._typer import AppCommands, WinTyperGroup
from file_conversor.cli.win import WinInstallMenuTyperCommand

from file_conversor.tests.utils import TestTyper, DATA_PATH


@pytest.mark.skipif(platform.system() != "Windows", reason="Windows-only test class")
@pytest.mark.skipif(not TestTyper.dependencies_installed(WinInstallMenuTyperCommand.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestWindowsInstallMenu:
    def test_win_install_menu_help(self,):
        TestTyper.invoke_test_help(AppCommands.WIN.value, WinTyperGroup.Commands.INSTALL_MENU.value)
