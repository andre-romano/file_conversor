# tests\cli\config\test__init.py

from file_conversor.cli import AppTyperGroup, ConfigTyperGroup

from file_conversor.tests.utils import TestTyper, DATA_PATH


class TestConfigHelp:
    def test_config_help(self,):
        result = TestTyper.invoke(AppTyperGroup.Commands.CONFIG.value, "--help")
        for mode in ConfigTyperGroup.Commands:
            assert mode.value in result.output
        assert result.exit_code == 0
