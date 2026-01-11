# tests\cli\image\test_image_info_cmd.py

import pytest

from file_conversor.cli.image._typer import COMMAND_NAME, INFO_NAME
from file_conversor.cli.image.info_cmd import EXTERNAL_DEPENDENCIES

from tests.file_conversor.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestImageInfo:
    def test_image_info_cases(self,):
        in_path = DATA_PATH / "test.png"

        result = Test.invoke(COMMAND_NAME, INFO_NAME, str(in_path))
        assert result.exit_code == 0
        assert "PNG" in result.stdout

    def test_image_info_help(self,):
        Test.invoke_test_help(COMMAND_NAME, INFO_NAME)
