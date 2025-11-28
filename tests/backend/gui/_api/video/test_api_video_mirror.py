# tests\backend\gui\_api\video\test_api_video_mirror.py

import platform
import pytest

from pathlib import Path


# user-provided imports
from file_conversor.backend.gui._api.video.mirror import api_video_mirror, EXTERNAL_DEPENDENCIES

from file_conversor.backend.gui import FlaskApiStatus, FlaskRoute

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestAPIVideoMirror:
    def test_mirror(self, tmp_path: Path):
        url = FlaskRoute.get_url(api_video_mirror)
        reply = Test.flask_api(url, data={
            "input-files": str([
                str(DATA_PATH.resolve() / "test.mp4"),
            ]),
            "output-dir": str(tmp_path.resolve()),
            "file-format": "mp4",

            "audio-bitrate": "0",
            "video-bitrate": "0",

            "video-encoding-speed": "fast",
            "video-quality": "medium",

            "mirror-axis": "x",

            "overwrite-output": "true",
        })
        status = Test.flask_api_status(FlaskApiStatus(**reply))
        assert (tmp_path / "test_mirrored.mp4").exists()
