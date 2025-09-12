
# tests/cli/audio_video/test_enhance.py

import pytest

from file_conversor.cli.audio_video._typer import COMMAND_NAME, ENHANCE_NAME
from file_conversor.cli.audio_video.enhance_cmd import EXTERNAL_DEPENDENCIES

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestAudioVideoEnhance:
    def test_audio_video_enhance(self, tmp_path):
        test_cases = [
            (DATA_PATH / "test.mp4", tmp_path / "test_enhanced.mp4"),
        ]

        for in_path, out_path in test_cases:
            result = Test.invoke(
                COMMAND_NAME, ENHANCE_NAME,
                str(in_path),
                "--contrast", "1.2",
                *Test.get_out_dir_params(out_path),
            )
            assert result.exit_code == 0
            assert out_path.exists()

    def test_audio_video_enhance_help(self,):
        Test.invoke_test_help(COMMAND_NAME, ENHANCE_NAME)
