
# tests/cli/video/test_list_formats.py

import pytest
from pathlib import Path

# user-provided imports
from file_conversor.cli._typer import AppCommands, VideoTyperGroup
from file_conversor.cli.video import VideoListFormatsTyperCommand

from file_conversor.tests.utils import TestTyper, DATA_PATH


@pytest.mark.skipif(not TestTyper.dependencies_installed(VideoListFormatsTyperCommand.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestVideoListFormats:
    def test_video_list_formats(self, tmp_path):
        test_cases: list[tuple[Path, Path]] = [
            (DATA_PATH / "test.mp4", tmp_path / "test.mp4"),
        ]

        for in_path, out_path in test_cases:
            result = TestTyper.invoke(
                AppCommands.VIDEO.value, VideoTyperGroup.Commands.LIST_FORMATS.value,
                *TestTyper.get_format_params(out_path),
            )
            assert result.exit_code == 0
            assert "mp4" in result.stdout

    def test_video_list_formats_help(self,):
        TestTyper.invoke_test_help(AppCommands.VIDEO.value, VideoTyperGroup.Commands.LIST_FORMATS.value)
