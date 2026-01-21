# tests\cli\hash\test__init.py

from file_conversor.cli._typer import AppCommands, HashTyperGroup

from file_conversor.tests.utils import TestTyper, DATA_PATH


class TestHashHelp:
    def test_hash_help(self,):
        result = TestTyper.invoke(AppCommands.HASH.value, "--help")
        for mode in HashTyperGroup.Commands:
            assert mode.value in result.output
        assert result.exit_code == 0
