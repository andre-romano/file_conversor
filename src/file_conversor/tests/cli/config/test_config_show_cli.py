# tests\cli\config\test_show_cmd.py

import pytest

from file_conversor.cli import AppTyperGroup, ConfigTyperGroup
from file_conversor.cli.config import ConfigShowCLI
from file_conversor.tests.utils import TestTyper


@pytest.mark.skipif(not TestTyper.dependencies_installed(ConfigShowCLI.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestConfigShowCLI:
    def test_config_show_help(self,):
        TestTyper.invoke_test_help(AppTyperGroup.Commands.CONFIG.value, ConfigTyperGroup.Commands.SHOW.value)
