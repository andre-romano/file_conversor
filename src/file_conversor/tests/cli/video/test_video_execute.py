
# tests/cli/video/test_execute.py

import pytest
from pathlib import Path

# user-provided imports
from file_conversor.cli._typer import AppCommands, VideoTyperGroup
from file_conversor.cli.video import VideoExecuteTyperCommand

from file_conversor.tests.utils import TestTyper, DATA_PATH


@pytest.mark.skipif(not TestTyper.dependencies_installed(VideoExecuteTyperCommand.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestVideoExecute:
    def test_video_execute(self, tmp_path):
        test_cases: list[tuple[Path, Path]] = [
            (DATA_PATH / "test.mp4", tmp_path / "test.mp3"),
        ]

        for in_path, out_path in test_cases:
            result = TestTyper.invoke(
                AppCommands.VIDEO.value, VideoTyperGroup.Commands.EXECUTE.value,
                str(in_path),
                *TestTyper.get_format_params(out_path),
                *TestTyper.get_out_dir_params(out_path),
            )
            assert result.exit_code == 0
            assert out_path.exists()

    def test_video_execute_help(self,):
        TestTyper.invoke_test_help(AppCommands.VIDEO.value, VideoTyperGroup.Commands.EXECUTE.value)
