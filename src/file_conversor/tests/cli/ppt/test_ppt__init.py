# tests\cli\ppt\test_ppt__init.py

# user-provided modules
from file_conversor.cli._typer import AppCommands, PptTyperGroup

from file_conversor.tests.utils import TestTyper, DATA_PATH


class TestPptHelp:
    def test_ppt_help(self):
        result = TestTyper.invoke(AppCommands.PPT.value, "--help")
        for mode in PptTyperGroup.Commands:
            assert mode.value in result.output
        assert result.exit_code == 0
