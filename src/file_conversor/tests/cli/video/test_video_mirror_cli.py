
# tests/cli/video/test_mirror.py

from pathlib import Path

import pytest

# user-provided imports
from file_conversor.cli import AppTyperGroup, VideoTyperGroup
from file_conversor.cli.video import VideoMirrorCLI
from file_conversor.tests.utils import DATA_PATH, TestTyper


@pytest.mark.skipif(not TestTyper.dependencies_installed(VideoMirrorCLI.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestVideoMirrorCLI:
    def test_video_mirror(self, tmp_path: Path):
        test_cases: list[tuple[Path, Path]] = [
            (DATA_PATH / "test.mp4", tmp_path / "test_mirrored.mp4"),
        ]

        for in_path, out_path in test_cases:
            result = TestTyper.invoke(
                AppTyperGroup.Commands.VIDEO.value, VideoTyperGroup.Commands.MIRROR.value,
                str(in_path),
                "-a", "x",
                *TestTyper.get_out_dir_params(out_path),
            )
            assert result.exit_code == 0
            assert out_path.exists()

    def test_video_mirror_help(self,):
        TestTyper.invoke_test_help(AppTyperGroup.Commands.VIDEO.value, VideoTyperGroup.Commands.MIRROR.value)
