
# tests/cli/video/test_check.py

from pathlib import Path

import pytest

# user-provided imports
from file_conversor.cli import AppTyperGroup, VideoTyperGroup
from file_conversor.cli.video import VideoCheckCLI
from file_conversor.tests.utils import DATA_PATH, TestTyper


@pytest.mark.skipif(not TestTyper.dependencies_installed(VideoCheckCLI.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestVideoCheckCLI:
    def test_video_check(self):
        test_cases: list[Path] = [
            DATA_PATH / "test.mp4",
        ]

        for in_path in test_cases:
            result = TestTyper.invoke(
                AppTyperGroup.Commands.VIDEO.value, VideoTyperGroup.Commands.CHECK.value,
                str(in_path),
            )
            assert result.exit_code == 0

    def test_video_check_help(self,):
        TestTyper.invoke_test_help(AppTyperGroup.Commands.VIDEO.value, VideoTyperGroup.Commands.CHECK.value)
