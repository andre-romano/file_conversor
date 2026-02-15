# tests\cli\config\test_set_cmd.py

import pytest

from file_conversor.cli import AppTyperGroup, ConfigTyperGroup
from file_conversor.cli.config import ConfigSetCLI
from file_conversor.tests.utils import TestTyper


@pytest.mark.skipif(not TestTyper.dependencies_installed(ConfigSetCLI.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestConfigSetCLI:
    def test_config_set_help(self):
        TestTyper.invoke_test_help(AppTyperGroup.Commands.CONFIG.value, ConfigTyperGroup.Commands.SET.value)
