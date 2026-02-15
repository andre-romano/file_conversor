
# tests/cli/ebook/test_ebook__init.py

from file_conversor.cli import AppTyperGroup, EbookTyperGroup
from file_conversor.tests.utils import TestTyper


class TestEbookHelpCLI:
    def test_ebook_help(self,):
        result = TestTyper.invoke(AppTyperGroup.Commands.EBOOK.value, "--help")
        for mode in EbookTyperGroup.Commands:
            assert mode.value in result.output
        assert result.exit_code == 0
