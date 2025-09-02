
# tests/cli/audio_video/test_info.py

import pytest
import shutil

from file_conversor.cli.audio_video._typer import COMMAND_NAME, INFO_NAME
from file_conversor.cli.audio_video.info_cmd import EXTERNAL_DEPENDENCIES

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestAudioVideoConvert:
    def test_audio_video_info(self, tmp_path):
        test_cases = [
            (DATA_PATH / "test.mp4", tmp_path / "test.mp4"),
        ]

        for in_path, out_path in test_cases:
            result = Test.invoke(
                COMMAND_NAME, INFO_NAME,
                str(in_path),
            )
            assert result.exit_code == 0
            assert "h264" in result.stdout

    def test_audio_video_info_help(self,):
        Test.invoke_test_help(COMMAND_NAME, INFO_NAME)
