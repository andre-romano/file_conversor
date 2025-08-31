# tests\cli\win\test_win_install_menu_cmd.py

import pytest
import platform

from file_conversor.cli.win._typer import COMMAND_NAME, INSTALL_MENU_NAME

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(platform.system() != "Windows", reason="Windows-only test class")
class TestWindowsInstallMenuCommand:
    def test_win_install_menu_help(self,):
        Test.invoke_test_help(COMMAND_NAME, INSTALL_MENU_NAME)
