# tests\cli\config\test_set_cmd.py

import pytest

from file_conversor.cli.config._typer import COMMAND_NAME, SET_NAME
from file_conversor.cli.config.set_cmd import EXTERNAL_DEPENDENCIES

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestConfigSet:
    def test_config_set_help(self,):
        Test.invoke_test_help(COMMAND_NAME, SET_NAME)
