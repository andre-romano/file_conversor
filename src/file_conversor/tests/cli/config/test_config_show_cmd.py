# tests\cli\config\test_show_cmd.py

import pytest

from file_conversor.cli import AppTyperGroup, ConfigTyperGroup
from file_conversor.cli.config import ConfigShowCommand

from file_conversor.tests.utils import TestTyper, DATA_PATH


@pytest.mark.skipif(not TestTyper.dependencies_installed(ConfigShowCommand.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestConfigShow:
    def test_config_show_help(self,):
        TestTyper.invoke_test_help(AppTyperGroup.Commands.CONFIG.value, ConfigTyperGroup.Commands.SHOW.value)
