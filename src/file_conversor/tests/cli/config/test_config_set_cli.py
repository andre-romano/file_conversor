# tests\cli\config\test_set_cmd.py

import pytest

from file_conversor.cli import AppTyperGroup, ConfigTyperGroup
from file_conversor.cli.config.set_cli import ConfigSetCommand
from file_conversor.tests.utils import TestTyper


@pytest.mark.skipif(not ConfigSetCommand.check_dependencies(), reason="External dependencies not installed")
class TestConfigSetCLI:
    def test_config_set_help(self):
        TestTyper.invoke_test_help(AppTyperGroup.Commands.CONFIG.value, ConfigTyperGroup.Commands.SET.value)
