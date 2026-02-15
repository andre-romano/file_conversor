
# tests/cli/video/test_info.py

from pathlib import Path

import pytest

# user-provided imports
from file_conversor.cli import AppTyperGroup, VideoTyperGroup
from file_conversor.cli.video import VideoInfoCLI
from file_conversor.tests.utils import DATA_PATH, TestTyper


@pytest.mark.skipif(not TestTyper.dependencies_installed(VideoInfoCLI.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestVideoInfoCLI:
    def test_video_info(self, tmp_path: Path):
        test_cases: list[tuple[Path, Path]] = [
            (DATA_PATH / "test.mp4", tmp_path / "test.mp4"),
        ]

        for in_path, _ in test_cases:
            result = TestTyper.invoke(
                AppTyperGroup.Commands.VIDEO.value, VideoTyperGroup.Commands.INFO.value,
                str(in_path),
            )
            assert result.exit_code == 0
            assert "h264" in result.stdout

    def test_video_info_help(self,):
        TestTyper.invoke_test_help(AppTyperGroup.Commands.VIDEO.value, VideoTyperGroup.Commands.INFO.value)
