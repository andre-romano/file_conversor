
# tests\cli\pipeline\test_pipeline_execute_cmd.py

from file_conversor.cli.pipeline._typer import COMMAND_NAME, EXECUTE_NAME

from tests.utils import Test, DATA_PATH, app_cmd


def test_pipeline_execute_help():
    Test.invoke_test_help(COMMAND_NAME, EXECUTE_NAME)
