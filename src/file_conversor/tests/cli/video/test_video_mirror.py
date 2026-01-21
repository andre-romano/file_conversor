
# tests/cli/video/test_mirror.py

import pytest
from pathlib import Path

# user-provided imports
from file_conversor.cli._typer import AppCommands, VideoTyperGroup
from file_conversor.cli.video import VideoMirrorTyperCommand

from file_conversor.tests.utils import TestTyper, DATA_PATH


@pytest.mark.skipif(not TestTyper.dependencies_installed(VideoMirrorTyperCommand.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestVideoMirror:
    def test_video_mirror(self, tmp_path):
        test_cases: list[tuple[Path, Path]] = [
            (DATA_PATH / "test.mp4", tmp_path / "test_mirrored.mp4"),
        ]

        for in_path, out_path in test_cases:
            result = TestTyper.invoke(
                AppCommands.VIDEO.value, VideoTyperGroup.Commands.MIRROR.value,
                str(in_path),
                "-a", "x",
                *TestTyper.get_out_dir_params(out_path),
            )
            assert result.exit_code == 0
            assert out_path.exists()

    def test_video_mirror_help(self,):
        TestTyper.invoke_test_help(AppCommands.VIDEO.value, VideoTyperGroup.Commands.MIRROR.value)
