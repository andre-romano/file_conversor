# tests\cli\win\test_win_uninstall_menu_cmd.py

import pytest
import platform

from file_conversor.cli.win._typer import COMMAND_NAME, UNINSTALL_MENU_NAME
from file_conversor.cli.win.uninstall_menu_cmd import EXTERNAL_DEPENDENCIES

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(platform.system() != "Windows", reason="Windows-only test class")
@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestWindowsUninstallMenu:
    def test_win_uninstall_menu_help(self,):
        Test.invoke_test_help(COMMAND_NAME, UNINSTALL_MENU_NAME)
