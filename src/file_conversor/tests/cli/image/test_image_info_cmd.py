# tests\cli\image\test_image_info_cmd.py

import pytest

# user-provided imports
from file_conversor.cli import AppTyperGroup, ImageTyperGroup
from file_conversor.cli.image import ImageInfoTyperCommand

from file_conversor.tests.utils import TestTyper, DATA_PATH


@pytest.mark.skipif(not TestTyper.dependencies_installed(ImageInfoTyperCommand.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestImageInfo:
    def test_image_info_cases(self,):
        in_path = DATA_PATH / "test.png"

        result = TestTyper.invoke(AppTyperGroup.Commands.IMAGE.value, ImageTyperGroup.Commands.INFO.value, str(in_path))
        assert result.exit_code == 0
        assert "PNG" in result.stdout

    def test_image_info_help(self,):
        TestTyper.invoke_test_help(AppTyperGroup.Commands.IMAGE.value, ImageTyperGroup.Commands.INFO.value)
