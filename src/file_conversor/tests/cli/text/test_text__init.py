# tests\cli\text\test_text__init.py

# user-provided modules
from file_conversor.cli import AppTyperGroup, TextTyperGroup
from file_conversor.tests.utils import TestTyper


class TestTextHelpCLI:
    def test_text_help(self,):
        result = TestTyper.invoke(AppTyperGroup.Commands.TEXT.value, "--help")
        for mode in TextTyperGroup.Commands:
            assert mode.value in result.output
        assert result.exit_code == 0
