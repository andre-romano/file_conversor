# tests\cli\win\test_win__init.py

import pytest
import platform

from file_conversor.cli.win._typer import COMMAND_NAME

from tests.file_conversor.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(platform.system() != "Windows", reason="Windows-only test class")
class TestWindowsHelp:
    def test_win_help(self,):
        Test.invoke_test_help(COMMAND_NAME)
