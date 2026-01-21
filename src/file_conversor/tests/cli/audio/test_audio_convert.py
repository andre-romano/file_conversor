
# tests/cli/audio/test_convert.py

import pytest
from pathlib import Path

from file_conversor.cli._typer import AppCommands, AudioTyperGroup
from file_conversor.cli.audio import AudioConvertCommand

from file_conversor.tests.utils import TestTyper, DATA_PATH


@pytest.mark.skipif(not TestTyper.dependencies_installed(AudioConvertCommand.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestAudioConvert:
    def test_audio_convert(self, tmp_path):
        test_cases: list[tuple[Path, Path]] = [
            (DATA_PATH / "test.mp3", tmp_path / "test.m4a"),
        ]

        for in_path, out_path in test_cases:
            result = TestTyper.invoke(
                AppCommands.AUDIO.value, AudioTyperGroup.Commands.CONVERT.value,
                str(in_path),
                *TestTyper.get_format_params(out_path),
                *TestTyper.get_out_dir_params(out_path),
            )
            assert result.exit_code == 0
            assert out_path.exists()

    def test_audio_convert_help(self,):
        TestTyper.invoke_test_help(AppCommands.AUDIO.value, AudioTyperGroup.Commands.CONVERT.value)
