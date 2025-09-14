
# tests/cli/audio/test_info.py

import pytest
import shutil

from file_conversor.cli.audio._typer import COMMAND_NAME, INFO_NAME
from file_conversor.cli.audio.info_cmd import EXTERNAL_DEPENDENCIES

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestAudioConvert:
    def test_audio_info(self, tmp_path):
        test_cases = [
            (DATA_PATH / "test.mp3", tmp_path / "test.mp3"),
        ]

        for in_path, out_path in test_cases:
            result = Test.invoke(
                COMMAND_NAME, INFO_NAME,
                str(in_path),
            )
            assert result.exit_code == 0
            assert "mp3" in result.stdout

    def test_audio_info_help(self,):
        Test.invoke_test_help(COMMAND_NAME, INFO_NAME)
