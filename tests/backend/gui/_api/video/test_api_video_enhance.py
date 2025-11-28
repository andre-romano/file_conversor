# tests\backend\gui\_api\video\test_api_video_enhance.py

import platform
import pytest

from pathlib import Path


# user-provided imports
from file_conversor.backend.gui._api.video.enhance import api_video_enhance, EXTERNAL_DEPENDENCIES

from file_conversor.backend.gui import FlaskApiStatus, FlaskRoute

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestAPIVideoEnhance:
    def test_enhance(self, tmp_path: Path):
        url = FlaskRoute.get_url(api_video_enhance)
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

            "resolution": "none",
            "fps": "none",

            "brightness": "1.2",
            "contrast": "1.2",
            "color": "1.2",
            "gamma": "1.2",

            "deshake": "off",
            "unsharp": "off",

            "overwrite-output": "true",
        })
        status = Test.flask_api_status(FlaskApiStatus(**reply))
        assert (tmp_path / "test_enhanced.mp4").exists()
