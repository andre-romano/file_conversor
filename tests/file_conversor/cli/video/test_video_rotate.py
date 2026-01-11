
# tests/cli/video/test_rotate.py

import pytest

from file_conversor.cli.video._typer import COMMAND_NAME, ROTATE_NAME
from file_conversor.cli.video.rotate_cmd import EXTERNAL_DEPENDENCIES

from tests.file_conversor.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestVideoRotate:
    def test_video_rotate(self, tmp_path):
        test_cases = [
            (DATA_PATH / "test.mp4", tmp_path / "test_rotated.mp4"),
        ]

        for in_path, out_path in test_cases:
            result = Test.invoke(
                COMMAND_NAME, ROTATE_NAME,
                str(in_path),
                "-r", "90",
                *Test.get_out_dir_params(out_path),
            )
            assert result.exit_code == 0
            assert out_path.exists()

    def test_video_rotate_help(self,):
        Test.invoke_test_help(COMMAND_NAME, ROTATE_NAME)
