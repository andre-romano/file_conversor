
# tests/cli/audio/test_check.py

import pytest

from file_conversor.cli.audio._typer import COMMAND_NAME, CHECK_NAME
from file_conversor.cli.audio.check_cmd import EXTERNAL_DEPENDENCIES

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestAudioCheck:
    def test_audio_check(self):
        test_cases = [
            DATA_PATH / "test.mp3",
        ]

        for in_path in test_cases:
            result = Test.invoke(
                COMMAND_NAME, CHECK_NAME,
                str(in_path),
            )
            assert result.exit_code == 0

    def test_audio_check_help(self,):
        Test.invoke_test_help(COMMAND_NAME, CHECK_NAME)
