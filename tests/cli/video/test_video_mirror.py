
# tests/cli/video/test_mirror.py

import pytest

from file_conversor.cli.video._typer import COMMAND_NAME, MIRROR_NAME
from file_conversor.cli.video.mirror_cmd import EXTERNAL_DEPENDENCIES

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestVideoMirror:
    def test_video_mirror(self, tmp_path):
        test_cases = [
            (DATA_PATH / "test.mp4", tmp_path / "test_mirrored.mp4"),
        ]

        for in_path, out_path in test_cases:
            result = Test.invoke(
                COMMAND_NAME, MIRROR_NAME,
                str(in_path),
                "-a", "x",
                *Test.get_out_dir_params(out_path),
            )
            assert result.exit_code == 0
            assert out_path.exists()

    def test_video_mirror_help(self,):
        Test.invoke_test_help(COMMAND_NAME, MIRROR_NAME)
