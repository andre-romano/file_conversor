# tests\cli\hash\test__init.py

from file_conversor.cli import AppTyperGroup, HashTyperGroup

from file_conversor.tests.utils import TestTyper, DATA_PATH


class TestHashHelp:
    def test_hash_help(self,):
        result = TestTyper.invoke(AppTyperGroup.Commands.HASH.value, "--help")
        for mode in HashTyperGroup.Commands:
            assert mode.value in result.output
        assert result.exit_code == 0
