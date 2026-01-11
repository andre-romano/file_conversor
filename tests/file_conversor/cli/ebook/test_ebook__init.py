
# tests/cli/ebook/test_ebook__init.py

from file_conversor.cli.ebook._typer import COMMAND_NAME

from tests.file_conversor.utils import Test, DATA_PATH, app_cmd


class TestEbookHelp:
    def test_ebook_help(self,):
        Test.invoke_test_help(COMMAND_NAME)
