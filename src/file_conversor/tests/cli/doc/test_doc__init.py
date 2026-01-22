# tests\cli\doc\test__init.py

from file_conversor.cli import AppTyperGroup, DocTyperGroup

from file_conversor.tests.utils import TestTyper, DATA_PATH


class TestDocHelp:
    def test_doc_help(self,):
        result = TestTyper.invoke(AppTyperGroup.Commands.DOC.value, "--help")
        for mode in DocTyperGroup.Commands:
            assert mode.value in result.output
        assert result.exit_code == 0
