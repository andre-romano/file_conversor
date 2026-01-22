
# tests/cli/video/test_check.py

import pytest
from pathlib import Path

# user-provided imports
from file_conversor.cli import AppTyperGroup, VideoTyperGroup
from file_conversor.cli.video import VideoCheckTyperCommand

from file_conversor.tests.utils import TestTyper, DATA_PATH


@pytest.mark.skipif(not TestTyper.dependencies_installed(VideoCheckTyperCommand.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestVideoCheck:
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
