
# tests/cli/audio/test_check.py

import pytest
from pathlib import Path

from file_conversor.cli import AppTyperGroup, AudioTyperGroup
from file_conversor.cli.audio import AudioCheckCommand

from file_conversor.tests.utils import TestTyper, DATA_PATH


@pytest.mark.skipif(not TestTyper.dependencies_installed(AudioCheckCommand.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestAudioCheck:
    def test_audio_check(self):
        test_cases: list[Path] = [
            DATA_PATH / "test.mp3",
        ]

        for in_path in test_cases:
            result = TestTyper.invoke(
                AppTyperGroup.Commands.AUDIO.value, AudioTyperGroup.Commands.CHECK.value,
                str(in_path),
            )
            assert result.exit_code == 0

    def test_audio_check_help(self,):
        TestTyper.invoke_test_help(AppTyperGroup.Commands.AUDIO.value, AudioTyperGroup.Commands.CHECK.value)
