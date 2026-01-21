# tests\cli\text\test_text__init.py

# user-provided modules
from file_conversor.cli._typer import AppCommands, TextTyperGroup

from file_conversor.tests.utils import TestTyper, DATA_PATH, app_cmd


class TestTextHelp:
    def test_text_help(self,):
        result = TestTyper.invoke(AppCommands.TEXT.value, "--help")
        for mode in TextTyperGroup.Commands:
            assert mode.value in result.output
        assert result.exit_code == 0
