
# tests/cli/video/test_list_formats.py

from pathlib import Path

import pytest

# user-provided imports
from file_conversor.cli import AppTyperGroup, VideoTyperGroup
from file_conversor.cli.video import VideoListFormatsCLI
from file_conversor.tests.utils import DATA_PATH, TestTyper


@pytest.mark.skipif(not TestTyper.dependencies_installed(VideoListFormatsCLI.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestVideoListFormatsCLI:
    def test_video_list_formats(self, tmp_path: Path):
        test_cases: list[tuple[Path, Path]] = [
            (DATA_PATH / "test.mp4", tmp_path / "test.mp4"),
        ]

        for _in_path, out_path in test_cases:
            result = TestTyper.invoke(
                AppTyperGroup.Commands.VIDEO.value, VideoTyperGroup.Commands.LIST_FORMATS.value,
                *TestTyper.get_format_params(out_path),
            )
            assert result.exit_code == 0
            assert "mp4" in result.stdout or "MP4" in result.stdout

    def test_video_list_formats_help(self,):
        TestTyper.invoke_test_help(AppTyperGroup.Commands.VIDEO.value, VideoTyperGroup.Commands.LIST_FORMATS.value)
