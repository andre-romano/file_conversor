# tests\cli\text\test_text__init.py

from file_conversor.cli.text._typer import COMMAND_NAME

from tests.file_conversor.utils import Test, DATA_PATH, app_cmd


class TestTextHelp:
    def test_text_help(self,):
        Test.invoke_test_help(COMMAND_NAME)
