# tests\cli\config\test_show_cmd.py

import pytest

from file_conversor.cli.config._typer import COMMAND_NAME, SHOW_NAME
from file_conversor.cli.config.show_cmd import EXTERNAL_DEPENDENCIES

from tests.file_conversor.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestConfigShow:
    def test_config_show_help(self,):
        Test.invoke_test_help(COMMAND_NAME, SHOW_NAME)
