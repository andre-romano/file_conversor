# tests\cli\ppt\test_ppt__init.py

from file_conversor.cli.ppt._typer import COMMAND_NAME

from tests.utils import Test, DATA_PATH


class TestPptHelp:
    def test_ppt_help(self):
        Test.invoke_test_help(COMMAND_NAME)
