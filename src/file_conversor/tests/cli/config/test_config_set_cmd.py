# tests\cli\config\test_set_cmd.py

import pytest

from file_conversor.cli._typer import AppCommands, ConfigTyperGroup
from file_conversor.cli.config import ConfigSetCommand

from file_conversor.tests.utils import TestTyper, DATA_PATH


@pytest.mark.skipif(not TestTyper.dependencies_installed(ConfigSetCommand.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestConfigSet:
    def test_config_set_help(self):
        TestTyper.invoke_test_help(AppCommands.CONFIG.value, ConfigTyperGroup.Commands.SET.value)
