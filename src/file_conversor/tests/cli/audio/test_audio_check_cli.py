
# tests/cli/audio/test_check.py

from pathlib import Path

import pytest

from file_conversor.cli import AppTyperGroup, AudioTyperGroup
from file_conversor.cli.audio.check_cli import AudioCheckCommand
from file_conversor.tests.utils import DATA_PATH, TestTyper


@pytest.mark.skipif(not AudioCheckCommand.check_dependencies(), reason="External dependencies not installed")
class TestAudioCheckCLI:
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
