# tests\cli\config\test__init.py

from file_conversor.cli._typer import AppCommands, ConfigTyperGroup

from file_conversor.tests.utils import TestTyper, DATA_PATH, app_cmd


class TestConfigHelp:
    def test_config_help(self,):
        result = TestTyper.invoke(AppCommands.CONFIG.value, "--help")
        for mode in ConfigTyperGroup.Commands:
            assert mode.value in result.output
        assert result.exit_code == 0
