
# tests/cli/audio_video/test_resize.py

import pytest

from file_conversor.cli.audio_video._typer import COMMAND_NAME, RESIZE_NAME
from file_conversor.cli.audio_video.resize_cmd import EXTERNAL_DEPENDENCIES

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestAudioVideoResize:
    def test_audio_video_resize(self, tmp_path):
        test_cases = [
            (DATA_PATH / "test.mp4", tmp_path / "test_resized.mp4"),
        ]

        for in_path, out_path in test_cases:
            result = Test.invoke(
                COMMAND_NAME, RESIZE_NAME,
                str(in_path),
                "-rs", "1024x768",
                *Test.get_out_dir_params(out_path),
            )
            assert result.exit_code == 0
            assert out_path.exists()

    def test_audio_video_resize_help(self,):
        Test.invoke_test_help(COMMAND_NAME, RESIZE_NAME)
