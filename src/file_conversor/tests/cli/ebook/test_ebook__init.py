
# tests/cli/ebook/test_ebook__init.py

from file_conversor.cli._typer import AppCommands, EbookTyperGroup

from file_conversor.tests.utils import TestTyper, DATA_PATH, app_cmd


class TestEbookHelp:
    def test_ebook_help(self,):
        result = TestTyper.invoke(AppCommands.EBOOK.value, "--help")
        for mode in EbookTyperGroup.Commands:
            assert mode.value in result.output
        assert result.exit_code == 0
