# tests\cli\image\test_image_blur_cmd.py

import pytest

from file_conversor.cli.image._typer import COMMAND_NAME, BLUR_NAME
from file_conversor.cli.image.blur_cmd import EXTERNAL_DEPENDENCIES

from tests.file_conversor.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestImageBlur:
    def test_image_blur_cases(self, tmp_path):
        test_cases = [
            (DATA_PATH / "test.png", tmp_path / "test_blurred.png"),
        ]

        for in_path, out_path in test_cases:
            result = Test.invoke(
                COMMAND_NAME, BLUR_NAME,
                str(in_path),
                "-r", "3",
                *Test.get_out_dir_params(out_path),
            )
            assert result.exit_code == 0
            assert out_path.exists()

    def test_image_blur_help(self,):
        Test.invoke_test_help(COMMAND_NAME, BLUR_NAME)
