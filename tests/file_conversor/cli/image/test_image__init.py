

import pytest

from pathlib import Path

# user-provided modules
from file_conversor.cli.image._typer import COMMAND_NAME

from tests.file_conversor.utils import Test, DATA_PATH, app_cmd


class TestImageHelp:
    def test_image_help(self,):
        Test.invoke_test_help(COMMAND_NAME)
