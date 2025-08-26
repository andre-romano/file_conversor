
from pathlib import Path

from file_conversor.cli.image._typer import COMMAND_NAME

from tests.utils import Test, DATA_PATH, app_cmd


def test_image_help():
    Test.invoke_test_help(COMMAND_NAME)
