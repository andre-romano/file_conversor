
# tests/cli/audio/test_info.py

import pytest
from pathlib import Path

from file_conversor.cli import AppTyperGroup, AudioTyperGroup
from file_conversor.cli.audio import AudioInfoCommand

from file_conversor.tests.utils import TestTyper, DATA_PATH


@pytest.mark.skipif(not TestTyper.dependencies_installed(AudioInfoCommand.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestAudioInfo:
    def test_audio_info(self):
        test_cases: list[Path] = [
            DATA_PATH / "test.mp3"
        ]

        for in_path in test_cases:
            result = TestTyper.invoke(
                AppTyperGroup.Commands.AUDIO.value, AudioTyperGroup.Commands.INFO.value,
                str(in_path),
            )
            assert result.exit_code == 0
            assert "mp3" in result.stdout

    def test_audio_info_help(self,):
        TestTyper.invoke_test_help(AppTyperGroup.Commands.AUDIO.value, AudioTyperGroup.Commands.INFO.value)
