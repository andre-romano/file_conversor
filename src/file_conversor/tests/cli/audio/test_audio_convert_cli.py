
# tests/cli/audio/test_convert.py

from pathlib import Path

import pytest

from file_conversor.cli import AppTyperGroup, AudioTyperGroup
from file_conversor.cli.audio.convert_cli import AudioConvertCommand
from file_conversor.tests.utils import DATA_PATH, TestTyper


@pytest.mark.skipif(not AudioConvertCommand.check_dependencies(), reason="External dependencies not installed")
class TestAudioConvertCLI:
    def test_audio_convert(self, tmp_path: Path):
        test_cases: list[tuple[Path, Path]] = [
            (DATA_PATH / "test.mp3", tmp_path / "test.m4a"),
        ]

        for in_path, out_path in test_cases:
            result = TestTyper.invoke(
                AppTyperGroup.Commands.AUDIO.value, AudioTyperGroup.Commands.CONVERT.value,
                str(in_path),
                *TestTyper.get_format_params(out_path),
                *TestTyper.get_out_dir_params(out_path),
            )
            assert result.exit_code == 0
            assert out_path.exists()

    def test_audio_convert_help(self,):
        TestTyper.invoke_test_help(AppTyperGroup.Commands.AUDIO.value, AudioTyperGroup.Commands.CONVERT.value)
