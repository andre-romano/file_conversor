# tests\cli\test_pipeline_cmd.py

from file_conversor.cli.pipeline._typer import COMMAND_NAME, CREATE_NAME

from tests.utils import Test, DATA_PATH, app_cmd


def test_pipeline_create_help():
    Test.invoke_test_help(COMMAND_NAME, CREATE_NAME)
