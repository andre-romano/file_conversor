# tests\cli\image\test_image_resize_cmd.py

import pytest

from file_conversor.cli.image._typer import COMMAND_NAME, RESIZE_NAME
from file_conversor.cli.image.resize_cmd import EXTERNAL_DEPENDENCIES

from tests.file_conversor.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestImageResize:
    def test_image_resize_scale(self, tmp_path):
        in_path = DATA_PATH / "test.png"
        out_path = tmp_path / "test_resized.png"

        result = Test.invoke(
            COMMAND_NAME, RESIZE_NAME,
            str(in_path),
            "-s", "2.0",
            *Test.get_out_dir_params(out_path),
        )
        assert result.exit_code == 0
        assert out_path.exists()

    def test_image_resize_width(self, tmp_path):
        in_path = DATA_PATH / "test.png"
        out_path = tmp_path / "test_resized.png"

        result = Test.invoke(
            COMMAND_NAME, RESIZE_NAME,
            str(in_path),
            "-w", "1024",
            *Test.get_out_dir_params(out_path),
        )
        assert result.exit_code == 0
        assert out_path.exists()

    def test_image(self,):
        Test.invoke_test_help(COMMAND_NAME, RESIZE_NAME)
