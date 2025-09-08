# tests\cli\image\test_image_enhance_cmd.py

import pytest

from file_conversor.cli.image._typer import COMMAND_NAME, ENHANCE_NAME
from file_conversor.cli.image.enhance_cmd import EXTERNAL_DEPENDENCIES

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestImageEnhance:
    def test_image_enhance_cases(self, tmp_path):
        test_cases = [
            (DATA_PATH / "test.png", tmp_path / "test_enhanced.png"),
        ]

        for in_path, out_path in test_cases:
            result = Test.invoke(
                COMMAND_NAME, ENHANCE_NAME,
                str(in_path),
                "-cl", "1.20",
                "-ct", "1.20",
                "-b", "1.20",
                "-s", "1.20",
                *Test.get_out_dir_params(out_path),
            )
            assert result.exit_code == 0
            assert out_path.exists()

    def test_image_enhance_help(self,):
        Test.invoke_test_help(COMMAND_NAME, ENHANCE_NAME)
