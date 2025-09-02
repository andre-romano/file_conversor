# tests\cli\image\test_image_mirror_cmd.py

import pytest

from file_conversor.cli.image._typer import COMMAND_NAME, MIRROR_NAME
from file_conversor.cli.image.mirror_cmd import EXTERNAL_DEPENDENCIES

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestImageMirror:
    def test_image_mirror_x(self, tmp_path):
        in_path = DATA_PATH / "test.png"
        out_path = tmp_path / "test_mirrored.png"

        result = Test.invoke(
            COMMAND_NAME, MIRROR_NAME,
            str(in_path),
            "-a", "x",
            *Test.get_out_dir_params(out_path),
        )
        assert result.exit_code == 0
        assert out_path.exists()

    def test_image_mirror_y(self, tmp_path):
        in_path = DATA_PATH / "test.png"
        out_path = tmp_path / "test_mirrored.png"

        result = Test.invoke(
            COMMAND_NAME, MIRROR_NAME,
            str(in_path),
            "-a", "y",
            *Test.get_out_dir_params(out_path),
        )
        assert result.exit_code == 0
        assert out_path.exists()

    def test_image_mirror_help(self,):
        Test.invoke_test_help(COMMAND_NAME, MIRROR_NAME)
