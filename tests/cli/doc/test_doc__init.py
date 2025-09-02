# tests\cli\doc\test__init.py

from file_conversor.cli.doc._typer import COMMAND_NAME

from tests.utils import Test, DATA_PATH


class TestDocHelp:
    def test_doc_help(self,):
        Test.invoke_test_help(COMMAND_NAME)
